"""
Long-term memory layer — persistent semantic + episodic memory backed by
SQL (facts/profiles) and a vector store (semantic recall).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import MemoryFact, UserProfile
from backend.database.session import session_scope
from backend.memory.embeddings import embed_text
from backend.memory.vector_store import VectorStore


@dataclass
class MemoryHit:
    id: str
    text: str
    score: float
    source: str = "vector"
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "text": self.text, "score": self.score,
                "source": self.source, "metadata": self.metadata or {}}


class LongTermMemory:
    def __init__(self, vector_store: VectorStore) -> None:
        self.vs = vector_store

    async def connect(self) -> None:
        await self.vs.connect()

    async def close(self) -> None:
        await self.vs.close()

    # ----- facts / profile -----------------------------------------
    async def get_profile(self, user_id: str) -> dict[str, Any]:
        async with session_scope() as s:  # type: AsyncSession
            row = await s.scalar(select(UserProfile).where(UserProfile.user_id == user_id))
            return row.data if row else {}

    async def upsert_fact(self, user_id: str, key: str, value: str, score: float = 0.5) -> None:
        async with session_scope() as s:
            fact = await s.scalar(
                select(MemoryFact).where(MemoryFact.user_id == user_id, MemoryFact.key == key)
            )
            if fact:
                fact.value, fact.score = value, score
            else:
                s.add(MemoryFact(user_id=user_id, key=key, value=value, score=score))

    # ----- semantic recall -----------------------------------------
    async def add(self, user_id: str, text: str, metadata: dict[str, Any] | None = None) -> str:
        vec = await embed_text(text)
        return await self.vs.upsert(user_id=user_id, text=text, vector=vec, metadata=metadata or {})

    async def search(self, user_id: str, query: str, k: int = 8) -> list[MemoryHit]:
        qvec = await embed_text(query)
        raw = await self.vs.search(user_id=user_id, vector=qvec, k=k)
        return [MemoryHit(id=r["id"], text=r["text"], score=r["score"], metadata=r.get("metadata"))
                for r in raw]
