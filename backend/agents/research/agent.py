"""ResearchAgent — uses web search + fetch tools to gather facts."""
from __future__ import annotations

from typing import Any

from backend.agents.base import AgentResult, BaseAgent


class ResearchAgent(BaseAgent):
    name = "research"
    description = "Performs web research using search + fetch tools."
    system_prompt = (
        "You are LEXI's research agent. Use web_search and web_fetch tools to "
        "gather up-to-date facts. Cite sources by URL. Be concise."
    )

    async def run(self, ctx: dict[str, Any]) -> AgentResult:
        query = ctx["context"].message
        self.log.info("research.start", query=query)

        results = await self._use_tool("web_search", query=query, top_k=5)
        fetched = []
        for r in results[:3]:
            try:
                page = await self._use_tool("web_fetch", url=r["url"])
                fetched.append({"url": r["url"], "title": r.get("title"), "text": page[:2000]})
            except Exception as e:  # noqa: BLE001
                self.log.warning("research.fetch_failed", url=r.get("url"), err=str(e))

        digest_prompt = (
            f"Question: {query}\n\nSources:\n" +
            "\n\n".join(f"[{i+1}] {f['url']}\n{f['text']}" for i, f in enumerate(fetched))
            + "\n\nWrite a concise, cited answer."
        )
        answer = await self._llm(digest_prompt)
        return AgentResult(
            output=answer,
            data={"sources": [f["url"] for f in fetched]},
            tools_used=["web_search", "web_fetch"],
            confidence=0.8,
        )
