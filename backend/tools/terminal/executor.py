"""
Terminal executor — runs commands inside a constrained allow-list.
Never executes arbitrary shell; only whitelisted programs.
"""
from __future__ import annotations
import asyncio
import shlex

from backend.tools.base import BaseTool, ToolPermission

ALLOWED_BIN = {"ls", "cat", "grep", "find", "wc", "head", "tail", "echo", "date", "pwd"}


class TerminalExecutorTool(BaseTool):
    name = "terminal"
    description = "Run a whitelisted shell command. Args: cmd."
    permissions = ToolPermission(shell=True)

    async def run(self, cmd: str, timeout: int = 10) -> dict:
        parts = shlex.split(cmd)
        if not parts or parts[0] not in ALLOWED_BIN:
            raise PermissionError(f"command not allowed: {parts[:1]}")
        proc = await asyncio.create_subprocess_exec(
            *parts, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        try:
            out, err = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            proc.kill()
            raise
        return {"stdout": out.decode(), "stderr": err.decode(), "code": proc.returncode}
