from __future__ import annotations

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    api_host: str = "0.0.0.0"  # noqa: S104 - container bind
    api_port: int = 8000
    agent_gateway_url: AnyHttpUrl = AnyHttpUrl("http://localhost:8100")
    agent_gateway_timeout_seconds: float = Field(default=30.0, gt=0)
    cors_allow_origins: str = "http://localhost:3000"
    llm_provider: str = "echo"

    @property
    def cors_origins(self) -> list[str]:
        return [part.strip() for part in self.cors_allow_origins.split(",") if part.strip()]
