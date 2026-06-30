"""Common base class for every specialized agent in LEXI."""
from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Any

from backend.memory.memory_router import MemoryRouter
from backend.services.llm_provider import LLMProvider
from backend.tools.registry import ToolRegistry
from backend.utils.logger import get_logger


@dataclass
class AgentResult:
    output: str
    data: dict[str, Any] = field(default_factory=dict)
    tools_used: list[str] = field(default_factory=list)
    confidence: float = 0.0


class BaseAgent(abc.ABC):
    """All agents inherit from this."""

    name: str = "base"
    description: str = ""
    system_prompt: str = "You are a helpful specialized agent."

    def __init__(self, llm: LLMProvider, tools: ToolRegistry, memory: MemoryRouter):
        self.llm = llm
        self.tools = tools
        self.memory = memory
        self.log = get_logger(f"agent.{self.name}")

    @abc.abstractmethod
    async def run(self, ctx: dict[str, Any]) -> AgentResult: ...

    # --- helpers ----------------------------------------------------
    async def _llm(self, prompt: str, **kw) -> str:
        return await self.llm.complete(system=self.system_prompt, prompt=prompt, **kw)

    async def _use_tool(self, name: str, **kwargs) -> Any:
        tool = self.tools.get(name)
        if not tool:
            raise ValueError(f"unknown tool: {name}")
        self.log.info("tool.call", tool=name, kwargs=list(kwargs))
        return await tool.run(**kwargs)
