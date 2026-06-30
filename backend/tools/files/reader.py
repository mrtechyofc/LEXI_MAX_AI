"""File reader — sandboxed under DATA_ROOT."""
from __future__ import annotations
import os
import aiofiles  # type: ignore

from backend.tools.base import BaseTool, ToolPermission

DATA_ROOT = os.path.abspath(os.environ.get("LEXI_DATA_ROOT", "./data"))


def _safe(path: str) -> str:
    p = os.path.abspath(os.path.join(DATA_ROOT, path))
    if not p.startswith(DATA_ROOT):
        raise PermissionError("path outside DATA_ROOT")
    return p


class FileReaderTool(BaseTool):
    name = "file_read"
    description = "Read a file inside DATA_ROOT. Args: path."
    permissions = ToolPermission(filesystem_read=True)

    async def run(self, path: str, max_bytes: int = 200_000) -> str:
        full = _safe(path)
        async with aiofiles.open(full, "rb") as f:
            data = await f.read(max_bytes)
        return data.decode("utf-8", errors="replace")
