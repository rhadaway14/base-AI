import pytest
from agent_gateway.settings import GatewaySettings
from app_llm import LlmClient, build_llm_client


@pytest.mark.asyncio
async def test_echo_provider_satisfies_protocol_and_is_deterministic() -> None:
    client = build_llm_client(GatewaySettings(_env_file=None))
    assert isinstance(client, LlmClient)
    assert await client.health() is True
    assert await client.generate("hello") == "[local echo provider] hello"
