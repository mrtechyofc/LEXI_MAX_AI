"""Tools registry + invocation."""
from __future__ import annotations
from fastapi import APIRouter, HTTPException, Request

router = APIRouter()


@router.get("")
async def list_tools(request: Request):
    reg = request.app.state.brain.router.tools
    return [{"name": t.name, "description": t.description} for t in reg.all()]


@router.post("/{name}/invoke")
async def invoke(name: str, payload: dict, request: Request):
    reg = request.app.state.brain.router.tools
    tool = reg.get(name)
    if not tool:
        raise HTTPException(404, f"tool not found: {name}")
    return {"result": await tool.run(**payload)}
