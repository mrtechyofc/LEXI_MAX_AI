"""In-memory short-term conversation buffer with Redis fallback."""
from __future__ import annotations
import json
from collections import defaultdict, deque
from typing import Deque

import redis.asyncio as aioredis

from backend.config.settings import settings
from backend.utils.logger import get_logger

log = get_logger("memory.short_term")


class ShortTermMemory:
    """Bounded rolling buffer keyed by (user_id, session_id)."""

    def __init__(self, window: int = 32) -> None:
        self.window = window
        self._local: dict[tuple[str, str], Deque[dict]] = defaultdict(lambda: deque(maxlen=window))
        self._redis: aioredis.Redis | None = None

    async def connect(self) -> None:
        try:
            self._redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
            await self._redis.ping()
            log.info("short_term.redis_connected")
        except Exception as e:  # noqa: BLE001
            log.warning("short_term.redis_unavailable", err=str(e))
            self._redis = None

    async def close(self) -> None:
        if self._redis:
            await self._redis.aclose()

    def _key(self, user_id: str, session_id: str) -> str:
        return f"lexi:stm:{user_id}:{session_id}"

    async def append(self, user_id: str, session_id: str, role: str, content: str) -> None:
        entry = {"role": role, "content": content}
        self._local[(user_id, session_id)].append(entry)
        if self._redis:
            k = self._key(user_id, session_id)
            await self._redis.rpush(k, json.dumps(entry))
            await self._redis.ltrim(k, -self.window, -1)
            await self._redis.expire(k, 60 * 60 * 24)

    async def recent(self, user_id: str, session_id: str, n: int = 12) -> list[dict]:
        if self._redis:
            items = await self._redis.lrange(self._key(user_id, session_id), -n, -1)
            return [json.loads(i) for i in items]
        return list(self._local[(user_id, session_id)])[-n:]
