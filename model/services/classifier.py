import io
import logging
import numpy as np
import librosa
import torch
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification

MODEL_CHECKPOINT = "Vladimirlv/ast-finetuned-audioset-10-10-0.4593-heart-sounds"
TIME_LIMIT_SECONDS = 30
SAMPLE_RATE = 16000

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class Classifier:
    def __init__(self):
        logger.info("Initializing classifier with model checkpoint: %s", MODEL_CHECKPOINT)
        self.extractor = AutoFeatureExtractor.from_pretrained(
            MODEL_CHECKPOINT,
            do_normalize=True,
            token=None
        )
        self.model = AutoModelForAudioClassification.from_pretrained(
            MODEL_CHECKPOINT,
            token=None
        )
        self.model.eval()
        self.sample_rate = SAMPLE_RATE
        self.target_length = SAMPLE_RATE * TIME_LIMIT_SECONDS

    def preprocess_audio(self, audio_bytes: bytes) -> np.ndarray:
        logger.info("Preprocessing audio")
        audio_buffer = io.BytesIO(audio_bytes)
        audio_array, sr = librosa.load(audio_buffer, sr=self.sample_rate)
        logger.info("Audio loaded: sample rate %s, length %s", sr, len(audio_array))
        if len(audio_array) < self.target_length:
            logger.info("Padding audio from length %s to target length %s", len(audio_array), self.target_length)
            audio_array = np.pad(audio_array, (0, self.target_length - len(audio_array)), mode='constant')
        else:
            logger.info("Truncating audio from length %s to target length %s", len(audio_array), self.target_length)
            audio_array = audio_array[:self.target_length]
        return audio_array

    def classify_audio(self, audio_bytes: bytes) -> str:
        logger.info("Starting audio classification")
        audio_array = self.preprocess_audio(audio_bytes)
        logger.info("Audio preprocessed, extracting features")
        inputs = self.extractor(
            audio_array,
            sampling_rate=self.sample_rate,
            truncation=False,
            return_tensors="pt"
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_class_id = logits.argmax(-1).item()
        predicted_label = self.model.config.id2label[predicted_class_id]
        logger.info("Audio classified successfully", extra={"class": predicted_label})
        return predicted_label