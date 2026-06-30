"""
LEXI - FastAPI application entrypoint.

Wires together:
  • Configuration & structured logging
  • Database / Redis / vector-store lifespans
  • Core brain singleton
  • REST + WebSocket routers
  • Prometheus metrics + OpenTelemetry tracing
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from backend.api.routes import chat, agents, memory, tools, voice, vision, tasks, system, auth
from backend.api.websocket.realtime import router as ws_router
from backend.api.middleware.request_id import RequestIDMiddleware
from backend.api.middleware.rate_limit import RateLimitMiddleware
from backend.config.settings import settings
from backend.core.brain import Brain
from backend.database.session import init_db, close_db
from backend.services.observability import setup_logging, setup_tracing
from backend.memory.vector_store import VectorStore

logger = logging.getLogger("lexi.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown hooks for shared singletons."""
    setup_logging(settings.LOG_LEVEL)
    setup_tracing(settings.OTEL_EXPORTER_OTLP_ENDPOINT)

    logger.info("LEXI starting up - env=%s", settings.ENV)
    await init_db()

    # Initialize and stash singletons on app.state
    app.state.vector_store = VectorStore.create(settings)
    app.state.brain = Brain(settings=settings, vector_store=app.state.vector_store)
    await app.state.brain.warmup()

    yield

    logger.info("LEXI shutting down")
    await app.state.brain.shutdown()
    await close_db()


def create_app() -> FastAPI:
    app = FastAPI(
        title="LEXI - The Ultimate AI Assistant",
        description="A modular, multi-agent AI operating system.",
        version="0.1.0",
        lifespan=lifespan,
    )

    # ---- Middleware --------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(RateLimitMiddleware)

    # ---- Routers -----------------------------------------------------
    app.include_router(auth.router,   prefix="/api/auth",   tags=["auth"])
    app.include_router(chat.router,   prefix="/api/chat",   tags=["chat"])
    app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
    app.include_router(memory.router, prefix="/api/memory", tags=["memory"])
    app.include_router(tools.router,  prefix="/api/tools",  tags=["tools"])
    app.include_router(voice.router,  prefix="/api/voice",  tags=["voice"])
    app.include_router(vision.router, prefix="/api/vision", tags=["vision"])
    app.include_router(tasks.router,  prefix="/api/tasks",  tags=["tasks"])
    app.include_router(system.router, prefix="/api/system", tags=["system"])

    app.include_router(ws_router, prefix="/ws", tags=["websocket"])

    # ---- Metrics endpoint -------------------------------------------
    if settings.PROMETHEUS_ENABLED:
        app.mount("/metrics", make_asgi_app())

    @app.get("/health", tags=["system"])
    async def health():
        return {"status": "ok", "service": "lexi", "version": app.version}

    return app


app = create_app()
