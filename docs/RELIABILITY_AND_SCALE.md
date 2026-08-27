# Reliability and Scale

## Failure is normal

Remote models, databases, search services and external APIs will fail. Design bounded failure behavior before production.

## Retry policy

Retry transient errors only. Use exponential backoff and jitter. Set a retry budget. Avoid nested retry storms where gateway, service and SDK each retry independently.

## Circuit breakers

If a dependency is failing consistently, stop sending it full traffic temporarily. This protects both systems and reduces cascading failure.

## Timeouts

Set deadlines for each dependency and an end-to-end request deadline. Downstream timeouts should fit inside the parent deadline.

## Concurrency control

Horizontal scaling can overwhelm a provider faster. Use semaphores, queues, connection-pool limits and quotas to cap in-flight work.

## Graceful degradation

Examples:

- stale-but-acceptable cached data with a freshness label;
- read-only mode when a write dependency is unavailable;
- fallback to an approved alternate model;
- human handoff;
- explicit "temporarily unavailable" rather than fabricated completion.

## State and recovery

Long-running workflows should checkpoint state so another worker can resume. Define exactly-once vs at-least-once behavior for side effects.

## Scaling

Prefer stateless API/worker replicas. Scale based on meaningful pressure signals such as concurrency, queue depth and latency, not CPU alone when the service is mostly waiting on network/model calls.

## Multi-region

Multi-region designs add latency, replication and consistency concerns. Use them when availability, locality or regulatory requirements justify the complexity.
