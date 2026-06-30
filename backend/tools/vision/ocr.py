"""OCR tool via pytesseract."""
from __future__ import annotations
import io
from PIL import Image
import pytesseract

from backend.tools.base import BaseTool


class OCRTool(BaseTool):
    name = "ocr"
    description = "Extract text from an image. Args: image_bytes (b64) or image_path."

    async def run(self, image_bytes: bytes | None = None, image_path: str | None = None) -> str:
        if image_bytes is not None:
            img = Image.open(io.BytesIO(image_bytes))
        elif image_path:
            img = Image.open(image_path)
        else:
            raise ValueError("provide image_bytes or image_path")
        return pytesseract.image_to_string(img)
