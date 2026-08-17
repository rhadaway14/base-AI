from enum import StrEnum
from typing import Protocol


class LlmProvider(StrEnum):
    ECHO = "echo"
    BEDROCK = "bedrock"


class LlmSettings(Protocol):
    llm_provider: LlmProvider
    bedrock_model_id: str
    aws_region: str
