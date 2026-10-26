"""
CelebrateAI - Generative AI Service & Synthesis Engine
Integrates Google Gemini 2.5/2.0 Flash SDK with an intelligent offline fallback engine.
"""

import os
import json
import re
import uuid
import logging
from typing import Optional, Dict, Any, List

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
            return json.loads(text[first:last+1])
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
            prompt = f"""
You are an elite, world-class event planner and creative director.
Generate a complete, deeply detailed event plan in JSON format based on the following specifications:

Event Type: {request.eventType}
Event Title: {request.title or f"{request.eventType.capitalize()} Celebration"}
Estimated Guests: {request.guestCount}
Total Budget: {request.totalBudget} {request.currency}
Target Date: {request.date or "Flexible / Upcoming Season"}
Location / Setting: {request.location or "City / Venue of choice"}
Vibe & Aesthetic Style: {request.vibeAndStyle}
Special Wishes / Requests: {request.specialRequests or "None specified"}

Respond ONLY with a valid JSON object matching this schema exactly:
{{
  "id": "gen-{uuid.uuid4().hex[:8]}",
  "title": "{request.title or f'{request.eventType.capitalize()} Celebration'}",
  "eventType": "{request.eventType}",
  "date": "{request.date}",
  "location": "{request.location}",
  "guestCount": {request.guestCount},
  "currency": "{request.currency}",
  "totalBudget": {request.totalBudget},
  "vibeAndStyle": "{request.vibeAndStyle}",
  "specialRequests": "{request.specialRequests}",
  "ideas": {{
    "themeTitle": "Creative theme title",
    "themeConcept": "2-3 sentences explaining the overarching design, aesthetic and guest experience",
    "colorPalette": [
      {{"name": "Color Name", "hex": "#HEXCODE"}},
      {{"name": "Color Name", "hex": "#HEXCODE"}},
      {{"name": "Color Name", "hex": "#HEXCODE"}},
      {{"name": "Color Name", "hex": "#HEXCODE"}},
      {{"name": "Color Name", "hex": "#HEXCODE"}}
    ],
    "signatureFoodAndDrinks": ["Item 1 with ingredients & flavor profile", "Item 2", "Item 3", "Item 4"],
    "activitiesAndEntertainment": ["Interactive activity 1", "Music / entertainment 2", "Activity 3", "Activity 4"],
    "decorAndAtmosphere": ["Decor detail 1", "Lighting / floral detail 2", "Atmosphere touch 3", "Decor detail 4"],
    "surpriseElements": ["Surprise 1", "Surprise 2", "Surprise 3"],
    "moodboardPrompt": "Detailed visual text prompt for AI image generation of this event setting"
  }},
  "budgetBreakdown": [
    {{
      "id": "b1",
      "category": "Category name (e.g. Venue, Catering & Bar, Decor & Floral, Photography/Video, Entertainment, Permits/Logistics, Contingency)",
      "item": "Item name and description",
      "estimatedCost": 0.0,
      "actualCost": 0.0,
      "paidAmount": 0.0,
      "status": "planned",
      "notes": "Practical planning advice or inclusions"
    }}
  ],
  "timeline": [
    {{
      "id": "t1",
      "phase": "Milestone phase (e.g. 6-9 Months Out, 3 Months Out, 1 Month Out, Week Of)",
      "title": "Milestone title",
      "description": "Actionable task instructions",
      "dueDate": "",
      "completed": false,
      "category": "Category tag"
    }}
  ],
  "dayOfSchedule": [
    {{
      "id": "s1",
      "time": "09:00 AM",
      "activity": "Detailed activity name",
      "location": "Specific zone / room",
      "coordinator": "Role or person in charge",
      "notes": "Key cues and instructions",
      "status": "upcoming"
    }}
  ],
  "vendorChecklist": [
    {{
      "id": "v1",
      "category": "Vendor category",
      "vendorName": "Type or placeholder name",
      "contact": "Contact info / inquiry email template note",
      "estimatedCost": 0.0,
      "contractedCost": 0.0,
      "status": "researching",
      "checklist": [
        {{"id": "c1", "task": "Checklist task description", "completed": false}},
        {{"id": "c2", "task": "Checklist task description", "completed": false}}
      ],
      "notes": "Key contractual questions or deliverables"
    }}
  ]
}}

Ensure realistic budget allocations that sum up near {request.totalBudget} {request.currency}.
"""
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
    title = request.title or (
        f"Enchanted Celebration: {request.vibeAndStyle}" if request.vibeAndStyle else f"Custom {ev_type.capitalize()} Experience"
    )

    plan_id = f"plan-{uuid.uuid4().hex[:8]}"

    if ev_type == "wedding":
        return _synthesize_wedding(plan_id, title, request, total_b, guests, curr)
    elif ev_type == "birthday":
        return _synthesize_birthday(plan_id, title, request, total_b, guests, curr)
    elif ev_type == "community":
        return _synthesize_community(plan_id, title, request, total_b, guests, curr)
    else:
        return _synthesize_custom(plan_id, title, request, total_b, guests, curr)

