"""
CelebrateAI - Generative AI Service & Synthesis Engine
Integrates Google Gemini 2.5/2.0 Flash SDK with an intelligent offline fallback engine.
"""

import os
import json
import re
import uuid
import logging
from typing import Optional, Any

from .models import (
    GeneratePlanRequest, EventPlan, EventIdeas, ColorSwatch,
    BudgetItem, TimelineMilestone, ScheduleItem, VendorItem, ChecklistTask,
    ChatRequest
)

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
            return json.loads(text[first:last + 1])
    except Exception as e:
        logger.debug(f"JSON block extraction non-fatal parse failure: {e}")
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
        logger.warning(f"Unable to initialize Gemini client: {e}")
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
                f"Guests: {request.guestCount}, Budget: {request.totalBudget} {request.currency}\n"
                f"Date: {request.date or 'TBD'}, Location: {request.location or 'TBD'}\n"
                f"Vibe: {request.vibeAndStyle}\n"
                f"Respond ONLY with a JSON object matching EventPlan schema."
            )
            for model_name in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    parsed = extract_json_block(response.text)
                    if parsed:
                        logger.info(f"Successfully generated event plan via {model_name}")
                        return EventPlan(**parsed)
                except Exception as err:
                    logger.warning(f"Gemini generation fallback with {model_name}: {err}")
                    continue
        except Exception as e:
            logger.error(f"Gemini API invocation failure: {e}")

    logger.info("Engaging intelligent heuristic fallback synthesis engine.")
    return synthesize_smart_event_plan(request)


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
    elif ev_type == "birthday":
        return _synthesize_birthday(plan_id, title, request, total_b, guests, curr)
    elif ev_type == "community":
        return _synthesize_community(plan_id, title, request, total_b, guests, curr)
    else:
        return _synthesize_custom(plan_id, title, request, total_b, guests, curr)


