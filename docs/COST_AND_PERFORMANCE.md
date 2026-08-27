# Cost and Performance Engineering

## Start with an objective

Define latency and cost objectives by task class. A conversational lookup may need low TTFT; a batch summarization job may optimize for throughput and price.

## Latency decomposition

```text
Total latency = gateway/auth
              + context retrieval
              + model queue/network
              + model generation
              + tool calls
              + subsequent model calls
              + persistence
```

Measure each span before optimizing.

## Percentiles

- **p50:** median experience.
- **p95:** slower tail experienced by roughly 1 in 20 requests.
- **p99:** severe tail experienced by roughly 1 in 100 requests.

Averages can hide operational pain.

## LLM serving metrics

- **TTFT:** request accepted to first generated token; important for perceived responsiveness.
- **ITL:** delay between generated tokens.
- **tokens/sec:** generation throughput for a stream/request.
- **requests/sec:** service throughput.

## Cost controls

- model routing by task complexity;
- input-context minimization;
- output token caps;
- caching where authorization/freshness allow;
- batch noninteractive workloads;
- rate limits and quotas;
- per-tenant budgets;
- max agent steps/tool calls;
- alerting on cost/task regression.

## Semantic caching caution

Similarity is not authorization. Cache keys must preserve tenant, identity/permission scope and relevant freshness dimensions. Do not return another user's sensitive answer because two questions embed similarly.

## Capacity testing

Load test representative workflows including model latency variance and tool dependencies. A service that handles 1,000 cheap mocked requests per second may handle far fewer real multi-step agent tasks.
