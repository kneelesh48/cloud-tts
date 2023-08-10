import os
from typing import List

import streamlit as st
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

st.set_page_config(page_title="Azure TTS", page_icon="🔊", layout="wide")

with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

speech_config = speechsdk.SpeechConfig(
    subscription=os.environ.get("SPEECH_KEY"),
    region=os.environ.get("SPEECH_REGION")
)

if not os.path.exists("temp"):
    os.makedirs("temp")

file_config = speechsdk.audio.AudioOutputConfig(filename="temp/audio.wav")

@st.cache_data
def list_languages() -> List[str]:
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)
    response = synthesizer.get_voices_async().get()
    locales = set([voice.locale for voice in response.voices])
    return [l for l in sorted(locales) if l.startswith("en")]

@st.cache_data
def list_voices(locale: str) -> List[str]:
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)
    result = synthesizer.get_voices_async(locale=locale).get()
    voices = sorted(result.voices, key=lambda voice: voice.short_name)

    l = []
    for voice in voices:
        name = voice.short_name
        gender = voice.gender.name
        l.append(f"{name} | {gender}")
    return l

@st.cache_data
def text_to_wav(voice_name: str, text: str) -> bytes:
    audio_config = speechsdk.audio.AudioOutputConfig(filename=f"temp/{voice_name}.wav")
    speech_config.speech_synthesis_voice_name = voice_name
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
    result = synthesizer.speak_text_async(text).get()
    return result.audio_data

st.title("Azure TTS")

with st.sidebar:
    options = list_languages()
    language = st.selectbox(
        "Select language",
        options=options,
        index=options.index("en-US"),
        key="language"
    )

    options = list_voices(str(language))
    voice_name = st.radio(
        "Select voice",
        options=options,
        index=0,
        key="voice_name"
    )

wavenet_description = """Microsoft Azure Text-to-Speech is a cloud-based service that allows developers to add natural-sounding speech synthesis to their applications. 
It provides a simple and scalable way to generate high-quality speech from text, with a variety of voices and languages to choose from.
"""
# The service uses deep neural networks to generate speech that is expressive and realistic, making it ideal for a wide range of applications, including virtual assistants, audiobooks, and voiceovers for movies and TV shows.

text = st.text_area("Text to synthesize", value=wavenet_description, height=400)

audio_content = text_to_wav(voice_name=str(voice_name).split(" | ")[0], text=text)
if isinstance(audio_content, bytes):
    st.audio(audio_content, format="audio/wav")
else:
    st.error(f"Error: {audio_content}")
