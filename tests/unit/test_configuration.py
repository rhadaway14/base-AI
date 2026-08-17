import pytest
from agent_gateway.settings import GatewaySettings
from app_llm.settings import LlmProvider
from pydantic import ValidationError


def test_echo_is_the_offline_default() -> None:
    assert GatewaySettings(_env_file=None).llm_provider is LlmProvider.ECHO


def test_echo_is_refused_in_production() -> None:
    with pytest.raises(ValidationError, match="echo is refused"):
        GatewaySettings(app_env="production", llm_provider="echo", _env_file=None)


def test_bedrock_requires_model_configuration() -> None:
    with pytest.raises(ValidationError, match="BEDROCK_MODEL_ID"):
        GatewaySettings(llm_provider="bedrock", bedrock_model_id="", _env_file=None)
