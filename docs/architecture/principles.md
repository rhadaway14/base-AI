# Engineering Principles

These are the reusable principles carried into new projects from the reference architecture.

## 1. Start with a walking skeleton

The first milestone is not a feature list. It is the thinnest production-shaped vertical slice that proves:

- frontend can reach the API;
- API can reach the AI/provider boundary;
- the provider can run in a deterministic offline mode;
- health, readiness, configuration, logs, and tests behave as designed;
- the deployment artifact is the same kind of artifact production will use.

Domain complexity comes after the seams are proven.

## 2. Freeze contracts at expensive seams

Provider APIs, event streams, persistence abstractions, authorization context, and cross-service request models are expensive to change after multiple consumers exist. Define a typed application-owned contract first, then adapt external systems to it.

Do **not** let a model framework, database SDK, or cloud SDK become the domain model.

## 3. Application code owns guarantees

Prompts can request behavior; they cannot guarantee it. Anything that must always happen—authorization, verification, approval, redaction, policy gates, destructive-operation protection—belongs in code and should be tested.

## 4. Report capabilities truthfully

A UI, API client, or demo should never have to guess whether a feature is real. Expose capability state from the running system and derive presentation from it. Planned, degraded, disabled, and implemented are different states.

## 5. Fail closed on unsafe configuration

A dangerous configuration should fail startup rather than fail later in front of a user. Examples:

- development authentication in production;
- an AI provider selected without its required model configuration;
- TLS disabled for a production data service;
- missing signing/encryption secrets;
- a benchmark-only mode selected for production.

## 6. Keep external systems behind replaceable seams

Application code depends on `Protocol`/interfaces. Concrete adapters belong in dedicated packages. A provider change should be a composition-root change plus a new adapter, not a rewrite of routes, domain models, and tests.

## 7. Make architecture testable

Protect material claims with tests when practical:

- provider/framework imports do not cross boundaries;
- security filters are applied before data leaves storage;
- event sequence is monotonic;
- logs redact sensitive fields;
- configured capabilities match behavior;
- unsafe production modes are rejected;
- generated schemas/index definitions have one source of truth.

A test that cannot fail is not a guard.

## 8. Separate liveness from readiness

`/healthz` answers “is this process alive?” without external calls. `/readyz` answers “can this instance perform its required work?” and may probe dependencies. This prevents a dependency outage from causing restart loops while still keeping bad instances out of service.

## 9. Prefer one source of truth

If a value affects code, infrastructure, tests, and documentation, generate or derive secondary representations where possible. Duplicated schema definitions, vector dimensions, ports, capability flags, or security rules drift silently.

## 10. Preserve replayability and provenance for AI work

For substantial AI workflows, persist application-level events, tool calls, evidence references, model/provider metadata, timing, and final artifacts. Do not persist private model chain-of-thought. The goal is operational replay and auditability, not hidden reasoning capture.

## 11. Treat evaluation as product code

AI quality is not established by a handful of interactive prompts. Add frozen fixtures, expected outcomes, scoring scripts, and regression thresholds as soon as the project has behavior worth measuring.

## 12. Add services only for a reason

A new service should buy something concrete: independent scaling, security isolation, failure isolation, deployment cadence, or ownership. Otherwise keep the boundary as a package until pressure justifies a network hop.

## 13. Documentation is part of the implementation

Architecture, ADRs, security assumptions, operations, and handoff state live in Git. A material code change that makes those documents false is incomplete.
