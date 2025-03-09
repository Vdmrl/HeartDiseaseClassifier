import base64
import io
import numpy as np
import torch
import librosa
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification

MODEL_CHECKPOINT = "Vladimirlv/ast-finetuned-audioset-10-10-0.4593-heart-sounds"
TIME_LIMIT_SECONDS = 10
SAMPLE_RATE = 16000


class Classifier:
    """
        A classifier for audio files using a pretrained audio classification model.

        This class decodes a base64-encoded audio string, preprocesses the audio
        to ensure a fixed length, extracts features using a pretrained feature extractor,
        and performs classification with a pretrained audio classification model.
    """

    def __init__(self):
        """
            Initialize the Classifier with a pretrained feature extractor and model.

            The model is set to evaluation mode. The target length for audio is defined
            based on the sample rate and time limit (10 seconds).
        """
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
            Preprocess audio file bytes.

            This method reads the audio from bytes using librosa with the specified
            sample rate and ensures that the resulting audio array is exactly the
            target length by padding or truncating as necessary.

            Parameters:
                audio_bytes (bytes): Raw audio file bytes.

            Returns:
                np.ndarray: A numpy array representing the preprocessed audio waveform.
        """
        audio_buffer = io.BytesIO(audio_bytes)
        audio_array, sr = librosa.load(audio_buffer, sr=self.sample_rate)
        # Pad or truncate the audio to have a fixed length
        if len(audio_array) < self.target_length:
            audio_array = np.pad(audio_array, (0, self.target_length - len(audio_array)), mode='constant')
        else:
            audio_array = audio_array[:self.target_length]
        return audio_array

    def classify_audio(self, audio_base64: str):
        """
            Classify audio from a base64-encoded string.

            This method preprocesses the audio, extracts features using the pretrained feature extractor,
            performs inference with the pretrained audio classification model, and returns the predicted class label.

            Parameters:
                audio_base64 (str): Base64 encoded audio data.

            Returns:
                str: The predicted class label.
        """
        # Preprocess the audio from the base64 string
        audio_array = self.preprocess_audio(audio_base64)
        # Extract features without truncation, as we fixed the length manually
        inputs = self.extractor(
            audio_array,
            sampling_rate=self.sample_rate,
            truncation=False,
            return_tensors="pt"
        )
        # Run inference
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Select the class with the highest logit
        logits = outputs.logits
        predicted_class_id = logits.argmax(-1).item()
        predicted_label = self.model.config.id2label[predicted_class_id]
        return predicted_label
