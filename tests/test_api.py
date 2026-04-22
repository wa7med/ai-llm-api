from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


@patch("app.api.routes.call_llm")
def test_process(mock_call_llm):
    mock_call_llm.return_value = {
        "action": "schedule_meeting",
        "person": "Ali",
        "time": "2026-04-23T15:00:00"
    }

    response = client.post(
        "/process",
        json={"input": "Schedule a meeting with Ali tomorrow at 3pm"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["action"] == "schedule_meeting"
    assert data["person"] == "Ali"
    assert data["time"] == "2026-04-23T15:00:00"


@patch("app.api.routes.call_llm")
def test_process_extracted_data(mock_call_llm):
    mock_call_llm.return_value = {
        "action": "call",
        "person": "Ahmed",
        "time": "2026-04-24T00:00:00"
    }

    response = client.post(
        "/process",
        json={"input": "Call Ahmed tomorrow"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "action" in data


def test_process_empty_request():
    response = client.post("/process", json={})
    assert response.status_code == 422
