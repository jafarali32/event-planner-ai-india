"""
CelebrateAI - FastAPI Application Server
Provides secure REST endpoints, GZip compression, security headers, and caching.
"""

import os
import logging
from functools import lru_cache
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from .models import GeneratePlanRequest, ChatRequest, EventPlan
from .sample_data import SAMPLE_EVENTS
from .ai_service import generate_event_plan, ask_event_assistant

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("celebrate_ai")

app = FastAPI(
    title="CelebrateAI - GenAI Event Planning Assistant",
    description="Production-grade AI planner for weddings, birthdays, and community festivals.",
    version="1.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# 1. Performance: GZip Compression Middleware
app.add_middleware(GZipMiddleware, minimum_size=500)


# 2. Security: Custom HTTP Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response


app.add_middleware(SecurityHeadersMiddleware)

# 3. Security: CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse, tags=["Web"])
async def serve_index():
    """Serves the main application single-page interface."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read(), status_code=200)
        except Exception as e:
            logger.error(f"Error reading index.html: {e}")
            raise HTTPException(status_code=500, detail="Internal file error")
    return HTMLResponse("<h1>CelebrateAI is initializing...</h1>", status_code=200)


@app.get("/api/health", tags=["System"])
async def health_check():
    """Health check endpoint reporting API engine status and configuration."""
    has_env_key = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    return {
        "status": "healthy",
        "gemini_api_configured": has_env_key,
        "engine": "Gemini 2.5/2.0 Flash + Intelligent Heuristic Fallback",
        "version": "1.1.0"
    }


@lru_cache(maxsize=16)
def _get_cached_sample(event_type: str) -> Dict[str, Any]:
    """In-memory LRU cache for preset blueprints to guarantee O(1) response times."""
    return SAMPLE_EVENTS[event_type]


@app.get("/api/samples/{event_type}", tags=["Blueprints"])
async def get_sample_event(event_type: str):
    """Retrieves an optimized sample preset for wedding, birthday, or community events."""
    ev_type = event_type.lower().strip()
    if ev_type in SAMPLE_EVENTS:
        return _get_cached_sample(ev_type)
    logger.warning(f"Requested invalid sample event type: {event_type}")
    raise HTTPException(
        status_code=404,
        detail=f"Sample for event type '{event_type}' not found. Supported types: wedding, birthday, community"
    )


@app.post("/api/generate", tags=["AI Engine"])
async def generate_plan(request: GeneratePlanRequest):
    """Synthesizes a full event blueprint using Gemini or deterministic fallback."""
    try:
        plan = generate_event_plan(request)
        return plan
    except ValueError as ve:
        logger.error(f"Validation error during generation: {ve}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.exception(f"Unexpected generation failure: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during event plan generation.")


@app.post("/api/chat", tags=["AI Assistant"])
async def chat_assistant(request: ChatRequest):
    """Context-aware conversational planning Q&A with EventGenie AI."""
    try:
        reply = ask_event_assistant(request)
        return {"reply": reply}
    except Exception as e:
        logger.exception(f"Chat assistant exception: {e}")
        raise HTTPException(status_code=500, detail="Unable to process chat request at this time.")


@app.post("/api/export/markdown", tags=["Export"])
async def export_plan_markdown(plan: EventPlan):
    """Converts a structured event blueprint into formatted GitHub-flavored Markdown."""
    try:
        lines = []
        lines.append(f"# {plan.title}")
        header_meta = (
            f"**Type:** {plan.eventType.capitalize()} | "
            f"**Date:** {plan.date or 'TBD'} | "
            f"**Location:** {plan.location or 'TBD'}"
        )
        lines.append(header_meta)
        lines.append(f"**Guests:** {plan.guestCount} | **Budget:** {plan.currency} {plan.totalBudget:,.2f}")
        lines.append(f"**Vibe & Style:** {plan.vibeAndStyle}\n")

        lines.append(f"## 🌟 Theme & Concept: {plan.ideas.themeTitle}")
        lines.append(f"{plan.ideas.themeConcept}\n")

        lines.append("### Color Palette")
        for color in plan.ideas.colorPalette:
            lines.append(f"- **{color.name}** (`{color.hex}`)")
        lines.append("")

        lines.append("### Signature Culinary & Beverages")
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
            row = (
                f"| {b.category} | {b.item} | {plan.currency} {b.estimatedCost:,.2f} | "
                f"{plan.currency} {b.actualCost:,.2f} | {plan.currency} {b.paidAmount:,.2f} | "
                f"{b.status.capitalize()} |"
            )
            lines.append(row)
        lines.append("")

        lines.append("## ⏱️ Milestone Timeline")
        for t in plan.timeline:
            status_box = "[x]" if t.completed else "[ ]"
            lines.append(
                f"- {status_box} **{t.phase}** - {t.title}: {t.description} *(Due: {t.dueDate or 'Flexible'})*"
            )
        lines.append("")

        lines.append("## 🕒 Day-of Schedule (Run of Show)")
        lines.append("| Time | Activity | Location | Coordinator | Notes |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for s in plan.dayOfSchedule:
            lines.append(
                f"| {s.time} | {s.activity} | {s.location or '-'} | {s.coordinator or '-'} | {s.notes or '-'} |"
            )
        lines.append("")

        lines.append("## 📋 Vendor Checklist & CRM")
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

        return {"markdown": "\n".join(lines)}
    except Exception as e:
        logger.exception(f"Export markdown error: {e}")
        raise HTTPException(status_code=500, detail="Failed to export markdown.")
