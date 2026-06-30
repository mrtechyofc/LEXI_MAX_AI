"""
AgentRouter — decides which specialised agents handle a request and
runs them through a LangGraph workflow.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from backend.agents.base import AgentResult, BaseAgent
from backend.agents.coding.agent import CodingAgent
from backend.agents.critic.agent import CriticAgent
from backend.agents.memory.agent import MemoryAgent
from backend.agents.planner.agent import PlannerAgent
from backend.agents.reasoning.agent import ReasoningAgent
from backend.agents.reflection.agent import ReflectionAgent
from backend.agents.research.agent import ResearchAgent
from backend.agents.task_execution.agent import TaskExecutionAgent
from backend.agents.vision.agent import VisionAgent
from backend.agents.voice.agent import VoiceAgent
from backend.memory.memory_router import MemoryRouter
from backend.services.llm_provider import LLMProvider
from backend.tools.registry import ToolRegistry
from backend.utils.logger import get_logger

log = get_logger("router")


@dataclass
class RoutingDecision:
    agents: list[str]
    rationale: str
    attachments: list[dict[str, Any]] = field(default_factory=list)
    plan: Any = None
    context: Any = None
    memories: list[Any] = field(default_factory=list)


@dataclass
class ExecutionResult:
    final_text: str
    agent_results: dict[str, AgentResult]
    tools_used: list[str]

    @property
    def summary(self) -> str:
        return f"{len(self.agent_results)} agents, tools={self.tools_used}"


class AgentRouter:
    """Selects + sequences agents and tools per request."""

    def __init__(self, llm: LLMProvider, memory: MemoryRouter):
        self.llm = llm
        self.memory = memory
        self.tools = ToolRegistry()
        self.agents: dict[str, BaseAgent] = {}

    async def bootstrap(self) -> None:
        self.tools.discover()
        self.agents = {
            "planner":        PlannerAgent(self.llm, self.tools, self.memory),
            "reasoning":      ReasoningAgent(self.llm, self.tools, self.memory),
            "memory":         MemoryAgent(self.llm, self.tools, self.memory),
            "research":       ResearchAgent(self.llm, self.tools, self.memory),
            "vision":         VisionAgent(self.llm, self.tools, self.memory),
            "voice":          VoiceAgent(self.llm, self.tools, self.memory),
            "coding":         CodingAgent(self.llm, self.tools, self.memory),
            "task_execution": TaskExecutionAgent(self.llm, self.tools, self.memory),
            "critic":         CriticAgent(self.llm, self.tools, self.memory),
            "reflection":     ReflectionAgent(self.llm, self.tools, self.memory),
        }
        log.info("router.bootstrap", agents=list(self.agents.keys()), tools=self.tools.names())

    # ------------------------------------------------------------------
    async def route(self, message: str, plan, context, memories, attachments) -> RoutingDecision:
        """Use the LLM to pick a sub-set of agents."""
        sys = (
            "You are LEXI's routing controller. Given a user message and a plan, "
            "pick the minimum set of specialised agents required. "
            "Return a JSON object: {agents: [...], rationale: '...'}. "
            f"Available agents: {list(self.agents.keys())}."
        )
        decision = await self.llm.json(
            system=sys,
            prompt=f"USER: {message}\nPLAN: {plan.summary}\nATTACHMENTS: {bool(attachments)}",
        )
        agents = [a for a in decision.get("agents", []) if a in self.agents] or ["reasoning"]
        return RoutingDecision(
            agents=agents,
            rationale=decision.get("rationale", ""),
            attachments=attachments,
            plan=plan,
            context=context,
            memories=memories,
        )

    async def execute(self, routed: RoutingDecision) -> ExecutionResult:
        results: dict[str, AgentResult] = {}
        tools_used: list[str] = []

        running_context = {
            "plan":       routed.plan,
            "context":    routed.context,
            "memories":   routed.memories,
            "attachments": routed.attachments,
            "prior":      results,
        }

        for name in routed.agents:
            agent = self.agents[name]
            log.info("router.exec.agent", name=name)
            res = await agent.run(running_context)
            results[name] = res
            tools_used.extend(res.tools_used)

        # The last "reasoning" or final agent supplies the response
        final = results.get("reasoning") or list(results.values())[-1]
        return ExecutionResult(
            final_text=final.output,
            agent_results=results,
            tools_used=tools_used,
        )
