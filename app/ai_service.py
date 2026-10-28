"""
CelebrateAI - Generative AI Service & Synthesis Engine
Integrates Google Gemini 2.5/2.0 Flash SDK with an intelligent offline fallback engine.
"""

import copy
import json
import logging
import os
import re
import uuid
from typing import Any, Dict, Optional

from .models import (
    BudgetItem,
    ChatRequest,
    ColorSwatch,
    EventIdeas,
    EventPlan,
    GeneratePlanRequest,
    ScheduleItem,
    TimelineMilestone,
    VendorItem,
)
from .sample_data import SAMPLE_EVENTS

logger = logging.getLogger("celebrate_ai.ai_service")
GEMINI_API_KEY_ENV = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def extract_json_block(text: str) -> Optional[dict]:
    """Helper to cleanly extract a JSON object from text or markdown code fence.

    Args:
        text (str): Raw string output from LLM.

    Returns:
        Optional[dict]: Parsed JSON dictionary if found, else None.
    """
    try:
        pattern = r"```(?:json)?\s*(\{.*?\})\s*```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        trimmed = text.strip()
        if trimmed.startswith("{") and trimmed.endswith("}"):
            return json.loads(trimmed)
        first = text.find("{")
        last = text.rfind("}")
        if first != -1 and last != -1 and last > first:
            return json.loads(text[first : last + 1])
    except Exception as e:
        logger.debug("JSON block extraction non-fatal parse failure: %s", e)
    return None


def build_gemini_client(api_key: Optional[str] = None) -> Optional[Any]:
    """Initializes and returns the official Google Gemini SDK client.

    Args:
        api_key (Optional[str]): Explicit user-provided API key or falls back to env.

    Returns:
        Optional[Any]: Google GenAI Client instance if key exists, else None.
    """
    key = api_key or GEMINI_API_KEY_ENV
    if not key:
        return None
    try:
        from google import genai

        return genai.Client(api_key=key)
    except Exception as e:
        logger.warning("Unable to initialize Gemini client: %s", e)
        return None


def generate_event_plan(request: GeneratePlanRequest) -> EventPlan:
    """Generates an end-to-end event plan with budgets, timeline, vendor checklist,
    and personalized creative ideas. Uses Gemini when available, or smart synthesis.

    Args:
        request (GeneratePlanRequest): Validated event request payload.

    Returns:
        EventPlan: Fully populated and validated event blueprint.
    """
    client = build_gemini_client(request.apiKey)
    if client:
        try:
            ev_title = request.title or f"{request.eventType.capitalize()} Celebration"
            prompt = (
                f"You are an elite event planner.\n"
                f"Generate a detailed event plan in JSON for:\n"
                f"Type: {request.eventType}, Title: {ev_title}\n"
                f"Guests: {request.guestCount}, "
                f"Budget: {request.totalBudget} {request.currency}\n"
                f"Date: {request.date or 'TBD'}, Location: {request.location or 'TBD'}\n"
                f"Vibe: {request.vibeAndStyle}\n"
                f"Respond ONLY with a JSON object matching EventPlan schema."
            )
            for model_name in [
                "gemini-2.5-flash",
                "gemini-2.0-flash",
                "gemini-1.5-flash",
            ]:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    parsed = extract_json_block(response.text)
                    if parsed:
                        logger.info(
                            "Successfully generated event plan via %s", model_name
                        )
                        return EventPlan(**parsed)
                except Exception as err:
                    logger.warning(
                        "Gemini generation fallback with %s: %s", model_name, err
                    )
                    continue
        except Exception as e:
            logger.error("Gemini API invocation failure: %s", e)

    logger.info("Engaging intelligent heuristic fallback synthesis engine.")
    return synthesize_smart_event_plan(request)


def _scale_budget_items(
    raw_items: list, scale: float, guests: int
) -> list[BudgetItem]:
    """Scales budget items proportionally and updates per-guest calculations."""
    budget_items = []
    for b in raw_items:
        est = round(float(b.get("estimatedCost", 0)) * scale, 2)
        act = round(float(b.get("actualCost", 0)) * scale, 2)
        paid = round(float(b.get("paidAmount", 0)) * scale, 2)
        notes = b.get("notes", "")
        if "Catering" in b.get("category", ""):
            per_guest = round(est / max(guests, 1), 2)
            notes = f"Allocated ~{per_guest} per guest across functions"
        budget_items.append(
            BudgetItem(
                id=b.get("id"),
                category=b.get("category"),
                item=b.get("item"),
                estimatedCost=est,
                actualCost=act,
                paidAmount=paid,
                status=b.get("status", "planned"),
                notes=notes,
            )
        )
    return budget_items


