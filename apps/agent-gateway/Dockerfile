FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
WORKDIR /app
COPY pyproject.toml ./
COPY packages/domain-models/pyproject.toml packages/domain-models/
COPY packages/llm-client/pyproject.toml packages/llm-client/
COPY packages/observability/pyproject.toml packages/observability/
COPY packages/couchbase-client/pyproject.toml packages/couchbase-client/
COPY apps/api/pyproject.toml apps/api/
COPY apps/agent-gateway/pyproject.toml apps/agent-gateway/
RUN uv sync --no-dev --no-install-workspace
COPY packages/ packages/
COPY apps/api/ apps/api/
COPY apps/agent-gateway/ apps/agent-gateway/
RUN uv sync --no-dev

FROM python:3.12-slim AS runtime
RUN groupadd --system --gid 1001 app && useradd --system --uid 1001 --gid app --home /app app
WORKDIR /app
COPY --from=builder --chown=app:app /app /app
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
USER app
EXPOSE 8100
HEALTHCHECK --interval=15s --timeout=3s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8100/healthz', timeout=2)"
CMD ["python", "-m", "agent_gateway"]
