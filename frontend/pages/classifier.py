import io
import streamlit as st
import requests
from streamlit_advanced_audio import WaveSurferOptions, audix
from pydub import AudioSegment

from logger import logger

# Set target frame rate
TIME_LIMIT_SECONDS = 30
FRAME_RATE = 16000

st.title("Heart Disease Classifier")
st.header("1. Upload Heart Auscultation Audio")

# File uploader for WAV, MP3, and OGG formats
uploaded_file = st.file_uploader(
    "Upload an audio file",
    type=["wav", "mp3", "ogg"],
    help="Supports WAV, MP3, and OGG formats",
)

if uploaded_file is not None:
    logger.info("File uploaded", extra={"file_name": uploaded_file.name})
    try:
        # Reset pointer and determine file format
        uploaded_file.seek(0)
        file_format = uploaded_file.name.split('.')[-1]
        # Load audio with pydub
        audio = AudioSegment.from_file(uploaded_file, format=file_format)
        logger.info("Audio file loaded successfully", extra={"format": file_format})
    except Exception as e:
        logger.exception("Error reading the audio file")
        st.error("Error reading the audio file: " + str(e))
        audio = None

    if audio is not None:
        # Resample if needed
        if audio.frame_rate != FRAME_RATE:
            logger.info("Resampling audio",
                        extra={"original_frame_rate": audio.frame_rate, "target_frame_rate": FRAME_RATE})
            audio = audio.set_frame_rate(FRAME_RATE)

        # Export the (possibly resampled) audio into an in-memory buffer
        out_audio = io.BytesIO()
        audio.export(out_audio, format="wav")
        out_audio.seek(0)

        st.subheader(f"2. Crop audio sample (up to {TIME_LIMIT_SECONDS} seconds)")
        result = audix(
            out_audio,
            wavesurfer_options=WaveSurferOptions(
                wave_color="#e17055", cursor_color="#d63031"
            ),
        )
        if result and "selectedRegion" in result and result["selectedRegion"]:
            # Assume result returns start and end times in seconds
            start = result["selectedRegion"].get("start", 0)
            end = result["selectedRegion"].get("end", 0)
            duration = end - start
            logger.info("Audio crop selected", extra={"start": start, "end": end, "duration": duration})

            # Crop the audio (pydub works in milliseconds)
            cropped_audio = audio[int(start * 1000): int(end * 1000)]

            # Export cropped audio to a BytesIO buffer
            cropped_buffer = io.BytesIO()
            cropped_audio.export(cropped_buffer, format="wav")
            cropped_buffer.seek(0)

            files = {"audio": ("cropped.wav", cropped_buffer, "audio/wav")}
            try:
                logger.info("Sending cropped audio to backend", extra={"duration": duration})
                response = requests.post("http://backend:8000/detector/get_audio_class", files=files)
                logger.info("Received response from backend",
                            extra={"status_code": response.status_code, "response_text": response.text})
                if response.ok:
                    response_data = response.json()
                    result_str = response_data.get("audio_class")
                    logger.info("result received successfully", extra={"result": result_str})
                    if result_str == "healthy":
                        st.success("Analysis Result: Normal heart sounds detected.")
                    elif result_str == "unhealthy":
                        st.error(
                            "Analysis Result: Abnormal heart sounds detected. Please consult a healthcare professional.")
                    else:  # Error during audio recording
                        st.warning(
                            "Error during audio recording. Please try to re-record or select a different fragment.")
                else:
                    st.error("Backend error: " + response.text)
                    logger.error("Backend returned an error",
                                 extra={"status_code": response.status_code, "response_text": response.text})
            except Exception as e:
                st.error("Error sending request to backend: " + str(e))
                logger.exception("Exception while sending request to backend")

            # If the user selects more than TIME_LIMIT_SECONDS seconds, limit to the first TIME_LIMIT_SECONDS seconds.
            if duration > TIME_LIMIT_SECONDS:
                st.warning(f"Warning: Selection is longer than {TIME_LIMIT_SECONDS} seconds. Limiting to the first {TIME_LIMIT_SECONDS} seconds.")
                logger.warning(f"Selection longer than {TIME_LIMIT_SECONDS} seconds; limiting to {TIME_LIMIT_SECONDS} seconds",
                               extra={"original_duration": duration})
                end = start + TIME_LIMIT_SECONDS
                duration = TIME_LIMIT_SECONDS

# Disclaimer
st.markdown(
    """
    <p style='font-size: 0.8em; color: grey; text-align: center;'>
        Disclaimer: The results provided by this classifier are not completely accurate and should not be considered a substitute for professional medical advice. Please consult a doctor for any health concerns.
    </p>
    """,
    unsafe_allow_html=True
)
