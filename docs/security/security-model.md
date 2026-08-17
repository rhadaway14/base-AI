# Security Model

This is a starter threat model. Replace generic statements with project-specific assets, actors, trust boundaries, and controls.

## Assets

- user identity and authorization context;
- source/application data;
- model prompts and tool inputs;
- model/provider credentials;
- database credentials;
- generated outputs and provenance;
- audit/operational logs.

## Trust boundaries

At minimum review browser → API, API → internal services, service → database, service → model provider, CI → deployment platform, and operator → production configuration.

## Baseline invariants

1. Secrets are configuration, never committed source.
2. Development-only or deterministic AI providers are refused in production.
3. Provider SDK types do not leak into domain/public contracts.
4. Sensitive log fields are redacted before rendering.
5. Authorization must be enforced in code/data access—not delegated to model instructions.
6. Retrieved or user-provided content is data, not trusted instruction.
7. Health endpoints disclose minimal information; detailed dependency state belongs on protected operational surfaces where appropriate.
8. Dependency and secret scanning are blocking CI checks for severe findings.

## Project-specific threats

Add abuse cases and enforcement points here. For AI applications consider prompt injection, tool misuse, data exfiltration, excessive agency, untrusted document ingestion, cross-tenant retrieval, citation/provenance fabrication, and model/provider outage behavior.

## Exceptions

Security exceptions must be explicit, dated, scoped, and linked to a remediation or review condition. Do not hide them with blanket scanner disables.
