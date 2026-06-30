"""Routes vision requests to the appropriate provider/pipeline."""
from __future__ import annotations
from backend.vision.image_analyzer import ImageAnalyzer
from backend.vision.screen_parser import ScreenParser
from backend.vision.webcam import Webcam


class MultimodalRouter:
    def __init__(self) -> None:
        self.image = ImageAnalyzer()
        self.screen = ScreenParser()
        self.webcam = Webcam()
