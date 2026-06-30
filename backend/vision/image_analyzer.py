"""Multimodal image analyzer — routes to a vision-capable LLM."""
from __future__ import annotations
import base64

from backend.config.settings import settings


class ImageAnalyzer:
    async def describe(self, image_bytes: bytes, prompt: str = "Describe the image.") -> str:
        if not settings.OPENAI_API_KEY:
            return "[vision unavailable: no OPENAI_API_KEY configured]"
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        b64 = base64.b64encode(image_bytes).decode()
        res = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                ],
            }],
        )
        return res.choices[0].message.content or ""
