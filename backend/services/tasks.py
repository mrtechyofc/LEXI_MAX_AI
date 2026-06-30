"""Background tasks registered with Celery."""
from __future__ import annotations

from backend.services.celery_app import celery
from backend.utils.logger import get_logger

log = get_logger("celery")


@celery.task(name="backend.services.tasks.prune_memory")
def prune_memory() -> dict:
    log.info("celery.prune_memory")
    # Real impl: connect to DB + vector store, drop low-score entries older than N days.
    return {"pruned": 0}


@celery.task(name="backend.services.tasks.summarize_sessions")
def summarize_sessions() -> dict:
    log.info("celery.summarize_sessions")
    return {"summarized": 0}
