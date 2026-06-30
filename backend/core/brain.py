"""
Brain — the central orchestrator of LEXI.

Pipeline (hidden chain-of-thought):

    intent → context → memory recall → planning →
    tool selection → execution (agents/tools) → reflection → response

The Brain is a long-lived singleton attached to FastAPI app.state.
It owns the LLM clients, the agent router, memory manager and
personality engine. All public callers should use :meth:`think` or
:meth:`stream_think`.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, AsyncIterator

from backend.config.settings import Settings
from backend.core.context_manager import ContextManager
from backend.core.personality_engine import PersonalityEngine
from backend.core.router import AgentRouter
from backend.core.thinking_engine import ThinkingEngine, Thought
from backend.memory.memory_router import MemoryRouter
from backend.memory.vector_store import VectorStore
from backend.services.llm_provider import LLMProvider
from backend.utils.logger import get_logger

log = get_logger("brain")


@dataclass
class BrainResponse:
    text: str
    thoughts: list[Thought] = field(default_factory=list)
    used_tools: list[str] = field(default_factory=list)
    used_agents: list[str] = field(default_factory=list)
    memory_hits: list[dict[str, Any]] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)


class Brain:
    """Top-level coordinator. Stateless per-request, stateful across the app."""

    def __init__(self, settings: Settings, vector_store: VectorStore) -> None:
        self.settings = settings
        self.llm = LLMProvider(settings)
        self.memory = MemoryRouter(vector_store=vector_store, settings=settings)
        self.personality = PersonalityEngine()
        self.context = ContextManager(memory=self.memory)
        self.thinking = ThinkingEngine(llm=self.llm)
        self.router = AgentRouter(llm=self.llm, memory=self.memory)
        self._lock = asyncio.Lock()

    # ----------------------------------------------------------------
    # Lifecycle
    # ----------------------------------------------------------------
    async def warmup(self) -> None:
        log.info("brain.warmup.start")
        await self.llm.connect()
        await self.memory.connect()
        await self.router.bootstrap()
        log.info("brain.warmup.done")

    async def shutdown(self) -> None:
        await self.llm.close()
        await self.memory.close()

    # ----------------------------------------------------------------
    # Main entrypoint
    # ----------------------------------------------------------------
    async def think(
        self,
        user_id: str,
        message: str,
        *,
        attachments: list[dict[str, Any]] | None = None,
        session_id: str | None = None,
    ) -> BrainResponse:
        """One-shot reasoning + response."""
        ctx = await self.context.build(user_id=user_id, session_id=session_id, message=message)
        thoughts: list[Thought] = []

        # 1) Intent + planning
        plan = await self.thinking.plan(message, ctx)
        thoughts.append(Thought(step="plan", content=plan.summary))

        # 2) Memory recall
        recalls = await self.memory.recall(user_id=user_id, query=message, k=8)
        thoughts.append(Thought(step="recall", content=f"{len(recalls)} memories"))

        # 3) Route to agent(s) + tools
        routed = await self.router.route(
            message=message, plan=plan, context=ctx, memories=recalls,
            attachments=attachments or [],
        )
        thoughts.append(Thought(step="route", content=f"agents={routed.agents}"))

        # 4) Execute
        execution = await self.router.execute(routed)
        thoughts.append(Thought(step="execute", content=execution.summary))

        # 5) Reflection / critique
        critique = await self.thinking.reflect(execution=execution, context=ctx)
        thoughts.append(Thought(step="reflect", content=critique.notes))

        # 6) Final response — styled by personality
        styled = await self.personality.style(execution.final_text, context=ctx)

        # 7) Persist relevant memory
        await self.memory.write_turn(
            user_id=user_id, message=message, response=styled, session_id=ctx.session_id,
        )

        return BrainResponse(
            text=styled,
            thoughts=thoughts,
            used_tools=execution.tools_used,
            used_agents=routed.agents,
            memory_hits=[m.to_dict() for m in recalls],
            meta={"session_id": ctx.session_id, "plan_id": plan.id},
        )

    async def stream_think(self, user_id: str, message: str, **kw) -> AsyncIterator[dict[str, Any]]:
        """Server-Sent / WebSocket streaming variant. Yields chunks of work-in-progress."""
        yield {"type": "status", "stage": "thinking"}
        response = await self.think(user_id=user_id, message=message, **kw)
        for thought in response.thoughts:
            yield {"type": "thought", "step": thought.step, "content": thought.content}
        # Stream the final answer word by word so the UI feels alive
        for token in response.text.split():
            yield {"type": "token", "value": token + " "}
            await asyncio.sleep(0)
        yield {"type": "done", "meta": response.meta, "tools": response.used_tools}
