import pytest
from backend.memory.embeddings import embed_text


@pytest.mark.asyncio
async def test_embed_deterministic_offline():
    v1 = await embed_text("hello world")
    v2 = await embed_text("hello world")
    assert v1 == v2
    assert len(v1) == 1536
