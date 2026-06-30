"""ContextManager — builds the per-turn working context for the brain."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from backend.memory.memory_router import MemoryRouter


@dataclass
class Context:
    user_id: str
    session_id: str
    message: str
    recent: list[dict] = field(default_factory=list)
    profile: dict = field(default_factory=dict)

    def summary(self) -> str:
        return (
            f"user={self.user_id} session={self.session_id} "
            f"recent_turns={len(self.recent)} profile_keys={list(self.profile)}"
        )


class ContextManager:
    def __init__(self, memory: MemoryRouter) -> None:
        self.memory = memory

    async def build(self, user_id: str, session_id: str | None, message: str) -> Context:
        sid = session_id or uuid.uuid4().hex
        recent = await self.memory.short_term.recent(user_id=user_id, session_id=sid, n=12)
        profile = await self.memory.long_term.get_profile(user_id=user_id)
        return Context(user_id=user_id, session_id=sid, message=message, recent=recent, profile=profile)
