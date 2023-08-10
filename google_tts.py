import os
from typing import Sequence

import requests
import streamlit as st
from dotenv import load_dotenv
import google.cloud.texttospeech as tts

load_dotenv()

st.set_page_config(page_title="Google WaveNet", page_icon="🔊", layout="wide")

with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not os.path.exists("google-service-account.json"):
    url = os.environ.get("GOOGLE_API_KEY_URL")
    with open("google-service-account.json", "w") as f:
        f.write(requests.get(url).text)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-service-account.json"

client = tts.TextToSpeechClient()

st.title("Google WaveNet")

wavenet_description = """Google WaveNet is a deep neural network-based generative model for speech synthesis. 
It uses raw audio waveforms as input and generates high-quality speech in a variety of languages and voices.
"""
# WaveNet is known for its ability to produce natural-sounding speech with a high degree of expressiveness and realism.
# It has been used in a variety of applications, including virtual assistants, audiobooks, and voiceovers for movies and TV shows.
# WaveNet is available as part of Google's Cloud Text-to-Speech API, which provides a simple and scalable way to generate high-quality speech from text.

with st.sidebar:
    def unique_languages_from_voices(voices: Sequence[tts.Voice]) -> list:
        language_set = set()
        for voice in voices:
            for language_code in voice.language_codes:
                language_set.add(language_code)
        return sorted(language_set)

    @st.cache_data
    def list_languages() -> list:
        response = client.list_voices()
        languages = unique_languages_from_voices(response.voices)
        return [l for l in languages if l.startswith("en")]

    options = list_languages()
    language = st.selectbox(
        "Select language", 
        options=options, 
        index=options.index("en-US")
    )

    @st.cache_data
    def list_voices(language_code: str) -> list[str]:
        response = client.list_voices(language_code=language_code)
        voices = sorted(response.voices, key=lambda voice: voice.name)

        l = []
        for voice in voices:
            if voice.name.startswith(language_code):
                name = voice.name
                gender = tts.SsmlVoiceGender(voice.ssml_gender).name
                l.append(f"{name} | {gender.title()}")
        return l

    options = list_voices(str(language))
    voice_name = st.radio("Select voice", options=options, index=0, key="voice_name")


text = st.text_area("Text to synthesize", value=wavenet_description, height=400)


@st.cache_data
def text_to_wav(voice_name: str = "", text: str = ""):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()

    try:
        response = client.synthesize_speech(
            input=text_input,
            voice=voice_params,
            audio_config=audio_config,
        )
    except Exception as exc:
        return exc
    else:
        return response.audio_content


audio_content = text_to_wav(voice_name=str(voice_name).split(" | ")[0], text=text)
if isinstance(audio_content, bytes):
    st.audio(audio_content, format="audio/wav")
else:
    st.error(f"Error: {audio_content}")
