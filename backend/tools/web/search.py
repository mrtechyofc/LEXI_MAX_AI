"""Web search tool — uses DuckDuckGo HTML endpoint (no API key required)."""
from __future__ import annotations
import re
import httpx

from backend.tools.base import BaseTool, ToolPermission


class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web. Args: query, top_k."
    permissions = ToolPermission(network=True)

    async def run(self, query: str, top_k: int = 5) -> list[dict]:
        url = "https://duckduckgo.com/html/"
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as c:
            r = await c.post(url, data={"q": query})
            html = r.text
        results = []
        for m in re.finditer(
            r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html
        ):
            href, title = m.group(1), re.sub(r"<.*?>", "", m.group(2))
            results.append({"url": href, "title": title})
            if len(results) >= top_k:
                break
        return results
