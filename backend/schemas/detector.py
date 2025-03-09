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

'''
class PostAudio(BaseModel):
    audio: str  # Base64-encoded WAV audio string

    @field_validator('audio')
    @classmethod
    def validate_audio(cls, v: str) -> str:
        try:
            base64.b64decode(v)  # Decode to check validity
        except Exception as e:
            raise ValueError("Invalid base64 encoding") from e
        return v
'''