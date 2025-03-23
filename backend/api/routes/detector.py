import base64
from fastapi import APIRouter, File, UploadFile, status, HTTPException, Depends
from logger import logger
from schemas.detector import (
    AudioClassResponse,
    ClassificationResult,
    UserResultResponse,
)
from typing import List
from celery.result import AsyncResult
from celery_app import celery_app
from core.db.models import User
from repositories.results import get_user_results, add_user_result
from api.routes.fastapi_users import current_active_user

router = APIRouter(prefix="/detector", tags=["Detector"])

@router.post(
    "/classify_audio",
    summary="Enqueue audio classification task",
    status_code=status.HTTP_202_ACCEPTED,
)
async def classify_audio(audio: UploadFile = File(...), user: User = Depends(current_active_user)):
    """
    Accepts an audio file, encodes it as base64, enqueues a Celery task,
    and returns the task ID.
    """
    logger.info("Received asynchronous classification request")
    audio_bytes = await audio.read()
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    task = celery_app.send_task("classify_audio_task", args=[audio_base64])
    logger.info(f"Task enqueued with ID: {task.id}")
    return {"task_id": task.id}

@router.get(
    "/classify_audio/result/{task_id}",
    response_model=AudioClassResponse,
    status_code=status.HTTP_200_OK,
    summary="get classification results"
)
async def get_classification_result(task_id: str, user: User = Depends(current_active_user)):
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
        audio_class_enum = ClassificationResult(result.get().lower())
        # Add the classification result to the database if classification correct
        await add_user_result(user.id, audio_class_enum)
    except ValueError:
        audio_class_enum = ClassificationResult.error
    return AudioClassResponse(task_id=task_id, audio_class=audio_class_enum)

@router.get(
    "/results",
    response_model=List[UserResultResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all user results",
)
async def get_user_history(user: User = Depends(current_active_user)):
    """
    Retrieve all results for the currently authenticated user.
    """
    results = await get_user_results(user.id)

    return results
