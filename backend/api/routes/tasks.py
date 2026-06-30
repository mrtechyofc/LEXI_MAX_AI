"""Task planning + execution routes."""
from __future__ import annotations
from fastapi import APIRouter, Depends, Request

from backend.api.auth.deps import current_user
from backend.models.schemas import TaskCreate
from backend.tasks.executor import TaskExecutor
from backend.tasks.planner import TaskPlanner

router = APIRouter()


@router.post("")
async def create_task(body: TaskCreate, request: Request, uid: str = Depends(current_user)):
    brain = request.app.state.brain
    plan = await TaskPlanner(brain.llm).plan(body.goal)
    executor = TaskExecutor(brain.router.tools)
    await executor.execute(plan)
    return {
        "id": plan.id,
        "goal": plan.goal,
        "steps": [
            {"id": s.id, "action": s.action, "status": s.status, "result": s.result}
            for s in plan.steps
        ],
    }
