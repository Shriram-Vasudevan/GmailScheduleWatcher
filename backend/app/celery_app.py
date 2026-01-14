from celery import Celery
import os
from datetime import datetime, timezone

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "gmail_scheduler",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks", "app.celery_app"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    result_expires=3600,
)
