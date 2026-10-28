"""
CelebrateAI - Comprehensive Test Suite
Validates API endpoints, security headers, input validation, edge cases,
Gemini integration, heuristic synthesizers, and export capabilities.
"""

from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient

from app.ai_service import (
    ask_event_assistant,
    build_gemini_client,
    extract_json_block,
    generate_event_plan,
    synthesize_smart_event_plan,
)
from app.main import app
from app.models import ChatMessage, ChatRequest, GeneratePlanRequest
from app.sample_data import SAMPLE_EVENTS
import run

client = TestClient(app)


# -------------------------------------------------------------
# 1. System & Security Header Tests
# -------------------------------------------------------------
def test_health_endpoint():
    """Validates health check status and engine reporting."""
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "engine" in data


def test_security_headers():
    """Validates standard and advanced security headers (CSP, HSTS)."""
    res = client.get("/api/health")
    headers = res.headers
    assert headers.get("x-content-type-options") == "nosniff"
    assert headers.get("x-frame-options") == "SAMEORIGIN"
    assert headers.get("x-xss-protection") == "1; mode=block"
    assert headers.get("referrer-policy") == "strict-origin-when-cross-origin"
    assert "geolocation=()" in headers.get("permissions-policy", "")
    assert "Content-Security-Policy" in headers
    assert "Strict-Transport-Security" in headers


def test_static_index_serving():
    """Validates root route serving the SPA with accessibility hooks."""
    res = client.get("/")
    assert res.status_code == 200
    assert "CelebrateAI" in res.text
    assert "skip to main content" in res.text.lower()


def test_serve_index_missing_file():
    """Validates graceful fallback when index.html is missing."""
    with patch("os.path.exists", return_value=False):
        res = client.get("/")
        assert res.status_code == 200
        assert "CelebrateAI is initializing" in res.text


def test_serve_index_read_error():
    """Validates 500 error when index.html read raises an IO error."""
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", side_effect=IOError("Disk error")):
            res = client.get("/")
            assert res.status_code == 500


# -------------------------------------------------------------
# 2. Sample Blueprints & Caching Tests
# -------------------------------------------------------------
@pytest.mark.parametrize("ev_type", ["wedding", "birthday", "community"])
def test_sample_events_retrieval(ev_type):
    """Verifies retrieval of curated Indian event blueprints."""
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
    """Validates 404 response on unknown event type."""
    res = client.get("/api/samples/nonexistent_type")
    assert res.status_code == 404
    assert "not found" in res.json()["detail"].lower()


# -------------------------------------------------------------
# 3. Validation & Boundary Condition Tests
# -------------------------------------------------------------
def test_generate_plan_negative_budget_rejected():
    """Ensures negative budgets are rejected with 422 Unprocessable Entity."""
    res = client.post("/api/generate", json={
        "eventType": "wedding",
        "title": "Invalid Budget Wedding",
        "guestCount": 50,
        "totalBudget": -500.0,
        "currency": "INR"
    })
    assert res.status_code == 422


def test_generate_plan_zero_guests_rejected():
    """Ensures 0 guests are rejected with 422."""
    res = client.post("/api/generate", json={
        "eventType": "wedding",
        "title": "Zero Guests Wedding",
        "guestCount": 0,
        "totalBudget": 50000.0,
        "currency": "INR"
    })
    assert res.status_code == 422


def test_generate_plan_invalid_currency_rejected():
    """Ensures currencies longer than 3 characters are rejected."""
    res = client.post("/api/generate", json={
        "eventType": "birthday",
        "title": "Invalid Currency Party",
        "guestCount": 20,
        "totalBudget": 20000.0,
        "currency": "TOOLONG"
    })
    assert res.status_code == 422


def test_string_sanitization_xss_protection():
    """Verifies HTML escaping across all input fields."""
    req = GeneratePlanRequest(
        eventType="wedding",
        title="<script>alert('xss')</script> Wedding",
        guestCount=70,
        totalBudget=150000.0,
        currency="INR",
        location="<b>Delhi</b>",
        vibeAndStyle="<img src=x onerror=alert(1)>",
        specialRequests=None
    )
    assert "<script>" not in req.title
    assert "&lt;script&gt;" in req.title
    assert "<b>" not in req.location
    assert "&lt;b&gt;" in req.location


def test_chat_message_sanitization():
    """Verifies XSS prevention in chat input messages."""
    req = ChatRequest(
        message="<script>stealCookies()</script> Budget help",
        eventContext=None,
        chatHistory=[]
    )
    assert "<script>" not in req.message
    assert "&lt;script&gt;" in req.message


