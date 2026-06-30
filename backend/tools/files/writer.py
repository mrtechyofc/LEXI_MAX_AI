"""File writer — sandboxed under DATA_ROOT."""
from __future__ import annotations
import os
import aiofiles  # type: ignore

from backend.tools.base import BaseTool, ToolPermission
from backend.tools.files.reader import _safe


class FileWriterTool(BaseTool):
    name = "file_write"
    description = "Write to a file under DATA_ROOT. Args: path, content."
    permissions = ToolPermission(filesystem_write=True)

    async def run(self, path: str, content: str) -> dict:
        full = _safe(path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        async with aiofiles.open(full, "w") as f:
            await f.write(content)
        return {"path": full, "bytes": len(content)}
