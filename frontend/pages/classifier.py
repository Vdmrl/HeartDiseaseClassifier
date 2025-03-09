import io
import streamlit as st
import requests
from streamlit_advanced_audio import WaveSurferOptions, audix
from pydub import AudioSegment

# set target frame rate
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
    try:
        # Reset pointer and determine file format
        uploaded_file.seek(0)
        file_format = uploaded_file.name.split('.')[-1]
        # Load audio with pydub
        audio = AudioSegment.from_file(uploaded_file, format=file_format)
    except Exception as e:
        st.error("Error reading the audio file: " + str(e))
        audio = None

    if audio is not None:
        # Resample if needed
        if audio.frame_rate != FRAME_RATE:
            audio = audio.set_frame_rate(FRAME_RATE)

        # Export the (possibly resampled) audio into an in-memory buffer
        out_audio = io.BytesIO()
        audio.export(out_audio, format="wav")
        out_audio.seek(0)

        st.subheader("2. Crop audio sample (up to 10 seconds)")
        result = audix(
            out_audio,
            wavesurfer_options=WaveSurferOptions(
                wave_color="#e17055", cursor_color="#d63031"
            ),
        )
        if result and "selectedRegion" in result.keys():
            # Assume result returns start and end times in seconds
            start = result["selectedRegion"].get("start", 0)
            end = result["selectedRegion"].get("end", 0)
            duration = end - start

            # If the user selects more than 10 seconds, limit to the first 10 seconds.
            if duration > 10:
                st.warning("Selection is longer than 10 seconds. Limiting to the first 10 seconds.")
                end = start + 10
                duration = 10
            else:
                # Crop the audio (pydub works in milliseconds)
                cropped_audio = audio[start * 1000: end * 1000]

                # Export cropped audio to a BytesIO buffer
                cropped_buffer = io.BytesIO()
                cropped_audio.export(cropped_buffer, format="wav")
                cropped_buffer.seek(0)

                # Send the cropped result to the backend only if its duration is less than 10 seconds.
                if duration < 10:
                    files = {"file": ("cropped.wav", cropped_buffer, "audio/wav")}
                    try:
                        response = requests.post("http://backend:8000/detector/get_audio_class", files=files)
                        if response.ok:
                            result_str = response.text
                            st.write("Detected Audio Class:", result_str)
                        else:
                            st.error("Backend error: " + response.text)
                    except Exception as e:
                        st.error("Error sending request to backend: " + str(e))
                else:
                    st.info("Cropped audio is 10 seconds long and was not sent to the backend.")
