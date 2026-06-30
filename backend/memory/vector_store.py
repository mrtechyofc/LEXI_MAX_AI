"""Vector store abstraction: ChromaDB primary, FAISS fallback."""
from __future__ import annotations

import os
import uuid
from abc import ABC, abstractmethod
from typing import Any

from backend.config.settings import Settings
from backend.utils.logger import get_logger

log = get_logger("memory.vector_store")


class VectorStore(ABC):
    @staticmethod
    def create(settings: Settings) -> "VectorStore":
        if settings.VECTOR_BACKEND == "chromadb":
            return ChromaVectorStore(settings.CHROMA_PERSIST_DIR)
        return FaissVectorStore(settings.FAISS_PERSIST_DIR)

    @abstractmethod
    async def connect(self) -> None: ...
    @abstractmethod
    async def close(self) -> None: ...
    @abstractmethod
    async def upsert(self, user_id: str, text: str, vector: list[float], metadata: dict) -> str: ...
    @abstractmethod
    async def search(self, user_id: str, vector: list[float], k: int) -> list[dict[str, Any]]: ...


class ChromaVectorStore(VectorStore):
    def __init__(self, persist_dir: str) -> None:
        self.persist_dir = persist_dir
        self._client = None
        self._coll = None

    async def connect(self) -> None:
        import chromadb
        os.makedirs(self.persist_dir, exist_ok=True)
        self._client = chromadb.PersistentClient(path=self.persist_dir)
        self._coll = self._client.get_or_create_collection("lexi_memory")
        log.info("chroma.connected", dir=self.persist_dir)

    async def close(self) -> None:
        self._client = None
        self._coll = None

    async def upsert(self, user_id: str, text: str, vector: list[float], metadata: dict) -> str:
        mid = uuid.uuid4().hex
        self._coll.upsert(
            ids=[mid], embeddings=[vector], documents=[text],
            metadatas=[{**metadata, "user_id": user_id}],
        )
        return mid

    async def search(self, user_id: str, vector: list[float], k: int) -> list[dict[str, Any]]:
        res = self._coll.query(
            query_embeddings=[vector], n_results=k, where={"user_id": user_id},
        )
        out = []
        ids, docs, dists, metas = (res.get(x, [[]])[0] for x in ("ids", "documents", "distances", "metadatas"))
        for i, (mid, doc, dist, meta) in enumerate(zip(ids, docs, dists, metas)):
            out.append({"id": mid, "text": doc, "score": 1 / (1 + dist), "metadata": meta})
        return out


class FaissVectorStore(VectorStore):
    """Simple FAISS fallback. Persistence is best-effort (rebuilt from SQL on cold start)."""
    def __init__(self, persist_dir: str) -> None:
        self.persist_dir = persist_dir
        self._index = None
        self._items: list[dict] = []

    async def connect(self) -> None:
        import faiss, numpy as np  # noqa
        self._faiss = faiss
        self._np = np
        self._index = faiss.IndexFlatIP(1536)  # default OpenAI embedding size
        log.info("faiss.connected", dir=self.persist_dir)

    async def close(self) -> None:
        self._index = None

    async def upsert(self, user_id, text, vector, metadata):
        mid = uuid.uuid4().hex
        v = self._np.array([vector], dtype="float32")
        self._index.add(v)
        self._items.append({"id": mid, "text": text, "user_id": user_id, "metadata": metadata})
        return mid

    async def search(self, user_id, vector, k):
        if not self._items:
            return []
        v = self._np.array([vector], dtype="float32")
        D, I = self._index.search(v, min(k, len(self._items)))
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(self._items):
                continue
            item = self._items[idx]
            if item["user_id"] != user_id:
                continue
            results.append({"id": item["id"], "text": item["text"], "score": float(score),
                            "metadata": item["metadata"]})
        return results
