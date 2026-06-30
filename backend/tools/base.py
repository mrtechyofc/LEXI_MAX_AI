"""Base classes for the LEXI tool system."""
from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Any


@dataclass
class ToolPermission:
    network: bool = False
    filesystem_read: bool = False
    filesystem_write: bool = False
    shell: bool = False


class BaseTool(abc.ABC):
    name: str = "tool"
    description: str = ""
    permissions: ToolPermission = ToolPermission()

    @abc.abstractmethod
    async def run(self, **kwargs) -> Any: ...

    def validate(self, **kwargs) -> None:
        """Override to enforce arg validation."""
        return None
