from enum import Enum
from pydantic import BaseModel

class ClassificationResult(str, Enum):
    healthy = "healthy"
    unhealthy = "unhealthy"
    error = "artifact"

class AudioClassResult(BaseModel):
    audio_class: ClassificationResult

class ClassificationWebhookPayload(BaseModel):
    task_id: str
    audio_class: ClassificationResult

class AudioClassResponse(BaseModel):
    task_id: str
    audio_class: ClassificationResult