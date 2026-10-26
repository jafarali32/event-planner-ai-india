"""
CelebrateAI - Comprehensive Test Suite
Validates API endpoints, security headers, input validation, edge cases, and AI generation.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import (
    GeneratePlanRequest, ChatRequest, EventPlan, ColorSwatch, BudgetItem
)
from app.ai_service import (
    generate_event_plan, ask_event_assistant,
    _synthesize_wedding, _synthesize_birthday, _synthesize_community,
    _generate_heuristic_chat_reply
)
from app.sample_data import SAMPLE_EVENTS

client = TestClient(app)

# -------------------------------------------------------------
# 1. System & Security Header Tests
# -------------------------------------------------------------
def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "engine" in data

def test_security_headers():
    res = client.get("/api/health")
    assert res.headers.get("x-content-type-options") == "nosniff"
    assert res.headers.get("x-frame-options") == "SAMEORIGIN"
    assert res.headers.get("x-xss-protection") == "1; mode=block"
    assert res.headers.get("referrer-policy") == "strict-origin-when-cross-origin"
    assert "geolocation=()" in res.headers.get("permissions-policy", "")

def test_static_index_serving():
    res = client.get("/")
    assert res.status_code == 200
    assert "CelebrateAI" in res.text
    assert "skip to main content" in res.text.lower()

# -------------------------------------------------------------
# 2. Sample Blueprints & Caching Tests
# -------------------------------------------------------------
@pytest.mark.parametrize("ev_type", ["wedding", "birthday", "community"])
def test_sample_events_retrieval(ev_type):
    res = client.get(f"/api/samples/{ev_type}")
    assert res.status_code == 200
    data = res.json()
    assert data["eventType"] == ev_type
    assert len(data["ideas"]["colorPalette"]) >= 3
    assert len(data["budgetBreakdown"]) >= 5
    assert len(data["timeline"]) >= 3
    assert len(data["dayOfSchedule"]) >= 5
    assert len(data["vendorChecklist"]) >= 2

def test_sample_event_invalid_type_404():
    res = client.get("/api/samples/nonexistent_type")
    assert res.status_code == 404
    assert "not found" in res.json()["detail"].lower()

# -------------------------------------------------------------
# 3. Validation & Boundary Condition Tests
# -------------------------------------------------------------
def test_generate_plan_negative_budget_rejected():
    res = client.post("/api/generate", json={
        "eventType": "wedding",
        "title": "Invalid Budget Wedding",
        "guestCount": 50,
        "totalBudget": -500.0,
        "currency": "USD"
    })
    assert res.status_code == 422

def test_generate_plan_zero_guests_rejected():
    res = client.post("/api/generate", json={
        "eventType": "wedding",
        "title": "Zero Guests Wedding",
        "guestCount": 0,
        "totalBudget": 5000.0,
        "currency": "USD"
    })
    assert res.status_code == 422

def test_generate_plan_invalid_currency_rejected():
    res = client.post("/api/generate", json={
        "eventType": "birthday",
        "title": "Invalid Currency Party",
        "guestCount": 20,
        "totalBudget": 2000.0,
        "currency": "TOOLONG"
    })
    assert res.status_code == 422

def test_string_sanitization_xss_protection():
    req = GeneratePlanRequest(
        eventType="wedding",
        title="<script>alert('xss')</script> Wedding",
        guestCount=70,
        totalBudget=15000.0,
        currency="USD"
    )
    assert "<script>" not in req.title
    assert "&lt;script&gt;" in req.title

# -------------------------------------------------------------
# 4. AI Synthesis Unit Tests
# -------------------------------------------------------------
def test_synthesize_wedding():
    req = GeneratePlanRequest(
        eventType="wedding",
        title="Amalfi Dream",
        guestCount=120,
        totalBudget=45000.0,
        currency="USD"
    )
    plan = generate_event_plan(req)
    assert plan.eventType == "wedding"
    assert plan.guestCount == 120
    assert plan.totalBudget == 45000.0
    assert any(b.category.startswith("Venue") for b in plan.budgetBreakdown)
    assert len(plan.timeline) >= 5

def test_synthesize_birthday():
    req = GeneratePlanRequest(
        eventType="birthday",
        title="Alex 30th Birthday",
        guestCount=40,
        totalBudget=5000.0,
        currency="USD"
    )
    plan = generate_event_plan(req)
    assert plan.eventType == "birthday"
    assert plan.guestCount == 40
    assert len(plan.ideas.signatureFoodAndDrinks) > 0

def test_synthesize_community():
    req = GeneratePlanRequest(
        eventType="community",
        title="Oakwood Charity Gala",
        guestCount=400,
        totalBudget=16000.0,
        currency="USD"
    )
    plan = generate_event_plan(req)
    assert plan.eventType == "community"
    assert plan.guestCount == 400
    assert any("Permits" in b.category for b in plan.budgetBreakdown)

# -------------------------------------------------------------
# 5. Chat Assistant Tests
# -------------------------------------------------------------
def test_chat_budget_advice():
    res = client.post("/api/chat", json={
        "message": "How can I cut my catering budget by 15%?",
        "eventContext": SAMPLE_EVENTS["wedding"],
        "chatHistory": []
    })
    assert res.status_code == 200
    reply = res.json()["reply"]
    assert "Budget Advice" in reply or "50/30/20" in reply

def test_chat_timeline_advice():
    res = client.post("/api/chat", json={
        "message": "How should I structure the day-of schedule and avoid timeline delays?",
        "eventContext": SAMPLE_EVENTS["wedding"],
        "chatHistory": []
    })
    assert res.status_code == 200
    reply = res.json()["reply"]
    assert "Timeline" in reply or "Run-of-Show" in reply

def test_chat_vendor_advice():
    res = client.post("/api/chat", json={
        "message": "What questions should I ask my wedding caterer and photographer?",
        "eventContext": SAMPLE_EVENTS["wedding"],
        "chatHistory": []
    })
    assert res.status_code == 200
    reply = res.json()["reply"]
    assert "Vendor" in reply or "Caterer" in reply

def test_chat_empty_context():
    res = client.post("/api/chat", json={
        "message": "Hello! What can you help me with?",
        "eventContext": None,
        "chatHistory": []
    })
    assert res.status_code == 200
    reply = res.json()["reply"]
    assert len(reply) > 20

# -------------------------------------------------------------
# 6. Export Markdown Endpoint Tests
# -------------------------------------------------------------
def test_export_markdown():
    res = client.post("/api/export/markdown", json=SAMPLE_EVENTS["wedding"])
    assert res.status_code == 200
    md = res.json()["markdown"]
    assert "# Elena & Lucas" in md
    assert "Budget Breakdown" in md
    assert "Milestone Timeline" in md
    assert "Day-of Schedule" in md
    assert "Vendor Checklist" in md
