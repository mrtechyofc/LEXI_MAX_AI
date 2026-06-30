"""
Wake-word detector.

Uses Porcupine when an access key is provided, otherwise falls back to
a simple keyword spotter over Whisper transcripts.
"""
from __future__ import annotations
import os

from backend.config.settings import settings


class WakeWord:
    def __init__(self, phrase: str | None = None) -> None:
        self.phrase = (phrase or settings.WAKE_WORD).lower()
        self._porcupine = None
        access_key = os.getenv("PORCUPINE_ACCESS_KEY")
        if access_key:
            try:
                import pvporcupine
                self._porcupine = pvporcupine.create(access_key=access_key, keywords=["jarvis"])
            except Exception:
                self._porcupine = None

    def matches(self, transcript: str) -> bool:
        return self.phrase in transcript.lower()
