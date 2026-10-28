"""
CelebrateAI (India Edition) - Predefined Indian Event Blueprints
Curated presets for Big Fat Indian Weddings, Milestone Birthdays,
and Vibrant Community Festivals.
"""

from typing import Dict, Any

SAMPLE_EVENTS: Dict[str, Dict[str, Any]] = {
    "wedding": {
        "id": "sample-wedding-india",
        "title": "Aarav & Ananya's Royal Jaipur Heritage Wedding",
        "eventType": "wedding",
        "date": "2027-11-24",
        "location": "Chomu Palace Heritage Resort, Jaipur, Rajasthan",
        "guestCount": 250,
        "currency": "INR",
        "totalBudget": 2800000.0,
        "vibeAndStyle": (
            "Royal Rajasthani heritage, marigold and rajnigandha floral "
            "cascades, brass diyas, vibrant Sangeet beats, royal Baraat with "
            "nagada, traditional Vedic pheras at twilight"
        ),
        "specialRequests": (
            "Include multi-station Live Chaat Gali, traditional Shehnai "
            "welcoming, candid cinematic 4K drone cinematography, dedicated "
            "Safa-tying station, and midnight Pheras snacks."
        ),
        "ideas": {
            "themeTitle": "Shahi Virasat: Royal Marigold & Crimson Grandeur",
            "themeConcept": (
                "A majestic three-day celebration rooted in timeless Indian "
                "heritage. Featuring velvet canopies, hand-carved jharokhas, "
                "traditional Mewari hospitality, live Sufi & Bollywood fusion "
                "melodies, and curated royal Rajasthani and Pan-Indian "
                "delicacies."
            ),
            "colorPalette": [
                {
                    "name": "Genda Marigold",
                    "hex": "#F59E0B",
                },
                {
                    "name": "Royal Rani Pink",
                    "hex": "#E11D48",
                },
                {
                    "name": "Peacock Royal Blue",
                    "hex": "#1D4ED8",
                },
                {
                    "name": "Haldi Turmeric Gold",
                    "hex": "#FBBF24",
                },
                {
                    "name": "Emerald Panna Green",
                    "hex": "#059669",
                },
            ],
            "signatureFoodAndDrinks": [
                (
                    "Kesariya Kesar Thandai & Aam Panna welcome coolers with "
                    "rose petal garnish"
                ),
                (
                    "Live Purani Dilli Chaat Gali: Banarasi Tamatar Chaat, "
                    "Golgappe with 5 flavored waters, Palak Patta Chaat"
                ),
                (
                    "Royal Shahi Thali: Dal Baati Churma, Paneer Lababdar, Dum "
                    "Biryani, and Amritsari Kulcha"
                ),
                (
                    "Live Mithai Kadhai: Garma-garam Malpua with Rabri, Jalebi "
                    "counter, and artisanal Kulfi Falooda"
                ),
                (
                    "Midnight Masala Chai Bar with assorted Mathris and Khasta "
                    "Kachoris during late-night Pheras"
                ),
            ],
            "activitiesAndEntertainment": [
                (
                    "High-voltage Sangeet Dance Competition choreographed for "
                    "Groom vs Bride families"
                ),
                (
                    "Grand Royal Baraat with authentic Punjabi Dhol, vintage "
                    "convertible car, and brass band"
                ),
                (
                    "Royal Welcome with Shehnai maestro and flower petal shower "
                    "from Palace balconies"
                ),
                (
                    "Live Sufi Fusion Ensemble & Bollywood Celebrity DJ set "
                    "after the Varmala"
                ),
                (
                    "Traditional Joota Chupai negotiation and playful post- "
                    "wedding family games"
                ),
            ],
            "decorAndAtmosphere": [
                (
                    "Mandap floating on Lotus water pond adorned with 50,000 "
                    "marigolds and fresh rajnigandha stems"
                ),
                (
                    "Traditional brass urli bowls with floating marigolds and "
                    "scented mogra candles"
                ),
                (
                    "Handcrafted puppet and Lac bangle maker live stall for "
                    "guest souvenirs"
                ),
                (
                    "Fairytale tree canopies wrapped with warm fairy string "
                    "lights and hanging glass lamps"
                ),
            ],
            "surpriseElements": [
                (
                    "Surprise cold-spark pyrotechnic display firing 360-degrees "
                    "during the Varmala garland exchange"
                ),
                (
                    "Personalized Shahi Ittar (organic Indian perfume) flacons "
                    "gifted in brocade silk pouches"
                ),
                (
                    "Surprise flash-mob entrance by the bride's cousins to "
                    "classic 90s Bollywood anthems"
                ),
            ],
            "moodboardPrompt": (
                "Grand Indian royal destination wedding in Jaipur palace "
                "courtyard at sunset, royal mandap with orange and yellow "
                "marigold flowers, brass diyas, bride in crimson red lehenga, "
                "groom in ivory sherwani, fairy lights, cinematic 8k"
            ),
        },
        "budgetBreakdown": [
            {
                "id": "b1",
                "category": "Venue & Hospitality",
                "item": "Heritage Palace Resort (2 Days & 40 Guest Rooms)",
                "estimatedCost": 950000.0,
                "actualCost": 920000.0,
                "paidAmount": 450000.0,
                "status": "booked",
                "notes": "Includes lawn, poolside for Haldi, and banquet hall for Sangeet",
            },
            {
                "id": "b2",
                "category": "Catering & Live Stalls",
                "item": "Royal Multi-Cuisine Feast (250 guests x 4 functions)",
                "estimatedCost": 850000.0,
                "actualCost": 870000.0,
                "paidAmount": 300000.0,
                "status": "booked",
                "notes": "Includes Live Chaat, Shahi dinner, midnight snacks, and high tea",
            },
            {
                "id": "b3",
                "category": "Decor & Mandap",
                "item": "Vedic Lotus Mandap, Sangeet Stage, Haldi Theme & Lighting",
                "estimatedCost": 350000.0,
                "actualCost": 340000.0,
                "paidAmount": 150000.0,
                "status": "booked",
                "notes": (
                    "Fresh marigolds, rajnigandha, royal drapes, and ambient "
                    "palace uplighting"
                ),
            },
            {
                "id": "b4",
                "category": "Photography & Video",
                "item": "Cinematic Candid Photo, Drone & 4K Wedding Film (3 Days)",
                "estimatedCost": 220000.0,
                "actualCost": 200000.0,
                "paidAmount": 100000.0,
                "status": "booked",
                "notes": "Team of 4 shooters, drone coverage, teaser reel in 48 hours",
            },
            {
                "id": "b5",
                "category": "Entertainment & DJ",
                "item": "Sangeet Bollywood DJ, Punjabi Dhol Troupe & Shehnai Artist",
                "estimatedCost": 120000.0,
                "actualCost": 110000.0,
                "paidAmount": 60000.0,
                "status": "booked",
                "notes": (
                    "Includes state-of-the-art JBL Line Array sound setup and "
                    "wireless mics"
                ),
            },
            {
                "id": "b6",
                "category": "Makeup & Mehndi",
                "item": "Bridal HD Makeup (3 Functions) + Professional Mehndi Team",
                "estimatedCost": 90000.0,
                "actualCost": 85000.0,
                "paidAmount": 40000.0,
                "status": "booked",
                "notes": "Lead artist for bride + 5 assistant artists for 60 female guests",
            },
            {
                "id": "b7",
                "category": "Safas, Favors & Gifts",
                "item": "Rajasthani Pagdis (150 Safas) + Custom Mithai Gift Hampers",
                "estimatedCost": 90000.0,
                "actualCost": 85000.0,
                "paidAmount": 85000.0,
                "status": "paid",
                "notes": "Delivered to packaging room",
            },
            {
                "id": "b8",
                "category": "Panditji & Rituals",
                "item": "Head Vedic Acharya, Samagri & Havan Setup",
                "estimatedCost": 30000.0,
                "actualCost": 30000.0,
                "paidAmount": 15000.0,
                "status": "booked",
                "notes": "Includes all puja samagri, dry fruits, and gangajal",
            },
            {
                "id": "b9",
                "category": "Contingency & Tips",
                "item": "Cash Envelopes for Service Staff, Drivers & Shagun Buffer",
                "estimatedCost": 100000.0,
                "actualCost": 0.0,
                "paidAmount": 0.0,
                "status": "planned",
                "notes": "Pre-filled shagun envelopes ready in locker",
            },
        ],
        "timeline": [
            {
                "id": "t1",
                "phase": "9-12 Months Out",
                "title": "Book Heritage Venue & Block Muhurat Date",
                "description": (
                    "Consult family astrologer for auspicious Shubh Muhurat and "
                    "lock in Palace resort."
                ),
                "dueDate": "2026-12-01",
                "completed": True,
                "category": "Venue",
            },
            {
                "id": "t2",
                "phase": "6-8 Months Out",
                "title": "Hire Master Caterer, Photographer & Decorator",
                "description": (
                    "Conduct food tasting session, select live counters, and "
                    "approve Mandap design."
                ),
                "dueDate": "2027-03-15",
                "completed": True,
                "category": "Vendors",
            },
            {
                "id": "t3",
                "phase": "3-5 Months Out",
                "title": "Bridal Lehenga/Sherwani Trials & Sangeet Choreographer",
                "description": (
                    "Finalize designer couture outfits and start weekend dance "
                    "rehearsals with family."
                ),
                "dueDate": "2027-06-20",
                "completed": True,
                "category": "Attire",
            },
            {
                "id": "t4",
                "phase": "2 Months Out",
                "title": "Send Digital WhatsApp Invites & Royal Box Cards",
                "description": (
                    "Dispatch mithai invitation boxes and collect guest arrival "
                    "flight/train details."
                ),
                "dueDate": "2027-09-15",
                "completed": False,
                "category": "Guests",
            },
            {
                "id": "t5",
                "phase": "3 Weeks Out",
                "title": "Final Room Allocation & Safa Headcounts",
                "description": (
                    "Assign room keys, coordinate airport pickup shuttle, and "
                    "deliver vendor badges."
                ),
                "dueDate": "2027-11-03",
                "completed": False,
                "category": "Logistics",
            },
            {
                "id": "t6",
                "phase": "Wedding Week",
                "title": "Pack Shagun Envelopes, Havan Samagri & Haldi Gear",
                "description": (
                    "Distribute timeline cards to immediate family; coordinate "
                    "with Panditji."
                ),
                "dueDate": "2027-11-20",
                "completed": False,
                "category": "Final Prep",
            },
        ],
        "dayOfSchedule": [
            {
                "id": "s1",
                "time": "09:00 AM",
                "activity": "Peeli Haldi & Phoolon ki Holi",
                "location": "Palace Poolside Lawn",
                "coordinator": "Bride & Groom Cousins",
                "notes": "Yellow dress code; organic herbal turmeric and marigold petals",
                "status": "upcoming",
            },
            {
                "id": "s2",
                "time": "12:30 PM",
                "activity": "Traditional Rajasthani High Tea & Lunch",
                "location": "Courtyard Dining",
                "coordinator": "Catering Lead",
                "notes": "Live Dal Baati and Kachori counters open",
                "status": "upcoming",
            },
            {
                "id": "s3",
                "time": "03:30 PM",
                "activity": "Bridal & Groom Royal Dressing & Safa Bandhai",
                "location": "Royal Suites",
                "coordinator": "Stylist & Pagdi Master",
                "notes": "Candid photos of jewelry, sehra, and kaleeras",
                "status": "upcoming",
            },
            {
                "id": "s4",
                "time": "05:00 PM",
                "activity": "Royal Baraat Assembly & Swagat",
                "location": "Palace Main Gate",
                "coordinator": "Dhol Master & Groom Team",
                "notes": "Vintage car lead, Punjabi Dhol beat, rosewater spray",
                "status": "upcoming",
            },
            {
                "id": "s5",
                "time": "06:15 PM",
                "activity": "Milni Ceremony & Royal Gateway Welcome",
                "location": "Inner Palace Courtyard",
                "coordinator": "Family Elders",
                "notes": "Garland exchange by fathers, Shehnai welcoming notes",
                "status": "upcoming",
            },
            {
                "id": "s6",
                "time": "07:00 PM",
                "activity": "Grand Varmala Ceremony under Cold Sparks",
                "location": "Grand Palace Stage",
                "coordinator": "Event Coordinator",
                "notes": "Dramatic smoke curtain and 360-degree cold fire fountains",
                "status": "upcoming",
            },
            {
                "id": "s7",
                "time": "07:45 PM",
                "activity": "Royal Wedding Reception Dinner & Live Sufi Set",
                "location": "Main Lawn & Banquet",
                "coordinator": "Catering Manager",
                "notes": "All 12 live food stations active; photo ops with couple",
                "status": "upcoming",
            },
            {
                "id": "s8",
                "time": "10:30 PM",
                "activity": "Vedic Pheras & Kanyadaan at the Lotus Mandap",
                "location": "Lakeside Lotus Mandap",
                "coordinator": "Panditji & Siblings",
                "notes": "Sacred Agni havan, 7 vows recitation, Sindoor & Mangalsutra",
                "status": "upcoming",
            },
            {
                "id": "s9",
                "time": "12:30 AM",
                "activity": "Emotional Vidaai Ceremony",
                "location": "Palace Gateway",
                "coordinator": "Parents & Coordinator",
                "notes": "Floral coin toss, vintage car departure",
                "status": "upcoming",
            },
        ],
        "vendorChecklist": [
            {
                "id": "v1",
                "category": "Heritage Venue",
                "vendorName": "Chomu Palace Heritage Hotel",
                "contact": "weddings@chomupalace.com | +91 98290 12345",
                "estimatedCost": 950000.0,
                "contractedCost": 920000.0,
                "status": "booked",
                "checklist": [
                    {
                        "id": "c1",
                        "task": "Pay 50% reservation advance",
                        "completed": True,
                    },
                    {
                        "id": "c2",
                        "task": "Submit rooming list with check-in/out times",
                        "completed": True,
                    },
                    {
                        "id": "c3",
                        "task": (
                            "Confirm sound curfew rules (10:00 PM on lawn, "
                            "indoor banquet after)"
                        ),
                        "completed": True,
                    },
                    {
                        "id": "c4",
                        "task": "Inspect Mandap power connection and backup generator",
                        "completed": False,
                    },
                ],
                "notes": "40 heritage rooms booked for 2 nights with breakfast included.",
            },
            {
                "id": "v2",
                "category": "Royal Catering",
                "vendorName": "Maharaja Royal Rasoi Catering",
                "contact": "chef_rajesh@maharajarasoi.in | +91 98110 56789",
                "estimatedCost": 850000.0,
                "contractedCost": 870000.0,
                "status": "booked",
                "checklist": [
                    {
                        "id": "c5",
                        "task": "Menu tasting completed and Chaat list finalized",
                        "completed": True,
                    },
                    {
                        "id": "c6",
                        "task": "Confirm separate Pure Vegetarian and Jain counters",
                        "completed": True,
                    },
                    {
                        "id": "c7",
                        "task": (
                            "Arrange copper service chafing dishes and royal "
                            "turbans for staff"
                        ),
                        "completed": False,
                    },
                ],
                "notes": (
                    "Providing 12 live cooking stations including Banarasi Chaat "
                    "and Jalebi Rabri."
                ),
            },
            {
                "id": "v3",
                "category": "Photo & Cinema",
                "vendorName": "Royal Shutterbug Films",
                "contact": "contact@royalshutterbug.com",
                "estimatedCost": 220000.0,
                "contractedCost": 200000.0,
                "status": "booked",
                "checklist": [
                    {
                        "id": "c8",
                        "task": "Drone flying permission from palace authorities",
                        "completed": True,
                    },
                    {
                        "id": "c9",
                        "task": "Provide list of VIP elders for stage portraits",
                        "completed": False,
                    },
                    {
                        "id": "c10",
                        "task": "Confirm 48-hour Instagram teaser reel deliverable",
                        "completed": True,
                    },
                ],
                "notes": "Lead cinematic director + 3 candid shooters + 1 drone operator.",
            },
            {
                "id": "v4",
                "category": "Floral & Mandap",
                "vendorName": "Pushp Utsav Floral Art",
                "contact": "hello@pushputsav.in",
                "estimatedCost": 350000.0,
                "contractedCost": 340000.0,
                "status": "booked",
                "checklist": [
                    {
                        "id": "c11",
                        "task": "Approve Mandap 3D render with lotus motifs",
                        "completed": True,
                    },
                    {
                        "id": "c12",
                        "task": "Order 100 kg fresh orange & yellow marigolds",
                        "completed": True,
                    },
                    {
                        "id": "c13",
                        "task": "Ensure teardown protocol clean by 03:00 AM",
                        "completed": False,
                    },
                ],
                "notes": (
                    "Floral arrangements repurposed from Sangeet stage to "
                    "morning breakfast."
                ),
            },
        ],
    },
    "birthday": {
        "id": "sample-birthday-india",
        "title": "Kabir's Royal 1st Birthday & Annaprashan Utsav",
        "eventType": "birthday",
        "date": "2026-11-20",
        "location": "The Grand Orchid Banquet Hall, Bangalore / Delhi NCR",
        "guestCount": 80,
        "currency": "INR",
        "totalBudget": 200000.0,
        "vibeAndStyle": (
            "Vibrant Indian cultural blend with modern playful Jungle Safari, "
            "morning Vedic Annaprashan puja, evening celebration with live "
            "music, caricature artist, and traditional South/North Indian feast"
        ),
        "specialRequests": (
            "Include traditional gold coin kheer feeding ceremony, customized "
            "return gift boxes with dry fruits, live cotton candy and kulfi "
            "counters for kids."
        ),
        "ideas": {
            "themeTitle": "Nanhi Jaan: Royal Prince & Jungle Safari Utsav",
            "themeConcept": (
                "A joyful celebration celebrating baby Kabir's 1st year "
                "milestone. Starting with a serene morning Annaprashan (first "
                "rice eating ceremony) attended by elders, transitioning into an "
                "energetic evening party filled with balloon arches, interactive "
                "toddler games, and sweet culinary nostalgia."
            ),
            "colorPalette": [
                {
                    "name": "Royal Turquoise",
                    "hex": "#0284C7",
                },
                {
                    "name": "Warm Haldi Yellow",
                    "hex": "#F59E0B",
                },
                {
                    "name": "Soft Sage Leaf",
                    "hex": "#10B981",
                },
                {
                    "name": "Festive Gold",
                    "hex": "#EAB308",
                },
                {
                    "name": "Pearly Cream",
                    "hex": "#FDFBF7",
                },
            ],
            "signatureFoodAndDrinks": [
                "Shahi Kesar Badam Milk & Fresh Tender Coconut Water welcome drinks",
                (
                    "Live South & North Indian Chaat Station: Dahi Papdi, Mini "
                    "Idli Podi Skewers, Aloo Tikki"
                ),
                (
                    "Gourmet Birthday Dinner: Paneer Makhani, Vegetable Biryani, "
                    "Butter Naan, and Dal Bukhara"
                ),
                (
                    "Traditional Annaprashan Payasam / Kheer served in earthen "
                    "clay handis"
                ),
                "Live Kulfi-Falooda & Warm Jalebi Cart with rabri dips",
            ],
            "activitiesAndEntertainment": [
                (
                    "Vedic Annaprashan Ritual: Baby Kabir picks traditional "
                    "objects (Book, Gold Coin, Pen) predicting future virtues"
                ),
                (
                    "Professional Magician & Puppet Show keeping kids mesmerized "
                    "for 45 minutes"
                ),
                (
                    "Live Caricature Artist sketching personalized family "
                    "portrait keepsakes on branded cardstock"
                ),
                "Toddler Soft Play Zone with ball pit and balloon twisting station",
                "High-Energy Bollywood Dance Set featuring child-friendly party hits",
            ],
            "decorAndAtmosphere": [
                (
                    "10-foot organic balloon garland in shades of turquoise, "
                    "gold, and jungle sage"
                ),
                "Custom illuminated LED cutout sign reading 'Kabir Turns 1'",
                (
                    "Traditional marigold flower toran framing the entrance door "
                    "with brass bells"
                ),
                (
                    "Milestone chalkboard photo gallery showcasing photos from "
                    "Month 1 to Month 12"
                ),
            ],
            "surpriseElements": [
                (
                    "Surprise 3-minute emotional video montage of baby Kabir's "
                    "first smiles and milestones"
                ),
                (
                    "Personalized storybook favors with each child guest's name "
                    "printed as the hero"
                ),
                (
                    "Gourmet customized 2-tier animal safari fondant cake with "
                    "sparkling sparkler candle"
                ),
            ],
            "moodboardPrompt": (
                "First birthday Indian celebration in luxury banquet hall, gold "
                "and turquoise balloon arch, cute baby boy in silk kurta, "
                "parents smiling, marigold flower details, live chaat stalls in "
                "background, warm festive lighting"
            ),
        },
        "budgetBreakdown": [
            {
                "id": "b1",
                "category": "Banquet Venue",
                "item": "Air-Conditioned Banquet Hall Rental (5 Hours)",
                "estimatedCost": 60000.0,
                "actualCost": 58000.0,
                "paidAmount": 30000.0,
                "status": "booked",
                "notes": "Includes sound gear, round tables, and air conditioning",
            },
            {
                "id": "b2",
                "category": "Food & Beverages",
                "item": "Buffet Dinner + Live Chaat & Kulfi Counter (80 Guests)",
                "estimatedCost": 75000.0,
                "actualCost": 76000.0,
                "paidAmount": 35000.0,
                "status": "booked",
                "notes": "Approx Rs. 950 per plate with 3 live counters",
            },
            {
                "id": "b3",
                "category": "Decor & Lighting",
                "item": "Jungle Safari Balloon Backdrop, LED Name & Milestone Board",
                "estimatedCost": 25000.0,
                "actualCost": 24000.0,
                "paidAmount": 12000.0,
                "status": "booked",
                "notes": "Completed setup 1 hour before guest arrival",
            },
            {
                "id": "b4",
                "category": "Kids Entertainment",
                "item": "Magician, Puppet Show, Balloon Modeler & Caricature Artist",
                "estimatedCost": 15000.0,
                "actualCost": 14000.0,
                "paidAmount": 7000.0,
                "status": "booked",
                "notes": "2-hour engagement slot",
            },
            {
                "id": "b5",
                "category": "Designer Cake",
                "item": "3 Kg 2-Tier Designer Butterscotch Safari Cake",
                "estimatedCost": 8000.0,
                "actualCost": 7500.0,
                "paidAmount": 7500.0,
                "status": "paid",
                "notes": "Delivered to venue at 05:00 PM",
            },
            {
                "id": "b6",
                "category": "Photo & Video",
                "item": "Professional Candid Photographer (4 Hours)",
                "estimatedCost": 12000.0,
                "actualCost": 12000.0,
                "paidAmount": 6000.0,
                "status": "booked",
                "notes": "All edited soft copies delivered in 5 days",
            },
            {
                "id": "b7",
                "category": "Return Gifts",
                "item": "Customized Dry Fruit Jars + Kids Puzzle Favors (40 packs)",
                "estimatedCost": 5000.0,
                "actualCost": 4800.0,
                "paidAmount": 4800.0,
                "status": "paid",
                "notes": "Gift bags ready in reception lobby",
            },
        ],
        "timeline": [
            {
                "id": "t1",
                "phase": "6 Weeks Out",
                "title": "Book Banquet Hall & Confirm Date",
                "description": "Lock in venue deposit and verify catering menu.",
                "dueDate": "2026-10-09",
                "completed": True,
                "category": "Venue",
            },
            {
                "id": "t2",
                "phase": "4 Weeks Out",
                "title": "Send Digital WhatsApp Video Invites",
                "description": "Send animated Canva invite to 80 guests and track RSVP headcount.",
                "dueDate": "2026-10-23",
                "completed": True,
                "category": "Guests",
            },
            {
                "id": "t3",
                "phase": "2 Weeks Out",
                "title": "Book Magician, Decorator & Order Cake",
                "description": (
                    "Approve jungle safari balloon mockup and finalize 2-tier "
                    "cake sketch."
                ),
                "dueDate": "2026-11-06",
                "completed": True,
                "category": "Entertainment",
            },
            {
                "id": "t4",
                "phase": "1 Week Out",
                "title": "Compile Baby 1st Year Photo Slideshow",
                "description": "Collect pictures from birth to Month 12 for projector screening.",
                "dueDate": "2026-11-13",
                "completed": False,
                "category": "Memories",
            },
            {
                "id": "t5",
                "phase": "Day Before",
                "title": "Pack Puja Samagri, Baby Outfits & Return Gifts",
                "description": (
                    "Ensure backup kurta set, baby snacks, and return gift bags "
                    "are ready."
                ),
                "dueDate": "2026-11-19",
                "completed": False,
                "category": "Logistics",
            },
        ],
        "dayOfSchedule": [
            {
                "id": "s1",
                "time": "10:30 AM",
                "activity": "Vedic Annaprashan Puja & Kheer Feeding",
                "location": "Home / Banquet Mandir",
                "coordinator": "Grandparents & Panditji",
                "notes": "Traditional rituals, shlokas, and gold coin kheer feeding",
                "status": "upcoming",
            },
            {
                "id": "s2",
                "time": "04:30 PM",
                "activity": "Decor Setup & Soundcheck",
                "location": "Main Banquet",
                "coordinator": "Decorator & Host",
                "notes": "Turn on LED name sign, check background nursery playlist",
                "status": "upcoming",
            },
            {
                "id": "s3",
                "time": "05:30 PM",
                "activity": "Cake Delivery & Catering Check",
                "location": "Center Stage",
                "coordinator": "Venue Manager",
                "notes": "Inspect 2-tier safari cake, chill badam milk bottles",
                "status": "upcoming",
            },
            {
                "id": "s4",
                "time": "06:30 PM",
                "activity": "Guests Arrive & Welcome Drinks",
                "location": "Foyer & Lounge",
                "coordinator": "Host Family",
                "notes": "Serve Kesar Badam milk and hot Chaat snacks",
                "status": "upcoming",
            },
            {
                "id": "s5",
                "time": "07:15 PM",
                "activity": "Magician & Interactive Puppet Show",
                "location": "Kids Corner",
                "coordinator": "Magician Lead",
                "notes": "Gathers all kids for interactive laughter games",
                "status": "upcoming",
            },
            {
                "id": "s6",
                "time": "08:15 PM",
                "activity": "Cake Cutting & Birthday Anthem Singalong",
                "location": "Main Stage",
                "coordinator": "Parents & Cousins",
                "notes": "Sparkler candles lit, baby Kabir in traditional silk kurta",
                "status": "upcoming",
            },
            {
                "id": "s7",
                "time": "08:30 PM",
                "activity": "Surprise Video Montage Screening",
                "location": "Projector Screen",
                "coordinator": "Host Best Friend",
                "notes": "Dim hall lights, 3-minute nostalgic journey",
                "status": "upcoming",
            },
            {
                "id": "s8",
                "time": "08:45 PM",
                "activity": "Grand Indian Buffet Dinner Opens",
                "location": "Dining Hall",
                "coordinator": "Catering Lead",
                "notes": "All hot entrees and live Kulfi counters active",
                "status": "upcoming",
            },
            {
                "id": "s9",
                "time": "10:00 PM",
                "activity": "Return Gift Distribution & Farewell",
                "location": "Exit Gateway",
                "coordinator": "Host Family",
                "notes": "Hand over customized gift hampers to leaving families",
                "status": "upcoming",
            },
        ],
        "vendorChecklist": [
            {
                "id": "v1",
                "category": "Banquet Hall",
                "vendorName": "The Grand Orchid Banquets",
                "contact": "manager@grandorchid.in | +91 99001 23456",
                "estimatedCost": 60000.0,
                "contractedCost": 58000.0,
                "status": "booked",
                "checklist": [
                    {
                        "id": "c1",
                        "task": "Confirm projector and HDMI audio setup",
                        "completed": True,
                    },
                    {
                        "id": "c2",
                        "task": "Check baby feeding / diaper changing room access",
                        "completed": True,
                    },
                ],
                "notes": "Dedicated private green room provided for baby nap.",
            },
            {
                "id": "v2",
                "category": "Catering",
                "vendorName": "Spice Symphony Caterers",
                "contact": "orders@spicesymphony.com",
                "estimatedCost": 75000.0,
                "contractedCost": 76000.0,
                "status": "booked",
                "checklist": [
                    {
                        "id": "c3",
                        "task": "Ensure kid-friendly non-spicy pasta & fries counter",
                        "completed": True,
                    },
                    {
                        "id": "c4",
                        "task": "Verify rabri jalebi live tawa readiness",
                        "completed": False,
                    },
                ],
                "notes": "Staff wearing hygienic gloves and chef caps.",
            },
            {
                "id": "v3",
                "category": "Entertainment",
                "vendorName": "Jolly Kids Events (Anand)",
                "contact": "anand@jollykids.in",
                "estimatedCost": 15000.0,
                "contractedCost": 14000.0,
                "status": "booked",
                "checklist": [
                    {
                        "id": "c5",
                        "task": "Confirm magic show sound mic",
                        "completed": True,
                    },
                    {
                        "id": "c6",
                        "task": "Bring 100 colorful twisting balloons",
                        "completed": True,
                    },
                ],
                "notes": "Caricature artist starts at 06:30 PM.",
            },
        ],
    },
    "community": {
        "id": "sample-community-india",
        "title": "Gokuldham Grand Diwali Mela & Dandiya Raas Utsav",
        "eventType": "community",
        "date": "2026-11-01",
        "location": "Gokuldham Society Central Clubhouse Grounds, Mumbai / Pune",
        "guestCount": 600,
        "currency": "INR",
        "totalBudget": 450000.0,
        "vibeAndStyle": (
            "Vibrant festive Diwali spirit, rhythmic Gujarati Dandiya Raas, "
            "colorful ethnic Kurta/Chaniya Choli dress code, glittering fairy "
            "light canopy, community food stalls, eco-friendly green fireworks"
        ),
        "specialRequests": (
            "Obtain local police sound clearance until 10:00 PM, organize "
            "certified electrical safety inspection for food stalls, manage 20 "
            "youth society volunteer marshals, and provide complimentary Dandiya "
            "sticks."
        ),
        "ideas": {
            "themeTitle": "Roshni & Raas: Diwali Milan & Dandiya Utsav",
            "themeConcept": (
                "An exhilarating community festival uniting 600 society "
                "residents and families. Celebrating Diwali lights and Navratri "
                "festive joy with traditional Garba beats, artisanal home-chef "
                "food bazaars, rangoli contests, and an unforgettable evening of "
                "cultural unity."
            ),
            "colorPalette": [
                {
                    "name": "Deep Sindoor Red",
                    "hex": "#DC2626",
                },
                {
                    "name": "Bright Festive Orange",
                    "hex": "#EA580C",
                },
                {
                    "name": "Shimmering Diya Gold",
                    "hex": "#CA8A04",
                },
                {
                    "name": "Peacock Teal",
                    "hex": "#0D9488",
                },
                {
                    "name": "Festive Purple",
                    "hex": "#7C3AED",
                },
            ],
            "signatureFoodAndDrinks": [
                "Warm Masala Doodh & Fresh Badam Halwa welcome counters",
                (
                    "Society Resident Home-Chef Food Mela: 15 diverse regional "
                    "Indian food stalls (Pav Bhaji, Momos, Dhokla, Biryani)"
                ),
                "Live Hot Jalebi & Fafda station with tangy raw papaya sambharo",
                (
                    "Street-Style Mumbai Vada Pav, Dahi Sev Puri, and Masala "
                    "Sweet Corn cups"
                ),
                (
                    "Complimentary Kesar Kheer and Dry Fruit Modak boxes for all "
                    "resident families"
                ),
            ],
            "activitiesAndEntertainment": [
                (
                    "Mega Dandiya & Garba Raas with Live 7-Piece Gujarati Folk "
                    "Band & Dhol Troupe"
                ),
                (
                    "Inter-Tower Mega Rangoli & Diya Decoration Competition with "
                    "trophies"
                ),
                (
                    "Best Traditional Dressed Resident (Best Chaniya Choli & "
                    "Best Kurta Pajama)"
                ),
                "Kids DIY Diya Painting & Lantern Craft Workshop",
                "Eco-Friendly Green Fireworks and Cold-Spark Light Show at 09:30 PM",
            ],
            "decorAndAtmosphere": [
                (
                    "Grand canopy of 2,000 meters of golden fairy string lights "
                    "covering the central open lawn"
                ),
                (
                    "1,001 traditional clay Diyas hand-lit by society elders "
                    "across clubhouse walkways"
                ),
                (
                    "Huge decorative floral Rangoli at the society entrance arch "
                    "crafted with fresh marigold petals"
                ),
                (
                    "Colorful traditional Rajasthani umbrellas and bandhani "
                    "drapes adorning stall booths"
                ),
            ],
            "surpriseElements": [
                (
                    "Surprise high-energy Dhol-Tasha troop entrance leading the "
                    "final Maha-Garba circle"
                ),
                (
                    "Lucky Diwali Bumper Resident Raffle with smart TVs and gold "
                    "coins sponsored by local businesses"
                ),
                (
                    "Grand Community Lantern release ceremony sending glowing "
                    "wishes into the twilight sky"
                ),
            ],
            "moodboardPrompt": (
                "Diwali community mela festival in India at night, thousands of "
                "fairy lights, people dancing Dandiya in colorful traditional "
                "Indian clothes, food stalls with steam rising, marigold "
                "decorations, festive joyous atmosphere, 8k"
            ),
        },
        "budgetBreakdown": [
            {
                "id": "b1",
                "category": "Stage & Sound",
                "item": "High-Output Sound PA System, Stage Trussing & Band Gear",
                "estimatedCost": 120000.0,
                "actualCost": 115000.0,
                "paidAmount": 60000.0,
                "status": "booked",
                "notes": "Includes sound operator and sound clearance compliance",
            },
            {
                "id": "b2",
                "category": "Lighting & Fairy Canopy",
                "item": "2,000m Fairy Light Canopy, Pathway Uplighting & GenSet Backup",
                "estimatedCost": 90000.0,
                "actualCost": 88000.0,
                "paidAmount": 45000.0,
                "status": "booked",
                "notes": "Quiet 60KVA generator on standby for power backup",
            },
            {
                "id": "b3",
                "category": "Live Band & Dhol",
                "item": "Live 7-Piece Folk Band & Nasik Dhol-Tasha Troupe Honorarium",
                "estimatedCost": 85000.0,
                "actualCost": 85000.0,
                "paidAmount": 40000.0,
                "status": "booked",
                "notes": "Confirmed 07:00 PM to 10:00 PM",
            },
            {
                "id": "b4",
                "category": "Tents & Food Stalls",
                "item": "15 Commercial Canopy Stalls, 250 Chairs & Dining Tables",
                "estimatedCost": 60000.0,
                "actualCost": 58000.0,
                "paidAmount": 30000.0,
                "status": "booked",
                "notes": "Setup on outer perimeter to keep dance lawn spacious",
            },
            {
                "id": "b5",
                "category": "Prizes, Dandiya & Crafts",
                "item": "300 Pairs of Dandiya Sticks, Competition Trophies & Kid Paints",
                "estimatedCost": 35000.0,
                "actualCost": 34000.0,
                "paidAmount": 34000.0,
                "status": "paid",
                "notes": "Delivered to committee office",
            },
            {
                "id": "b6",
                "category": "Safety, Permits & First-Aid",
                "item": "Police Sound NOC, Fire Extinguishers & First Aid Station",
                "estimatedCost": 25000.0,
                "actualCost": 22000.0,
                "paidAmount": 22000.0,
                "status": "paid",
                "notes": "Police permission letter received and framed",
            },
            {
                "id": "b7",
                "category": "Emergency & Cleanup",
                "item": "Waste Segregation Bins, Post-Event Society Cleaning Crew",
                "estimatedCost": 35000.0,
                "actualCost": 0.0,
                "paidAmount": 0.0,
                "status": "planned",
                "notes": "10 dedicated cleaning personnel for midnight sweep",
            },
        ],
        "timeline": [
            {
                "id": "t1",
                "phase": "6 Weeks Out",
                "title": "Submit Police Sound Clearance & AGM Approval",
                "description": (
                    "Obtain society managing committee approval and apply for "
                    "local police sound NOC."
                ),
                "dueDate": "2026-09-20",
                "completed": True,
                "category": "Permits",
            },
            {
                "id": "t2",
                "phase": "4 Weeks Out",
                "title": "Stall Allotment for Society Home-Chefs & Sponsor Drive",
                "description": (
                    "Host lottery for 15 food stalls and secure local branch "
                    "bank co-sponsorship."
                ),
                "dueDate": "2026-10-04",
                "completed": True,
                "category": "Community",
            },
            {
                "id": "t3",
                "phase": "2 Weeks Out",
                "title": "Book Live Folk Band, Sound Operator & Genset",
                "description": (
                    "Lock in live Garba singers and test society electrical "
                    "feeder lines."
                ),
                "dueDate": "2026-10-18",
                "completed": True,
                "category": "Logistics",
            },
            {
                "id": "t4",
                "phase": "5 Days Out",
                "title": "Purchase Dandiya Sticks & Competition Trophies",
                "description": (
                    "Procure 300 wooden dandiya sets and award trophies for Best "
                    "Rangoli."
                ),
                "dueDate": "2026-10-27",
                "completed": False,
                "category": "Prizes",
            },
            {
                "id": "t5",
                "phase": "Day Before",
                "title": "Electrical Safety Audit & Volunteer Briefing",
                "description": (
                    "Brief 20 youth marshals on emergency exits, crowd flow, and "
                    "first-aid points."
                ),
                "dueDate": "2026-10-31",
                "completed": False,
                "category": "Safety",
            },
        ],
        "dayOfSchedule": [
            {
                "id": "s1",
                "time": "08:00 AM",
                "activity": "Ground Staging & Tent Stalls Load-In",
                "location": "Society Central Lawn",
                "coordinator": "Logistics Lead",
                "notes": "Direct canopy and light trussing delivery trucks",
                "status": "upcoming",
            },
            {
                "id": "s2",
                "time": "01:00 PM",
                "activity": "Electrical Wiring & Sound System Installation",
                "location": "Stage Area",
                "coordinator": "Sound Engineer",
                "notes": "Check all heavy electrical wiring with rubber covers",
                "status": "upcoming",
            },
            {
                "id": "s3",
                "time": "04:00 PM",
                "activity": "Inter-Tower Rangoli Competition Commences",
                "location": "Clubhouse Corridors",
                "coordinator": "Cultural Committee",
                "notes": "30 resident teams allocated marked floor squares",
                "status": "upcoming",
            },
            {
                "id": "s4",
                "time": "05:30 PM",
                "activity": "Food Stalls Open & Diya Lighting Puja",
                "location": "Food Bazaar Row",
                "coordinator": "Society President & Elders",
                "notes": "Lighting of central 108 Maha-Diya by senior residents",
                "status": "upcoming",
            },
            {
                "id": "s5",
                "time": "06:30 PM",
                "activity": "Soundcheck & Free Dandiya Sticks Distribution",
                "location": "Registration Desk",
                "coordinator": "Youth Marshals",
                "notes": "Hand over complimentary dandiya sticks to families",
                "status": "upcoming",
            },
            {
                "id": "s6",
                "time": "07:00 PM",
                "activity": "Maha-Aarti & Garba Raas Round 1 (Traditional)",
                "location": "Central Lawn Circle",
                "coordinator": "Folk Band Leader",
                "notes": "Slow 2-Taali and 3-Taali traditional Garba",
                "status": "upcoming",
            },
            {
                "id": "s7",
                "time": "08:15 PM",
                "activity": "Rangoli & Best Dressed Prize Ceremony",
                "location": "Main Stage",
                "coordinator": "Committee Secretary",
                "notes": "Award trophies and gift vouchers to winners",
                "status": "upcoming",
            },
            {
                "id": "s8",
                "time": "08:45 PM",
                "activity": "High-Energy Dandiya Round 2 with Nasik Dhol",
                "location": "Central Lawn",
                "coordinator": "Dhol Master & Band",
                "notes": "Peak crowd energy with synchronized Dandiya clacks",
                "status": "upcoming",
            },
            {
                "id": "s9",
                "time": "09:45 PM",
                "activity": "Eco-Friendly Cold Fireworks & Closing Remarks",
                "location": "Safe Perimeter Zone",
                "coordinator": "Safety Officer",
                "notes": "Announcement of Diwali greetings and funds raised",
                "status": "upcoming",
            },
            {
                "id": "s10",
                "time": "10:00 PM",
                "activity": "Music Curfew Compliance & Cleanliness Drive",
                "location": "Society Grounds",
                "coordinator": "All Volunteers",
                "notes": "Strict audio shutdown as per police norms; waste cleanup",
                "status": "upcoming",
            },
        ],
        "vendorChecklist": [
            {
                "id": "v1",
                "category": "Stage & Sound",
                "vendorName": "Swara Sound & Stage Tech",
                "contact": "info@swarasound.com | +91 98200 78901",
                "estimatedCost": 120000.0,
                "contractedCost": 115000.0,
                "status": "booked",
                "checklist": [
                    {
                        "id": "c1",
                        "task": "Verify wireless mics for 4 live singers",
                        "completed": True,
                    },
                    {
                        "id": "c2",
                        "task": "Ensure sound shutdown exactly at 10:00 PM",
                        "completed": True,
                    },
                ],
                "notes": "Sound engineer on-site from 04:00 PM to 10:30 PM.",
            },
            {
                "id": "v2",
                "category": "Electrical & Lights",
                "vendorName": "Roshni Electricians & Gensets",
                "contact": "roshnielectric@gmail.com",
                "estimatedCost": 90000.0,
                "contractedCost": 88000.0,
                "status": "booked",
                "checklist": [
                    {
                        "id": "c3",
                        "task": "Verify 60KVA quiet generator fuel tank is full",
                        "completed": True,
                    },
                    {
                        "id": "c4",
                        "task": "Inspect MCB trip switches on all 15 food stalls",
                        "completed": True,
                    },
                ],
                "notes": "Fire extinguishers stationed beside generator.",
            },
            {
                "id": "v3",
                "category": "Folk Band & Dhol",
                "vendorName": "Rangilo Gujarat Folk Troupe",
                "contact": "booking@rangilogarba.in",
                "estimatedCost": 85000.0,
                "contractedCost": 85000.0,
                "status": "booked",
                "checklist": [
                    {
                        "id": "c5",
                        "task": "Finalize list of must-play Gujarati Garba hits",
                        "completed": True,
                    },
                    {
                        "id": "c6",
                        "task": "Confirm arrival time at 06:00 PM sharp",
                        "completed": True,
                    },
                ],
                "notes": "Team includes 2 lead vocalists, octapad, dholak, and keyboard.",
            },
        ],
    },
}