def _synthesize_wedding(
    plan_id: str, title: str, req: GeneratePlanRequest, budget: float, guests: int, curr: str
) -> EventPlan:
    """Generates an authentic, luxury Indian wedding (Shaadi) celebration blueprint."""
    fallback_title = "Aarav & Ananya's Royal Jaipur Heritage Wedding"
    effective_title = title if title and title != "Enchanted Wedding Celebration" else fallback_title
    ideas = EventIdeas(
        themeTitle="Shahi Virasat: Royal Marigold & Crimson Grandeur",
        themeConcept=(
            f"A majestic Indian celebration rooted in timeless heritage for {guests} cherished guests. "
            f"Featuring fragrant marigold and rajnigandha floral cascades, authentic Shehnai and Punjabi "
            f"Dhol melodies, live Chaat Gali and Shahi Feast counters, and sacred Vedic twilight pheras."
        ),
        colorPalette=[
            ColorSwatch(name="Genda Marigold", hex="#F59E0B"),
            ColorSwatch(name="Royal Rani Pink", hex="#E11D48"),
            ColorSwatch(name="Peacock Royal Blue", hex="#1D4ED8"),
            ColorSwatch(name="Haldi Turmeric Gold", hex="#FBBF24"),
            ColorSwatch(name="Emerald Panna Green", hex="#059669")
        ],
        signatureFoodAndDrinks=[
            "Kesariya Kesar Thandai & Aam Panna welcome coolers with rose petal garnish",
            "Live Purani Dilli Chaat Gali: Banarasi Tamatar Chaat, Golgappe with 5 flavoured waters, Palak Patta Chaat",
            f"Royal Shahi Feast for {guests} guests: Dal Baati Churma, Paneer Lababdar, Dum Biryani, and Amritsari Kulcha",
            "Live Mithai Kadhai: Garma-garam Malpua with Rabri, Jalebi counter, and artisanal Kulfi Falooda",
            "Midnight Masala Chai Bar with assorted Mathris during late-night Vedic Pheras"
        ],
        activitiesAndEntertainment=[
            "High-voltage Sangeet Dance Competition choreographed for Groom vs Bride families",
            "Grand Royal Baraat with authentic Punjabi Dhol, vintage convertible car, and brass band",
            "Royal Welcome with Shehnai maestro and flower petal shower from Palace balconies",
            "Live Sufi Fusion Ensemble & Bollywood Celebrity DJ set after the Varmala",
            "Traditional Joota Chupai negotiation and playful post-wedding family games"
        ],
        decorAndAtmosphere=[
            "Mandap floating on Lotus water pond adorned with 50,000 marigolds and fresh rajnigandha stems",
            "Traditional brass urli bowls with floating marigolds and scented mogra candles",
            "Handcrafted puppet and Lac bangle maker live stall for guest souvenirs",
            "Fairytale tree canopies wrapped with warm fairy string lights and hanging glass lamps"
        ],
        surpriseElements=[
            "Surprise cold-spark pyrotechnic display firing 360-degrees during the Varmala garland exchange",
            "Personalized Shahi Ittar (organic Indian perfume) flacons gifted in brocade silk pouches",
            "Surprise flash-mob entrance by the bride's cousins to classic 90s Bollywood anthems"
        ],
        moodboardPrompt=(
            f"Grand Indian royal destination wedding in Jaipur palace courtyard at sunset, royal mandap "
            f"with orange and yellow marigold flowers, brass diyas, bride in crimson red lehenga, groom in "
            f"ivory sherwani, fairy lights, {guests} guests enjoying celebration, 8k cinematic photography"
        )
    )

    budget_breakdown = [
        BudgetItem(
            id="b1", category="Venue & Hospitality",
            item="Heritage Palace Resort (2 Days & Guest Rooms)",
            estimatedCost=round(budget * 0.34, 2),
            notes="Includes lawn, poolside for Haldi, and banquet hall for Sangeet"
        ),
        BudgetItem(
            id="b2", category="Catering & Live Stalls",
            item=f"Royal Multi-Cuisine Feast & Live Chaat Gali ({guests} guests)",
            estimatedCost=round(budget * 0.30, 2),
            notes=f"Approx {round((budget * 0.30) / max(guests, 1), 2)} per guest across 4 functions"
        ),
        BudgetItem(
            id="b3", category="Decor & Mandap",
            item="Vedic Lotus Mandap, Sangeet Stage, Haldi Theme & Lighting",
            estimatedCost=round(budget * 0.12, 2),
            notes="Fresh marigolds, rajnigandha, royal drapes, and ambient palace uplighting"
        ),
        BudgetItem(
            id="b4", category="Photography & Video",
            item="Cinematic Candid Photo, Drone & 4K Wedding Film (3 Days)",
            estimatedCost=round(budget * 0.08, 2),
            notes="Team of 4 shooters, drone coverage, teaser reel in 48 hours"
        ),
        BudgetItem(
            id="b5", category="Entertainment & DJ",
            item="Sangeet Bollywood DJ, Punjabi Dhol Troupe & Shehnai Artist",
            estimatedCost=round(budget * 0.05, 2),
            notes="Includes state-of-the-art Line Array sound setup and wireless mics"
        ),
        BudgetItem(
            id="b6", category="Makeup & Mehndi",
            item="Bridal HD Makeup (3 Functions) + Professional Mehndi Team",
            estimatedCost=round(budget * 0.035, 2),
            notes="Lead artist for bride + assistant artists for female guests"
        ),
        BudgetItem(
            id="b7", category="Safas, Favors & Gifts",
            item="Rajasthani Pagdis/Safas + Custom Mithai Gift Hampers",
            estimatedCost=round(budget * 0.035, 2),
            notes="Delivered to packaging room; includes Shahi Ittar flacons"
        ),
        BudgetItem(
            id="b8", category="Contingency & Shagun Buffer",
            item="Cash Envelopes for Service Staff, Drivers & Shagun Reserve",
            estimatedCost=round(budget * 0.04, 2),
            notes="Kept strictly reserved for unforeseen day-of expenses and dakshina"
        )
    ]

    timeline = [
        TimelineMilestone(
            id="t1", phase="9-12 Months Out",
            title="Book Heritage Venue & Block Shubh Muhurat Date",
            description="Consult family astrologer for auspicious Muhurat and lock in Palace resort contract.",
            completed=True, category="Venue"
        ),
        TimelineMilestone(
            id="t2", phase="6-8 Months Out",
            title="Hire Master Caterer, Photographer & Decorator",
            description="Conduct food tasting session, select live counters, and approve Lotus Mandap design.",
            completed=True, category="Vendors"
        ),
        TimelineMilestone(
            id="t3", phase="3-5 Months Out",
            title="Bridal Couture Trials & Sangeet Choreographer",
            description="Finalize bridal lehengas, sherwanis, and initiate weekend dance rehearsals with family.",
            completed=True, category="Attire"
        ),
        TimelineMilestone(
            id="t4", phase="2 Months Out",
            title="Send Digital WhatsApp Invites & Royal Box Cards",
            description="Dispatch mithai invitation boxes and collect guest arrival flight/train details.",
            completed=False, category="Guests"
        ),
        TimelineMilestone(
            id="t5", phase="3 Weeks Out",
            title="Final Room Allocation & Safa Headcounts",
            description="Assign room keys, coordinate airport pickup shuttle, and deliver vendor badges.",
            completed=False, category="Logistics"
        ),
        TimelineMilestone(
            id="t6", phase="Wedding Week",
            title="Pack Shagun Envelopes, Havan Samagri & Haldi Gear",
            description="Distribute timeline cards to immediate family; coordinate with Panditji.",
            completed=False, category="Final Prep"
        )
    ]

    schedule = [
        ScheduleItem(
            id="s1", time="09:00 AM", activity="Peeli Haldi & Phoolon ki Holi",
            location="Palace Poolside Lawn", coordinator="Bride & Groom Cousins",
            notes="Yellow dress code; organic herbal turmeric and marigold petals"
        ),
        ScheduleItem(
            id="s2", time="12:30 PM", activity="Traditional Rajasthani High Tea & Lunch",
            location="Courtyard Dining", coordinator="Catering Lead",
            notes="Live Dal Baati and Kachori counters open"
        ),
        ScheduleItem(
            id="s3", time="03:30 PM", activity="Bridal & Groom Royal Dressing & Safa Bandhai",
            location="Royal Suites", coordinator="Stylist & Pagdi Master",
            notes="Candid photos of jewelry, sehra, and kaleeras"
        ),
        ScheduleItem(
            id="s4", time="05:00 PM", activity="Royal Baraat Assembly & Swagat",
            location="Palace Main Gate", coordinator="Dhol Master & Groom Team",
            notes="Vintage car lead, Punjabi Dhol beat, rosewater spray"
        ),
        ScheduleItem(
            id="s5", time="06:15 PM", activity="Milni Ceremony & Royal Gateway Welcome",
            location="Inner Palace Courtyard", coordinator="Family Elders",
            notes="Garland exchange by fathers, Shehnai welcoming notes"
        ),
        ScheduleItem(
            id="s6", time="07:00 PM", activity="Grand Varmala Ceremony under Cold Sparks",
            location="Grand Palace Stage", coordinator="Event Coordinator",
            notes="Dramatic smoke curtain and 360-degree cold fire fountains"
        ),
        ScheduleItem(
            id="s7", time="07:45 PM", activity="Royal Wedding Reception Feast & Live Sufi Set",
            location="Main Lawn & Banquet", coordinator="Catering Manager",
            notes="All live food stations active; photo ops with couple"
        ),
        ScheduleItem(
            id="s8", time="10:30 PM", activity="Vedic Pheras & Kanyadaan at the Lotus Mandap",
            location="Lakeside Lotus Mandap", coordinator="Panditji & Siblings",
            notes="Sacred Agni havan, 7 vows recitation, Sindoor & Mangalsutra"
        ),
        ScheduleItem(
            id="s9", time="12:30 AM", activity="Emotional Vidaai Ceremony",
            location="Palace Gateway", coordinator="Parents & Coordinator",
            notes="Floral coin toss, vintage car departure"
        )
    ]

    vendors = [
        VendorItem(
            id="v1", category="Heritage Venue", vendorName="Chomu Palace Heritage Resort",
            contact="weddings@chomupalace.com | +91 98290 12345",
            estimatedCost=round(budget * 0.34, 2), status="booked",
            checklist=[
                ChecklistTask(id="c1", task="Confirm 2-day booking and 40 guest rooms", completed=True),
                ChecklistTask(id="c2", task="Review outdoor lawn sound curfew rules (10:00 PM)", completed=True),
                ChecklistTask(id="c3", task="Inspect Mandap power connection and backup generator", completed=False)
            ]
        ),
        VendorItem(
            id="v2", category="Catering & Live Stalls", vendorName="Shahi Dawat Caterers & Chaat Co.",
            contact="catering@shahidawat.in | +91 98110 54321",
            estimatedCost=round(budget * 0.30, 2), status="booked",
            checklist=[
                ChecklistTask(id="c4", task="Conduct tasting for 5-flavor Golgappe & Banarasi Chaat", completed=True),
                ChecklistTask(id="c5", task="Confirm dedicated Pure Veg & Jain counters", completed=False),
                ChecklistTask(id="c6", task="Ensure midnight Masala Chai and Garma-garam Jalebi service", completed=False)
            ]
        ),
        VendorItem(
            id="v3", category="Photography & Video", vendorName="Drishti Films & Candid Arts",
            contact="contact@drishtifilms.in | +91 99201 67890",
            estimatedCost=round(budget * 0.08, 2), status="booked",
            checklist=[
                ChecklistTask(id="c7", task="Confirm 4-member camera crew + 4K drone operator", completed=True),
                ChecklistTask(id="c8", task="Deliver 60-second Instagram teaser reel in 48 hours", completed=False),
                ChecklistTask(id="c9", task="Capture complete family VIP portraits before Baraat", completed=False)
            ]
        ),
        VendorItem(
            id="v4", category="Decor & Mandap", vendorName="Utsav Mandap & Floral Designers",
            contact="design@utsavmandap.in | +91 97170 98765",
            estimatedCost=round(budget * 0.12, 2), status="booked",
            checklist=[
                ChecklistTask(id="c10", task="Approve floating Lotus Mandap and marigold motifs", completed=True),
                ChecklistTask(id="c11", task="Order 100 kg fresh orange & yellow marigolds", completed=True),
                ChecklistTask(id="c12", task="Ensure teardown protocol clean by 03:00 AM", completed=False)
            ]
        )
    ]

    return EventPlan(
        id=plan_id, title=effective_title, eventType="wedding",
        date=req.date or "2027-11-24", location=req.location or "Chomu Palace Heritage Resort, Jaipur, Rajasthan",
        guestCount=guests, currency=curr, totalBudget=budget,
        vibeAndStyle=req.vibeAndStyle or "Royal Rajasthani heritage, marigold cascades, brass diyas, vibrant Sangeet beats",
        specialRequests=req.specialRequests or "",
        ideas=ideas, budgetBreakdown=budget_breakdown,
        timeline=timeline, dayOfSchedule=schedule, vendorChecklist=vendors
    )


