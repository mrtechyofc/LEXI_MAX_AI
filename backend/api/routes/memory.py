"""Memory inspection + manual write."""
from __future__ import annotations
from fastapi import APIRouter, Depends, Request

from backend.api.auth.deps import current_user
from backend.models.schemas import MemoryQuery, MemoryWrite

router = APIRouter()


@router.post("/search")
async def search(body: MemoryQuery, request: Request, uid: str = Depends(current_user)):
    hits = await request.app.state.brain.memory.recall(user_id=uid, query=body.query, k=body.k)
    return [h.to_dict() for h in hits]


@router.post("/write")
async def write(body: MemoryWrite, request: Request, uid: str = Depends(current_user)):
    mid = await request.app.state.brain.memory.long_term.add(
        user_id=uid, text=body.text, metadata=body.metadata,
    )
    return {"id": mid}
