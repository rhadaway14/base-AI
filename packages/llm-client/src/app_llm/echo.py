from __future__ import annotations


class EchoLlmClient:
    @property
    def provider(self) -> str:
        return "echo"

    async def generate(self, prompt: str) -> str:
        return f"[local echo provider] {prompt}"

    async def health(self) -> bool:
        return True

    async def close(self) -> None:
        return None
