import os

import streamlit as st
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

st.set_page_config(page_title="Azure TTS", page_icon="🔊", layout="wide")

with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not os.path.exists("temp"):
    os.makedirs("temp")

speech_config = speechsdk.SpeechConfig(
    subscription=os.environ.get("SPEECH_KEY"), region=os.environ.get("SPEECH_REGION")
)

file_config = speechsdk.audio.AudioOutputConfig(filename="temp/audio.wav")


@st.cache_data
def list_languages() -> list[str]:
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=file_config
        )
    response = synthesizer.get_voices_async().get()
    locales = set([voice.locale for voice in response.voices])
    return sorted(locales)


@st.cache_data
def list_voices(locale: str) -> list[str]:
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=file_config
        )
    result = synthesizer.get_voices_async(locale=locale).get()
    voices = sorted(result.voices, key=lambda voice: voice.short_name)

    return [f"{voice.short_name} | {voice.gender.name}" for voice in voices]


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

wavenet_description = """Microsoft Azure Text-to-Speech is a cloud-based service that allows developers to add natural-sounding speech synthesis to their applications. 
It provides a simple and scalable way to generate high-quality speech from text, with a variety of voices and languages to choose from.
"""
# The service uses deep neural networks to generate speech that is expressive and realistic, making it ideal for a wide range of applications, including virtual assistants, audiobooks, and voiceovers for movies and TV shows.

with st.sidebar:
    locales = list_languages()

    languages = sorted(set([l.split("-")[0] for l in locales]))
    language = st.selectbox("Select language", options=languages, index=languages.index("en"), key="language")

    locales2 = [l for l in locales if l.startswith(language)]
    locale = st.selectbox("Select locale", options=locales2, index=locales2.index("en-US") if language == "en" else 0, key="locale")

    voices = list_voices(locale)

    gender = st.selectbox("Select gender", options=["All", "Female", "Male"], index=0, key="gender")
    if gender != "All":
        voices = [voice for voice in voices if voice.split(" | ")[-1] == gender]

    voice_name = st.radio("Select voice", options=voices, index=0, key="voice_name")

text = st.text_area("Text to synthesize", value=wavenet_description, height=400)

audio_content = text_to_wav(voice_name=str(voice_name).split(" | ")[0], text=text)
if isinstance(audio_content, bytes):
    st.audio(audio_content, format="audio/wav")
else:
    st.error(f"Error: {audio_content}")
