"""Cron-like scheduler using Celery beat schedules."""
from __future__ import annotations
from celery.schedules import crontab

BEAT_SCHEDULE = {
    "memory-prune-nightly": {
        "task": "backend.services.tasks.prune_memory",
        "schedule": crontab(hour=3, minute=0),
    },
    "summarize-sessions-hourly": {
        "task": "backend.services.tasks.summarize_sessions",
        "schedule": crontab(minute=0),
    },
}
