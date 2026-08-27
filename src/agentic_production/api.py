from uuid import uuid4
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

from .config import get_settings
from .models import AgentRequest, AgentResponse
from .observability import REQUESTS, configure_logging, latency_timer
from .rate_limit import InMemoryRateLimiter
from .security import Principal, authenticate
from .service import AgentExecutionError, AgentService

settings = get_settings()
configure_logging(settings.log_level)
app = FastAPI(title="Agentic AI Production Reference", version="0.1.0")
service = AgentService(settings=settings)
limiter = InMemoryRateLimiter(settings.default_rate_limit_per_minute)


@app.middleware("http")
async def correlation_id(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    return response


@app.get("/health/live")
async def live():
    return {"status": "ok"}


@app.get("/health/ready")
async def ready():
    # Real readiness may include required local dependencies, but avoid making
    # it dependent on a flaky remote model provider unless that is intentional.
    return {"status": "ready"}


@app.get("/metrics", include_in_schema=False)
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/v1/agent/query", response_model=AgentResponse)
async def query_agent(
    payload: AgentRequest,
    request: Request,
    principal: Principal = Depends(authenticate),
):
    if not await limiter.allow(f"{principal.tenant_id}:{principal.subject}"):
        REQUESTS.labels("rate_limited").inc()
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    try:
        with latency_timer():
            result = await service.run(payload, principal, request.state.request_id)
        REQUESTS.labels("success").inc()
        return result
    except AgentExecutionError as exc:
        REQUESTS.labels("agent_error").inc()
        return JSONResponse(
            status_code=503,
            content={
                "request_id": request.state.request_id,
                "code": "AGENT_UNAVAILABLE",
                "message": str(exc),
            },
        )
