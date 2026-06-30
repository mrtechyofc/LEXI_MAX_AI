"""TaskExecutionAgent — Executes ordered task plans, using tools as needed."""
from __future__ import annotations

from typing import Any

from backend.agents.base import AgentResult, BaseAgent


class TaskExecutionAgent(BaseAgent):
    name = "task_execution"
    description = "Executes ordered task plans, using tools as needed."
    system_prompt = (
        "You are LEXI's task_execution agent. Executes ordered task plans, using tools as needed. "
        "Always return clear structured answers."
    )

    async def run(self, ctx: dict[str, Any]) -> AgentResult:
        self.log.info("agent.run", name=self.name)
        message = ctx["context"].message
        memories = "\n".join(m.text for m in ctx.get("memories", [])[:5])

        prompt = (
            f"User message:\n{message}\n\n"
            f"Relevant memories:\n{memories or '(none)'}\n\n"
            f"Prior agent outputs:\n{ {k: v.output[:300] for k, v in ctx.get('prior', {}).items()} }"
        )
        output = await self._llm(prompt)
        return AgentResult(output=output, confidence=0.75)
