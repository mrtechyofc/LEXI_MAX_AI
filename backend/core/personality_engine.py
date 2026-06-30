"""
PersonalityEngine — applies LEXI's voice / tone to outputs.

Traits: intelligent · calm · strategic · logical · adaptive.
"""
from __future__ import annotations

DEFAULT_PROFILE = {
    "tone": "calm, concise, intelligent",
    "habits": [
        "challenges flawed assumptions politely",
        "uses short paragraphs and bullets when helpful",
        "remembers user preferences and prior context",
        "never reveals chain-of-thought verbatim",
    ],
}


class PersonalityEngine:
    def __init__(self, profile: dict | None = None) -> None:
        self.profile = profile or DEFAULT_PROFILE

    async def style(self, text: str, *, context) -> str:
        """
        Light-weight stylistic pass. In production this can call the LLM
        with a system prompt; here we keep it deterministic so the brain
        stays cheap when responses are already well-formed.
        """
        text = text.strip()
        if not text:
            return "Acknowledged."
        # Soft personality hint: trim filler openings.
        for filler in ("Sure!", "Absolutely!", "Of course,"):
            if text.startswith(filler):
                text = text[len(filler):].lstrip()
        return text
