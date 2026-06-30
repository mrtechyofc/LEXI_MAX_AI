"""Voice REST endpoints — STT and TTS."""
from __future__ import annotations
from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import Response

from backend.api.auth.deps import current_user
from backend.voice.stt import get_stt
from backend.voice.tts import get_tts
from backend.voice.voice_router import VoiceRouter

router = APIRouter()


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    audio = await file.read()
    return await get_stt().transcribe(audio)


@router.post("/synthesize")
async def synthesize(payload: dict):
    text = payload.get("text", "")
    audio = await get_tts().synth(text)
    return Response(content=audio, media_type="audio/wav")


@router.post("/turn")
async def voice_turn(request: Request, file: UploadFile = File(...), uid: str = Depends(current_user)):
    vr = VoiceRouter(brain=request.app.state.brain)
    audio = await file.read()
    result = await vr.handle_voice_turn(uid, audio)
    return {"transcript": result["transcript"], "response_text": result["response_text"]}
