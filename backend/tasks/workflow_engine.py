"""
LangGraph-style workflow engine adapter — used by agents that need
explicit graph branching (planner → tool → critic → final).
"""
from __future__ import annotations
from typing import Any, Callable, Awaitable


class Node:
    def __init__(self, name: str, fn: Callable[[dict], Awaitable[dict]]):
        self.name, self.fn = name, fn


class Workflow:
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: dict[str, list[str]] = {}
        self.entry: str | None = None

    def add(self, name: str, fn: Callable[[dict], Awaitable[dict]]):
        self.nodes[name] = Node(name, fn); self.edges.setdefault(name, [])
        if self.entry is None: self.entry = name
        return self

    def connect(self, src: str, dst: str):
        self.edges[src].append(dst); return self

    async def run(self, state: dict[str, Any]) -> dict[str, Any]:
        assert self.entry, "no entry node"
        current = [self.entry]
        while current:
            nxt = []
            for n in current:
                state = await self.nodes[n].fn(state)
                nxt.extend(self.edges.get(n, []))
            current = nxt
        return state
