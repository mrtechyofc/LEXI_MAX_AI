"""High-level voice orchestrator: STT → Brain → TTS."""
from __future__ import annotations
from typing import AsyncIterator

from backend.core.brain import Brain
from backend.voice.stt import get_stt
from backend.voice.tts import get_tts


class VoiceRouter:
    def __init__(self, brain: Brain) -> None:
        self.brain = brain
        self.stt = get_stt()
        self.tts = get_tts()

    async def handle_voice_turn(self, user_id: str, audio_bytes: bytes) -> dict:
        transcript = await self.stt.transcribe(audio_bytes)
        response = await self.brain.think(user_id=user_id, message=transcript["text"])
        audio_out = await self.tts.synth(response.text)
        return {"transcript": transcript["text"], "response_text": response.text, "audio": audio_out}
