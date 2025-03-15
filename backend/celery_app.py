from celery import Celery
from db.config import settings

# Create a Celery instance using settings from configuration.
celery_app = Celery(
    "backend",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.imports = ["services.classifier_worker"]

# celery_app.autodiscover_tasks(["services"])

if __name__ == '__main__':
    celery_app.start()
