"""Speech-to-Text pipeline (Whisper local or OpenAI API)."""
from __future__ import annotations
import io
import tempfile
from typing import AsyncIterator

from backend.config.settings import settings
from backend.utils.logger import get_logger

log = get_logger("voice.stt")


class WhisperLocalSTT:
    def __init__(self, model_name: str = "base") -> None:
        self.model_name = model_name
        self._model = None

    def _load(self):
        if self._model is None:
            import whisper
            self._model = whisper.load_model(self.model_name)
            log.info("whisper.loaded", model=self.model_name)
        return self._model

    async def transcribe(self, audio_bytes: bytes) -> dict:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as f:
            f.write(audio_bytes); f.flush()
            model = self._load()
            result = model.transcribe(f.name)
        return {"text": result["text"], "language": result.get("language")}


class OpenAIWhisperSTT:
    async def transcribe(self, audio_bytes: bytes) -> dict:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        buf = io.BytesIO(audio_bytes); buf.name = "audio.wav"
        res = await client.audio.transcriptions.create(model="whisper-1", file=buf)
        return {"text": res.text, "language": None}


def get_stt():
    if settings.STT_BACKEND == "openai-whisper-api":
        return OpenAIWhisperSTT()
    return WhisperLocalSTT(model_name=settings.WHISPER_MODEL)