def _scale_vendor_items(raw_vendors: list, scale: float) -> list[VendorItem]:
    """Scales vendor costs proportionally and creates typed VendorItem instances."""
    vendors = []
    for v in raw_vendors:
        est = round(float(v.get("estimatedCost", 0)) * scale, 2)
        raw_con = v.get("contractedCost")
        con = round(float(raw_con) * scale, 2) if raw_con is not None else None
        vendors.append(
            VendorItem(
                id=v.get("id"),
                category=v.get("category"),
                vendorName=v.get("vendorName"),
                contact=v.get("contact", ""),
                estimatedCost=est,
                contractedCost=con,
                status=v.get("status", "contacted"),
                notes=v.get("notes", ""),
                checklist=v.get("checklist", []),
            )
        )
    return vendors


def _build_ideas(raw_ideas: dict, title: str) -> EventIdeas:
    """Constructs typed EventIdeas schema."""
    palette = [
        ColorSwatch(name=c.get("name"), hex=c.get("hex"))
        for c in raw_ideas.get("colorPalette", [])
    ]
    return EventIdeas(
        themeTitle=raw_ideas.get("themeTitle", f"{title} Theme"),
        themeConcept=raw_ideas.get("themeConcept", ""),
        colorPalette=palette,
        signatureFoodAndDrinks=raw_ideas.get("signatureFoodAndDrinks", []),
        activitiesAndEntertainment=raw_ideas.get("activitiesAndEntertainment", []),
        decorAndAtmosphere=raw_ideas.get("decorAndAtmosphere", []),
        surpriseElements=raw_ideas.get("surpriseElements", []),
        moodboardPrompt=raw_ideas.get("moodboardPrompt", ""),
    )


def _build_plan_from_blueprint(
    raw: Dict[str, Any],
    plan_id: str,
    title: str,
    req: GeneratePlanRequest,
    target_budget: float,
    guests: int,
    curr: str,
) -> EventPlan:
    """Dynamically scales and constructs a typed EventPlan from a blueprint."""
    base_budget = float(raw.get("totalBudget", target_budget or 1.0))
    scale = (target_budget / base_budget) if base_budget > 0 else 1.0

    budget_items = _scale_budget_items(raw.get("budgetBreakdown", []), scale, guests)
    vendors = _scale_vendor_items(raw.get("vendorChecklist", []), scale)
    ideas = _build_ideas(raw.get("ideas", {}), title)

    timeline = [TimelineMilestone(**t) for t in raw.get("timeline", [])]
    schedule = [ScheduleItem(**s) for s in raw.get("dayOfSchedule", [])]

    default_gen_title = f"Enchanted {req.eventType.capitalize()} Celebration"
    effective_title = (
        title if title and title != default_gen_title else raw.get("title", title)
    )

    return EventPlan(
        id=plan_id,
        title=effective_title,
        eventType=req.eventType.lower(),
        date=req.date or raw.get("date", "2027-11-24"),
        location=req.location or raw.get("location", "TBD"),
        guestCount=guests,
        currency=curr,
        totalBudget=target_budget,
        vibeAndStyle=req.vibeAndStyle or raw.get("vibeAndStyle", ""),
        specialRequests=req.specialRequests or "",
        ideas=ideas,
        budgetBreakdown=budget_items,
        timeline=timeline,
        dayOfSchedule=schedule,
        vendorChecklist=vendors,
    )


def _synthesize_wedding(
    plan_id: str,
    title: str,
    req: GeneratePlanRequest,
    budget: float,
    guests: int,
    curr: str,
) -> EventPlan:
    """Generates an authentic luxury Indian wedding celebration blueprint."""
    raw = copy.deepcopy(SAMPLE_EVENTS["wedding"])
    return _build_plan_from_blueprint(raw, plan_id, title, req, budget, guests, curr)


