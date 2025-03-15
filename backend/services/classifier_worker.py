import base64
import logging
from celery import Celery
from db.config import settings
from services.classifier import Classifier
from celery_app import celery_app
from logger import logger

# Global classifier instance so the model isn’t reloaded every time
classifier_instance = None

def get_classifier():
    global classifier_instance
    if classifier_instance is None:
        classifier_instance = Classifier()
    return classifier_instance

@celery_app.task(name="classify_audio_task", bind=True)
def classify_audio_task(self, audio_base64: str):
    """
    Decodes the audio, runs classification, and returns the result.
    """
    try:
        # Decode the base64 string to raw bytes
        audio_bytes = base64.b64decode(audio_base64)
        clf = get_classifier()
        audio_class = clf.classify_audio(audio_bytes)
        # Normalize classification string to lower-case for consistency
        audio_class = audio_class.lower()
        task_id = self.request.id
        logger.info("Task %s completed with result: %s", task_id, audio_class)
        return audio_class
    except Exception as e:
        logger.exception("Error in classify_audio_task: %s", e)
        raise e
