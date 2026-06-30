"""Web fetch tool — downloads a URL and strips HTML to readable text."""
from __future__ import annotations
import httpx
from bs4 import BeautifulSoup

from backend.tools.base import BaseTool, ToolPermission


class WebFetchTool(BaseTool):
    name = "web_fetch"
    description = "Fetch a URL and return readable text."
    permissions = ToolPermission(network=True)

    async def run(self, url: str) -> str:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as c:
            r = await c.get(url, headers={"User-Agent": "LEXI/0.1"})
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = "\n".join(line.strip() for line in soup.get_text().splitlines() if line.strip())
        return text[:50000]