def _synthesize_wedding(plan_id: str, title: str, req: GeneratePlanRequest, budget: float, guests: int, curr: str) -> EventPlan:
    """Generates an authentic, luxury wedding celebration blueprint."""
    ideas = EventIdeas(
        themeTitle="Opulent Botanicals & Golden Hour Radiance",
        themeConcept=f"An unforgettable wedding blending timeless romantic architecture with modern botanical splendor. Natural cascading florals, ambient candlelight, customized culinary storytelling, and an unforgettable celebration for {guests} cherished guests.",
        colorPalette=[
            ColorSwatch(name="Champagne Gold", hex="#E6CA65"),
            ColorSwatch(name="Sage & Eucalyptus", hex="#607D67"),
            ColorSwatch(name="Dusty Rose", hex="#C98986"),
            ColorSwatch(name="Warm Alabaster", hex="#F7F5F0"),
            ColorSwatch(name="Deep Slate Charcoal", hex="#2C3539")
        ],
        signatureFoodAndDrinks=[
            "The Vow & Tonic: Botanical gin, elderflower liqueur, fresh clarified grapefruit, and thyme sprig",
            "Golden Hour Bourbon Smash: Bourbon, peach puree, mint, honey-ginger drizzle",
            f"Artisanal Farm-to-Table Plated Dinner customized for {guests} guests with vegan and gluten-free pairings",
            "Midnight Truffle Fry & Gourmet Brioche Slider Station"
        ],
        activitiesAndEntertainment=[
            "Live String Trio for Ceremony & Cocktail Hour transitioning into high-energy live band",
            "Audio Guestbook in a restored vintage phone for heartfelt audio voicemail keepsakes",
            "Custom 360-degree slow motion video lounge with instant phone airdrop",
            "Sparkler and cold-spark fountain arch for the newlyweds' grand farewell"
        ],
        decorAndAtmosphere=[
            "Suspended floral chandeliers with warm Edison bulb filament glow",
            "Custom calligraphed linen seating charts and acrylic table identifiers",
            "Lush ceremony arch draped with ivory chiffon, garden roses, and olive foliage",
            "Floor-standing mirror photo moments with custom monogram decal"
        ],
        surpriseElements=[
            "Surprise choreographed first dance dip with low-lying dry ice fog cloud effect",
            "Personalized handwritten thank-you notes waiting under each guest's dinner napkin",
            "Surprise espresso martini cart rolling out during the 10:00 PM dance peak"
        ],
        moodboardPrompt=f"Romantic luxury wedding reception ballroom, golden hour candlelight, lush greenery and white rose centerpieces, farm tables, ambient fairy lights, {guests} guests enjoying celebration, 8k cinematic photography"
    )

    budget_breakdown = [
        BudgetItem(id="b1", category="Venue & Rentals", item="Ceremony & Reception Venue Hire with Tables/Chairs", estimatedCost=round(budget * 0.28, 2), notes="Includes 10-hour access and bridal preparation suite"),
        BudgetItem(id="b2", category="Catering & Bar", item=f"Gourmet Meal & Open Bar Service ({guests} guests)", estimatedCost=round(budget * 0.35, 2), notes=f"Approx {round((budget * 0.35) / max(guests, 1), 2)} per guest for food, drinks, and service staff"),
        BudgetItem(id="b3", category="Photography & Video", item="Full Day 2-Shooter Photo & Cinematic Drone Video", estimatedCost=round(budget * 0.12, 2), notes="8 hours coverage, online gallery, and teaser film"),
        BudgetItem(id="b4", category="Floral & Decor", item="Ceremony Arch, Centerpieces, Bouquets & Mood Lighting", estimatedCost=round(budget * 0.10, 2), notes="Repurposes ceremony floral arrangements to the bridal table"),
        BudgetItem(id="b5", category="Entertainment & DJ", item="Ceremony Acoustic Strings + Reception Live Band/DJ", estimatedCost=round(budget * 0.07, 2), notes="Includes wireless microphones, sound PA system and dancefloor lighting"),
        BudgetItem(id="b6", category="Attire, Hair & Makeup", item="Hair & Makeup Glam Team for Bride and Party", estimatedCost=round(budget * 0.04, 2), notes="Includes prior hair/makeup trial session"),
        BudgetItem(id="b7", category="Contingency & Emergency Buffer", item="Weather backup, last-minute additions and vendor tips", estimatedCost=round(budget * 0.04, 2), notes="Kept strictly reserved for unforeseen day-of expenses")
    ]

    timeline = [
        TimelineMilestone(id="t1", phase="9-12 Months Out", title="Establish Budget & Book Ceremony/Reception Venue", description="Lock in wedding date, pay deposit, and secure venue contract.", completed=True, category="Venue"),
        TimelineMilestone(id="t2", phase="6-8 Months Out", title="Select Photographer, Videographer & Caterer", description="Conduct menu tasting, review vendor portfolios, and execute contracts.", completed=True, category="Vendors"),
        TimelineMilestone(id="t3", phase="4-5 Months Out", title="Launch Wedding Website & Send Formal Invitations", description="Collect guest RSVPs, dietary needs, and hotel block bookings.", completed=False, category="Stationery"),
        TimelineMilestone(id="t4", phase="2-3 Months Out", title="Finalize Attire, Florals & Music Playlists", description="Submit must-play and do-not-play track lists, review floral centerpiece mockups.", completed=False, category="Design"),
        TimelineMilestone(id="t5", phase="1 Month Out", title="Final RSVP Count & Seating Plan Submission", description="Deliver final meal counts to caterer and create physical seating chart.", completed=False, category="Logistics"),
        TimelineMilestone(id="t6", phase="Week Of", title="Wedding Rehearsal & Emergency Kit Pack", description="Run through ceremony processional, prepare vendor gratuity envelopes.", completed=False, category="Rehearsal")
    ]

    schedule = [
        ScheduleItem(id="s1", time="08:30 AM", activity="Bridal Suite Hair & Makeup Glam Session", location="Bridal Suite", coordinator="Lead Stylist", notes="Light breakfast and mimosa bar for wedding party"),
        ScheduleItem(id="s2", time="11:30 AM", activity="Vendor Rentals & Florist Load-In", location="Main Hall & Garden", coordinator="Day-of Coordinator", notes="Inspect table layout, linens, and floral arch"),
        ScheduleItem(id="s3", time="01:30 PM", activity="Groom & Groomsmen Getting Ready", location="Groom Lounge", coordinator="Best Man", notes="Boutonnières pinned, detail flat-lay photos"),
        ScheduleItem(id="s4", time="03:00 PM", activity="First Look & Private Couple Portraits", location="Garden Terrace", coordinator="Photographer", notes="Intimate portrait session before guests arrive"),
        ScheduleItem(id="s5", time="04:30 PM", activity="Guest Arrival & Pre-Ceremony Refreshments", location="Courtyard Foyer", coordinator="Venue Greeters", notes="Infused water and soft acoustic prelude music"),
        ScheduleItem(id="s6", time="05:00 PM", activity="Wedding Ceremony Processional", location="Outdoor Lawn / Altar", coordinator="Officiant & Coordinator", notes="Cue music; ring bearer and vows"),
        ScheduleItem(id="s7", time="05:45 PM", activity="Cocktail Hour & Passed Hors d'oeuvres", location="Terrace Lounge", coordinator="Catering Lead", notes="Family and wedding party formal group photos"),
        ScheduleItem(id="s8", time="07:00 PM", activity="Grand Entrance & Plated Dinner Service", location="Reception Hall", coordinator="MC / DJ", notes="Welcome toasts, champagne pours, main course"),
        ScheduleItem(id="s9", time="08:30 PM", activity="First Dance & Cake Cutting Ceremony", location="Dance Floor", coordinator="DJ", notes="Cue special lighting effect and dessert station opening"),
        ScheduleItem(id="s10", time="09:00 PM", activity="High-Energy Dance Party & Espresso Bar", location="Main Hall", coordinator="Band / DJ", notes="Late night slider snacks served at 10:30 PM"),
        ScheduleItem(id="s11", time="11:30 PM", activity="Sparkler Grand Send-Off & Departure", location="Front Portico", coordinator="Coordinator", notes="Light safety sparklers; getaway vehicle staged")
    ]

    vendors = [
        VendorItem(
            id="v1", category="Venue & Logistics", vendorName="Grand Estate & Garden Pavilion",
            contact="events@grandestatevenue.com", estimatedCost=round(budget * 0.28, 2), status="contacted",
            checklist=[
                ChecklistTask(id="c1", task="Confirm 10-hour rental window and curfew", completed=True),
                ChecklistTask(id="c2", task="Review sound decibel regulations", completed=False),
                ChecklistTask(id="c3", task="Submit third-party event insurance binder", completed=False)
            ]
        ),
        VendorItem(
            id="v2", category="Catering & Bar", vendorName="Epicurean Celebrations Co.",
            contact="catering@epicureancelebrations.com", estimatedCost=round(budget * 0.35, 2), status="researching",
            checklist=[
                ChecklistTask(id="c4", task="Schedule private tasting for 4 guests", completed=False),
                ChecklistTask(id="c5", task="Finalize cocktail menu and alcohol ordering model", completed=False),
                ChecklistTask(id="c6", task="Confirm dietary and allergy protocol", completed=False)
            ]
        ),
        VendorItem(
            id="v3", category="Photography & Video", vendorName="Prism Light Media Arts",
            contact="booking@prismlightmedia.com", estimatedCost=round(budget * 0.12, 2), status="researching",
            checklist=[
                ChecklistTask(id="c7", task="Review complete full-day wedding gallery samples", completed=False),
                ChecklistTask(id="c8", task="Confirm dual-photographer coverage & timeline", completed=False),
                ChecklistTask(id="c9", task="Deliver specific VIP family photo shot list", completed=False)
            ]
        ),
        VendorItem(
            id="v4", category="Floral & Styling", vendorName="Botanica Bloom Studio",
            contact="designer@botanicablooms.com", estimatedCost=round(budget * 0.10, 2), status="researching",
            checklist=[
                ChecklistTask(id="c10", task="Approve color palette and seasonal stem selections", completed=False),
                ChecklistTask(id="c11", task="Plan ceremony arch repurposing to reception stage", completed=False),
                ChecklistTask(id="c12", task="Confirm midnight teardown and cleanup logistics", completed=False)
            ]
        )
    ]

    return EventPlan(
        id=plan_id, title=title, eventType="wedding",
        date=req.date or "2027-06-20", location=req.location or "Scenic Country Club / Garden Estate",
        guestCount=guests, currency=curr, totalBudget=budget,
        vibeAndStyle=req.vibeAndStyle or "Timeless, romantic, and breathtaking",
        specialRequests=req.specialRequests or "",
        ideas=ideas, budgetBreakdown=budget_breakdown,
        timeline=timeline, dayOfSchedule=schedule, vendorChecklist=vendors
    )

