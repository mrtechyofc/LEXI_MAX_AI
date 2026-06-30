"""Screen parser — combines screenshot + OCR + multimodal LLM for UI understanding."""
from __future__ import annotations

from backend.tools.vision.ocr import OCRTool
from backend.tools.vision.screenshot import ScreenshotTool
from backend.vision.image_analyzer import ImageAnalyzer


class ScreenParser:
    def __init__(self) -> None:
        self.screenshot = ScreenshotTool()
        self.ocr = OCRTool()
        self.analyzer = ImageAnalyzer()

    async def parse(self) -> dict:
        shot = await self.screenshot.run()
        import base64
        img_bytes = base64.b64decode(shot["base64"])
        text = await self.ocr.run(image_bytes=img_bytes)
        description = await self.analyzer.describe(
            img_bytes, "Describe the user interface and highlight clickable elements."
        )
        return {"ocr_text": text, "description": description, "size": (shot["width"], shot["height"])}
