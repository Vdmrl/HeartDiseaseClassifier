from fastapi import APIRouter, File, UploadFile, status, Request, Depends
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from logger import logger

from schemas.detector import AudioClassResult, ClassificationResult

from services.classifaer import Classifier

router = APIRouter()


def get_classifier(request: Request) -> Classifier:
    # Dependency that retrieves the classifier from app.state
    return request.app.state.classifier


@router.post(
    "/get_audio_class",
    summary="return class of sent audio",
    status_code=status.HTTP_200_OK,
    response_model=AudioClassResult,
)
@cache(expire=3600)  # 1 hour cache
async def get_audio_class(
        audio: UploadFile = File(...),
        classifier: Classifier = Depends(get_classifier)
):
    logger.info("Received request for audio classification")
    # Read audio file bytes
    audio_bytes = await audio.read()
    # Classify the audio and get predicted class
    audio_class = classifier.classify_audio(audio_bytes)
    logger.info("Audio classified successfully", extra={"class": audio_class})
    return AudioClassResult(audio_class=audio_class)
