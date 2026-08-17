from __future__ import annotations

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app_llm.settings import LlmProvider


class GatewaySettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    agent_gateway_host: str = "0.0.0.0"  # noqa: S104 - container bind
    agent_gateway_port: int = 8100
    llm_provider: LlmProvider = LlmProvider.ECHO
    bedrock_model_id: str = ""
    aws_region: str = "us-east-1"
    max_output_characters: int = Field(default=20_000, gt=0)

    @model_validator(mode="after")
    def reject_unwired_or_unsafe_production_provider(self) -> "GatewaySettings":
        if self.app_env == "production" and self.llm_provider is LlmProvider.ECHO:
            raise ValueError("LLM_PROVIDER=echo is refused when APP_ENV=production")
        if self.llm_provider is LlmProvider.BEDROCK and not self.bedrock_model_id:
            raise ValueError("BEDROCK_MODEL_ID is required when LLM_PROVIDER=bedrock")
        return self
