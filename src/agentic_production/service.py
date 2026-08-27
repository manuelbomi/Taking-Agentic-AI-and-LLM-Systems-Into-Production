import asyncio
import time
from uuid import uuid4
from google import genai
from google.genai import types

from .config import Settings, get_settings
from .models import AgentRequest, AgentResponse
from .observability import MODEL_CALLS, TOKENS, log_event
from .security import Principal
from .tools.registry import functions_for_role


class AgentExecutionError(RuntimeError):
    pass


class AgentService:
    """Production-shaped orchestration boundary around the model SDK."""

    def __init__(self, settings: Settings | None = None, client=None):
        self.settings = settings or get_settings()
        self.client = client or genai.Client(api_key=self.settings.gemini_api_key or None)

    async def run(self, request: AgentRequest, principal: Principal, request_id: str | None = None) -> AgentResponse:
        request_id = request_id or str(uuid4())
        started = time.perf_counter()

        # Never trust user-provided user_id as identity. In a real app, map the
        # request to the authenticated principal and enforce tenant boundaries.
        tools = functions_for_role(principal.role)

        system_instruction = (
            "You are a concise weather assistant. Use available tools when current weather is needed. "
            "Do not claim to have executed a tool that was not provided. State uncertainty clearly."
        )
        config = types.GenerateContentConfig(
            tools=tools,
            temperature=0.0,
            max_output_tokens=self.settings.max_output_tokens,
            system_instruction=system_instruction,
        )

        log_event("agent_request_started", request_id=request_id, subject=principal.subject)
        try:
            response = await asyncio.wait_for(
                self.client.aio.models.generate_content(
                    model=self.settings.model_name,
                    contents=request.query,
                    config=config,
                ),
                timeout=self.settings.request_timeout_seconds,
            )
            MODEL_CALLS.labels(self.settings.model_name, "success").inc()
        except TimeoutError as exc:
            MODEL_CALLS.labels(self.settings.model_name, "timeout").inc()
            raise AgentExecutionError("Model request timed out") from exc
        except Exception as exc:
            MODEL_CALLS.labels(self.settings.model_name, "error").inc()
            raise AgentExecutionError("Model request failed") from exc

        usage = getattr(response, "usage_metadata", None)
        input_tokens = getattr(usage, "prompt_token_count", None) if usage else None
        output_tokens = getattr(usage, "candidates_token_count", None) if usage else None
        total_tokens = getattr(usage, "total_token_count", None) if usage else None

        if input_tokens is not None:
            TOKENS.labels("input", self.settings.model_name).inc(input_tokens)
        if output_tokens is not None:
            TOKENS.labels("output", self.settings.model_name).inc(output_tokens)

        latency_ms = (time.perf_counter() - started) * 1000
        log_event(
            "agent_request_completed",
            request_id=request_id,
            latency_ms=round(latency_ms, 2),
            total_tokens=total_tokens,
        )
        return AgentResponse(
            request_id=request_id,
            text=response.text or "",
            model=self.settings.model_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            latency_ms=latency_ms,
        )
