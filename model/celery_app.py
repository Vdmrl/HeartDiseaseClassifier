from celery import Celery
from config import settings

celery_app = Celery(
    "model_worker",
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

# Import the ML worker task
celery_app.conf.imports = ["services.classifier_worker"]

if __name__ == '__main__':
    celery_app.start()