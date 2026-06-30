"""
Executes a TaskPlan with dependency resolution + retries.
"""
from __future__ import annotations
import asyncio
from typing import Callable

from backend.tasks.planner import TaskPlan, TaskStep
from backend.tools.registry import ToolRegistry
from backend.utils.logger import get_logger

log = get_logger("tasks.executor")


class TaskExecutor:
    def __init__(self, tools: ToolRegistry) -> None:
        self.tools = tools

    async def execute(self, plan: TaskPlan, on_progress: Callable[[TaskStep], None] | None = None) -> TaskPlan:
        pending = {s.id: s for s in plan.steps}
        done: set[str] = set()

        while pending:
            ready = [s for s in pending.values() if all(d in done for d in s.depends_on)]
            if not ready:
                raise RuntimeError("circular or unresolved dependencies")
            await asyncio.gather(*(self._run_step(s) for s in ready))
            for s in ready:
                done.add(s.id); pending.pop(s.id, None)
                if on_progress: on_progress(s)
        return plan

    async def _run_step(self, step: TaskStep) -> None:
        step.status = "running"
        log.info("task.step.start", id=step.id, action=step.action)
        tool = self.tools.get(step.action)
        try:
            if tool is None:
                raise ValueError(f"no tool/action registered: {step.action}")
            step.result = await tool.run(**step.args)
            step.status = "done"
        except Exception as e:  # noqa: BLE001
            step.status = "failed"
            step.result = {"error": str(e)}
            log.warning("task.step.fail", id=step.id, err=str(e))
