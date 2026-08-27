# Context Engineering for Production Agents

Context engineering is the disciplined construction of the model's working information environment.

## Prompt engineering vs context engineering

- **Prompt engineering:** how instructions/questions are expressed.
- **Context engineering:** what instructions, evidence, state, memory, tools and permissions the model receives for a particular task step.

## Context sources

A mature context builder may combine:

1. system policy and task instructions;
2. authenticated identity, tenant and role;
3. authorization scope;
4. current request and workflow goal;
5. selected recent conversation turns;
6. long-term memory when product policy permits it;
7. RAG documents;
8. structured database records;
9. ontology/knowledge-graph relationships;
10. tool definitions permitted for this principal;
11. previous tool outputs and workflow state;
12. safety/policy constraints;
13. freshness timestamps and provenance.

## Minimum sufficient context

More context is not automatically better. Excess context increases token cost and latency and can dilute important evidence.

A common pipeline:

```text
query/goal
 -> candidate retrieval
 -> tenant + authorization filter
 -> freshness/quality filter
 -> reranking
 -> deduplication
 -> compression/summarization
 -> token budget allocation
 -> assembly with provenance
 -> model
```

## Authorization belongs before context exposure

Do not retrieve sensitive data, pass it to the model, then ask the model not to mention it. Filter deterministically before the content enters the model context.

## Memory is a product decision

Separate:

- **turn state:** current tool/model exchange;
- **session memory:** context for the active conversation;
- **durable memory:** facts intentionally retained across sessions;
- **enterprise knowledge:** authoritative source systems, not "memory" invented by the model.

Retention, deletion, consent and tenant isolation must apply to memory just as they do to other user data.

## Ontology and semantic context

A semantic/ontology layer can add relationships that plain chunk retrieval misses. For example:

```text
Machine M102 -> belongs_to -> Line 7
Machine M102 -> processing -> Batch B921
Batch B921   -> governed_by -> QualitySpec QS72
Batch B921   -> fulfills -> CustomerOrder O828
```

A question about defects on Line 7 can then retrieve telemetry, the active batch, quality specification and related maintenance events as connected context rather than unrelated text chunks.

## Context quality telemetry

Measure retrieval latency and, where possible, relevance/groundedness. Keep provenance so a response or action can be traced back to evidence.