def _synthesize_birthday(
    plan_id: str, title: str, req: GeneratePlanRequest, budget: float, guests: int, curr: str
) -> EventPlan:
    """Generates an authentic milestone Indian birthday (Janamdin / Annaprashan) blueprint."""
    fallback_title = "Kabir's Royal 1st Birthday & Annaprashan Utsav"
    effective_title = title if title and title != "Enchanted Birthday Celebration" else fallback_title
    ideas = EventIdeas(
        themeTitle="Bal Gopal Jungle Safari & Annaprashan Utsav",
        themeConcept=(
            f"A heartwarming milestone celebration uniting {guests} loved ones. Featuring traditional "
            f"Vedic Annaprashan blessings, an immersive pastel jungle safari backdrop, live South Indian "
            f"and chaat gastronomy, interactive children's entertainers, and bespoke family return gifts."
        ),
        colorPalette=[
            ColorSwatch(name="Haldi Gold", hex="#F59E0B"),
            ColorSwatch(name="Sage Jungle Green", hex="#10B981"),
            ColorSwatch(name="Baby Sky Blue", hex="#38BDF8"),
            ColorSwatch(name="Warm Amber Ochre", hex="#D97706"),
            ColorSwatch(name="Pure Pearl White", hex="#F8FAFC")
        ],
        signatureFoodAndDrinks=[
            "Mango Lassi & Fresh Sugarcane Juice welcome coolers with mint sprigs",
            "Live South Indian Live Dosa & Crispy Vada Cart with 4 homemade chutneys",
            "Live Purani Dilli Chaat Counter: Sev Puri, Dahi Papdi Chaat, and Pani Puri",
            "Custom 2-tier Jungle Safari eggless Vanilla Mango fresh cream cake",
            "Artisanal Matka Kulfi & Garam Gulab Jamun live dessert station"
        ],
        activitiesAndEntertainment=[
            "Vedic Annaprashan Ceremony: First rice feeding blessing by maternal uncle with engraved silver spoon",
            "Traditional Thali Choice ritual (Baby selects between pen, coin, book, and clay)",
            "Interactive Rajasthani Puppet Show & live balloon twister artist for kids",
            "Custom Baby Milestone Trivia game and childhood photo memory wall",
            "High-energy family musical chairs and baby dance floor set"
        ],
        decorAndAtmosphere=[
            "Pastel balloon arch and safari animal cutout backdrop with warm custom neon baby name",
            "Fresh marigold and mango leaf toran entrance archway",
            "Custom illuminated photo booth with baby monthly milestone photo cards",
            "Low brass tables with comfortable floor gaddas and silk bolsters for elders"
        ],
        surpriseElements=[
            "Surprise emotional first-year retrospective video montage projected on LED wall",
            "Baby's royal grand entry in a flower-decorated wooden chariot pushed by cousins",
            "Bespoke return gift hampers with personalized brass diyas and artisanal dry fruits"
        ],
        moodboardPrompt=(
            f"Joyful Indian 1st birthday and Annaprashan celebration, pastel jungle safari and marigold "
            f"floral decor, brass urlis, warm fairy lights, happy Indian family and baby in traditional "
            f"kurta, live food stalls, {guests} guests, cinematic 8k"
        )
    )

    budget_breakdown = [
        BudgetItem(
            id="b1", category="Venue & Hall",
            item="Boutique Banquet Lawn & Indoor AC Hall (6 Hours)",
            estimatedCost=round(budget * 0.30, 2),
            notes="Includes stage, kid-friendly play area, dining hall, and generator backup"
        ),
        BudgetItem(
            id="b2", category="Food & Beverage Catering",
            item=f"Pure Veg Multi-Cuisine Feast & Live Counters ({guests} guests)",
            estimatedCost=round(budget * 0.35, 2),
            notes="Includes Live Dosa, Chaat counter, mocktails, lunch buffet, and high tea"
        ),
        BudgetItem(
            id="b3", category="Decor, Safari Theme & Balloons",
            item="Jungle Safari Backdrop, Balloon Garland & Neon Name Sign",
            estimatedCost=round(budget * 0.14, 2),
            notes="Includes entrance arch, stage setup, and custom acrylic cutouts"
        ),
        BudgetItem(
            id="b4", category="Photography & Video",
            item="Candid Baby & Family Photography + Highlight Video Reel",
            estimatedCost=round(budget * 0.08, 2),
            notes="Includes dedicated pre-event cake smash photoshoot and edited album"
        ),
        BudgetItem(
            id="b5", category="Kids Entertainment & Magic Show",
            item="Emcee, Puppet Show, Balloon Twister & Tattoo Artist",
            estimatedCost=round(budget * 0.05, 2),
            notes="2.5 hours of high-engagement children entertainment and party games"
        ),
        BudgetItem(
            id="b6", category="Cake & Desserts",
            item="Designer 2-Tier Eggless Cake + Live Matka Kulfi",
            estimatedCost=round(budget * 0.04, 2),
            notes="Custom jungle safari modeling chocolate toppers"
        ),
        BudgetItem(
            id="b7", category="Return Gifts & Favors",
            item="Personalized Return Gift Hampers for Kids and Elders",
            estimatedCost=round(budget * 0.04, 2),
            notes="Customized educational activity kits for kids; brass diyas for family"
        )
    ]

    timeline = [
        TimelineMilestone(
            id="t1", phase="6-8 Weeks Out", title="Consult Astrologer & Book Banquet Hall",
            description="Fix auspicious Annaprashan Muhurat time and secure family venue contract.",
            completed=True, category="Venue"
        ),
        TimelineMilestone(
            id="t2", phase="4 Weeks Out", title="Send Digital WhatsApp Video Invitations",
            description="Design personalized cartoon video invite and collect guest confirmations.",
            completed=False, category="Guestlist"
        ),
        TimelineMilestone(
            id="t3", phase="3 Weeks Out", title="Finalize Live Counters & Order Theme Cake",
            description="Approve Live Dosa and Chaat menu; finalize eggless fruit cake flavor.",
            completed=False, category="Catering"
        ),
        TimelineMilestone(
            id="t4", phase="1 Week Out", title="Compile 12-Month Photo Montage & Playlist",
            description="Gather monthly baby photos for projector screening; finalize kids nursery dance tracks.",
            completed=False, category="Media"
        ),
        TimelineMilestone(
            id="t5", phase="Day Before", title="Pack Silver Thali, Puja Samagri & Return Gifts",
            description="Engrave silver bowl and spoon, prepare baby extra outfits and favor bags.",
            completed=False, category="Prep"
        )
    ]

    schedule = [
        ScheduleItem(
            id="s1", time="10:00 AM", activity="Host Arrival & Stage/Balloon Decor Inspection",
            location="Main Hall", coordinator="Parents", notes="Verify AC cooling and baby changing lounge"
        ),
        ScheduleItem(
            id="s2", time="11:00 AM", activity="Guest Welcoming & Fresh Mango Lassi Coolers",
            location="Entrance Foyer", coordinator="Family Greeters", notes="Distribute welcome badges and wristbands"
        ),
        ScheduleItem(
            id="s3", time="11:30 AM", activity="Vedic Annaprashan Puja & First Rice Feeding",
            location="Puja Mandap Stage", coordinator="Panditji & Mama", notes="Sacred kheer feeding with silver spoon"
        ),
        ScheduleItem(
            id="s4", time="12:15 PM", activity="Traditional Thali Selection Ritual & Photos",
            location="Stage", coordinator="Grandparents", notes="Baby chooses item; family blessing"
        ),
        ScheduleItem(
            id="s5", time="12:45 PM", activity="Kids Magic Show, Puppet Act & Balloon Twisting",
            location="Kids Play Zone", coordinator="Emcee Artist", notes="High crowd engagement for children"
        ),
        ScheduleItem(
            id="s6", time="01:15 PM", activity="Grand Birthday Cake Cutting & Confetti Blast",
            location="Main Stage", coordinator="All Family", notes="Singing birthday song; light sparkler candles"
        ),
        ScheduleItem(
            id="s7", time="01:30 PM", activity="Grand Feast & Live Dosa/Chaat Counters Open",
            location="Dining Pavilion", coordinator="Catering Lead", notes="All 4 live food stations operational"
        ),
        ScheduleItem(
            id="s8", time="03:00 PM", activity="Return Gift Distribution & Farewell",
            location="Lobby Exit", coordinator="Host Team", notes="Hand over customized return hampers"
        )
    ]

    vendors = [
        VendorItem(
            id="v1", category="Banquet Venue", vendorName="Royal Greens Banquet & Lawns",
            contact="events@royalgreens.in | +91 98765 43210", estimatedCost=round(budget * 0.30, 2), status="booked",
            checklist=[
                ChecklistTask(id="c1", task="Confirm 6-hour hall access and AC setup", completed=True),
                ChecklistTask(id="c2", task="Verify kid play zone safety mats", completed=False)
            ]
        ),
        VendorItem(
            id="v2", category="Pure Veg Catering", vendorName="Annapurna Celebrations Caterers",
            contact="chefavinash@annapurna.in | +91 99887 76655", estimatedCost=round(budget * 0.35, 2), status="booked",
            checklist=[
                ChecklistTask(id="c3", task="Confirm 4 varieties of live dosas and crispy vadas", completed=False),
                ChecklistTask(id="c4", task="Ensure pure cow milk kheer for Annaprashan ritual", completed=True)
            ]
        ),
        VendorItem(
            id="v3", category="Theme Decorator", vendorName="Balloon Magic & Kids Decor",
            contact="info@balloonmagic.in | +91 91234 56789", estimatedCost=round(budget * 0.14, 2), status="researching",
            checklist=[
                ChecklistTask(id="c5", task="Approve pastel balloon garland color shade", completed=False),
                ChecklistTask(id="c6", task="Confirm custom neon baby name signage", completed=False)
            ]
        )
    ]

    return EventPlan(
        id=plan_id, title=effective_title, eventType="birthday",
        date=req.date or "2026-11-20", location=req.location or "Royal Greens Banquet & Lawns, New Delhi",
        guestCount=guests, currency=curr, totalBudget=budget,
        vibeAndStyle=req.vibeAndStyle or "Vedic Annaprashan puja, jungle safari backdrop, return gifts, live chaat and kulfi",
        specialRequests=req.specialRequests or "",
        ideas=ideas, budgetBreakdown=budget_breakdown,
        timeline=timeline, dayOfSchedule=schedule, vendorChecklist=vendors
    )


