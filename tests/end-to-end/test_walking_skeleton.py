import os

import httpx
import pytest

API_BASE_URL = os.getenv("E2E_API_BASE_URL", "http://localhost:8000")


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_browser_facing_api_can_reach_the_offline_ai_provider() -> None:
    async with httpx.AsyncClient(base_url=API_BASE_URL, timeout=20.0) as client:
        try:
            health = await client.get("/healthz")
        except httpx.HTTPError:
            pytest.skip("API not running; start the full stack with `make up`")
        assert health.status_code == 200
        response = await client.post("/api/v1/ask", json={"prompt": "walking skeleton"})
        assert response.status_code == 200
        body = response.json()
        assert body["provider"] == "echo"
        assert body["answer"] == "[local echo provider] walking skeleton"
        assert body["verified"] is False
