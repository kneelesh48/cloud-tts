"""Eleven Labs TTS"""

import os

import streamlit as st
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

st.set_page_config(page_title="Elevenlabs TTS", page_icon="🔊", layout="wide")

with open("static/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

@st.cache_data
def list_voices() -> list[str]:
    response = client.voices.get_all()
    return response.voices


@st.cache_data
def text_to_wav(voice_name: str = "Rachel", text: str = "") -> bytes:
    audio = client.generate(
        text=text,
        voice=voice_name,
        # voice_settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
    )

    audio_content = b"".join(audio)
    return audio_content

st.title("Elevenlabs TTS")

with st.sidebar:
    voice_list = list_voices()

    gender = st.selectbox("Select gender", options=['All', 'Female', 'Male'], index=0, key="gender")
    if gender != "All":
        voice_list = [voice for voice in voice_list if voice.labels['gender'].title() == gender]

    def format_func(voice):
        try:
            return f"{voice.name} | {voice.labels['age'].title()} {voice.labels['accent'].title()} {voice.labels['gender'].title()} | {voice.labels['description'].title()} {voice.labels['use case'].title()}"
        except KeyError:
            labels = list(voice.labels.values())
            return f"{voice.name} | {labels[1].title()} {labels[0].title()} | {labels[2].title()} | {labels[4].title()} {labels[3].title()}"

    voice = st.radio("Select voice", options=voice_list, index=0, key="voice_name", format_func=format_func)

wavenet_description = """This is a test of the Elevenlabs TTS service."""

text = st.text_area("Text to synthesize", value=wavenet_description, height=400)

audio_content = text_to_wav(voice_name=voice.name, text=text)
if isinstance(audio_content, bytes):
    st.audio(audio_content, format="audio/wav")
else:
    st.error(f"Error: {audio_content}")
