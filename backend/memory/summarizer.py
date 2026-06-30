"""Memory compression utilities."""
from __future__ import annotations
from backend.services.llm_provider import LLMProvider


class MemorySummarizer:
    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    async def summarize_turns(self, turns: list[dict]) -> str:
        blob = "\n".join(f"{t['role']}: {t['content']}" for t in turns)
        return await self.llm.complete(
            system="Summarize the conversation in 3-5 short bullets, focus on facts the user revealed.",
            prompt=blob,
        )
