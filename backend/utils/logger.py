"""Structured logger using structlog with stdlib bridging."""
from __future__ import annotations
import logging, sys
import structlog


def get_logger(name: str | None = None) -> structlog.BoundLogger:
    return structlog.get_logger(name)


def configure(level: str = "INFO") -> None:
    logging.basicConfig(stream=sys.stdout, level=level, format="%(message)s")
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(colors=False),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, level)),
        cache_logger_on_first_use=True,
    )