def _synthesize_community(
    plan_id: str, title: str, req: GeneratePlanRequest, budget: float, guests: int, curr: str
) -> EventPlan:
    """Generates an inclusive Indian community festival (Diwali Mela / Dandiya Raas) blueprint."""
    fallback_title = "Gokuldham Grand Diwali Mela & Dandiya Raas Utsav"
    effective_title = title if title and title != "Enchanted Community Celebration" else fallback_title
    ideas = EventIdeas(
        themeTitle="Deepavali Mahotsav & Dandiya Raas Milan",
        themeConcept=(
            f"A vibrant, grand cultural festival uniting {guests} community residents and families. "
            f"Featuring authentic Gujarati Dandiya Raas, live Garba orchestra, multi-regional Indian "
            f"street food stalls, traditional Rangoli contests, and a grand 108-diya Maha Aarti."
        ),
        colorPalette=[
            ColorSwatch(name="Genda Marigold Orange", hex="#EA580C"),
            ColorSwatch(name="Peacock Green", hex="#16A34A"),
            ColorSwatch(name="Deep Royal Indigo", hex="#312E81"),
            ColorSwatch(name="Kesar Yellow", hex="#EAB308"),
            ColorSwatch(name="Gulal Crimson Red", hex="#DC2626")
        ],
        signatureFoodAndDrinks=[
            "Garma-garam Masala Chai & Kesar Badam Milk stalls in authentic clay kulhads",
            "Live Street Food Bazaar: Mumbai Pav Bhaji, Delhi Chole Bhature, and Banarasi Chaat",
            "Community Mithai Mela: Hot Kaju Katli, Motichoor Ladoos, and Garma-garam Jalebi-Fafda",
            "Complimentary Roasted Bhutta (Sweet Corn), Cotton Candy, and Popcorn for children"
        ],
        activitiesAndEntertainment=[
            "Grand Dandiya Raas & Traditional Garba with Live Gujarati Folk & Bollywood Fusion Band",
            "Inter-Society Rangoli Making Championship with cash prizes and trophies",
            "Grand Deepotsav Maha Aarti with 108 brass lamps and conch blowing",
            "Children's Ramayana Character Fancy Dress Competition & Talent Showcase",
            "Grand Bumper Diwali Lucky Draw Raffle sponsored by local community merchants"
        ],
        decorAndAtmosphere=[
            "10,000 warm glowing fairy lights and traditional Marigold torans across society perimeter",
            "Grand entrance floral Rangoli with brass urlis and floating scented diyas",
            "Dedicated Dandiya stick distribution booth and colorful selfie photo pavilion",
            "Eco-friendly zero-waste dry/wet trash segregation points with volunteer marshals"
        ],
        surpriseElements=[
            "Grand synchronized cold-pyrotechnic sparkle shower during peak Dandiya round at 09:30 PM",
            "Surprise Bumper Diwali Gift Hamper draw announced by Community Association President",
            "Free distribution of handcrafted eco-friendly clay diyas to every attending family"
        ],
        moodboardPrompt=(
            f"Vibrant Indian Diwali community festival and Dandiya Raas at night, open society grounds, "
            f"colorful traditional lehengas and kurtas, thousands of fairy lights and diyas, live music stage, "
            f"food stalls, {guests} attendees, cinematic 8k"
        )
    )

    budget_breakdown = [
        BudgetItem(
            id="b1", category="Permits, Security & Police NOC",
            item="Police Permission, Fire Safety NOC, Security Guards & Ambulance",
            estimatedCost=round(budget * 0.15, 2),
            notes="Mandatory compliance for public gathering and sound curfew at 10:00 PM"
        ),
        BudgetItem(
            id="b2", category="Sound, Stage & Lighting",
            item="Professional Line Array Sound, Garba Stage & 10,000 Fairy Lights",
            estimatedCost=round(budget * 0.25, 2),
            notes="Includes silent diesel generator backup and audio mixing console"
        ),
        BudgetItem(
            id="b3", category="Tents, Seating & Sanitation",
            item="Waterproof Canopies, 300 Chairs, Mobile Toilets & Dustbins",
            estimatedCost=round(budget * 0.22, 2),
            notes="Ensures senior-friendly seating and clean sanitization"
        ),
        BudgetItem(
            id="b4", category="Live Garba Band & Singers",
            item="Traditional Gujarati Folk Ensemble & Celebrity Emcee",
            estimatedCost=round(budget * 0.18, 2),
            notes="4 hours of high-energy live Dandiya Raas and Garba music"
        ),
        BudgetItem(
            id="b5", category="Kids Zone & Competitions",
            item="Trophies, Rangoli Colors, Bumper Raffle Prizes & Games",
            estimatedCost=round(budget * 0.10, 2),
            notes="Prizes for best dressed, best dancers, and Rangoli winners"
        ),
        BudgetItem(
            id="b6", category="Decor & Diyas",
            item="Fresh Marigolds, 500 Clay Diyas, Urlis & Signage Banners",
            estimatedCost=round(budget * 0.05, 2),
            notes="Traditional cultural ambiance and directional entry signs"
        ),
        BudgetItem(
            id="b7", category="First Aid & Emergency Buffer",
            item="First Aid Post, Free Hydration Dispensers & Contingency Reserve",
            estimatedCost=round(budget * 0.05, 2),
            notes="Safety marshals reserve"
        )
    ]

    timeline = [
        TimelineMilestone(
            id="t1", phase="6-8 Weeks Out", title="Apply for Police Permission & Fire NOC",
            description="Submit festival blueprint to local police station and municipal corporation.",
            completed=True, category="Permits"
        ),
        TimelineMilestone(
            id="t2", phase="4 Weeks Out", title="Book Live Garba Orchestra & Sound Vendor",
            description="Sign contracts with live folk singers, dhol troupe, and lighting contractor.",
            completed=True, category="Vendors"
        ),
        TimelineMilestone(
            id="t3", phase="3 Weeks Out", title="Allot Society Food Stalls & Announce Contests",
            description="Invite home-chefs for stalls; open registrations for Rangoli & Fancy Dress.",
            completed=False, category="Community"
        ),
        TimelineMilestone(
            id="t4", phase="1 Week Out", title="Order 500 Pairs of Dandiya Sticks & Diyas",
            description="Procure wooden dandiya sticks, clay diyas, and printed winner trophies.",
            completed=False, category="Supplies"
        ),
        TimelineMilestone(
            id="t5", phase="Day of Event", title="Electrical Audit & Volunteer Safety Briefing",
            description="Inspect all wire insulation, fire extinguishers, and assign volunteer marshal posts.",
            completed=False, category="Safety"
        )
    ]

    schedule = [
        ScheduleItem(
            id="s1", time="04:00 PM", activity="Food Stalls & Artisan Booths Setup",
            location="Society Ground Perimeter", coordinator="Vendor Coordinator", notes="Inspect fire extinguishers at stalls"
        ),
        ScheduleItem(
            id="s2", time="05:00 PM", activity="Inter-Society Rangoli Competition Kickoff",
            location="Central Pathway", coordinator="Cultural Committee", notes="Participants create vibrant Rangolis"
        ),
        ScheduleItem(
            id="s3", time="06:30 PM", activity="Official Welcome & Grand Deepotsav Maha Aarti",
            location="Main Stage & Temple Area", coordinator="President & Elders", notes="108 brass lamps lit with Vedic chants"
        ),
        ScheduleItem(
            id="s4", time="07:00 PM", activity="Children's Ramayana Fancy Dress Showcase",
            location="Main Stage", coordinator="Youth Club", notes="Kids perform mythological characters"
        ),
        ScheduleItem(
            id="s5", time="07:45 PM", activity="Round 1: Traditional Slow Garba (Taali Raas)",
            location="Central Dance Circle", coordinator="Live Band & MC", notes="All families dance together"
        ),
        ScheduleItem(
            id="s6", time="08:45 PM", activity="Round 2: High-Energy Dandiya Raas with Dhol",
            location="Central Dance Circle", coordinator="Live Band", notes="Dandiya sticks clicking to fast beats"
        ),
        ScheduleItem(
            id="s7", time="09:40 PM", activity="Prize Distribution & Bumper Raffle Draw",
            location="Main Stage", coordinator="RWA Committee", notes="Awards for Best Dancers, Rangoli, and Raffle"
        ),
        ScheduleItem(
            id="s8", time="10:00 PM", activity="Sound Curfew Compliance & Silent Music Transition",
            location="Main Stage", coordinator="Sound Operator", notes="Strict 10:00 PM loudspeaker cutoff compliance"
        ),
        ScheduleItem(
            id="s9", time="10:30 PM", activity="Community Cleanup & Eco-Waste Sorting",
            location="Entire Grounds", coordinator="Green Volunteer Team", notes="Ensure clean grounds by midnight"
        )
    ]

    vendors = [
        VendorItem(
            id="v1", category="Police & Permissions", vendorName="Local Municipal & Police Authorities",
            contact="support@delhipolice.gov.in", estimatedCost=round(budget * 0.15, 2), status="booked",
            checklist=[
                ChecklistTask(id="c1", task="Submit sound permit application for outdoor public event", completed=True),
                ChecklistTask(id="c2", task="Strict 10:00 PM loudspeaker curfew enforcement protocol", completed=True)
            ]
        ),
        VendorItem(
            id="v2", category="Sound & Lighting", vendorName="Utsav Sound & Stage Production",
            contact="sound@utsavproduction.in | +91 98101 23456", estimatedCost=round(budget * 0.25, 2), status="booked",
            checklist=[
                ChecklistTask(id="c3", task="Set up dual Line Array speakers and stage monitoring", completed=True),
                ChecklistTask(id="c4", task="String 10,000 warm LED fairy lights along perimeter", completed=False)
            ]
        ),
        VendorItem(
            id="v3", category="Live Band", vendorName="Sur Tarang Folk Garba Ensemble",
            contact="booking@surtarang.in | +91 99200 11223", estimatedCost=round(budget * 0.18, 2), status="contacted",
            checklist=[
                ChecklistTask(id="c5", task="Confirm 8-member orchestra with live dhol and dholak", completed=False),
                ChecklistTask(id="c6", task="Submit playlist of classic Gujarati Garba and Bollywood hits", completed=False)
            ]
        )
    ]

    return EventPlan(
        id=plan_id, title=effective_title, eventType="community",
        date=req.date or "2026-10-31", location=req.location or "Gokuldham Central Society Grounds, Mumbai",
        guestCount=guests, currency=curr, totalBudget=budget,
        vibeAndStyle=req.vibeAndStyle or "Dandiya Raas, Rangoli competition, 10 PM sound curfew compliance, home-chef stalls",
        specialRequests=req.specialRequests or "",
        ideas=ideas, budgetBreakdown=budget_breakdown,
        timeline=timeline, dayOfSchedule=schedule, vendorChecklist=vendors
    )


