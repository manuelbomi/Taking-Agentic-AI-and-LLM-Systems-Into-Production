# Observability for Agentic and LLM Systems

## Observe a trace, not a blob

An agent request is a distributed trace:

```text
HTTP request
  -> auth
  -> context retrieval
  -> model call #1
  -> tool call
  -> model call #2
  -> persistence
  -> response
```

Attach one correlation/trace ID across services.

## Metrics

### API/service
- request rate;
- p50, p95, p99 end-to-end latency;
- error/timeout/rate-limit counts;
- CPU, memory, queue depth, connection pool saturation.

### Model
- model/provider name and version;
- time to first token (TTFT) for streaming;
- inter-token latency (ITL);
- input/output/total tokens;
- tokens per second;
- requests per second;
- provider errors and retry count;
- estimated cost.

### Agent
- steps per task;
- model calls per task;
- tool calls per task;
- budget terminations;
- human escalations;
- task completion/success rate.

### Tool
- call count by tool/version;
- p50/p95/p99 latency;
- timeout/error rate;
- policy denial count;
- downstream dependency status.

### Retrieval/context
- retrieval latency;
- number of candidates/chunks;
- context tokens;
- reranker latency;
- groundedness/citation quality when evaluated.

## Logging

Prefer structured logs with fields such as:

```json
{
  "event": "tool_call_completed",
  "request_id": "...",
  "tenant_id": "...",
  "tool": "inventory.lookup",
  "duration_ms": 84,
  "status": "success"
}
```

Do not blindly log full prompts and tool payloads. Define redaction rules.

## Tracing

OpenTelemetry-style traces are useful for correlating API, retrieval, model and tool spans. Capture safe metadata; avoid turning telemetry into an uncontrolled sensitive-data store.

## Alerting

Alert on user-impacting symptoms and SLOs rather than every transient exception. Useful alerts include sustained p95 latency regression, provider failure rate, queue backlog, policy-denial spikes and abnormal cost/token growth.

## Evaluation as observability

For LLM systems, correctness is partly behavioral. Periodically run a known evaluation set and track quality by release (model + prompt + retrieval + tool schema + policy), not merely by code commit.
