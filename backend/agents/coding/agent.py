"""CodingAgent — writes / refactors / reviews code, optionally executes it."""
from __future__ import annotations

from typing import Any

from backend.agents.base import AgentResult, BaseAgent


class CodingAgent(BaseAgent):
    name = "coding"
    description = "Writes, refactors and reviews code; may execute in a sandbox."
    system_prompt = (
        "You are LEXI's coding agent. Output runnable code in fenced blocks. "
        "Prefer Python unless the user requests otherwise. Add type hints and docstrings."
    )

    async def run(self, ctx: dict[str, Any]) -> AgentResult:
        request = ctx["context"].message
        code = await self._llm(f"Write or fix the following:\n{request}")
        tools_used: list[str] = []

        if "RUN_CODE" in request.upper():
            try:
                result = await self._use_tool("code_runner", code=code, language="python")
                tools_used.append("code_runner")
                code += f"\n\n--- run output ---\n{result['stdout']}"
            except Exception as e:  # noqa: BLE001
                self.log.warning("code_run_failed", err=str(e))

        return AgentResult(output=code, tools_used=tools_used, confidence=0.7)
