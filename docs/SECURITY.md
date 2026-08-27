# Security and Tool Safety

## Threat model first

Agent systems inherit ordinary application threats and add model-specific ones: prompt injection, malicious retrieved content, unsafe tool selection, cross-tenant context leakage and over-trusting generated arguments.

## Authentication and authorization

Use enterprise OIDC/OAuth/JWT patterns. Validate tokens in deterministic code. Derive trusted identity and tenant from validated claims, not request fields.

Apply authorization at multiple boundaries:

```text
request -> data retrieval -> context inclusion -> tool exposure -> tool execution -> result disclosure
```

## Tool least privilege

Expose only the tools required for the task and principal. Do not give the model a universal admin credential.

Classify tools:

- read-only;
- reversible write;
- irreversible/consequential write;
- privileged administration.

Higher-risk classes should require stronger policy and often human approval.

## Side effects and idempotency

A retry of `get_weather()` is harmless. A retry of `create_payment()` may create two payments. Write tools should use idempotency keys, transactional guards or workflow state to make retries safe.

## Prompt injection

Treat user content and retrieved documents as untrusted data. Instructions found inside a document are not automatically system policy.

Controls include:

- isolate system/developer policy from retrieved data;
- restrict tool capabilities;
- validate arguments against schema and business rules;
- avoid secrets in prompts;
- require approval for consequential actions;
- log policy decisions;
- red-team retrieval and tool paths.

## Secrets

Do not store provider keys, database credentials or JWT secrets in source control. Use managed secrets and workload identity where possible. Rotate credentials and scope them narrowly.

## Data privacy

Define what may be logged. Raw prompts/tool outputs can contain sensitive data. Use redaction/tokenization, encryption at rest/in transit, retention policies, access logging and deletion processes appropriate to the domain.

## Network security

Restrict egress from agent/tool workloads to approved destinations. Network segmentation reduces the blast radius of a compromised tool or prompt-injection chain.

## Human-in-the-loop

Human approval is not required for every tool call. Use it where consequences, ambiguity or policy justify it—for example payments, account closure, high-impact eligibility decisions or critical infrastructure commands.