def _synthesize_birthday(
    plan_id: str,
    title: str,
    req: GeneratePlanRequest,
    budget: float,
    guests: int,
    curr: str,
) -> EventPlan:
    """Generates a vibrant Indian milestone birthday and Annaprashan blueprint."""
    raw = copy.deepcopy(SAMPLE_EVENTS["birthday"])
    return _build_plan_from_blueprint(raw, plan_id, title, req, budget, guests, curr)


def _synthesize_community(
    plan_id: str,
    title: str,
    req: GeneratePlanRequest,
    budget: float,
    guests: int,
    curr: str,
) -> EventPlan:
    """Generates a high-energy Indian community festival blueprint."""
    raw = copy.deepcopy(SAMPLE_EVENTS["community"])
    return _build_plan_from_blueprint(raw, plan_id, title, req, budget, guests, curr)


def _synthesize_custom(
    plan_id: str,
    title: str,
    req: GeneratePlanRequest,
    budget: float,
    guests: int,
    curr: str,
) -> EventPlan:
    """Fallback custom synthesizer routing to birthday generator."""
    return _synthesize_birthday(plan_id, title, req, budget, guests, curr)


def synthesize_smart_event_plan(request: GeneratePlanRequest) -> EventPlan:
    """Intelligent heuristic generative synthesis engine that creates richly detailed,
    proportionally balanced plans according to event type, budget, and guest count.

    Args:
        request (GeneratePlanRequest): Validated event request.

    Returns:
        EventPlan: Deterministically structured event plan.
    """
    ev_type = request.eventType.lower()
    total_b = float(request.totalBudget)
    guests = int(request.guestCount)
    curr = request.currency
    fallback_title = f"Enchanted {ev_type.capitalize()} Celebration"
    title = request.title or fallback_title
    plan_id = f"plan-{uuid.uuid4().hex[:8]}"

    if ev_type == "wedding":
        return _synthesize_wedding(plan_id, title, request, total_b, guests, curr)
    if ev_type == "birthday":
        return _synthesize_birthday(plan_id, title, request, total_b, guests, curr)
    if ev_type == "community":
        return _synthesize_community(plan_id, title, request, total_b, guests, curr)
    return _synthesize_custom(plan_id, title, request, total_b, guests, curr)


def ask_event_assistant(req: ChatRequest) -> str:
    """Interactive event planning assistant chat powered by Gemini when API key is available,
    or smart contextual event planning expert knowledge.

    Args:
        req (ChatRequest): Validated chat request with context and history.

    Returns:
        str: Formatted Markdown response from assistant.
    """
    client = build_gemini_client(req.apiKey)
    if client:
        try:
            context_str = (
                json.dumps(req.eventContext, indent=2)
                if req.eventContext
                else "No context."
            )
            system_instruction = (
                f"You are EventGenie AI, an experienced event planner.\n"
                f"Context: {context_str}\n"
                f"Be inspiring, empathetic, structured, and practical."
            )
            messages = [
                {
                    "role": m.role if m.role == "user" else "model",
                    "parts": [{"text": m.content}],
                }
                for m in req.chatHistory[-6:]
            ]
            messages.append({"role": "user", "parts": [{"text": req.message}]})

            for model_name in [
                "gemini-2.5-flash",
                "gemini-2.0-flash",
                "gemini-1.5-flash",
            ]:
                try:
                    resp = client.models.generate_content(
                        model=model_name,
                        contents=[
                            {"text": system_instruction},
                            *[m["parts"][0]["text"] for m in messages],
                        ],
                    )
                    if resp.text:
                        return resp.text
                except Exception as err:
                    logger.warning("Chat generation error with %s: %s", model_name, err)
                    continue
        except Exception as e:
            logger.error("Chat Gemini model invocation error: %s", e)

    return _generate_heuristic_chat_reply(req.message, req.eventContext)


def _reply_budget(event_title: str, currency: str, budget: Any) -> str:
    """Generates strategic budget allocation markdown guidance."""
    return (
        f"### 💡 Strategic Budget Advice for {event_title}\n\n"
        f"Here is a balanced framework based on your total budget "
        f"of **{currency} {budget}**:\n\n"
        f"1. **The 50/30/20 Rule for Indian Celebrations**:\n"
        f"   - **50% Experience Core**: Venue & Heritage Catering.\n"
        f"   - **30% Aesthetics**: Decor, Lotus Mandap/Stage, Sound.\n"
        f"   - **20% Memories & Buffer**: 4K Cinema, Shagun buffer.\n\n"
        f"2. **3 High-Impact Savings Tactics**:\n"
        f"   - **Seasonal Floral Mix**: Blend marigolds with local foliage.\n"
        f"   - **Curated Multi-Station Stalls**: Focus on interactive Chaat.\n"
        f"   - **Off-Peak Timings**: Morning or Sunday afternoon slots.\n"
    )


