# Architecture: From Agent Script to Production System

## The architectural shift

A prototype optimizes for learning. Production optimizes for predictable operation under concurrency, failure, change, security constraints and organizational ownership.

```text
Prototype                         Production
---------                         ----------
CLI/script                        Stable service/API contract
Local process                     Replicated stateless compute
Python dict                        External state/cache/store
One implicit user                 Authenticated principal + tenant
Direct tool call                  Tool registry + policy + audit
One prompt                        Versioned context pipeline
One provider                      Model gateway/adapter + quotas
print()                           structured logs + metrics + traces
manual run                        CI/CD + staged rollout + rollback
works once                        evaluated continuously
```

## Recommended responsibility boundaries

### Entry layer
API gateway/load balancer handles TLS termination, routing, WAF controls, request size and coarse quotas.

### Application API
Validates payloads, attaches correlation IDs, translates application errors into stable client errors, and owns the public contract.

### Orchestrator
Owns the task state machine: model calls, tool calls, max steps, deadlines, cost/token budgets, fallbacks and handoffs.

### Context service
Builds task-specific context from identity, policy, memory, enterprise data, RAG and structured knowledge. It should filter before model exposure.

### Tool registry
Defines capabilities the model may request. Each tool has schema, owner, policy, side-effect classification, timeout, idempotency rules and telemetry.

### Model gateway
Centralizes model/provider selection, credentials, quotas, telemetry and optional routing/fallback policy. Keep provider-specific code behind an interface when portability or multi-model operation is important.

### State and storage
Persist only what is required by product, audit and recovery needs. Separate ephemeral caches from durable records.

## Stateless replicas

API/agent workers should generally be replaceable. Shared state belongs outside the container. This makes horizontal scaling, failover and rolling deployments much simpler.

## Agent execution budgets

A request should not be able to reason forever. Enforce maximum wall clock, steps, model calls, tool calls, tokens and/or cost. A budget breach is a normal controlled termination path, not an exceptional mystery.

## Async and backpressure

Use asynchronous I/O for concurrent remote calls. But async is not capacity control. Protect dependencies with connection pools, semaphores/concurrency caps, queues and admission control.

## Synchronous vs asynchronous workflows

Interactive tasks can stay request/response if they finish inside the product latency objective. Long-running or retry-heavy workflows should often become job-based:

```text
POST /jobs -> durable queue -> worker/orchestrator -> state/checkpoints -> callback/poll/event
```

This avoids holding client connections open and enables retries/checkpoint recovery.