def _synthesize_birthday(plan_id: str, title: str, req: GeneratePlanRequest, budget: float, guests: int, curr: str) -> EventPlan:
    """Generates an energetic milestone birthday blueprint."""
    ideas = EventIdeas(
        themeTitle="Electric Glow & Skyline Celebration",
        themeConcept=f"An electrifying, interactive celebration curated for {guests} guests. Featuring elevated street-gourmet gastronomy, an immersive audio-visual ambiance, nostalgic custom games, and surprise high-impact reveals.",
        colorPalette=[
            ColorSwatch(name="Vibrant Coral", hex="#FF6F61"),
            ColorSwatch(name="Neon Teal", hex="#00E5FF"),
            ColorSwatch(name="Electric Violet", hex="#8B5CF6"),
            ColorSwatch(name="Midnight Onyx", hex="#0F172A"),
            ColorSwatch(name="Warm Golden Amber", hex="#F59E0B")
        ],
        signatureFoodAndDrinks=[
            "The Birthday Spark: Sparkling prosecco, guava nectar, lime juice, and edible golden stars",
            "Smoked Citrus Margarita with chili-lime sea salt rim",
            "Interactive Bao Bun & Gourmet Taco Slider Station with plant-based options",
            "Mini Churro Bites with Mexican chocolate dip & Warm Salted Caramel Pretzel Skewers"
        ],
        activitiesAndEntertainment=[
            "Custom-curated Birthday Trivia game loaded with embarrassing throwback photos",
            "Retro Polaroid Photo Booth with customized instant printed photo strip sleeves",
            "Live vinyl DJ blending crowd favorites, throwback anthems, and modern remixes",
            "Signature giant Jenga and illuminated cornhole competition lounge"
        ],
        decorAndAtmosphere=[
            "Custom glowing LED neon name sign mounted over an organic balloon and foliage wall",
            "Warm wireless uplighting creating a stylish lounge club vibe",
            "Metallic foil fringe dramatic entryway for VIP photo arrivals",
            "Cocktail high-tops illuminated with geometric amber hurricane lanterns"
        ],
        surpriseElements=[
            "Surprise birthday video montage with heartfelt messages from far-away friends",
            "Champagne bottle parade with cold-spark fountains during the cake reveal",
            "Late-night hot gourmet pizza delivery right when the dance floor hits its peak"
        ],
        moodboardPrompt=f"Trendy milestone birthday party at night, stylish loft lounge, neon lighting, fashionable friends laughing and dancing, gourmet appetizers, polaroid photos, cinematic lighting"
    )

    budget_breakdown = [
        BudgetItem(id="b1", category="Venue & Lounge Space", item="Private Loft or Rooftop Space Rental (5 Hours)", estimatedCost=round(budget * 0.32, 2), notes="Includes seating, restrooms, sound hookup"),
        BudgetItem(id="b2", category="Food & Bar Catering", item=f"Gourmet Finger Foods, Bites & Bartender ({guests} guests)", estimatedCost=round(budget * 0.36, 2), notes="Covers craft cocktail service and heavy appetizers"),
        BudgetItem(id="b3", category="DJ & Audio/Lighting", item="Professional DJ, Sound System & Ambient Uplighting", estimatedCost=round(budget * 0.14, 2), notes="4 hours of live music set with wireless mic for toasts"),
        BudgetItem(id="b4", category="Decor, Neon & Backdrops", item="Custom Neon Sign, Balloon Garland & Photo Backdrop", estimatedCost=round(budget * 0.08, 2), notes="Client keeps the custom neon sign after the event!"),
        BudgetItem(id="b5", category="Custom Cake & Desserts", item="Designer Birthday Cake + Dessert Station", estimatedCost=round(budget * 0.05, 2), notes="Custom tiered cake matching party theme"),
        BudgetItem(id="b6", category="Contingency & Favors", item="Polaroid Film, Party Favors & Last-Minute Buffer", estimatedCost=round(budget * 0.05, 2), notes="Guest souvenirs and emergency supply kit")
    ]

    timeline = [
        TimelineMilestone(id="t1", phase="6-8 Weeks Out", title="Select Venue & Lock in Date", description="Sign rental agreement and pay venue holding deposit.", completed=True, category="Venue"),
        TimelineMilestone(id="t2", phase="4 Weeks Out", title="Send Digital Invitations & Collect RSVPs", description="Send invites via Partiful/Paperless Post; track dietary allergies.", completed=False, category="Guestlist"),
        TimelineMilestone(id="t3", phase="3 Weeks Out", title="Book DJ, Catering & Order Custom Cake", description="Approve catering menu and send cake inspiration sketch.", completed=False, category="Vendors"),
        TimelineMilestone(id="t4", phase="1 Week Out", title="Gather Photo Slideshow & Finalize Playlist", description="Compile childhood photos for surprise video and finalize playlist.", completed=False, category="Entertainment"),
        TimelineMilestone(id="t5", phase="Day Before", title="Stock Drinks, Charge Gear & Assemble Favors", description="Verify ice, cups, chargers, props, and cash envelopes.", completed=False, category="Prep")
    ]

    schedule = [
        ScheduleItem(id="s1", time="05:00 PM", activity="Host Arrival & Venue Access", location="Venue Loft", coordinator="Event Host", notes="Verify air conditioning, lighting presets, and soundcheck"),
        ScheduleItem(id="s2", time="05:45 PM", activity="Catering & Bartender Load-In", location="Bar Area", coordinator="Catering Lead", notes="Chill champagne, prep cocktail garnishes, prep food warmers"),
        ScheduleItem(id="s3", time="06:30 PM", activity="DJ Arrival & Soundcheck", location="DJ Booth", coordinator="DJ", notes="Test wireless mic and dancefloor sound balance"),
        ScheduleItem(id="s4", time="07:30 PM", activity="Guest Doors Open & Welcome Cocktail Hour", location="Lounge & Terrace", coordinator="Bartender & Host", notes="Pass out signature cocktail; upbeat lounge playlist"),
        ScheduleItem(id="s5", time="08:30 PM", activity="Food Stations Open & Polaroid Photo Lounge", location="Dining Station", coordinator="Co-Host", notes="Encourage guests to snap polaroid photos for guestbook"),
        ScheduleItem(id="s6", time="09:30 PM", activity="Surprise Tribute Video & Birthday Toast", location="Main Screen", coordinator="Best Friend", notes="Gather everyone together; display secret video reel"),
        ScheduleItem(id="s7", time="09:45 PM", activity="Cake Cutting & Sparkling Champagne Toast", location="Center Table", coordinator="Host Team", notes="Light celebratory sparkler candles; sing birthday anthem"),
        ScheduleItem(id="s8", time="10:00 PM", activity="Full Dance Floor Mode & DJ Set", location="Dance Floor", coordinator="DJ", notes="High energy dance tracks; late night pizza arrival at 11:15 PM"),
        ScheduleItem(id="s9", time="12:00 AM", activity="Party Wrap-Up & Departure", location="Lobby", coordinator="Host Team", notes="Distribute party favors and coordinate ride shares")
    ]

    vendors = [
        VendorItem(
            id="v1", category="Venue", vendorName="Skyline Urban Loft",
            contact="manager@skylineloft.com", estimatedCost=round(budget * 0.32, 2), status="contacted",
            checklist=[
                ChecklistTask(id="c1", task="Confirm load-in door elevator access", completed=True),
                ChecklistTask(id="c2", task="Review cleanup guidelines and trash removal rules", completed=False)
            ]
        ),
        VendorItem(
            id="v2", category="Catering & Bar", vendorName="Twist & Bite Pop-Up Catering",
            contact="chef@twistandbite.com", estimatedCost=round(budget * 0.36, 2), status="researching",
            checklist=[
                ChecklistTask(id="c3", task="Confirm 2 signature cocktail batch recipes", completed=False),
                ChecklistTask(id="c4", task="Confirm glassware vs compostable drinkware", completed=False)
            ]
        ),
        VendorItem(
            id="v3", category="Music & DJ", vendorName="SoundVibe Entertainment",
            contact="dj@soundvibe.io", estimatedCost=round(budget * 0.14, 2), status="researching",
            checklist=[
                ChecklistTask(id="c5", task="Submit top 20 requested songs", completed=False),
                ChecklistTask(id="c6", task="Confirm projector audio connection", completed=False)
            ]
        )
    ]

    return EventPlan(
        id=plan_id, title=title, eventType="birthday",
        date=req.date or "2026-11-20", location=req.location or "Downtown Rooftop / Private Loft",
        guestCount=guests, currency=curr, totalBudget=budget,
        vibeAndStyle=req.vibeAndStyle or "Festive, energetic, stylish, and unforgettable",
        specialRequests=req.specialRequests or "",
        ideas=ideas, budgetBreakdown=budget_breakdown,
        timeline=timeline, dayOfSchedule=schedule, vendorChecklist=vendors
    )

