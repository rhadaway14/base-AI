from __future__ import annotations

from typing import Any
from uuid import uuid4

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app_api.settings import ApiSettings
from app_observability import reset_correlation_id, set_correlation_id

settings = ApiSettings()
app = FastAPI(title="Architected AI Starter API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


class AskRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=10_000)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    # Liveness is intentionally dependency-free.
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(f"{settings.agent_gateway_url}readyz")
            response.raise_for_status()
            gateway: dict[str, Any] = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=f"agent gateway not ready: {exc}") from exc
    return {"status": "ok", "agent_gateway": gateway}


@app.get("/api/v1/capabilities")
async def capabilities() -> dict[str, object]:
    return {
        "model_inference_enabled": settings.llm_provider != "echo",
        "deterministic_local_provider": settings.llm_provider == "echo",
        "streaming_enabled": False,
        "persistence_enabled": False,
        "llm_provider": settings.llm_provider,
    }


@app.post("/api/v1/ask")
async def ask(request: AskRequest) -> dict[str, object]:
    async with httpx.AsyncClient(timeout=settings.agent_gateway_timeout_seconds) as client:
        try:
            response = await client.post(
                f"{settings.agent_gateway_url}api/v1/generate",
                json={"prompt": request.prompt},
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail="AI gateway request failed") from exc
        payload: dict[str, object] = response.json()
    return payload


def run() -> None:
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
