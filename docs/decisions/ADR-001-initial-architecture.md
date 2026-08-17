# ADR-001: Initial project architecture

- **Status:** Accepted as starter; amend or supersede during project initialization
- **Date:** 2026-08-17
- **Deciders:** Project team

## Context

The project needs a reusable baseline that supports rapid AI application development without coupling domain code to a model provider or cloud SDK. It should run locally, support strict Python quality gates, provide a web/API boundary, and be able to add Couchbase-backed persistence without restructuring the repository.

## Decision

Use a monorepo with:

- Python 3.12–3.13 and a `uv` workspace;
- FastAPI for service APIs;
- a separate AI gateway when model workloads justify an independent failure/scaling boundary;
- Next.js/TypeScript for the frontend;
- Pydantic for application-owned contracts;
- provider-neutral AI interfaces with a deterministic echo adapter for CI/local work;
- Couchbase behind a dedicated package boundary;
- Docker Compose for local topology;
- Terraform as the default cloud infrastructure definition;
- architecture, security, and project invariants enforced through automated tests where practical.

## Consequences

**Positive.** New projects start with tested seams, offline development, standard commands, and a place for architectural knowledge.

**Negative.** The skeleton contains more structure than a disposable single-file prototype. Projects should remove boundaries they genuinely do not need rather than preserving ceremony.

**Risks.** The starter can become stale. CI must test the claimed runtime/toolchain range, and project initialization should review every retained dependency rather than assuming the template is automatically correct forever.

## Verification

`make check`, `make web-check`, architecture tests, and CI enforce the baseline claims.
