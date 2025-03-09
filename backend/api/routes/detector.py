from fastapi import APIRouter, File, UploadFile, status
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

from logger import logger

from schemas.detector import AudioClassResult, ClassificationResult

from services.classifaer import Classifier


router = APIRouter()
classifier = Classifier()


@router.post(
    "/get_audio_class",
    summary="return class of sent audio",
    status_code=status.HTTP_200_OK,
    response_model=AudioClassResult,
)
@cache(expire=3600)  # 1 hour cache
async def get_audio_class(audio: UploadFile = File(...)):
    # Read audio file bytes
    audio_bytes = await audio.read()
    # Classify the audio and get predicted class
    audio_class = classifier.classify_audio(audio_bytes)
    logger.info("Audio classified successfully", extra={"class": audio_class})
    return AudioClassResult(audio_class=audio_class)


@router.on_event("startup")
async def startup():
    # redis init
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
