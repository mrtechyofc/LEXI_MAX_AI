"""ReasoningAgent — produces the *final* user-facing answer."""
from __future__ import annotations
from typing import Any
from backend.agents.base import AgentResult, BaseAgent


class ReasoningAgent(BaseAgent):
    name = "reasoning"
    description = "Composes the final answer using context + memory + agent outputs."
    system_prompt = (
        "You are LEXI's reasoning core. Synthesize the user's question, recalled "
        "memories and prior agent outputs into ONE final answer. Be calm, concise "
        "and direct. Never reveal internal chain-of-thought."
    )

    async def run(self, ctx: dict[str, Any]) -> AgentResult:
        message = ctx["context"].message
        recent = ctx["context"].recent
        memories = ctx.get("memories", [])
        prior = ctx.get("prior", {})

        mem_blob = "\n".join(f"- {m.text}" for m in memories[:6]) or "(no relevant memories)"
        prior_blob = "\n".join(f"[{k}] {v.output[:400]}" for k, v in prior.items()) or "(no prior agents)"
        history_blob = "\n".join(f"{t.get('role')}: {t.get('content','')[:200]}" for t in recent[-6:])

        prompt = (
            f"User message:\n{message}\n\n"
            f"Conversation so far:\n{history_blob}\n\n"
            f"Memories:\n{mem_blob}\n\n"
            f"Prior agent outputs:\n{prior_blob}\n\n"
            f"Now write LEXI's final response."
        )
        answer = await self._llm(prompt)
        return AgentResult(output=answer.strip(), confidence=0.85)
