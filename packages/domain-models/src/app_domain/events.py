from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field, TypeAdapter


class BaseEvent(BaseModel):
    run_id: str
    sequence: int = Field(ge=0)
    emitted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class RunStartedEvent(BaseEvent):
    type: Literal["run.started"] = "run.started"
    objective: str


class RunCompletedEvent(BaseEvent):
    type: Literal["run.completed"] = "run.completed"
    answer: str
    verified: bool = False


RunEvent = Annotated[RunStartedEvent | RunCompletedEvent, Field(discriminator="type")]
RUN_EVENT_ADAPTER = TypeAdapter(RunEvent)
