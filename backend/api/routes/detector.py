# backend/api/detector.py

import base64
from fastapi import APIRouter, File, UploadFile, status, HTTPException
from logger import logger
from services.classifier_worker import classify_audio_task  # Celery task for classification
from schemas.detector import (
    AudioClassResponse,
    ClassificationResult,
)
from celery.result import AsyncResult
from celery_app import celery_app  # Import the Celery app instance

router = APIRouter(prefix="/detector", tags=["Detector"])

@router.post(
    "/classify_audio",
    summary="Enqueue audio classification task",
    status_code=status.HTTP_202_ACCEPTED,
)
async def classify_audio(
    audio: UploadFile = File(...),
):
    """
    Accepts an audio file, encodes it as base64, enqueues a Celery task,
    and returns the task ID.
    """
    logger.info("Received asynchronous classification request")
    audio_bytes = await audio.read()
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    task = classify_audio_task.delay(audio_base64)
    logger.info(f"Task enqueued with ID: {task.id}")
    return {"task_id": task.id}


@router.get(
    "/classify_audio/result/{task_id}",
    response_model=AudioClassResponse,
    status_code=status.HTTP_200_OK,
)
async def get_classification_result(task_id: str):
    """
    Retrieves the classification result for a given task ID from Celery.
    If the task is not yet ready, a 404 error is raised.
    """
    result = AsyncResult(task_id, app=celery_app)
    if not result.ready():
        raise HTTPException(
            status_code=404,
            detail="Result not found or task still processing",
        )
    try:
        # Ensure result is lower-case to match our enum values
        audio_class_enum = ClassificationResult(result.get().lower())
    except ValueError:
        audio_class_enum = ClassificationResult.error
    return AudioClassResponse(task_id=task_id, audio_class=audio_class_enum)
