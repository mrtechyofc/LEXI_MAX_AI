"""Chat REST endpoint — non-streaming. WebSocket variant lives under /ws."""
from __future__ import annotations
from fastapi import APIRouter, Depends, Request

from backend.api.auth.deps import current_user
from backend.models.schemas import ChatRequest, ChatResponse

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest, request: Request, uid: str = Depends(current_user)):
    brain = request.app.state.brain
    res = await brain.think(
        user_id=uid, message=req.message,
        session_id=req.session_id, attachments=req.attachments,
    )
    return ChatResponse(
        text=res.text,
        session_id=res.meta["session_id"],
        used_tools=res.used_tools,
        used_agents=res.used_agents,
        memory_hits=res.memory_hits,
    )
