import io
import logging
import numpy as np
import torch
import librosa
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification

MODEL_CHECKPOINT = "Vladimirlv/ast-finetuned-audioset-10-10-0.4593-heart-sounds"
TIME_LIMIT_SECONDS = 10
SAMPLE_RATE = 16000

# Configure logging for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class Classifier:
    """
    A classifier for audio files using a pretrained audio classification model.

    This class handles the preprocessing of raw audio bytes, extraction of audio features
    using a pretrained feature extractor, and audio classification using a pretrained model.
    The model expects the audio input to be of a fixed length defined by the sample rate
    and a time limit (default: 10 seconds).
    """

    def __init__(self):
        """
        Initialize the Classifier with a pretrained feature extractor and model.

        Loads the model and feature extractor from the specified checkpoint, sets the model
        to evaluation mode, and defines the target length for audio based on the sample rate
        and time limit.
        """
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
        """
        Preprocess raw audio bytes into a numpy array of fixed length.

        The audio is loaded using librosa with the specified sample rate. If the audio is
        shorter than the target length, it is padded with zeros; if it is longer, it is truncated.

        Parameters:
            audio_bytes (bytes): Raw audio file bytes.

        Returns:
            np.ndarray: A numpy array representing the preprocessed audio waveform.
        """
        logger.info("Preprocessing audio")
        audio_buffer = io.BytesIO(audio_bytes)
        audio_array, sr = librosa.load(audio_buffer, sr=self.sample_rate)
        logger.info("Audio loaded: sample rate %s, length %s", sr, len(audio_array))
        # Pad or truncate the audio to have a fixed length
        if len(audio_array) < self.target_length:
            logger.info("Padding audio from length %s to target length %s", len(audio_array), self.target_length)
            audio_array = np.pad(audio_array, (0, self.target_length - len(audio_array)), mode='constant')
        else:
            logger.info("Truncating audio from length %s to target length %s", len(audio_array), self.target_length)
            audio_array = audio_array[:self.target_length]
        return audio_array

    def classify_audio(self, audio_bytes: bytes) -> str:
        """
        Classify audio from raw file bytes.

        The method preprocesses the input audio bytes, extracts features using the pretrained
        feature extractor, performs inference with the pretrained audio classification model, and
        returns the predicted class label.

        Parameters:
            audio_bytes (bytes): Raw audio file bytes.

        Returns:
            str: The predicted class label.
        """
        logger.info("Starting audio classification")
        # Preprocess the audio from the file bytes
        audio_array = self.preprocess_audio(audio_bytes)
        logger.info("Audio preprocessed, extracting features")
        inputs = self.extractor(
            audio_array,
            sampling_rate=self.sample_rate,
            truncation=False,
            return_tensors="pt"
        )
        # Run inference without gradient calculations
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_class_id = logits.argmax(-1).item()
        predicted_label = self.model.config.id2label[predicted_class_id]
        logger.info("Audio classified successfully", extra={"class": predicted_label})
        return predicted_label
