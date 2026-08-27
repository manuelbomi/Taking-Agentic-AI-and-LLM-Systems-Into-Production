# Production Readiness Checklist

Use this as a launch gate and periodic review aid.

## Architecture and ownership
- [ ] Public API contract is versioned.
- [ ] Service/tool/model ownership is documented.
- [ ] Agent execution has time/step/tool/token/cost budgets.
- [ ] Long-running workflows use durable jobs/checkpoints where appropriate.
- [ ] Failure modes and graceful degradation are documented.

## Identity and security
- [ ] AuthN uses approved enterprise identity.
- [ ] AuthZ is enforced in deterministic code.
- [ ] Tenant isolation is tested.
- [ ] Secrets are managed outside source control.
- [ ] Tool exposure follows least privilege.
- [ ] Consequential write tools have business-rule validation and idempotency.
- [ ] Prompt injection and malicious retrieval cases are tested.
- [ ] Network egress is restricted where appropriate.

## Context and data
- [ ] Context sources have ownership/provenance.
- [ ] Authorization filtering occurs before model exposure.
- [ ] Retrieval has freshness/quality controls.
- [ ] Context/token budgets are defined.
- [ ] Memory retention and deletion policies exist.
- [ ] Sensitive logging/redaction policy exists.

## Reliability
- [ ] Every remote call has a timeout.
- [ ] Retries are bounded and safe for the operation.
- [ ] Circuit breakers/concurrency limits are used where needed.
- [ ] Dependency outages have tested behavior.
- [ ] Health/readiness checks are meaningful.
- [ ] Backups and restore procedures are tested for durable state.

## Testing and evaluation
- [ ] Unit tests cover deterministic logic.
- [ ] Tool/provider contract tests exist.
- [ ] Integration tests cover major workflows.
- [ ] Behavioral evaluation dataset is versioned.
- [ ] Safety/adversarial cases are included.
- [ ] Load/capacity test has been run against realistic workflow shapes.
- [ ] Rollback criteria include quality metrics, not only HTTP errors.

## Observability and operations
- [ ] Structured logs carry correlation/trace IDs.
- [ ] Metrics cover API, model, agent, tools and retrieval.
- [ ] p50/p95/p99 latency dashboards exist.
- [ ] Token and cost telemetry exists.
- [ ] Alerts map to SLO/user impact.
- [ ] Runbooks and escalation paths exist.
- [ ] On-call ownership is defined.
- [ ] Incident review/postmortem process exists.

## Deployment
- [ ] Immutable container/artifact is built in CI.
- [ ] Dependency and image scanning is enabled.
- [ ] Staging/preproduction evaluation gates exist.
- [ ] Canary/blue-green or equivalent progressive rollout exists.
- [ ] Rollback is tested.
- [ ] Prompt/model/tool/policy versions are traceable to release.

## Responsible AI and compliance
- [ ] Intended use and prohibited use are documented.
- [ ] Human review is defined for high-impact actions.
- [ ] Audit events are retained appropriately.
- [ ] Privacy/retention/consent requirements are implemented.
- [ ] Model and application safety evaluations are documented.
- [ ] Users have an appropriate failure/escalation path.

## Cost and capacity
- [ ] Cost per successful task is measured.
- [ ] Per-user/tenant quotas are defined.
- [ ] Token/output limits are set.
- [ ] Provider quota limits are known.
- [ ] Capacity plan accounts for retries and peak concurrency.
- [ ] Cost anomaly alerts are configured.
