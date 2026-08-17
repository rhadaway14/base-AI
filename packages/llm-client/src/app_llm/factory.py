from __future__ import annotations

from app_llm.echo import EchoLlmClient
from app_llm.protocol import LlmClient
from app_llm.settings import LlmProvider, LlmSettings


def build_llm_client(settings: LlmSettings) -> LlmClient:
    if settings.llm_provider is LlmProvider.ECHO:
        return EchoLlmClient()
    if settings.llm_provider is LlmProvider.BEDROCK:
        raise RuntimeError(
            "Bedrock is intentionally not stubbed. Implement a real BedrockLlmClient "
            "behind LlmClient before setting LLM_PROVIDER=bedrock."
        )
    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
