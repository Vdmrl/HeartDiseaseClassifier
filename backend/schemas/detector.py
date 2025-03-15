from enum import Enum
from pydantic import BaseModel

class ClassificationResult(str, Enum):
    healthy = "healthy"
    unhealthy = "unhealthy"
    error = "artifact"

class AudioClassResponse(BaseModel):
    task_id: str
    audio_class: ClassificationResult