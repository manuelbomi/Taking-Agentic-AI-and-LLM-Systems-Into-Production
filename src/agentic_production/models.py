from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=128)
    session_id: str = Field(min_length=1, max_length=128)
    query: str = Field(min_length=1, max_length=8_000)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    request_id: str
    text: str
    model: str
    tool_calls: list[str] = Field(default_factory=list)
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    latency_ms: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ErrorResponse(BaseModel):
    request_id: str
    code: str
    message: str