def _reply_timeline(event_title: str) -> str:
    """Generates timeline and curfew guidance."""
    return (
        f"### ⏱️ Timeline & Schedule Optimization for {event_title}\n\n"
        f"Indian celebrations thrive on punctuality paired with warmth:\n\n"
        f"1. **Buffer Blocks (The 'Desi Time' Cushion)**: Add 30-min buffers.\n"
        f"2. **Curfew Compliance**: Outdoor loudspeakers curfew at 10:00 PM.\n"
        f"3. **Dual-Track Logistics**: Vendor arrivals 3 hours prior.\n"
    )


def _reply_vendor(event_title: str) -> str:
    """Generates vendor contract and management guidance."""
    return (
        f"### 🤝 Vendor Management & CRM Guidance for {event_title}\n\n"
        f"Ensure seamless execution with these vendor vetting tips:\n\n"
        f"1. **Tasting & Demo**: Conduct live food tastings.\n"
        f"2. **Deliverables in Writing**: Drone 4K deliverables within 48h.\n"
        f"3. **Payment Tranches**: 40% advance, 40% on arrival, 20% post.\n"
    )


def _reply_creative(event_title: str) -> str:
    """Generates creative thematic and decor suggestions."""
    return (
        f"### ✨ Personalized Creative Concepts for {event_title}\n\n"
        f"Fresh, culturally vibrant ideas to elevate the guest experience:\n\n"
        f"1. **Interactive Purani Dilli Chaat Gali**: Live Banarasi Chaat.\n"
        f"2. **Personalized Shahi Ittar Bar**: Sandalwood ittars in flacons.\n"
        f"3. **Family Sangeet Face-Off**: Dance face-off with cold sparks.\n"
        f"4. **Royal Lotus Floating Mandap**: Vedic twilight pheras.\n"
    )


def _reply_general(event_title: str, event_type: str, currency: str) -> str:
    """Generates general greeting and capabilities overview."""
    return (
        f"### 🌟 EventGenie AI at your service!\n\n"
        f"I am here to help you coordinate every detail of **{event_title}**.\n\n"
        f"- **Refine your Budget**: Reallocate funds in {currency}.\n"
        f"- **Perfect your Timeline**: Build a seamless day-of schedule.\n"
        f"- **Vendor CRM & Checklists**: Track caterers, decorators, and photo.\n"
        f"- **Creative Ideation**: Suggest royal themes and return gifts.\n\n"
        f"What specific aspect of your {event_type} would you like to explore next?\n"
    )


def _matches_topic(msg: str, keywords: tuple) -> bool:
    """Checks whether any keyword exists in the message."""
    for k in keywords:
        if k in msg:
            return True
    return False


def _generate_heuristic_chat_reply(message: str, context: Optional[dict]) -> str:
    """Rule-based contextual planning knowledge generator for offline scenarios.

    Args:
        message (str): Incoming user query.
        context (Optional[dict]): Serialized event plan dictionary.

    Returns:
        str: Domain-specific markdown guidance.
    """
    msg = message.lower()
    event_title = context.get("title", "your event") if context else "your event"
    event_type = context.get("eventType", "event") if context else "event"
    budget = context.get("totalBudget", "the budget") if context else "the budget"
    currency = context.get("currency", "INR") if context else "INR"

    if _matches_topic(msg, ("budget", "cost", "expensive", "cut", "save")):
        return _reply_budget(event_title, currency, budget)
    if _matches_topic(msg, ("timeline", "schedule", "delay", "curfew", "muhurat")):
        return _reply_timeline(event_title)
    if _matches_topic(msg, ("vendor", "contract", "caterer", "photographer", "dj")):
        return _reply_vendor(event_title)
    if _matches_topic(msg, ("idea", "theme", "decor", "game", "activity", "chaat")):
        return _reply_creative(event_title)
    return _reply_general(event_title, event_type, currency)
