# AI Engineering Instructions

These instructions apply to any AI coding assistant working in this repository.

## Read before changing code

Read, in this order:

1. `docs/product/project-brief.md`
2. `docs/architecture/system-architecture.md`
3. `docs/architecture/principles.md`
4. accepted ADRs in `docs/decisions/`
5. `docs/implementation-plan.md`
6. `docs/security/security-model.md`
7. `docs/ai/session-handoff.md`

Do not infer implemented capabilities from plans or comments. Inspect the code and tests.

## Non-negotiable working rules

- Preserve service and package boundaries unless an ADR explicitly changes them.
- Depend on protocols/interfaces at provider boundaries; do not leak vendor SDK types into domain or API contracts.
- Never hard-code credentials, account ids, model ids, cluster addresses, or environment-specific resource ids.
- Treat prompts as version-controlled source. Keep them in `prompts/` or a clearly owned package.
- A security, correctness, or architecture claim that matters should have an executable test when practical.
- Do not silently weaken or delete a failing invariant to make tests green. Fix the implementation or record a deliberate architectural change.
- Keep health (`/healthz`) dependency-free. Readiness (`/readyz`) may check required dependencies.
- Capability endpoints must report reality. A planned feature must not appear enabled.
- Add typed contracts before adding multiple implementations of the same behavior.
- Prefer one clear composition root per service. That is where concrete implementations are wired to protocols.
- Keep business/domain logic out of HTTP routers and provider adapters.
- New deployable services require a documented reason: independent scaling, security boundary, ownership boundary, or failure isolation.
- Update docs and `docs/ai/session-handoff.md` when a material decision or project state changes.

## Definition of done for a change

A change is not complete until applicable items pass:

```bash
make check
make web-check
```

For infrastructure/data-path changes, also run the relevant integration or end-to-end tests.

Before handing work to another AI assistant, update `docs/ai/session-handoff.md` with what changed, what was verified, and the next concrete step.
