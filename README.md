# ✨ CelebrateAI — GenAI Event Planning Assistant

An intelligent, full-stack generative AI planning assistant built to orchestrate **Weddings**, **Birthdays**, and **Community Festivals** with granular budget tracking, countdown timelines, day-of run-of-show schedules, vendor checklist management, and personalized creative concepts.

---

## 🌟 Key Features

### 1. 🎨 AI Ideas & Aesthetic Concepts
- **Theme & Creative Narrative**: Cohesive aesthetic concepts aligned with your vibe and location.
- **Interactive Color Palette**: Hand-curated color swatches with one-click hex code copying.
- **Signature Culinary & Bar Menu**: Distinctive signature cocktails, mocktails, and dining stations.
- **Surprise "WOW" Moments**: Memorable guest experiences, unexpected reveals, and entertainment highlights.
- **AI Moodboard Prompt**: Copy-ready prompt tailored for Midjourney, DALL-E, or Gemini Imagen.

### 2. 💰 Budget Maestro
- **Visual Allocation Doughnut**: Dynamic Chart.js breakdown by category (Venue, Catering, AV, Florals, Permits, Contingency).
- **Financial Health Gauges**: Live tracker of allocated vs. contracted vs. paid amounts and cushion balance.
- **Over-Budget Safeguards**: Real-time warnings when expenses exceed target allocations.
- **Itemized Ledger**: Interactive expense tracking with status workflows (`Planned` -> `Booked` -> `Paid`).

### 3. ⏱️ Timeline & Run-of-Show
- **Milestone Roadmap**: 12-month countdown with phase tracking, due dates, and completion celebrations (confetti!).
- **Day-of Run of Show**: Hour-by-hour master schedule with locations, assigned coordinators, and technical cues.

### 4. 📋 Vendor Checklists & CRM
- **Category Pipeline**: Comprehensive tracking for Venues, Catering, Photo/Video, Florists, Music/DJs, and Municipal Permits.
- **Status Workflow**: `Researching` ➔ `Contacted` ➔ `Quoted` ➔ `Booked` ➔ `Completed`.
- **Deliverables & Tasks**: Interactive sub-checklists per vendor with live progress percentage bars.

### 5. 🤖 EventGenie AI Interactive Assistant
- **Context-Aware Pair Planner**: Conversational chat interface with direct access to your active event blueprint.
- **Practical Problem Solving**: Request budget-cutting advice, vendor email inquiry drafts, rain contingency backup plans, and song ideas.

### 6. 📑 Export & Print Hub
- **Print / PDF Brief**: Clean, print-ready formatted event master brief.
- **Markdown Export**: Direct copyable markdown for Notion, Google Docs, or email briefing.
- **JSON Backup**: Download and restore entire event data structures.

---

## 🧠 Dual-Engine AI Architecture

CelebrateAI offers a resilient, zero-friction AI experience:

1. **Google Gemini 2.5 / 2.0 Flash Integration**:
   - Provide your Gemini API key via the top-bar key manager or `GEMINI_API_KEY` environment variable for real-time generative output.
2. **Built-In Intelligent Heuristic Fallback**:
   - Works immediately out of the box without requiring an API key or external internet connection. It calculates balanced budgets, generates phased timelines, and creates creative ideas tailored to your guest count, location, and aesthetic vibe.

---

## 🚀 Quickstart Guide

### 1. Requirements
- Python 3.10+
- Installed packages: `fastapi`, `uvicorn`, `pydantic`, `google-genai`

### 2. Launching the Application

From the project directory:

```powershell
python run.py
```

Open your browser at:
```
http://localhost:8000
```

### 3. Quick Demo Presets
CelebrateAI includes 3 realistic sample blueprints:
- **💍 Elena & Lucas's Coastal Mediterranean Wedding** ($38,000 | 110 guests)
- **🎂 Maya's 'Neon Oasis' 30th Milestone Birthday** ($5,500 | 45 guests)
- **🎪 Oakwood Community Harvest Fair & Charity Gala** ($14,000 | 450 attendees)

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the single-page responsive web application |
| `GET` | `/api/health` | Health check & Gemini engine configuration status |
| `GET` | `/api/samples/{event_type}` | Returns preset sample plan (`wedding`, `birthday`, `community`) |
| `POST` | `/api/generate` | Generates a complete event blueprint from user parameters |
| `POST` | `/api/chat` | Interactive Q&A with EventGenie AI planner |
| `POST` | `/api/export/markdown` | Converts event plan into formatted Markdown summary |

---

## 📁 Project Structure

```
event-planner-ai/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and route definitions
│   ├── models.py            # Pydantic data schemas
│   ├── sample_data.py       # Rich curated blueprints for weddings, birthdays, fairs
│   ├── ai_service.py        # Gemini SDK caller and intelligent synthesis engine
│   └── static/
│       ├── index.html       # Single-page UI with Tailwind & Lucide
│       ├── styles.css       # Custom styles, gradients & print media rules
│       └── app.js           # State controller, Chart.js, and API interactions
├── requirements.txt         # Dependency declarations
├── run.py                   # Server startup script
└── README.md                # Project documentation
```