# -------------------------------------------------------------
# 4. HTTP /api/generate Endpoint Tests
# -------------------------------------------------------------
@pytest.mark.parametrize("ev_type", ["wedding", "birthday", "community", "other"])
def test_api_generate_endpoint_success(ev_type):
    """Validates HTTP POST /api/generate for various event categories."""
    payload = {
        "eventType": ev_type,
        "title": f"Custom {ev_type.title()} Event",
        "guestCount": 150,
        "totalBudget": 500000.0,
        "currency": "INR",
        "location": "Bengaluru",
        "vibeAndStyle": "Elegant and professional"
    }
    res = client.post("/api/generate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["eventType"] == ev_type
    assert data["totalBudget"] == 500000.0
    assert data["guestCount"] == 150
    assert len(data["budgetBreakdown"]) > 0
    assert len(data["vendorChecklist"]) > 0


def test_api_generate_value_error_handling():
    """Validates 422 response when synthesis raises ValueError."""
    with patch("app.main.generate_event_plan", side_effect=ValueError("Invalid parameters")):
        res = client.post("/api/generate", json={
            "eventType": "wedding",
            "title": "Fail Wedding",
            "guestCount": 50,
            "totalBudget": 50000.0,
            "currency": "INR"
        })
        assert res.status_code == 422
        assert "Invalid parameters" in res.json()["detail"]


def test_api_generate_unexpected_error_handling():
    """Validates 500 response when unexpected server exception occurs."""
    with patch("app.main.generate_event_plan", side_effect=RuntimeError("Fatal error")):
        res = client.post("/api/generate", json={
            "eventType": "wedding",
            "title": "Crash Wedding",
            "guestCount": 50,
            "totalBudget": 50000.0,
            "currency": "INR"
        })
        assert res.status_code == 500
        assert "generation" in res.json()["detail"].lower()


# -------------------------------------------------------------
# 5. AI Service & Helper Functions
# -------------------------------------------------------------
def test_extract_json_block_markdown():
    """Validates extracting JSON inside markdown fences."""
    text = "Here is the plan:\n```json\n{\"id\": \"123\", \"title\": \"Plan\"}\n```\nEnjoy!"
    result = extract_json_block(text)
    assert result == {"id": "123", "title": "Plan"}


def test_extract_json_block_raw():
    """Validates extracting clean raw JSON string."""
    text = "  {\"status\": \"ok\", \"count\": 42}  "
    result = extract_json_block(text)
    assert result == {"status": "ok", "count": 42}


def test_extract_json_block_embedded():
    """Validates extracting JSON embedded inside unstructured text."""
    text = "Introductory text {\"embedded\": true} trailing text"
    result = extract_json_block(text)
    assert result == {"embedded": True}


def test_extract_json_block_invalid():
    """Validates returning None for malformed or non-JSON input."""
    assert extract_json_block("Plain text without any braces") is None
    assert extract_json_block("```json\n{unquoted_key: val}\n```") is None


def test_build_gemini_client():
    """Validates client initialization with and without keys."""
    assert build_gemini_client(None) is None

    mock_client = MagicMock()
    with patch("google.genai.Client", return_value=mock_client):
        client_inst = build_gemini_client("test-api-key")
        assert client_inst == mock_client

    with patch("google.genai.Client", side_effect=Exception("SDK failure")):
        assert build_gemini_client("test-api-key") is None


def test_gemini_generation_mock_success():
    """Validates successful end-to-end plan generation via Gemini LLM response."""
    import copy
    import json
    sample_plan = copy.deepcopy(SAMPLE_EVENTS["wedding"])
    sample_plan["title"] = "Royal Rajasthan Wedding"
    mock_response = MagicMock()
    mock_response.text = f"```json\n{json.dumps(sample_plan)}\n```"

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response

    req = GeneratePlanRequest(
        eventType="wedding",
        title="Royal Rajasthan Wedding",
        guestCount=200,
        totalBudget=2500000.0,
        currency="INR",
        apiKey="mock-gemini-key"
    )

    with patch("app.ai_service.build_gemini_client", return_value=mock_client):
        plan = generate_event_plan(req)
        assert plan.eventType == "wedding"
        assert plan.title == "Royal Rajasthan Wedding"


def test_gemini_generation_fallback_on_error():
    """Validates fallback to heuristic synthesis when Gemini API encounters errors."""
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = RuntimeError("Quota exhausted")

    req = GeneratePlanRequest(
        eventType="wedding",
        title="Jaipur Heritage Wedding",
        guestCount=200,
        totalBudget=2000000.0,
        currency="INR",
        apiKey="mock-key-triggering-fallback"
    )

    with patch("app.ai_service.build_gemini_client", return_value=mock_client):
        plan = generate_event_plan(req)
        assert plan.eventType == "wedding"
        assert plan.totalBudget == 2000000.0


def test_gemini_chat_error_fallback():
    """Validates chat fallback to heuristic generator when Gemini API errors."""
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = RuntimeError("Model timeout")

    req = ChatRequest(
        message="Help with catering budget",
        eventContext=SAMPLE_EVENTS["wedding"],
        chatHistory=[],
        apiKey="mock-key"
    )

    with patch("app.ai_service.build_gemini_client", return_value=mock_client):
        reply = ask_event_assistant(req)
        assert "Budget Advice" in reply


# -------------------------------------------------------------
# 6. Chat Assistant Tests & Heuristics
# -------------------------------------------------------------
def test_chat_gemini_mock_success():
    """Validates chat response when Gemini SDK succeeds."""
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.text = "Here is expert guidance tailored for your wedding."
    mock_client.models.generate_content.return_value = mock_resp

    req = ChatRequest(
        message="What is the best way to handle catering?",
        eventContext=SAMPLE_EVENTS["wedding"],
        chatHistory=[ChatMessage(role="user", content="Hello")],
        apiKey="mock-key"
    )

    with patch("app.ai_service.build_gemini_client", return_value=mock_client):
        reply = ask_event_assistant(req)
        assert "expert guidance" in reply


def test_chat_heuristic_budget_advice():
    """Validates offline heuristic response for budget queries."""
    res = client.post("/api/chat", json={
        "message": "How can I cut my catering cost and save budget?",
        "eventContext": SAMPLE_EVENTS["wedding"],
        "chatHistory": []
    })
    assert res.status_code == 200
    assert "Budget Advice" in res.json()["reply"]


def test_chat_heuristic_timeline_advice():
    """Validates offline heuristic response for timeline queries."""
    res = client.post("/api/chat", json={
        "message": "How should I structure the schedule to avoid delay and curfew?",
        "eventContext": SAMPLE_EVENTS["wedding"],
        "chatHistory": []
    })
    assert res.status_code == 200
    assert "Timeline & Schedule" in res.json()["reply"]


def test_chat_heuristic_vendor_advice():
    """Validates offline heuristic response for vendor queries."""
    res = client.post("/api/chat", json={
        "message": "What questions should I ask my caterer and photographer?",
        "eventContext": SAMPLE_EVENTS["wedding"],
        "chatHistory": []
    })
    assert res.status_code == 200
    assert "Vendor Management" in res.json()["reply"]


def test_chat_heuristic_idea_advice():
    """Validates offline heuristic response for creative ideas queries."""
    res = client.post("/api/chat", json={
        "message": "Suggest creative theme decor and chaat ideas.",
        "eventContext": SAMPLE_EVENTS["wedding"],
        "chatHistory": []
    })
    assert res.status_code == 200
    assert "Creative Concepts" in res.json()["reply"]


def test_chat_heuristic_general_advice():
    """Validates offline heuristic fallback for general queries."""
    res = client.post("/api/chat", json={
        "message": "Greetings, what are you able to help with?",
        "eventContext": None,
        "chatHistory": []
    })
    assert res.status_code == 200
    assert "EventGenie AI at your service" in res.json()["reply"]


def test_chat_endpoint_exception():
    """Validates 500 error when chat assistant raises an unhandled exception."""
    with patch("app.main.ask_event_assistant", side_effect=Exception("Server chat failure")):
        res = client.post("/api/chat", json={
            "message": "Hello",
            "eventContext": None,
            "chatHistory": []
        })
        assert res.status_code == 500


# -------------------------------------------------------------
# 7. Markdown Export Tests
# -------------------------------------------------------------
def test_export_markdown_success():
    """Validates exporting full markdown report."""
    res = client.post("/api/export/markdown", json=SAMPLE_EVENTS["wedding"])
    assert res.status_code == 200
    md = res.json()["markdown"]
    assert "Aarav & Ananya" in md
    assert "Budget Breakdown" in md
    assert "Milestone Timeline" in md
    assert "Day-of Schedule" in md
    assert "Vendor Checklist" in md


def test_export_markdown_failure():
    """Validates 500 error on markdown conversion exception."""
    import asyncio
    from app.main import export_plan_markdown
    from fastapi import HTTPException
    mock_plan = MagicMock()
    mock_plan.title = "Mock"
    mock_plan.ideas.colorPalette = None
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(export_plan_markdown(mock_plan))
    assert exc_info.value.status_code == 500
    assert "Failed to export markdown" in exc_info.value.detail


# -------------------------------------------------------------
# 8. Indian Edition Blueprints & Port Discovery Tests
# -------------------------------------------------------------
def test_synthesize_smart_event_plan_direct():
    """Validates direct invocation of heuristic synthesis engine."""
    req = GeneratePlanRequest(
        eventType="wedding",
        title="Direct Synthesis Wedding",
        guestCount=100,
        totalBudget=1000000.0,
        currency="INR"
    )
    plan = synthesize_smart_event_plan(req)
    assert plan.eventType == "wedding"
    assert plan.totalBudget == 1000000.0


def test_port_discovery_helpers():
    """Validates socket port checker and discovery utility in run.py."""
    assert isinstance(run.is_port_in_use(8080), bool)

    with patch.dict("os.environ", {"PORT": "9090"}):
        port = run.find_available_port(8080)
        assert port == 9090

    with patch.dict("os.environ", {"PORT": "invalid_port"}):
        port = run.find_available_port(8080)
        assert port in [8080, 8050, 8000, 8888, 5000]


def test_run_main():
    """Validates run.main server entrypoint execution with mock uvicorn."""
    with patch("uvicorn.run") as mock_uvicorn:
        run.main()
        mock_uvicorn.assert_called_once()
