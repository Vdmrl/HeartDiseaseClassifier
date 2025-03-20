import io
import time
import streamlit as st
import requests
from streamlit_advanced_audio import WaveSurferOptions, audix
from pydub import AudioSegment
from logger import logger

def run_classifier():
    # Set target frame rate and time limit.
    TIME_LIMIT_SECONDS = 30
    FRAME_RATE = 16000

    st.header("1. Upload Heart Auscultation Audio")

    # Get the access token from session state
    token = st.session_state.get("access_token")
    if not token:
        st.error("Authentication required! Please log in first.")
        return

    headers = {"Authorization": f"Bearer {token}"}

    uploaded_file = st.file_uploader(
        "Upload an audio file",
        type=["wav", "mp3", "ogg"],
        help="Supports WAV, MP3, and OGG formats",
    )

    if uploaded_file is not None:
        logger.info("File uploaded", extra={"file_name": uploaded_file.name})
        try:
            uploaded_file.seek(0)
            file_format = uploaded_file.name.split('.')[-1]
            audio = AudioSegment.from_file(uploaded_file, format=file_format)
            logger.info("Audio file loaded successfully", extra={"format": file_format})
        except Exception as e:
            logger.exception("Error reading the audio file")
            st.error("Error reading the audio file: " + str(e))
            audio = None

        if audio is not None:
            if audio.frame_rate != FRAME_RATE:
                logger.info("Resampling audio",
                            extra={"original_frame_rate": audio.frame_rate, "target_frame_rate": FRAME_RATE})
                audio = audio.set_frame_rate(FRAME_RATE)

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
                start = result["selectedRegion"].get("start", 0)
                end = result["selectedRegion"].get("end", 0)
                duration = end - start
                logger.info("Audio crop selected", extra={"start": start, "end": end, "duration": duration})

                cropped_audio = audio[int(start * 1000): int(end * 1000)]
                cropped_buffer = io.BytesIO()
                cropped_audio.export(cropped_buffer, format="wav")
                cropped_buffer.seek(0)

                if duration > TIME_LIMIT_SECONDS:
                    st.warning(
                        f"Warning: Selection is longer than {TIME_LIMIT_SECONDS} seconds. Limiting to the first {TIME_LIMIT_SECONDS} seconds.")
                    logger.warning("Selection longer than allowed; limiting duration",
                                   extra={"original_duration": duration})

                files = {"audio": ("cropped.wav", cropped_buffer, "audio/wav")}

                try:
                    logger.info("Sending cropped audio to backend for asynchronous classification",
                                extra={"duration": duration})
                    # Add headers to the request
                    response = requests.post(
                        "http://backend:8000/detector/classify_audio",
                        files=files,
                        headers=headers,
                        timeout=3600
                    )
                    logger.info("Received response from backend",
                                extra={"status_code": response.status_code, "response_text": response.text})
                    if response.ok:
                        task_id = response.json().get("task_id")
                        with st.spinner("Waiting for classification result..."):
                            result_data = None
                            max_attempts = 1000
                            attempt = 0
                            while result_data is None and attempt < max_attempts:
                                try:
                                    # Add headers to the result request
                                    result_response = requests.get(
                                        f"http://backend:8000/detector/classify_audio/result/{task_id}",
                                        headers=headers,
                                        timeout=3600
                                    )
                                    if result_response.status_code == 200:
                                        result_data = result_response.json()
                                    else:
                                        time.sleep(2)
                                        attempt += 1
                                except Exception as e:
                                    logger.exception("Error while polling classification result", extra={"error": str(e)})
                                    time.sleep(2)
                                    attempt += 1

                        if result_data is None:
                            st.error("Timed out waiting for classification result. Try again later")
                        else:
                            audio_class = result_data.get("audio_class")
                            if audio_class == "healthy":
                                st.success("Analysis Result: Normal heart sounds detected.")
                            elif audio_class == "unhealthy":
                                st.error("Analysis Result: Abnormal heart sounds detected. Please consult a healthcare professional.")
                            else:
                                st.warning("Error during audio recording. Please try to re-record or select a different fragment.")
                    else:
                        st.error("Backend error: " + response.text)
                        logger.error("Backend returned an error",
                                     extra={"status_code": response.status_code, "response_text": response.text})
                except Exception as e:
                    st.error("Error sending request to backend: " + str(e))
                    logger.exception("Exception while sending request to backend")

    st.markdown(
        """
        <p style='font-size: 0.8em; color: grey; text-align: center;'>
            Disclaimer: The results provided by this classifier are not completely accurate and should not be considered a substitute for professional medical advice. Please consult a doctor for any health concerns.
        </p>
        """,
        unsafe_allow_html=True
    )