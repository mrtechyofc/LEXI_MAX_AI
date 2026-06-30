"""Unified LLM provider abstraction (OpenAI / Anthropic / Gemini / Ollama)."""
from __future__ import annotations
import json
from typing import AsyncIterator

from backend.config.settings import Settings, settings
from backend.utils.logger import get_logger

log = get_logger("llm")


class LLMProvider:
    def __init__(self, cfg: Settings = settings) -> None:
        self.cfg = cfg
        self.provider = cfg.DEFAULT_LLM_PROVIDER
        self.model = cfg.DEFAULT_LLM_MODEL
        self._oa = None; self._anthro = None; self._gem = None; self._oll = None

    async def connect(self) -> None:
        if self.provider == "openai" and self.cfg.OPENAI_API_KEY:
            from openai import AsyncOpenAI; self._oa = AsyncOpenAI(api_key=self.cfg.OPENAI_API_KEY)
        elif self.provider == "anthropic" and self.cfg.ANTHROPIC_API_KEY:
            from anthropic import AsyncAnthropic; self._anthro = AsyncAnthropic(api_key=self.cfg.ANTHROPIC_API_KEY)
        elif self.provider == "gemini" and self.cfg.GOOGLE_API_KEY:
            import google.generativeai as genai
            genai.configure(api_key=self.cfg.GOOGLE_API_KEY); self._gem = genai
        elif self.provider == "ollama":
            import ollama; self._oll = ollama.AsyncClient(host=self.cfg.OLLAMA_BASE_URL)
        log.info("llm.connected", provider=self.provider, model=self.model)

    async def close(self) -> None:
        self._oa = self._anthro = self._gem = self._oll = None

    # ----- high level wrappers ------------------------------------
    async def complete(self, system: str, prompt: str, temperature: float = 0.4) -> str:
        if self._oa:
            res = await self._oa.chat.completions.create(
                model=self.model, temperature=temperature,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            )
            return res.choices[0].message.content or ""
        if self._anthro:
            res = await self._anthro.messages.create(
                model=self.model, max_tokens=2048, system=system,
                messages=[{"role": "user", "content": prompt}],
            )
            return "".join(b.text for b in res.content if hasattr(b, "text"))
        if self._gem:
            m = self._gem.GenerativeModel(self.model, system_instruction=system)
            res = await m.generate_content_async(prompt)
            return getattr(res, "text", "") or ""
        if self._oll:
            res = await self._oll.chat(
                model=self.model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            )
            return res["message"]["content"]
        # Offline / dev fallback
        return f"[dev-llm:{self.provider}] {prompt[:300]}"

    async def stream(self, system: str, prompt: str) -> AsyncIterator[str]:
        if self._oa:
            stream = await self._oa.chat.completions.create(
                model=self.model, stream=True,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            )
            async for chunk in stream:
                yield chunk.choices[0].delta.content or ""
        else:
            text = await self.complete(system, prompt)
            for tok in text.split():
                yield tok + " "

    async def json(self, system: str, prompt: str) -> dict:
        sys2 = system + "\nRespond ONLY with valid JSON. No prose, no fences."
        raw = await self.complete(sys2, prompt, temperature=0.2)
        try:
            return json.loads(raw)
        except Exception:
            # Try to extract JSON from fenced output
            import re
            m = re.search(r"\{.*\}", raw, re.S)
            if m:
                try: return json.loads(m.group(0))
                except Exception: pass
            return {"raw": raw}
