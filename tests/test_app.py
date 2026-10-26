import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import GeneratePlanRequest, ChatRequest
from app.ai_service import generate_event_plan, ask_event_assistant
from app.sample_data import SAMPLE_EVENTS

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "engine" in data

def test_sample_events():
    for ev_type in ["wedding", "birthday", "community"]:
        res = client.get(f"/api/samples/{ev_type}")
        assert res.status_code == 200
        data = res.json()
        assert data["eventType"] == ev_type
        assert "ideas" in data
        assert "budgetBreakdown" in data
        assert "timeline" in data
        assert "dayOfSchedule" in data
        assert "vendorChecklist" in data

def test_generate_event_plan_wedding():
    req = GeneratePlanRequest(
        eventType="wedding",
        title="Chloe & David's Garden Wedding",
        guestCount=80,
        totalBudget=25000,
        currency="USD",
        vibeAndStyle="Organic boho garden with candlelight"
    )
    plan = generate_event_plan(req)
    assert plan.eventType == "wedding"
    assert plan.guestCount == 80
    assert plan.totalBudget == 25000
    assert len(plan.budgetBreakdown) > 0
    assert len(plan.timeline) > 0
    assert len(plan.dayOfSchedule) > 0
    assert len(plan.vendorChecklist) > 0
    assert len(plan.ideas.colorPalette) > 0

def test_generate_event_plan_birthday():
    req = GeneratePlanRequest(
        eventType="birthday",
        title="Marcus 40th Milestone",
        guestCount=35,
        totalBudget=4000,
        currency="USD"
    )
    plan = generate_event_plan(req)
    assert plan.eventType == "birthday"
    assert len(plan.budgetBreakdown) > 0
    assert len(plan.ideas.signatureFoodAndDrinks) > 0

def test_generate_event_plan_community():
    req = GeneratePlanRequest(
        eventType="community",
        title="Riverside 5K & Eco Festival",
        guestCount=300,
        totalBudget=12000,
        currency="USD"
    )
    plan = generate_event_plan(req)
    assert plan.eventType == "community"
    assert len(plan.budgetBreakdown) > 0

def test_api_generate_endpoint():
    res = client.post("/api/generate", json={
        "eventType": "wedding",
        "title": "Test Wedding",
        "guestCount": 50,
        "totalBudget": 15000,
        "currency": "USD"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Test Wedding"
    assert len(data["budgetBreakdown"]) > 0

def test_api_chat_endpoint():
    res = client.post("/api/chat", json={
        "message": "How can I cut 10% from my catering budget?",
        "eventContext": SAMPLE_EVENTS["wedding"],
        "chatHistory": []
    })
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data
    assert len(data["reply"]) > 20

def test_api_export_markdown_endpoint():
    res = client.post("/api/export/markdown", json=SAMPLE_EVENTS["wedding"])
    assert res.status_code == 200
    data = res.json()
    assert "markdown" in data
    assert "# Elena & Lucas" in data["markdown"]
    assert "Budget Breakdown" in data["markdown"]

def test_home_page():
    res = client.get("/")
    assert res.status_code == 200
    assert "CelebrateAI" in res.text
