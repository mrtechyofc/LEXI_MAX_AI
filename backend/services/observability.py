"""Logging + tracing setup helpers."""
from __future__ import annotations
import logging

from backend.utils.logger import configure as configure_logging


def setup_logging(level: str = "INFO") -> None:
    configure_logging(level)
    for noisy in ("httpx", "uvicorn.access"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def setup_tracing(endpoint: str | None) -> None:
    if not endpoint:
        return
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

        provider = TracerProvider(resource=Resource.create({"service.name": "lexi"}))
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
        trace.set_tracer_provider(provider)
    except Exception:
        # OTel is optional; never fail boot on tracing.
        pass
