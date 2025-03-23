from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class ClassificationResult(str, Enum):
    healthy = "healthy"
    unhealthy = "unhealthy"
    error = "artifact"


class AudioClassResponse(BaseModel):
    task_id: str
    audio_class: ClassificationResult


class UserResultResponse(BaseModel):
    classified_at: datetime
    result: ClassificationResult

    class Config:
        from_attributes = True
