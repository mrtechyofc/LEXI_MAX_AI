"""Webcam capture via OpenCV."""
from __future__ import annotations
import asyncio


class Webcam:
    async def snapshot(self, device: int = 0) -> bytes:
        import cv2, io
        from PIL import Image

        def _grab():
            cap = cv2.VideoCapture(device)
            try:
                ok, frame = cap.read()
                if not ok:
                    raise RuntimeError("webcam capture failed")
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                return buf.getvalue()
            finally:
                cap.release()

        return await asyncio.to_thread(_grab)
