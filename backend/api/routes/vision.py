"""Vision REST endpoints."""
from __future__ import annotations
from fastapi import APIRouter, File, UploadFile

from backend.vision.image_analyzer import ImageAnalyzer
from backend.vision.screen_parser import ScreenParser
from backend.tools.vision.ocr import OCRTool

router = APIRouter()


@router.post("/describe")
async def describe(file: UploadFile = File(...), prompt: str = "Describe the image."):
    img = await file.read()
    return {"description": await ImageAnalyzer().describe(img, prompt)}


@router.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    img = await file.read()
    return {"text": await OCRTool().run(image_bytes=img)}


@router.get("/screen")
async def screen():
    return await ScreenParser().parse()
