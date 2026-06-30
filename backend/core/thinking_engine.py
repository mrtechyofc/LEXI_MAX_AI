"""
ThinkingEngine — hidden chain-of-thought reasoning utilities.

NEVER expose raw Thought.content to end-users; it is for internal
pipelines, logs and the agent activity monitor only.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from backend.services.llm_provider import LLMProvider


@dataclass
class Thought:
    step: str
    content: str


@dataclass
class Plan:
    id: str
    summary: str
    steps: list[str] = field(default_factory=list)


@dataclass
class Critique:
    notes: str
    score: float


class ThinkingEngine:
    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    async def plan(self, message: str, context: Any) -> Plan:
        sys = (
            "You are LEXI's internal planner. Given a user message and context, "
            "produce a concise 3-7 step plan as JSON: {summary, steps}. "
            "Do not include any user-facing prose."
        )
        data = await self.llm.json(system=sys, prompt=f"USER: {message}\nCONTEXT: {context.summary()}")
        return Plan(
            id=uuid.uuid4().hex,
            summary=data.get("summary", ""),
            steps=data.get("steps", []),
        )

    async def reflect(self, execution: Any, context: Any) -> Critique:
        sys = (
            "You are LEXI's internal critic. Given an execution trace, return "
            "JSON: {notes: '...', score: 0..1}. Focus on factuality and gaps."
        )
        data = await self.llm.json(
            system=sys,
            prompt=f"EXECUTION: {execution.summary}\nFINAL: {execution.final_text[:600]}",
        )
        return Critique(notes=data.get("notes", ""), score=float(data.get("score", 0.7)))
