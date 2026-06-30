"""
MemoryRouter — facade over short-term, long-term, and semantic memory.
Adds scoring + pruning logic and provides a single API to the Brain.
"""
from __future__ import annotations

from backend.config.settings import Settings
from backend.memory.long_term import LongTermMemory, MemoryHit
from backend.memory.short_term import ShortTermMemory
from backend.memory.vector_store import VectorStore
from backend.utils.logger import get_logger

log = get_logger("memory.router")


class MemoryRouter:
    def __init__(self, vector_store: VectorStore, settings: Settings) -> None:
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(vector_store)
        self.settings = settings

    async def connect(self) -> None:
        await self.short_term.connect()
        await self.long_term.connect()

    async def close(self) -> None:
        await self.short_term.close()
        await self.long_term.close()

    async def recall(self, user_id: str, query: str, k: int = 8) -> list[MemoryHit]:
        return await self.long_term.search(user_id=user_id, query=query, k=k)

    async def write_turn(self, user_id: str, message: str, response: str, session_id: str) -> None:
        await self.short_term.append(user_id, session_id, "user", message)
        await self.short_term.append(user_id, session_id, "assistant", response)
        # Persist meaningful turns (>40 chars) into long-term memory
        if len(message) > 40 or len(response) > 80:
            blob = f"User: {message}\nLEXI: {response}"
            await self.long_term.add(user_id=user_id, text=blob, metadata={"session_id": session_id})
