import httpx

payload = {
    "user_id": "u-123",
    "session_id": "s-001",
    "query": "What is the weather in Tokyo? Should I bring an umbrella?",
}

response = httpx.post(
    "http://localhost:8000/v1/agent/query",
    headers={"Authorization": "Bearer dev-token"},
    json=payload,
    timeout=40,
)
response.raise_for_status()
print(response.json())
