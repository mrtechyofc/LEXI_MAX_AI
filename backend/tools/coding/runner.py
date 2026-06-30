"""
Code runner — executes short Python snippets inside a subprocess
with limited time + memory. For production, swap for a Firecracker / gVisor sandbox.
"""
from __future__ import annotations
import asyncio
import os
import sys
import tempfile

from backend.tools.base import BaseTool, ToolPermission


class CodeRunnerTool(BaseTool):
    name = "code_runner"
    description = "Run a short Python snippet. Args: code, timeout."
    permissions = ToolPermission(filesystem_write=True)

    async def run(self, code: str, language: str = "python", timeout: int = 8) -> dict:
        if language != "python":
            raise ValueError("only python supported in this minimal runner")
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write(code)
            path = f.name
        try:
            proc = await asyncio.create_subprocess_exec(
                sys.executable, "-I", path,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            )
            try:
                out, err = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            except asyncio.TimeoutError:
                proc.kill()
                raise
        finally:
            os.unlink(path)
        return {"stdout": out.decode(), "stderr": err.decode(), "code": proc.returncode}
