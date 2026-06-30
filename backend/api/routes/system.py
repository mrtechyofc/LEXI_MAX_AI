"""System / health / introspection routes."""
from __future__ import annotations
import time
from fastapi import APIRouter, Request

from backend.config.settings import settings
from backend.models.schemas import SystemStatus

_start = time.time()
router = APIRouter()


@router.get("/status", response_model=SystemStatus)
async def status(request: Request):
    brain = request.app.state.brain
    return SystemStatus(
        version="0.1.0",
        env=settings.ENV,
        agents=list(brain.router.agents.keys()),
        tools=brain.router.tools.names(),
        uptime_seconds=time.time() - _start,
    )
