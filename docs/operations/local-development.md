# Local Development

## Prerequisites

- Docker / Docker Compose
- `uv`
- Node.js 22+
- Git

## First run

```bash
make install
make env
make check
make up
```

Open:

- Web: `http://localhost:3000`
- API: `http://localhost:8000/docs`
- AI gateway: `http://localhost:8100/docs`
- Couchbase UI: `http://localhost:8091`

The starter uses `LLM_PROVIDER=echo`. No AWS credentials are needed.

## Before adding a real provider

Implement the provider behind `app_llm.LlmClient`, add provider-specific health behavior, add tests proving the SDK does not leak outside the adapter package, and document exact production configuration. Do not turn on a provider value that merely points to a stub.

## Adding Couchbase persistence

The starter intentionally does not install the Couchbase SDK until a real repository/schema exists. When persistence work begins, add the SDK to `packages/couchbase-client/pyproject.toml`, implement the connection lifecycle there, and replace the skipped integration placeholder with a real contract test against the Docker service.
