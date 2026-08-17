from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class LlmClient(Protocol):
    @property
    def provider(self) -> str: ...

    async def generate(self, prompt: str) -> str: ...

    async def health(self) -> bool: ...

    async def close(self) -> None: ...
