import json
import logging
import time
from contextlib import contextmanager
from prometheus_client import Counter, Histogram

REQUESTS = Counter("agent_requests_total", "Agent API requests", ["status"])
LATENCY = Histogram("agent_request_latency_seconds", "End-to-end request latency")
MODEL_CALLS = Counter("agent_model_calls_total", "Model calls", ["model", "status"])
TOOL_CALLS = Counter("agent_tool_calls_total", "Tool calls", ["tool", "status"])
TOKENS = Counter("agent_tokens_total", "Observed model tokens", ["direction", "model"])


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO), format="%(message)s")


def log_event(event: str, **fields) -> None:
    logging.getLogger("agentic-production").info(json.dumps({"event": event, **fields}, default=str))


@contextmanager
def latency_timer(histogram=LATENCY):
    started = time.perf_counter()
    try:
        yield
    finally:
        histogram.observe(time.perf_counter() - started)