def _synthesize_community(plan_id: str, title: str, req: GeneratePlanRequest, budget: float, guests: int, curr: str) -> EventPlan:
    """Generates an inclusive community festival blueprint."""
    ideas = EventIdeas(
        themeTitle="Neighborhood Harmony & Community Festival",
        themeConcept=f"An inclusive, vibrant community gathering uniting {guests} attendees. Focused on local culture, family-friendly fun, sustainability, neighborhood empowerment, and accessible live entertainment.",
        colorPalette=[
            ColorSwatch(name="Sunburst Orange", hex="#EA580C"),
            ColorSwatch(name="Forest Meadow Green", hex="#16A34A"),
            ColorSwatch(name="Sky Blue", hex="#0284C7"),
            ColorSwatch(name="Warm Earth Ochre", hex="#CA8A04"),
            ColorSwatch(name="Clean Canvas White", hex="#FFFFFF")
        ],
        signatureFoodAndDrinks=[
            "Local Farmers Market Fresh Lemonade & Mint Coolers",
            "Neighborhood Food Truck Row (Artisanal Tacos, Woodfired Pizza, Veggie Bowls)",
            "Community Potluck & Bake-Off Pavilion with allergen labeling",
            "Complimentary Fresh Popcorn & Organic Cotton Candy for kids"
        ],
        activitiesAndEntertainment=[
            "Main Stage Community Showcase: Local high school bands, cultural dance troupes, and acoustic acts",
            "Interactive Kids Creative Zone: Chalk art festival, giant bubbles, and face painting",
            "Community Collaborative Canvas: A giant mural painted together by attendees",
            "Neighborhood Raffle & Charity Fundraiser Auction"
        ],
        decorAndAtmosphere=[
            "Colorful weatherproof fabric pennant bunting across trees and pathways",
            "Clear, high-contrast multilingual directional signposts",
            "Shaded picnic benches and reusable lawn seating mats",
            "Dedicated zero-waste green recycling and compost stations"
        ],
        surpriseElements=[
            "Surprise flash-mob musical performance by local youth choir",
            "Golden Ticket Scavenger Hunt with prizes donated by neighborhood merchants",
            "Evening twilight lantern stroll around the park perimeter"
        ],
        moodboardPrompt=f"Sunny outdoor community festival in a green park, diverse crowd of families and neighbors, colorful artisan tents, food trucks, children playing, live acoustic stage, uplifting documentary photography"
    )

    budget_breakdown = [
        BudgetItem(id="b1", category="Permits, Safety & City Fees", item="Park Rental, Sound Permit, Police/EMS Staging", estimatedCost=round(budget * 0.18, 2), notes="Mandatory city compliance and insurance binder"),
        BudgetItem(id="b2", category="Stage, Audio & Electrical", item="Sound System, Microphones, Tech Operator & Quiet Generator", estimatedCost=round(budget * 0.22, 2), notes="Handles all live performances and announcements"),
        BudgetItem(id="b3", category="Rentals & Sanitation", item="Canopy Tents, 150 Folding Chairs, Restrooms & Trash Bins", estimatedCost=round(budget * 0.24, 2), notes="Ensures sufficient shade and ADA accessibility"),
        BudgetItem(id="b4", category="Entertainment & Performers", item="Honorariums for Local Bands & Children's Entertainers", estimatedCost=round(budget * 0.14, 2), notes="Supports local performers and sound techs"),
        BudgetItem(id="b5", category="Kids Zone & Craft Supplies", item="Paints, Canvases, Carnival Games & Prizes", estimatedCost=round(budget * 0.10, 2), notes="Materials for hands-on activities"),
        BudgetItem(id="b6", category="Signage & Marketing", item="Park Banners, Directional Signs & Volunteer T-Shirts", estimatedCost=round(budget * 0.06, 2), notes="Ensures smooth crowd navigation and safety"),
        BudgetItem(id="b7", category="Contingency & First Aid", item="First aid supplies, hydration stations and weather buffer", estimatedCost=round(budget * 0.06, 2), notes="Emergency management reserve")
    ]

    timeline = [
        TimelineMilestone(id="t1", phase="4-6 Months Out", title="Submit City Park & Sound Permits", description="Submit permit applications to city parks department.", completed=True, category="Permits"),
        TimelineMilestone(id="t2", phase="3 Months Out", title="Recruit Food Trucks, Artisans & Sponsors", description="Finalize merchant agreements and local sponsorship support.", completed=True, category="Partnerships"),
        TimelineMilestone(id="t3", phase="6 Weeks Out", title="Call for Volunteers & Stage Lineup Confirmation", description="Organize 25 volunteer marshals and finalize performance times.", completed=False, category="Community"),
        TimelineMilestone(id="t4", phase="2 Weeks Out", title="Print Maps, Banners & Emergency Protocol", description="Create printed safety maps and assign volunteer shifts.", completed=False, category="Operations"),
        TimelineMilestone(id="t5", phase="Week Of", title="Site Walkthrough with Parks Ranger", description="Inspect power drops, water access, and parking flow.", completed=False, category="Logistics")
    ]

    schedule = [
        ScheduleItem(id="s1", time="07:00 AM", activity="Logistics Team Arrival & Rental Tents Setup", location="Park Main Field", coordinator="Operations Lead", notes="Direct rental truck delivery and restroom trailer placement"),
        ScheduleItem(id="s2", time="08:30 AM", activity="Food Trucks & Artisan Stalls Load-In", location="Vendor Lane", coordinator="Vendor Coordinator", notes="Inspect fire safety certificates and power cord covers"),
        ScheduleItem(id="s3", time="09:30 AM", activity="Volunteer Briefing & Gear Distribution", location="Info Tent", coordinator="Volunteer Lead", notes="Hand out high-vis shirts, radios, and site maps"),
        ScheduleItem(id="s4", time="10:00 AM", activity="Official Gates Open & Welcoming Acoustic Set", location="Main Stage", coordinator="MC", notes="Welcome address and opening blessing"),
        ScheduleItem(id="s5", time="11:30 AM", activity="Kids Activity Tent & Craft Stations Launch", location="Youth Pavilion", coordinator="Youth Director", notes="Chalk art and face painting begins"),
        ScheduleItem(id="s6", time="01:00 PM", activity="Community Leaders Address & Honor Roll", location="Main Stage", coordinator="Committee Chair", notes="Acknowledge local volunteers and sponsors"),
        ScheduleItem(id="s7", time="02:30 PM", activity="Community Games, Pie Contest & Raffle Draw", location="Center Lawn", coordinator="Activities Host", notes="High crowd engagement and awards"),
        ScheduleItem(id="s8", time="04:00 PM", activity="Headline Musical Ensemble Performance", location="Main Stage", coordinator="Stage Manager", notes="Crowd gathers on picnic blankets"),
        ScheduleItem(id="s9", time="06:00 PM", activity="Closing Remarks & Lantern Walk", location="Park Perimeter", coordinator="All Staff", notes="Thank you to attendees; announce funds raised"),
        ScheduleItem(id="s10", time="07:00 PM", activity="Grounds Cleanup & Waste Sorting", location="Entire Park", coordinator="Cleanup Crew", notes="Leave the park in pristine condition")
    ]

    vendors = [
        VendorItem(
            id="v1", category="City Department", vendorName="Municipal Parks & Recreation",
            contact="parks@city.gov", estimatedCost=round(budget * 0.18, 2), status="booked",
            checklist=[
                ChecklistTask(id="c1", task="Pay park security deposit", completed=True),
                ChecklistTask(id="c2", task="Review amplified sound curfew (strictly 07:00 PM)", completed=True)
            ]
        ),
        VendorItem(
            id="v2", category="Audio / Visual", vendorName="Community Sound & Stage Pro",
            contact="production@communitysound.org", estimatedCost=round(budget * 0.22, 2), status="contacted",
            checklist=[
                ChecklistTask(id="c3", task="Verify microphone count for multi-person choir", completed=False),
                ChecklistTask(id="c4", task="Confirm generator fuel supply for 10 hours", completed=False)
            ]
        ),
        VendorItem(
            id="v3", category="Equipment Rentals", vendorName="Citywide Tents & Event Rentals",
            contact="sales@citywiderentals.com", estimatedCost=round(budget * 0.24, 2), status="researching",
            checklist=[
                ChecklistTask(id="c5", task="Confirm delivery window at 07:00 AM", completed=False),
                ChecklistTask(id="c6", task="Ensure all tent weights are certified for high winds", completed=False)
            ]
        )
    ]

    return EventPlan(
        id=plan_id, title=title, eventType="community",
        date=req.date or "2026-10-15", location=req.location or "Oakwood Town Park & Pavilion",
        guestCount=guests, currency=curr, totalBudget=budget,
        vibeAndStyle=req.vibeAndStyle or "Welcoming, energetic, community-driven, and fun",
        specialRequests=req.specialRequests or "",
        ideas=ideas, budgetBreakdown=budget_breakdown,
        timeline=timeline, dayOfSchedule=schedule, vendorChecklist=vendors
    )

