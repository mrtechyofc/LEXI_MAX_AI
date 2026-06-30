"""Agents introspection routes."""
from __future__ import annotations
from fastapi import APIRouter, Request

router = APIRouter()


@router.get("")
async def list_agents(request: Request):
    router_obj = request.app.state.brain.router
    return [
        {"name": a.name, "description": a.description}
        for a in router_obj.agents.values()
    ]
