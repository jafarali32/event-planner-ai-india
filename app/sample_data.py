from typing import Dict
from .models import EventPlan, EventIdeas, ColorSwatch, BudgetItem, TimelineMilestone, ScheduleItem, VendorItem, ChecklistTask

SAMPLE_EVENTS: Dict[str, dict] = {
    "wedding": {
        "id": "sample-wedding-1",
        "title": "Elena & Lucas's Coastal Mediterranean Wedding",
        "eventType": "wedding",
        "date": "2027-06-18",
        "location": "Cliffside Villa & Terrace, Amalfi Coast / California Coast",
        "guestCount": 110,
        "currency": "USD",
        "totalBudget": 38000.0,
        "vibeAndStyle": "Sun-drenched Mediterranean romantic, organic olive branch greenery, terracotta accents, candlelit long tables, acoustic strings",
        "specialRequests": "Include vegan & gluten-free food options, a signature espresso martini bar after dessert, and an acoustic first dance.",
        "ideas": {
            "themeTitle": "Riviera Gold & Olive Breeze",
            "themeConcept": "An intimate, sun-kissed celebration capturing the warmth of coastal Italy. Natural linen textiles, hand-painted ceramic tile nameplates, lemon grove aromas, and an emphasis on shared gourmet dining and storytelling.",
            "colorPalette": [
                {"name": "Warm Terracotta", "hex": "#D97443"},
                {"name": "Olive Leaf", "hex": "#5D6D4E"},
                {"name": "Sun-Washed Gold", "hex": "#E8BA60"},
                {"name": "Sea Salt White", "hex": "#F9F8F5"},
                {"name": "Cerulean Blue", "hex": "#2B6CB0"}
            ],
            "signatureFoodAndDrinks": [
                "Amalfi Spritz: Prosecco, limoncello, soda water, fresh basil and charred lemon wheel",
                "Smoked Rosemary Old Fashioned: Bourbon, fig syrup, and aromatic bitters",
                "Family-Style Woodfired Porchetta & Herb-Crusted Wild Sea Bass",
                "Handmade Burrata Bar with heirloom tomatoes, aged balsamic reduction, and grilled focaccia",
                "Late-Night Gelato Cart with pistachio, salted caramel, and blood orange sorbet"
            ],
            "activitiesAndEntertainment": [
                "Acoustic Spanish and classical guitar duo during ceremony and cocktail hour",
                "Live Calligrapher writing personalized guest love-letters on handmade deckled paper",
                "Audio Guestbook housed in a restored 1970s vintage cream telephone",
                "7-piece Mediterranean Funk & Soul band transitioning into a high-energy DJ set",
                "Midnight sparkler send-off along the lit stone pathway"
            ],
            "decorAndAtmosphere": [
                "Long wooden imperial tables adorned with sheer ivory runners and potted olive branch trees",
                "Hand-stamped ceramic tile place cards that guests take home as keepsakes",
                "Fairy light canopy under open timber pergolas reflecting against crystal stemware",
                "Cluster of mismatched terracotta urns filled with wild rosemary, eucalyptus, and garden roses"
            ],
            "surpriseElements": [
                "Surprise acoustic serenade by the groom's brother during twilight toasts",
                "Custom Limoncello bottles with wax-sealed wax stamps as personalized farewell favors",
                "Cold spark fountains firing during the dramatic first dance dip"
            ],
            "moodboardPrompt": "Elegant Mediterranean coastal wedding reception, sunset golden hour, wooden farm tables with olive garlands, terracotta pottery, warm fairy string lights, candles, fine china, ocean horizon in background, cinematic, photorealistic 8k"
        },
        "budgetBreakdown": [
            {"id": "b1", "category": "Venue & Rentals", "item": "Villa Terrace Rental (10 hours)", "estimatedCost": 9500.0, "actualCost": 9200.0, "paidAmount": 4600.0, "status": "booked", "notes": "50% deposit paid; includes tables and crossback chairs"},
            {"id": "b2", "category": "Catering & Bar", "item": "Plated Dinner (110 guests + service staff)", "estimatedCost": 11500.0, "actualCost": 11800.0, "paidAmount": 3000.0, "status": "booked", "notes": "Includes cocktail hour bites and 3-course dinner"},
            {"id": "b3", "category": "Catering & Bar", "item": "Open Bar, Signature Drinks & Gelato Cart", "estimatedCost": 3200.0, "actualCost": 3000.0, "paidAmount": 1000.0, "status": "booked", "notes": "Specialty limoncello sourced locally"},
            {"id": "b4", "category": "Photography & Video", "item": "Full Day Photo + Drone Video Package", "estimatedCost": 4200.0, "actualCost": 4000.0, "paidAmount": 2000.0, "status": "booked", "notes": "8 hours coverage, 2 shooters, sneak peek in 48 hours"},
            {"id": "b5", "category": "Floral & Decor", "item": "Ceremony Arch, Tablescapes & Bouquets", "estimatedCost": 3500.0, "actualCost": 3400.0, "paidAmount": 1000.0, "status": "booked", "notes": "Focus on olive branches, local florals and terracotta pots"},
            {"id": "b6", "category": "Music & Entertainment", "item": "Acoustic Duo + 6-Piece Evening Band/DJ", "estimatedCost": 2800.0, "actualCost": 2800.0, "paidAmount": 1400.0, "status": "booked", "notes": "Sound system and wireless mics included for speeches"},
            {"id": "b7", "category": "Attire & Beauty", "item": "Hair & Makeup for Bride + Bridal Party", "estimatedCost": 1200.0, "actualCost": 1150.0, "paidAmount": 500.0, "status": "booked", "notes": "Trial completed and approved"},
            {"id": "b8", "category": "Stationery & Favors", "item": "Tile Nameplates, Menus & Limoncello Favors", "estimatedCost": 900.0, "actualCost": 850.0, "paidAmount": 850.0, "status": "paid", "notes": "Completed and packaged"},
            {"id": "b9", "category": "Contingency & Tips", "item": "Buffer for Weather/Vendor Tips", "estimatedCost": 1200.0, "actualCost": 0.0, "paidAmount": 0.0, "status": "planned", "notes": "Reserved in cash envelopes for event day"}
        ],
        "timeline": [
            {"id": "t1", "phase": "9-12 Months Out", "title": "Secure Venue and Date", "description": "Lock in ceremony and reception contracts with initial security deposits.", "dueDate": "2026-08-01", "completed": True, "category": "Milestone"},
            {"id": "t2", "phase": "6-9 Months Out", "title": "Book Photographer, Caterer & Music", "description": "Conduct food tasting session, select main entrees, and finalize shot list.", "dueDate": "2026-11-15", "completed": True, "category": "Vendor"},
            {"id": "t3", "phase": "4-6 Months Out", "title": "Send Save-The-Dates & Setup Website", "description": "Launch wedding website with lodging recommendations and RSVP portal.", "dueDate": "2027-01-10", "completed": True, "category": "Guests"},
            {"id": "t4", "phase": "2-3 Months Out", "title": "Mail Formal Invitations & Floral Mockup", "description": "Track dietary RSVPs and inspect centerpiece mockups with the florist.", "dueDate": "2027-03-25", "completed": False, "category": "Stationery"},
            {"id": "t5", "phase": "1 Month Out", "title": "Final Seating Chart & Vendor Walkthrough", "description": "Meet coordinator on-site to review power outlets, rain backup, and timeline.", "dueDate": "2027-05-18", "completed": False, "category": "Logistics"},
            {"id": "t6", "phase": "Week Of", "title": "Pack Wedding Day Emergency Kit & Rehearsal", "description": "Distribute timeline to bridal party, rehearse procession, prep tip envelopes.", "dueDate": "2027-06-15", "completed": False, "category": "Final Prep"}
        ],
        "dayOfSchedule": [
            {"id": "s1", "time": "08:30 AM", "activity": "Bridal Suite Hair & Makeup Begins", "location": "Villa Master Suite", "coordinator": "Lead Stylist & Maid of Honor", "notes": "Mimosas and light fruit brunch served", "status": "upcoming"},
            {"id": "s2", "time": "12:00 PM", "activity": "Florist & Rentals Load-In", "location": "Courtyard & Lawn", "coordinator": "Day-of Coordinator", "notes": "Check table placement and string lights", "status": "upcoming"},
            {"id": "s3", "time": "02:30 PM", "activity": "Bride & Groom Getting Dressed", "location": "Villa Suites", "coordinator": "Photographer", "notes": "Detail shots of rings, dress, stationery suite", "status": "upcoming"},
            {"id": "s4", "time": "03:45 PM", "activity": "First Look & Couple Portraits", "location": "Olive Grove Overlook", "coordinator": "Lead Photographer", "notes": "Private moment, emotional reveals", "status": "upcoming"},
            {"id": "s5", "time": "05:00 PM", "activity": "Guest Arrival & Welcome Refreshments", "location": "Terrace Entrance", "coordinator": "Venue Host", "notes": "Lemon herb water and sparkling prosecco", "status": "upcoming"},
            {"id": "s6", "time": "05:30 PM", "activity": "Ceremony Processional Begins", "location": "Cliffside Pergola", "coordinator": "Officiant & Planner", "notes": "Guitar duo plays acoustic Canon in D", "status": "upcoming"},
            {"id": "s7", "time": "06:15 PM", "activity": "Cocktail Hour & Passed Appetizers", "location": "Sun Terrace", "coordinator": "Catering Lead", "notes": "Burrata bar opens; family group photos", "status": "upcoming"},
            {"id": "s8", "time": "07:30 PM", "activity": "Grand Entrance & Golden Hour Dinner", "location": "Main Dining Courtyard", "coordinator": "MC / Band Lead", "notes": "Sunset toast right at 07:55 PM", "status": "upcoming"},
            {"id": "s9", "time": "09:00 PM", "activity": "First Dance & Parent Dances", "location": "Courtyard Dance Floor", "coordinator": "Band Lead", "notes": "Cold spark fountains trigger at chorus", "status": "upcoming"},
            {"id": "s10", "time": "09:30 PM", "activity": "Dessert Bar & Open Dance Floor", "location": "Courtyard", "coordinator": "DJ & Gelato Lead", "notes": "Espresso martini bar opens", "status": "upcoming"},
            {"id": "s11", "time": "11:30 PM", "activity": "Sparkler Farewell Send-Off", "location": "Stone Staircase Path", "coordinator": "Coordinator & Groomsmen", "notes": "36-inch sparklers and vintage getaway car", "status": "upcoming"}
        ],
        "vendorChecklist": [
            {
                "id": "v1", "category": "Venue", "vendorName": "Villa Bellavista Estate", "contact": "events@bellavistavilla.com | (555) 234-8901",
                "estimatedCost": 9500.0, "contractedCost": 9200.0, "status": "booked",
                "checklist": [
                    {"id": "c1", "task": "Pay 50% reservation deposit", "completed": True},
                    {"id": "c2", "task": "Obtain day-of liability insurance rider ($1M)", "completed": True},
                    {"id": "c3", "task": "Confirm load-in access time (strictly 11 AM)", "completed": True},
                    {"id": "c4", "task": "Final walkthrough with planner", "completed": False}
                ],
                "notes": "Curfew is 11:30 PM for outdoor amplified music."
            },
            {
                "id": "v2", "category": "Catering", "vendorName": "Artisanal Coast Culinary Co.", "contact": "chef_marco@artisancoast.com",
                "estimatedCost": 11500.0, "contractedCost": 11800.0, "status": "booked",
                "checklist": [
                    {"id": "c5", "task": "Tasting completed and menu approved", "completed": True},
                    {"id": "c6", "task": "Provide final headcount & allergen dietary list", "completed": False},
                    {"id": "c7", "task": "Confirm staff ratio (1 server per 10 guests)", "completed": True}
                ],
                "notes": "Bringing portable woodfire pizza oven for late night snack."
            },
            {
                "id": "v3", "category": "Photo & Video", "vendorName": "Lumina Sunbeam Studios", "contact": "claire@luminastudios.com",
                "estimatedCost": 4200.0, "contractedCost": 4000.0, "status": "booked",
                "checklist": [
                    {"id": "c8", "task": "Submit shot list & VIP family list", "completed": False},
                    {"id": "c9", "task": "Confirm drone clearance with venue", "completed": True},
                    {"id": "c10", "task": "Provide vendor meal count to caterer", "completed": False}
                ],
                "notes": "Two photographers + 1 drone videographer."
            },
            {
                "id": "v4", "category": "Florist", "vendorName": "Tuscan Bloom Bottega", "contact": "hello@tuscanblooms.com",
                "estimatedCost": 3500.0, "contractedCost": 3400.0, "status": "booked",
                "checklist": [
                    {"id": "c11", "task": "Approve final floral moodboard", "completed": True},
                    {"id": "c12", "task": "Order terracotta vessel rentals", "completed": True},
                    {"id": "c13", "task": "Schedule breakdown and teardown after sendoff", "completed": False}
                ],
                "notes": "Arrangements to be repurposed from ceremony arch to head table."
            }
        ]
    },

    "birthday": {
        "id": "sample-birthday-1",
        "title": "Maya's 'Neon Oasis' 30th Milestone Birthday",
        "eventType": "birthday",
        "date": "2026-11-14",
        "location": "Skyline Loft & Rooftop Patio, Downtown",
        "guestCount": 45,
        "currency": "USD",
        "totalBudget": 5500.0,
        "vibeAndStyle": "Vibrant 90s/Y2K retro-futuristic, neon glow aesthetics, chill electronic and R&B vibes, interactive cocktail stations, casual-chic party",
        "specialRequests": "Include a customized retro photo booth with nostalgic props, craft mocktails for non-drinkers, and a surprise video montage.",
        "ideas": {
            "themeTitle": "Neon Sunset & Retro Electric 30",
            "themeConcept": "A vibrant celebration marking the transition into the thirties with playful Y2K nostalgia blended with sleek modern rooftop luxury. Glowing neon signs, holographic accents, customized vinyl record favors, and throwback beats.",
            "colorPalette": [
                {"name": "Electric Fuchsia", "hex": "#E0218A"},
                {"name": "Cyber Cyan", "hex": "#00F0FF"},
                {"name": "Sunset Purple", "hex": "#7928CA"},
                {"name": "Midnight Obsidian", "hex": "#111827"},
                {"name": "Holographic Silver", "hex": "#D1D5DB"}
            ],
            "signatureFoodAndDrinks": [
                "The 'Dirty Thirty' Cosmo: Yuzu vodka, cranberry reduction, lime foam, edible glitter shimmer",
                "Electric Blue Zero-Proof: Blue spirulina, coconut water, lychee puree, popping boba",
                "Gourmet Slider Flight: Wagyu truffle, buttermilk fried hot chicken, and crispy halloumi slider",
                "Mini Street Taco Bar: Carne asada, citrus carnitas, and charred jackfruit with street corn cups",
                "Custom Retro Birthday Cake: 90s airbrush comic book style with funfetti filling"
            ],
            "activitiesAndEntertainment": [
                "Custom 90s/2000s Pop Culture & Birthday Trivia hosted by a witty friend",
                "Vintage Photobooth station with instant Polaroid strips and custom neon frame logo",
                "DIY Glitter & Temporary Flash Tattoo Station for guests",
                "Surprise 5-minute video tribute from childhood friends played on rooftop projector",
                "Curated Vinyl DJ spinning throwback disco, nostalgic R&B, and dance favorites"
            ],
            "decorAndAtmosphere": [
                "Custom pink neon sign reading ' Maya's Chapter 30 ' on a lush green boxwood wall",
                "Floating LED orb lights in the rooftop plunge pool / lounge area",
                "Holographic fringe curtain entrance with dramatic uplighting",
                "Retro arcade cabinet (e.g. Pac-Man or Street Fighter) set to free play"
            ],
            "surpriseElements": [
                "Secret champagne flash-toast delivered via glowing sparkler trays",
                "Personalized custom mini cassette tapes with a Spotify playlist link inside",
                "Midnight warm donut delivery from the birthday girl's favorite childhood bakery"
            ],
            "moodboardPrompt": "Modern trendy 30th birthday loft party at night, neon pink and cyan mood lighting, skyline view through floor-to-ceiling windows, fashionable young adults laughing, polaroid cameras, disco balls, cinematic lighting"
        },
        "budgetBreakdown": [
            {"id": "b1", "category": "Venue", "item": "Rooftop Loft Rental (6 hours)", "estimatedCost": 1800.0, "actualCost": 1750.0, "paidAmount": 875.0, "status": "booked", "notes": "Includes sound system and patio firepits"},
            {"id": "b2", "category": "Food & Beverages", "item": "Artisan Sliders, Taco Bar & Cocktail Service", "estimatedCost": 1900.0, "actualCost": 1950.0, "paidAmount": 600.0, "status": "booked", "notes": "Bartender included for 4 hours"},
            {"id": "b3", "category": "Entertainment & Music", "item": "DJ / Sound Gear + Free-Play Arcade Rental", "estimatedCost": 750.0, "actualCost": 700.0, "paidAmount": 350.0, "status": "booked", "notes": "DJ confirmed 8 PM to midnight"},
            {"id": "b4", "category": "Decor & Neon", "item": "Custom Neon Sign & Boxwood Wall", "estimatedCost": 450.0, "actualCost": 420.0, "paidAmount": 420.0, "status": "paid", "notes": "Delivered and tested"},
            {"id": "b5", "category": "Cake & Desserts", "item": "Airbrushed Funfetti 2-Tier Cake + Midnight Donuts", "estimatedCost": 350.0, "actualCost": 330.0, "paidAmount": 165.0, "status": "booked", "notes": "Pickup at 4 PM day-of"},
            {"id": "b6", "category": "Favors & Photo Station", "item": "Instant Polaroid Film & Custom Cassette Favors", "estimatedCost": 250.0, "actualCost": 220.0, "paidAmount": 220.0, "status": "paid", "notes": "Supplies on hand"}
        ],
        "timeline": [
            {"id": "t1", "phase": "6 Weeks Out", "title": "Reserve Loft Venue & Choose Theme", "description": "Lock in venue deposit and finalize Neon Oasis vibe palette.", "dueDate": "2026-10-03", "completed": True, "category": "Venue"},
            {"id": "t2", "phase": "4 Weeks Out", "title": "Send Digital Invites & Book DJ", "description": "Collect RSVPs via Partiful / Paperless Post and confirm song requests.", "dueDate": "2026-10-17", "completed": True, "category": "Guests"},
            {"id": "t3", "phase": "2 Weeks Out", "title": "Order Custom Neon Sign & Birthday Cake", "description": "Send reference art to bakery and approve neon mockup.", "dueDate": "2026-10-31", "completed": True, "category": "Decor"},
            {"id": "t4", "phase": "1 Week Out", "title": "Gather Secret Video Clips & Finalize Menu", "description": "Edit friend tribute reel and submit final food counts.", "dueDate": "2026-11-07", "completed": False, "category": "Surprise"},
            {"id": "t5", "phase": "Day Before", "title": "Pick Up Props, Liquor Stock & Favors", "description": "Prep polaroid cameras, pack batteries, charge speaker backups.", "dueDate": "2026-11-13", "completed": False, "category": "Logistics"}
        ],
        "dayOfSchedule": [
            {"id": "s1", "time": "04:30 PM", "activity": "Host Arrival & Venue Access", "location": "Skyline Loft", "coordinator": "Maya & Co-Host Bestie", "notes": "Unlock venue, test lighting presets", "status": "upcoming"},
            {"id": "s2", "time": "05:15 PM", "activity": "Caterer & DJ Load-In", "location": "Loft Bar & DJ Booth", "coordinator": "DJ & Catering Lead", "notes": "Soundcheck and bar ice setup", "status": "upcoming"},
            {"id": "s3", "time": "06:30 PM", "activity": "Decor Setup & Neon Wall Test", "location": "Photo Zone", "coordinator": "Decor Crew", "notes": "Load fresh polaroid film packs", "status": "upcoming"},
            {"id": "s4", "time": "07:30 PM", "activity": "Guests Arrive & Welcome Drinks", "location": "Rooftop Patio", "coordinator": "Bartender", "notes": "Signature 'Dirty Thirty' Cosmos poured", "status": "upcoming"},
            {"id": "s5", "time": "08:30 PM", "activity": "Taco & Slider Stations Open", "location": "Main Lounge", "coordinator": "Catering Lead", "notes": "Warm gourmet finger foods available", "status": "upcoming"},
            {"id": "s6", "time": "09:30 PM", "activity": "Surprise Tribute Video Projection & Toast", "location": "Rooftop Screen", "coordinator": "Co-Host", "notes": "Dim lights, cue emotional video", "status": "upcoming"},
            {"id": "s7", "time": "09:45 PM", "activity": "Cake Cutting & Sparkling Champagne Toast", "location": "Dessert Table", "coordinator": "Host", "notes": "Light sparkle candles for photos", "status": "upcoming"},
            {"id": "s8", "time": "10:00 PM", "activity": "Full Dance Floor & Retro DJ Set", "location": "Loft Main Room", "coordinator": "DJ", "notes": "High energy club & Y2K classics", "status": "upcoming"},
            {"id": "s9", "time": "11:30 PM", "activity": "Midnight Donut Surprise & Favors", "location": "Exit Lounge", "coordinator": "Co-Host", "notes": "Warm glazed boxes passed out", "status": "upcoming"},
            {"id": "s10", "time": "12:00 AM", "activity": "Wrap Up & Event Concludes", "location": "Loft", "coordinator": "Host Team", "notes": "Ride shares called for guests", "status": "upcoming"}
        ],
        "vendorChecklist": [
            {
                "id": "v1", "category": "Venue", "vendorName": "Skyline Urban Loft", "contact": "bookings@skylinelofts.com",
                "estimatedCost": 1800.0, "contractedCost": 1750.0, "status": "booked",
                "checklist": [
                    {"id": "c1", "task": "Confirm rooftop heater operation", "completed": True},
                    {"id": "c2", "task": "Obtain freight elevator access code", "completed": True}
                ],
                "notes": "Security deposit of $500 holds until post-party inspection."
            },
            {
                "id": "v2", "category": "Catering & Bar", "vendorName": "Craft & Flame Pop-Up", "contact": "chef_tori@craftandflame.com",
                "estimatedCost": 1900.0, "contractedCost": 1950.0, "status": "booked",
                "checklist": [
                    {"id": "c3", "task": "Finalize mocktail ingredients", "completed": True},
                    {"id": "c4", "task": "Confirm 200lbs ice supply delivery", "completed": False}
                ],
                "notes": "Bringing 2 mobile bar carts and glassware."
            },
            {
                "id": "v3", "category": "Music", "vendorName": "DJ NeonGroove (Sammy)", "contact": "sammy@neongroove.fm",
                "estimatedCost": 750.0, "contractedCost": 700.0, "status": "booked",
                "checklist": [
                    {"id": "c5", "task": "Send Spotify playlist of must-plays and do-not-plays", "completed": True},
                    {"id": "c6", "task": "Confirm HDMI connection for video projector", "completed": True}
                ],
                "notes": "Wireless mic provided for speeches."
            }
        ]
    },

    "community": {
        "id": "sample-community-1",
        "title": "Oakwood Community Harvest Fair & Charity Gala",
        "eventType": "community",
        "date": "2026-10-10",
        "location": "Oakwood Park & Town Pavilion Amphitheater",
        "guestCount": 450,
        "currency": "USD",
        "totalBudget": 14000.0,
        "vibeAndStyle": "Warm, inclusive, family-friendly, eco-conscious, celebrating local arts, farmers, and community unity with evening live music",
        "specialRequests": "Requires city park sound permits, ADA accessibility ramp verification, zero-waste recycling stations, and volunteer shift management.",
        "ideas": {
            "themeTitle": "Autumn Hearth: Roots & Neighbors",
            "themeConcept": "A neighborhood-wide celebration honoring local craftsmanship, sustainable living, and community connection. Hay bale seating, artisanal farm stands, children's maker tents, cider pressings, and a lively evening folk-rock concert.",
            "colorPalette": [
                {"name": "Autumn Amber", "hex": "#D97706"},
                {"name": "Forest Pine", "hex": "#1E3A2F"},
                {"name": "Cider Rust", "hex": "#9A3412"},
                {"name": "Sunflower Ochre", "hex": "#F59E0B"},
                {"name": "Natural Burlap", "hex": "#E5E0D8"}
            ],
            "signatureFoodAndDrinks": [
                "Hot Spiced Apple Cider Station with cinnamon sticks and orange peels",
                "Local Artisan Food Truck Village (Woodfired Pizza, Empanadas, Vegan Bowls)",
                "Community Bake-Off Tasting Tent: Pumpkin, pecan, and apple crisps",
                "Local Craft Brewery & Kombucha Garden (token-based charity fundraiser)",
                "Complimentary Roasted Corn on the Cob with herb butter spreads"
            ],
            "activitiesAndEntertainment": [
                "Main Pavilion Concert: 3 Local indie folk & acoustic bluegrass ensembles",
                "Kids Maker Zone: Pumpkin painting, birdhouse crafting, face painting",
                "Community Pie-Eating & Giant Pumpkin Weigh-In Contests",
                "Silent Charity Auction benefiting the Oakwood Youth Arts Center",
                "Local Makers Market with 25 independent neighborhood artisans"
            ],
            "decorAndAtmosphere": [
                "Natural straw bale seating clusters draped with plaid flannel blankets",
                "Warm festoon string lights crisscrossing the open park lawn",
                "Rustic wooden signposts pointing to Food Village, Kids Zone, and Stage",
                "Giant chalkboard community mural where attendees write: 'What I love about our neighborhood'"
            ],
            "surpriseElements": [
                "Surprise flash-mob choir performance by the Oakwood High School Chorus",
                "Golden Pumpkin scavenger hunt hidden across the park with local business gift certificates",
                "Lantern lighting ceremony around the central fountain at dusk"
            ],
            "moodboardPrompt": "Wholesome outdoor autumn community festival in a public park, golden fall foliage, wooden food trucks, string lights, hay bales, families smiling, artisan craft booths, warm daylight transitioning to sunset, high quality"
        },
        "budgetBreakdown": [
            {"id": "b1", "category": "Permits & Safety", "item": "City Park Permit, Sound Waiver & Police Detail", "estimatedCost": 1800.0, "actualCost": 1650.0, "paidAmount": 1650.0, "status": "paid", "notes": "Approved by City Council"},
            {"id": "b2", "category": "Stage & Audio/Visual", "item": "Pavilion Stage Sound System, Microphones & Tech Operator", "estimatedCost": 2800.0, "actualCost": 2700.0, "paidAmount": 1350.0, "status": "booked", "notes": "Operator on-site 10 AM to 8 PM"},
            {"id": "b3", "category": "Rentals & Logistics", "item": "Tents (10x10 and 20x40), Folding Tables, 200 Chairs & Restroom Trailers", "estimatedCost": 3500.0, "actualCost": 3600.0, "paidAmount": 1800.0, "status": "booked", "notes": "Delivery scheduled 07:00 AM"},
            {"id": "b4", "category": "Entertainment & Bands", "item": "3 Local Musical Acts Honorariums", "estimatedCost": 1800.0, "actualCost": 1800.0, "paidAmount": 900.0, "status": "booked", "notes": "Contracts signed"},
            {"id": "b5", "category": "Kids Zone & Activities", "item": "Craft Supplies, Pumpkins, Face Painters & Inflatables", "estimatedCost": 1500.0, "actualCost": 1400.0, "paidAmount": 700.0, "status": "booked", "notes": "2 face painters booked for 4 hrs"},
            {"id": "b6", "category": "Signage & Marketing", "item": "Flyers, Park Wayfinding Banners, Volunteer T-Shirts", "estimatedCost": 900.0, "actualCost": 850.0, "paidAmount": 850.0, "status": "paid", "notes": "Printed and boxed"},
            {"id": "b7", "category": "Waste & Eco-Stations", "item": "Compost & Recycling Sorting Bins + Waste Hauling", "estimatedCost": 700.0, "actualCost": 650.0, "paidAmount": 300.0, "status": "booked", "notes": "Eco-volunteer team monitoring"},
            {"id": "b8", "category": "Contingency Fund", "item": "Emergency Supplies, First Aid & Backup Generators", "estimatedCost": 1000.0, "actualCost": 0.0, "paidAmount": 0.0, "status": "planned", "notes": "On standby"}
        ],
        "timeline": [
            {"id": "t1", "phase": "6 Months Out", "title": "Submit City Park & Sound Permits", "description": "Lodge application with City Parks Dept and review public safety requirements.", "dueDate": "2026-04-15", "completed": True, "category": "Permits"},
            {"id": "t2", "phase": "4 Months Out", "title": "Artisan & Food Truck Applications Open", "description": "Select 25 craft vendors and 6 diverse food trucks.", "dueDate": "2026-06-15", "completed": True, "category": "Vendors"},
            {"id": "t3", "phase": "2 Months Out", "title": "Sponsor Outreach & Volunteer Drive", "description": "Secure local credit union sponsorship and recruit 30 volunteer marshals.", "dueDate": "2026-08-15", "completed": True, "category": "Volunteers"},
            {"id": "t4", "phase": "3 Weeks Out", "title": "Signage Print & Map Finalization", "description": "Plot booth grid coordinates, waste stations, and emergency access lanes.", "dueDate": "2026-09-19", "completed": False, "category": "Logistics"},
            {"id": "t5", "phase": "1 Week Out", "title": "Volunteer Orientation & Safety Briefing", "description": "Host 45-min Zoom walkthrough for shift captains and first aid leads.", "dueDate": "2026-10-03", "completed": False, "category": "Operations"}
        ],
        "dayOfSchedule": [
            {"id": "s1", "time": "06:30 AM", "activity": "Park Gates Open & Logistics Staging", "location": "Main Lawn & Gate A", "coordinator": "Logistics Chair", "notes": "Direct tent rental and restroom delivery trucks", "status": "upcoming"},
            {"id": "s2", "time": "07:30 AM", "activity": "Food Truck & Artisan Booth Load-In", "location": "Perimeter Road", "coordinator": "Vendor Marshal Team", "notes": "Check food safety certifications and generator hookups", "status": "upcoming"},
            {"id": "s3", "time": "09:00 AM", "activity": "Volunteer Shift 1 Check-In & Briefing", "location": "Information Gazebo", "coordinator": "Volunteer Coordinator", "notes": "Hand out branded safety tees, radios, and park maps", "status": "upcoming"},
            {"id": "s4", "time": "09:45 AM", "activity": "Audio Soundcheck & Safety Final Sweep", "location": "Amphitheater Stage", "coordinator": "Sound Engineer", "notes": "Test mics, emergency broadcast, and ADA ramps", "status": "upcoming"},
            {"id": "s5", "time": "10:00 AM", "activity": "Gates Open to the Public", "location": "Park Entrance", "coordinator": "Welcome Committee", "notes": "Live folk duo plays greeting set; welcome map handouts", "status": "upcoming"},
            {"id": "s6", "time": "11:30 AM", "activity": "Kids Craft Pavilion & Pumpkin Contest Open", "location": "North Lawn Tent", "coordinator": "Youth Director", "notes": "All supplies pre-divided into sanitized stations", "status": "upcoming"},
            {"id": "s7", "time": "01:00 PM", "activity": "Mayor & Community Leader Opening Remarks", "location": "Main Stage", "coordinator": "Committee Chair", "notes": "Honor local volunteers and charity partners", "status": "upcoming"},
            {"id": "s8", "time": "02:30 PM", "activity": "Community Pie-Eating & Scavenger Hunt Reveal", "location": "Center Court", "coordinator": "Activities Lead", "notes": "High crowd engagement; award ribbons", "status": "upcoming"},
            {"id": "s9", "time": "04:30 PM", "activity": "Headliner Bluegrass & Folk Band", "location": "Main Stage", "coordinator": "Stage Manager", "notes": "Crowd gathers with lawn blankets", "status": "upcoming"},
            {"id": "s10", "time": "06:30 PM", "activity": "Sunset Lantern Walk & Charity Auction Closing", "location": "Fountain Plaza", "coordinator": "All Staff", "notes": "Announce fundraising total raised for youth center", "status": "upcoming"},
            {"id": "s11", "time": "07:30 PM", "activity": "Event Closes & Teardown Protocol", "location": "Entire Park", "coordinator": "Cleanup Crew Lead", "notes": "Zero-waste sorting check, park inspection with rangers", "status": "upcoming"}
        ],
        "vendorChecklist": [
            {
                "id": "v1", "category": "City & Permits", "vendorName": "City Parks & Recreation Dept", "contact": "parks_permits@citygov.org | (555) 789-0123",
                "estimatedCost": 1800.0, "contractedCost": 1650.0, "status": "completed",
                "checklist": [
                    {"id": "c1", "task": "Permit issued and printed for day-of binder", "completed": True},
                    {"id": "c2", "task": "Fire Marshal inspection scheduled for 08:30 AM", "completed": True},
                    {"id": "c3", "task": "Park Ranger emergency contact saved", "completed": True}
                ],
                "notes": "Emergency vehicle path must be kept 15ft clear at all times."
            },
            {
                "id": "v2", "category": "AV & Stage", "vendorName": "SoundWave Stage Productions", "contact": "dave@soundwavepro.com",
                "estimatedCost": 2800.0, "contractedCost": 2700.0, "status": "booked",
                "checklist": [
                    {"id": "c4", "task": "Confirm electrical draw and quiet generator need", "completed": True},
                    {"id": "c5", "task": "Receive band stage plots and input lists", "completed": True},
                    {"id": "c6", "task": "Set up hearing accessibility loop", "completed": False}
                ],
                "notes": "Includes 4 wireless mics and monitors."
            },
            {
                "id": "v3", "category": "Rentals", "vendorName": "All-Occasions Party & Tent Rentals", "contact": "orders@alloccasionsrent.com",
                "estimatedCost": 3500.0, "contractedCost": 3600.0, "status": "booked",
                "checklist": [
                    {"id": "c7", "task": "200 folding chairs and 30 banquet tables confirmed", "completed": True},
                    {"id": "c8", "task": "Luxury 4-stall portable restroom trailer delivery time", "completed": True},
                    {"id": "c9", "task": "Water refill station installation", "completed": False}
                ],
                "notes": "Pickup morning following event at 08:00 AM."
            }
        ]
    }
}
