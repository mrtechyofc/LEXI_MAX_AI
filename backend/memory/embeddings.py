"""Embedding helpers - uses OpenAI when available, deterministic fallback otherwise."""
from __future__ import annotations
import hashlib

from backend.config.settings import settings


async def embed_text(text: str) -> list[float]:
    if settings.OPENAI_API_KEY:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        res = await client.embeddings.create(model=settings.EMBEDDING_MODEL, input=text[:8000])
        return res.data[0].embedding
    # Deterministic 1536-dim fallback for dev/offline.
    h = hashlib.sha512(text.encode()).digest()
    vec = []
    seed = int.from_bytes(h[:8], "little")
    rng = seed
    for _ in range(1536):
        rng = (rng * 1103515245 + 12345) & 0x7fffffff
        vec.append(((rng % 1000) / 500.0) - 1.0)
    # L2-normalize
    norm = sum(x * x for x in vec) ** 0.5 or 1.0
    return [x / norm for x in vec]
