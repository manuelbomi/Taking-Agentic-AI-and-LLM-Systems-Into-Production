from fastapi.testclient import TestClient
from agentic_production.api import app, service
from agentic_production.models import AgentResponse

client = TestClient(app)


async def fake_run(payload, principal, request_id=None):
    return AgentResponse(
        request_id=request_id or "r1",
        text="15 C and rainy; bring an umbrella.",
        model="test-model",
        latency_ms=1.0,
    )


def test_health():
    assert client.get("/health/live").status_code == 200


def test_query_requires_auth():
    response = client.post("/v1/agent/query", json={"user_id":"u","session_id":"s","query":"weather?"})
    assert response.status_code == 401


def test_query(monkeypatch):
    monkeypatch.setattr(service, "run", fake_run)
    response = client.post(
        "/v1/agent/query",
        headers={"Authorization": "Bearer dev-token"},
        json={"user_id":"u","session_id":"s","query":"weather in Tokyo?"},
    )
    assert response.status_code == 200
    assert "umbrella" in response.json()["text"]
