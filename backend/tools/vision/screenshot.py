"""Cross-platform screenshot tool using mss."""
from __future__ import annotations
import io, base64
import mss
from PIL import Image

from backend.tools.base import BaseTool


class ScreenshotTool(BaseTool):
    name = "screenshot"
    description = "Capture the primary screen and return base64 PNG."

    async def run(self, monitor: int = 1) -> dict:
        with mss.mss() as sct:
            shot = sct.grab(sct.monitors[monitor])
            img = Image.frombytes("RGB", shot.size, shot.rgb)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            b64 = base64.b64encode(buf.getvalue()).decode()
        return {"format": "png", "base64": b64, "width": img.width, "height": img.height}
