from __future__ import annotations

from typing import Any
from uuid import uuid4

import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

from agent_gateway.settings import GatewaySettings
from app_llm import build_llm_client
from app_observability import reset_correlation_id, set_correlation_id

settings = GatewaySettings()
llm = build_llm_client(settings)
app = FastAPI(title="Architected AI Starter Agent Gateway", version="0.1.0")


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
    correlation_id = request.headers.get("x-request-id") or str(uuid4())
    token = set_correlation_id(correlation_id)
    try:
        response = await call_next(request)
        response.headers["x-request-id"] = correlation_id
        return response
    finally:
        reset_correlation_id(token)


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=10_000)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> dict[str, Any]:
    healthy = await llm.health()
    return {"status": "ok" if healthy else "degraded", "llm_provider": llm.provider}


@app.post("/api/v1/generate")
async def generate(request: GenerateRequest) -> dict[str, object]:
    text = await llm.generate(request.prompt)
    return {"answer": text, "provider": llm.provider, "verified": False}


def run() -> None:
    uvicorn.run(app, host=settings.agent_gateway_host, port=settings.agent_gateway_port)