def _synthesize_custom(plan_id: str, title: str, req: GeneratePlanRequest, budget: float, guests: int, curr: str) -> EventPlan:
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
            context_str = json.dumps(req.eventContext, indent=2) if req.eventContext else "No active event context."
            system_instruction = f"""
You are "EventGenie AI", an experienced, creative, and pragmatic celebrity event planner.
You help users plan weddings, birthdays, and community events with budgets, timelines, checklists, and personalized creative ideas.
Current Event Context:
{context_str}

Be inspiring, empathetic, structured, and practical. Offer concrete recommendations with numbers, timelines, or vendor tips whenever relevant.
"""
            messages = [{"role": m.role if m.role == "user" else "model", "parts": [{"text": m.content}]} for m in req.chatHistory[-6:]]
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
    currency = context.get("currency", "$") if context else "$"

    if any(k in msg for k in ["budget", "cost", "expensive", "cut", "save"]):
        return f"""### 💡 Strategic Budget Advice for {event_title}

When managing your budget ({currency}{budget}):

1. **The 50/30/20 Rule for Events**:
   - **50%**: Guest experience core (Venue, Food & Beverage).
   - **30%**: Atmosphere & Memory keepers (Photo/Video, Music/DJ, Florals/Lighting).
   - **20%**: Logistics, Contingency & Attire/Favors.

2. **High-Impact Ways to Cut Costs Without Compromise**:
   - **Curate the Signature Bar**: Rather than a full open liquor bar, offer 2 signature cocktails + wine and beer. This typically saves 25-35% on bar fees!
   - **Repurpose Ceremony Florals**: Have your coordinator move the ceremony arch floral arrangements to behind the sweetheart or head table during cocktail hour.
   - **Digital-First Stationery**: Send digital Save-The-Dates and invitations with online RSVP tracking. Save hundreds in printing, calligraphy, and postage!
   - **Buffet or Family-Style vs. Plated**: Family-style platters create lively table conversation and require fewer service staff than formal plated courses.

Would you like me to suggest specific adjustments to any item in your budget breakdown?
"""
    elif any(k in msg for k in ["timeline", "schedule", "time", "delay", "hour"]):
        return f"""### ⏱️ Timeline & Run-of-Show Expert Tips

For a smooth flow during {event_title}:

1. **Build in 15-Minute 'Ghost Buffers'**:
   - Never schedule speeches or dances back-to-back without a 10-15 minute buffer. Guests always take longer to move from cocktail areas to dinner seating.
2. **Day-of Coordinator Designation**:
   - Designate one person (or trusted friend) as the 'Keeper of the Clock'. The hosts/honorees should never look at their watch on the day!
3. **Golden Hour Golden Rule**:
   - Check local sunset time! Schedule couple portraits or VIP photos 45 minutes before actual sunset for optimal lighting.
4. **Vendor Arrival Check**:
   - Venue access should precede caterer and DJ arrival by at least 1 hour so the floor plan is physically ready before equipment enters.

Do you want to adjust any specific milestone or time slot in your Day-of Schedule?
"""
    elif any(k in msg for k in ["vendor", "contract", "hire", "caterer", "photographer"]):
        return f"""### 📋 Essential Vendor Vetting Checklist

Key questions you must ask vendors before signing for {event_title}:

1. **For Caterers**:
   - *"Are tableware, napkins, glassware, and cleanup staff included in the per-person quote?"*
   - *"What is your policy on vendor meals during the reception?"*
2. **For Photographers & Videographers**:
   - *"Do you have backup cameras, dual-card recording, and liability insurance required by venues?"*
   - *"What is your exact turnaround time for sneak peek photos vs. full gallery delivery?"*
3. **For DJs / Entertainment**:
   - *"Do you provide wireless lapel and handheld microphones for speeches and toasts?"*
   - *"Will you handle MC duties and coordinate schedule cues with catering?"*
4. **Contracts & Payments**:
   - Never pay 100% upfront. Standard industry milestone is 25-50% deposit, and the balance due 7 to 14 days prior to the event.

Let me know which vendor you're vetting next, and I can generate custom interview questions for them!
"""
    elif any(k in msg for k in ["idea", "theme", "decor", "game", "activity"]):
        return f"""### ✨ Personalized Creative Concepts for {event_title}

Here are some fresh, memorable ideas to elevate the guest experience:

1. **Interactive Audio Guestbook**:
   - Rent a vintage rotary phone where guests pick up the receiver, hear a recorded greeting from you, and leave spontaneous voice messages after the tone.
2. **Signature Flavor Story**:
   - Pick two signature drinks or dessert items that represent meaningful memories (e.g. where the couple met, the birthday celebrant's favorite travel destination, or local harvest pride).
3. **Unexpected Wow Factor**:
   - A surprise midnight snack delivery (like warm gourmet donuts, mini grilled cheeses, or a local taco truck pulling up outside).
4. **Custom Color-Coordinated Photo Lounge**:
   - Combine a textured backdrop (like boxwood hedge or velvet drape) with a warm script neon sign and instant polaroid cameras.

Would you like more ideas tailored to a specific vibe or guest age range?
"""
    else:
        return f"""### 🌟 EventGenie AI at your service!

I am here to help you coordinate every detail of **{event_title}**. 

Here is what we can do together:
- **Refine your Budget**: Reallocate funds, calculate per-guest costs, or find smart savings.
- **Perfect your Timeline**: Build a seamless day-of schedule and long-term milestone checklist.
- **Vendor CRM & Checklists**: Draft email inquiry templates, contract clauses, and day-of instructions.
- **Creative Ideation**: Suggest personalized themes, signature cocktails, interactive games, and decor styling.

What specific aspect of your {event_type} would you like to explore next?
"""
