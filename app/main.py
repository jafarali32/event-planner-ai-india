import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .models import GeneratePlanRequest, ChatRequest, EventPlan
from .sample_data import SAMPLE_EVENTS
from .ai_service import generate_event_plan, ask_event_assistant

app = FastAPI(
    title="CelebrateAI - GenAI Event Planning Assistant",
    description="Intelligent AI planner for weddings, birthdays, and community events with budgets, timelines, checklists, and personalized ideas.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>CelebrateAI is loading...</h1>"

@app.get("/api/health")
async def health_check():
    has_env_key = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    return {
        "status": "healthy",
        "gemini_api_configured": has_env_key,
        "engine": "Gemini 2.5/2.0 Flash + Intelligent Heuristic Fallback"
    }

@app.get("/api/samples/{event_type}")
async def get_sample_event(event_type: str):
    ev_type = event_type.lower()
    if ev_type in SAMPLE_EVENTS:
        return SAMPLE_EVENTS[ev_type]
    raise HTTPException(status_code=404, detail=f"Sample for event type '{event_type}' not found. Available: wedding, birthday, community")

@app.post("/api/generate")
async def generate_plan(request: GeneratePlanRequest):
    try:
        plan = generate_event_plan(request)
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/api/chat")
async def chat_assistant(request: ChatRequest):
    try:
        reply = ask_event_assistant(request)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.post("/api/export/markdown")
async def export_plan_markdown(plan: EventPlan):
    try:
        lines = []
        lines.append(f"# {plan.title}")
        lines.append(f"**Type:** {plan.eventType.capitalize()} | **Date:** {plan.date or 'TBD'} | **Location:** {plan.location or 'TBD'}")
        lines.append(f"**Guests:** {plan.guestCount} | **Budget:** {plan.currency} {plan.totalBudget:,.2f}")
        lines.append(f"**Vibe & Style:** {plan.vibeAndStyle}\n")

        lines.append(f"## 🌟 Theme & Creative Concept: {plan.ideas.themeTitle}")
        lines.append(f"{plan.ideas.themeConcept}\n")

        lines.append("### Color Palette")
        for color in plan.ideas.colorPalette:
            lines.append(f"- **{color.name}** (`{color.hex}`)")
        lines.append("")

        lines.append("### Signature Food & Beverages")
        for item in plan.ideas.signatureFoodAndDrinks:
            lines.append(f"- {item}")
        lines.append("")

        lines.append("### Activities & Entertainment")
        for item in plan.ideas.activitiesAndEntertainment:
            lines.append(f"- {item}")
        lines.append("")

        lines.append("### Surprise Elements")
        for item in plan.ideas.surpriseElements:
            lines.append(f"- ✨ {item}")
        lines.append("")

        lines.append("## 💰 Budget Breakdown")
        lines.append("| Category | Item | Estimated | Actual | Paid | Status |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for b in plan.budgetBreakdown:
            lines.append(f"| {b.category} | {b.item} | {plan.currency} {b.estimatedCost:,.2f} | {plan.currency} {b.actualCost:,.2f} | {plan.currency} {b.paidAmount:,.2f} | {b.status.capitalize()} |")
        lines.append("")

        lines.append("## ⏱️ Milestone Timeline")
        for t in plan.timeline:
            status_box = "[x]" if t.completed else "[ ]"
            lines.append(f"- {status_box} **{t.phase}** - {t.title}: {t.description} *(Due: {t.dueDate or 'Flexible'})*")
        lines.append("")

        lines.append("## 🕒 Day-of Schedule (Run of Show)")
        lines.append("| Time | Activity | Location | Coordinator | Notes |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for s in plan.dayOfSchedule:
            lines.append(f"| {s.time} | {s.activity} | {s.location or '-'} | {s.coordinator or '-'} | {s.notes or '-'} |")
        lines.append("")

        lines.append("## 📋 Vendor Checklist")
        for v in plan.vendorChecklist:
            lines.append(f"### {v.category}: {v.vendorName} ({v.status.capitalize()})")
            lines.append(f"- **Contact:** {v.contact or 'Pending'}")
            lines.append(f"- **Estimated Cost:** {plan.currency} {v.estimatedCost:,.2f}")
            if v.notes:
                lines.append(f"- **Notes:** {v.notes}")
            lines.append("  **Tasks:**")
            for task in v.checklist:
                chk = "[x]" if task.completed else "[ ]"
                lines.append(f"  - {chk} {task.task}")
            lines.append("")

        md_content = "\n".join(lines)
        return {"markdown": md_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")
