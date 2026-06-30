"""Text-to-Speech pipeline supporting Coqui, ElevenLabs, or OpenAI."""
from __future__ import annotations
from typing import AsyncIterator

from backend.config.settings import settings


class CoquiTTS:
    def __init__(self) -> None:
        self._tts = None

    def _load(self):
        if self._tts is None:
            from TTS.api import TTS  # type: ignore
            self._tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
        return self._tts

    async def synth(self, text: str) -> bytes:
        import io, soundfile as sf
        tts = self._load()
        wav = tts.tts(text=text)
        buf = io.BytesIO()
        sf.write(buf, wav, samplerate=22050, format="WAV")
        return buf.getvalue()


class ElevenLabsTTS:
    async def synth(self, text: str) -> bytes:
        import httpx
        url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(
                url,
                headers={"xi-api-key": settings.ELEVENLABS_API_KEY or "", "Accept": "audio/mpeg"},
                json={"text": text, "model_id": "eleven_turbo_v2_5"},
            )
            r.raise_for_status()
            return r.content


class OpenAITTS:
    async def synth(self, text: str) -> bytes:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        res = await client.audio.speech.create(model="tts-1", voice="nova", input=text)
        return res.read()


def get_tts():
    backend = settings.TTS_BACKEND
    if backend == "elevenlabs": return ElevenLabsTTS()
    if backend == "openai": return OpenAITTS()
    return CoquiTTS()
