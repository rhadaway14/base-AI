# Reference Project → Reusable Template

This file records what was deliberately carried forward from the reference `legal_AI` repository and what was deliberately left behind.

## Retained as reusable structure

| Reference pattern | Template form | Why it stays |
| --- | --- | --- |
| `apps/` vs `packages/` | Same monorepo split | Keeps deployables separate from reusable application code. |
| `uv` workspace | Root Python workspace | One dependency graph and one developer entry point. |
| Typed `AgentEvent` seam | Minimal `RunEvent` contract | Establishes application-owned cross-service contracts before orchestration grows. |
| Bedrock abstraction + echo adapter | Provider-neutral `LlmClient` + deterministic echo | Local/CI operation does not require cloud access; provider SDKs stay replaceable. |
| Capability endpoint | Starter `/api/v1/capabilities` | UI/API behavior is based on what the running system actually supports. |
| `/healthz` vs `/readyz` | Same semantics | Separates process liveness from dependency readiness. |
| Architecture/security invariants in pytest | `tests/architecture` + unit policy tests | Important claims become executable constraints. |
| Architecture + ADR + operations + security docs | Same document classes | Project knowledge remains versioned with code. |
| Multi-layer tests | unit / integration / end-to-end / architecture | Preserves fast feedback and real-stack acceptance. |
| GitHub CI + separate security workflow | Generic equivalents | Quality and security are blocking automation, not manual cleanup. |
| Docker Compose walking skeleton | Couchbase + gateway + API + web | A clean checkout can exercise production-shaped boundaries locally. |
| Terraform environments/modules | Generic network baseline | Starts infrastructure as code without copying project-specific ECS resources. |
| Prompt source control | `prompts/` | Model behavior changes remain reviewable. |
| Synthetic test/demo corpus | `data/sample/` convention | Avoids using real customer data as development fixtures. |
| Detailed operations findings | Runbook/local-dev docs | Hard-won operational knowledge has a durable home. |

## Deliberately generalized or omitted

- **Legal matter concepts, collections, authorization rules, and synthetic case data** are domain-specific and are not copied.
- **The eight-agent legal investigation graph** is not a generic requirement. The starter keeps the provider/orchestration seam but adds agents only when a product need justifies them.
- **Bedrock is not stubbed to look implemented.** The only working provider in the starter is deterministic echo. A real Bedrock adapter must be implemented and tested before `LLM_PROVIDER=bedrock` can run.
- **Couchbase schema/index definitions are not invented.** The package boundary and local service exist, but the SDK/schema/repositories are added with the first real persistence contract.
- **AWS re:Invent demo infrastructure, Capella-specific resources, ethical-wall controls, retrieval indexes, and benchmark ladders** belong to the reference product, not every future project.
- **ECS vs Kubernetes is not pre-decided.** Terraform is provided; Kubernetes is an explicit optional path that requires an ADR.

## Template rule of thumb

A reusable template should carry **constraints that improve every project** and **seams that are expensive to retrofit**, but it should not carry features merely because one successful project needed them.
