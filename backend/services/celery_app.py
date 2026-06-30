"""Celery application + sample tasks for background work."""
from __future__ import annotations
from celery import Celery

from backend.config.settings import settings
from backend.tasks.scheduler import BEAT_SCHEDULE

celery = Celery(
    "lexi",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["backend.services.tasks"],
)
celery.conf.beat_schedule = BEAT_SCHEDULE
celery.conf.task_acks_late = True
celery.conf.worker_prefetch_multiplier = 1
