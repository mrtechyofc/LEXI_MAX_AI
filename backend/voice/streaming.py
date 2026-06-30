"""Streaming transcription helper — chunks audio frames and forwards to STT."""
from __future__ import annotations
from collections import deque
from typing import AsyncIterator

from backend.voice.stt import get_stt


class StreamingTranscriber:
    def __init__(self, chunk_ms: int = 1500) -> None:
        self.chunk_ms = chunk_ms
        self.stt = get_stt()
        self.buffer = deque()

    async def feed(self, audio_chunk: bytes) -> AsyncIterator[dict]:
        self.buffer.append(audio_chunk)
        blob = b"".join(self.buffer)
        if len(blob) > 32_000:  # ~1s of 16k PCM
            yield await self.stt.transcribe(blob)
            self.buffer.clear()
