"""ReflectionAgent — Performs meta-reasoning: lessons learned, follow-ups."""
from __future__ import annotations

from typing import Any

from backend.agents.base import AgentResult, BaseAgent


class ReflectionAgent(BaseAgent):
    name = "reflection"
    description = "Performs meta-reasoning: lessons learned, follow-ups."
    system_prompt = (
        "You are LEXI's reflection agent. Performs meta-reasoning: lessons learned, follow-ups. "
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
