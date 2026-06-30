"""High-level task planner — converts a goal into ordered actionable steps."""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from typing import Any

from backend.services.llm_provider import LLMProvider


@dataclass
class TaskStep:
    id: str
    action: str
    args: dict[str, Any] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)
    status: str = "pending"   # pending | running | done | failed
    result: Any = None


@dataclass
class TaskPlan:
    id: str
    goal: str
    steps: list[TaskStep] = field(default_factory=list)


class TaskPlanner:
    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    async def plan(self, goal: str) -> TaskPlan:
        data = await self.llm.json(
            system=(
                "You are LEXI's task planner. Convert a goal into a JSON object: "
                "{steps: [{action, args, depends_on?}]}. "
                "Actions reference tools or agents by name."
            ),
            prompt=f"GOAL: {goal}",
        )
        steps = [
            TaskStep(id=f"s{i}", action=s["action"], args=s.get("args", {}),
                     depends_on=s.get("depends_on", []))
            for i, s in enumerate(data.get("steps", []))
        ]
        return TaskPlan(id=uuid.uuid4().hex, goal=goal, steps=steps)
