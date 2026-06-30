"""Seed a few semantic memories for a user (dev helper)."""
import asyncio, sys
from backend.memory.embeddings import embed_text
from backend.memory.vector_store import VectorStore
from backend.config.settings import settings


async def main(user_id: str = "anonymous"):
    vs = VectorStore.create(settings); await vs.connect()
    for text in [
        "User prefers concise, bullet-point answers.",
        "User is building a JARVIS-style AI assistant called LEXI.",
        "User's stack: Python, FastAPI, Next.js, LangGraph.",
    ]:
        v = await embed_text(text)
        await vs.upsert(user_id=user_id, text=text, vector=v, metadata={"seed": True})
    print("seeded memories for", user_id)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "anonymous"))
