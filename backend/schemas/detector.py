from enum import Enum
from pydantic import BaseModel, field_validator
import base64


# Enum for classfication results
class ClassificationResult(str, Enum):
    healty = "healthy"
    unhealty = "unhealthy"
    error = "artifact"


# Pydantic model for the response
class AudioClassResult(BaseModel):
    audio_class: ClassificationResult