def _synthesize_custom(
    plan_id: str, title: str, req: GeneratePlanRequest, budget: float, guests: int, curr: str
) -> EventPlan:
    """Fallback custom synthesizer routing to birthday generator."""
    return _synthesize_birthday(plan_id, title, req, budget, guests, curr)


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
            context_str = json.dumps(req.eventContext, indent=2) if req.eventContext else "No context."
            system_instruction = (
                f"You are EventGenie AI, an experienced event planner.\n"
                f"Context: {context_str}\n"
                f"Be inspiring, empathetic, structured, and practical."
            )
            messages = [
                {"role": m.role if m.role == "user" else "model", "parts": [{"text": m.content}]}
                for m in req.chatHistory[-6:]
            ]
            messages.append({"role": "user", "parts": [{"text": req.message}]})

            for model_name in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
                try:
                    resp = client.models.generate_content(
                        model=model_name,
                        contents=[{"text": system_instruction}, *[m["parts"][0]["text"] for m in messages]]
                    )
                    if resp.text:
                        return resp.text
                except Exception as err:
                    logger.warning(f"Chat generation error with {model_name}: {err}")
                    continue
        except Exception as e:
            logger.error(f"Chat Gemini model invocation error: {e}")

    return _generate_heuristic_chat_reply(req.message, req.eventContext)


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
    currency = context.get("currency", "₹") if context else "₹"

    if any(k in msg for k in ["budget", "cost", "expensive", "cut", "save"]):
        return f"""### 💡 Strategic Budget Advice for {event_title}

When managing your budget ({currency} {budget}):

1. **The 50/30/20 Rule for Events**:
   - **50%**: Guest experience core (Venue, Catering, Live Chaat & Mithai counters).
   - **30%**: Atmosphere & Memory keepers (Candid Photography/Drone, Sangeet/DJ, Mandap & Floral Decor).
   - **20%**: Logistics, Contingency, Shagun Envelopes & Gifts/Safas.

2. **High-Impact Ways to Cut Costs Without Compromise**:
   - **Repurpose Floral Decor**: Repurpose Haldi yellow marigolds and brass urlis into the evening Pheras Mandap or dining entrance.
   - **Digital-First WhatsApp Box Invites**: Send bespoke motion video invites with RSVP tracking instead of heavy printed paper boxes.
   - **Composite Vendor Packages**: Bundle Pre-wedding shoot, Drone, and 4K Cinematic film under one production crew.
   - **Curate Live Counters**: Select 4 high-energy specialty live stalls (e.g. Purani Dilli Chaat, Live Dosa, Matka Kulfi) rather than endless buffet duplicates.

Would you like me to suggest specific adjustments to any item in your budget breakdown?
"""
    elif any(k in msg for k in ["timeline", "schedule", "time", "delay", "hour", "curfew", "police"]):
        return f"""### ⏱️ Timeline & Run-of-Show Expert Tips

For a smooth flow during {event_title}:

1. **Build in 15-Minute Ghost Buffers**:
   - Indian Baraats and Varmala ceremonies notoriously run 30-45 minutes late. Always schedule the Baraat arrival 45 minutes before the actual Varmala muhurat.
2. **Supreme Court 10:00 PM Sound Curfew Compliance**:
   - Transition amplified outdoor Punjabi Dhol and lawn DJ music into an acoustically insulated indoor banquet hall by 10:00 PM to comply with local police regulations.
3. **Day-of Coordinator Designation**:
   - Designate a trusted cousin or coordinator as the "Keeper of the Clock" to manage Panditji samagri and Muhurat timing.
4. **Golden Hour Twilight Portraits**:
   - Schedule bride and groom royal portraits 45 minutes before sunset for ethereal lighting.

Do you want to adjust any specific milestone or time slot in your Day-of Schedule?
"""
    elif any(k in msg for k in ["vendor", "contract", "hire", "caterer", "photographer", "pandit"]):
        return f"""### 📋 Essential Vendor Vetting Checklist

Key questions you must ask vendors before signing for {event_title}:

1. **For Caterers & Live Stalls**:
   - Are live stall gas cylinders, chafing dishes, pure-veg separation, and cleanup staff included in the per-plate quote?
   - What is your policy on midnight Masala Chai and hot snacks for late-night Pheras?
2. **For Photographers & Videographers**:
   - Do you have dual-slot memory backup, drone flight clearances, and backup camera bodies?
   - What is the turnaround timeline for the 60-second Instagram teaser reel and 4K full wedding film?
3. **For DJs, Dhol & Entertainment**:
   - Do you provide wireless microphones for the Panditji and family Sangeet performances?
4. **Contracts & Dakshina/Shagun Envelopes**:
   - Never pay 100% upfront. Standard industry milestone is 25-50% booking advance, balance after the main event.

Let me know which vendor you are vetting next, and I can generate custom questions for them!
"""
    elif any(k in msg for k in ["idea", "theme", "decor", "game", "activity", "chaat"]):
        return f"""### ✨ Personalized Creative Concepts for {event_title}

Here are some fresh, culturally vibrant ideas to elevate the guest experience:

1. **Interactive Purani Dilli Chaat Gali**:
   - Set up live Banarasi Tamatar Chaat, Palak Patta Chaat, and 5-flavored water Golgappe with personalized spice levels.
2. **Personalized Shahi Ittar Bar**:
   - A master perfumer blends organic Indian rose and sandalwood ittars live into personalized glass flacons for guest souvenirs.
3. **Family Sangeet Face-Off & Flash-Mob**:
   - A choreographed dance face-off between Bride and Groom teams with cold-spark fireworks on the hook step!
4. **Royal Lotus Floating Mandap**:
   - Twilight Vedic Pheras on a water-stage surrounded by 10,000 marigolds, scented mogra strings, and floating brass diyas.

Would you like more ideas tailored to a specific vibe or guest age range?
"""
    else:
        return f"""### 🌟 EventGenie AI at your service!

I am here to help you coordinate every detail of **{event_title}**.

Here is what we can do together:
- **Refine your Budget**: Reallocate funds in INR (₹), calculate per-guest costs, and optimize vendor quotes.
- **Perfect your Timeline**: Build a seamless day-of schedule, Shubh Muhurat alignment, and 10 PM sound curfew management.
- **Vendor CRM & Checklists**: Track caterers, decorators, photographers, Panditji, and dhol troupes.
- **Creative Ideation**: Suggest royal themes, live Chaat Gali setups, Sangeet concepts, and personalized return gifts.

What specific aspect of your {event_type} would you like to explore next?
"""
