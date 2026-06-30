"""Real-time WebSocket — streams brain thoughts + tokens to the frontend."""
from __future__ import annotations
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.utils.logger import get_logger

log = get_logger("ws")
router = APIRouter()


@router.websocket("/chat")
async def chat_ws(ws: WebSocket):
    await ws.accept()
    brain = ws.app.state.brain
    try:
        while True:
            raw = await ws.receive_text()
            payload = json.loads(raw)
            user_id = payload.get("user_id", "anonymous")
            message = payload.get("message", "")
            async for event in brain.stream_think(user_id=user_id, message=message):
                await ws.send_text(json.dumps(event))
    except WebSocketDisconnect:
        log.info("ws.disconnect")
    except Exception as e:  # noqa: BLE001
        log.warning("ws.error", err=str(e))
        await ws.close(code=1011)
