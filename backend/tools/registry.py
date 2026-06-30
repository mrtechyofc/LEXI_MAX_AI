"""Tool registry — auto-discovers tools at startup."""
from __future__ import annotations

from typing import Iterable

from backend.tools.base import BaseTool
from backend.utils.logger import get_logger

log = get_logger("tools.registry")


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def names(self) -> list[str]:
        return list(self._tools.keys())

    def all(self) -> Iterable[BaseTool]:
        return self._tools.values()

    def discover(self) -> None:
        """Import + register all built-in tools."""
        from backend.tools.web.search import WebSearchTool
        from backend.tools.web.fetch import WebFetchTool
        from backend.tools.files.reader import FileReaderTool
        from backend.tools.files.writer import FileWriterTool
        from backend.tools.terminal.executor import TerminalExecutorTool
        from backend.tools.coding.runner import CodeRunnerTool
        from backend.tools.automation.calculator import CalculatorTool
        from backend.tools.automation.email import EmailTool
        from backend.tools.automation.calendar import CalendarTool
        from backend.tools.vision.ocr import OCRTool
        from backend.tools.vision.screenshot import ScreenshotTool

        for cls in (
            WebSearchTool, WebFetchTool, FileReaderTool, FileWriterTool,
            TerminalExecutorTool, CodeRunnerTool, CalculatorTool, EmailTool,
            CalendarTool, OCRTool, ScreenshotTool,
        ):
            self.register(cls())
        log.info("tools.discovered", count=len(self._tools), tools=list(self._tools.keys()))
