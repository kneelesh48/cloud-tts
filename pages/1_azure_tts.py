"""Azure TTS"""
# https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-text-to-speech

import os

import streamlit as st
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

st.set_page_config(page_title="Azure TTS", page_icon="🔊", layout="wide")

with open("static/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not os.path.exists("temp"):
    os.makedirs("temp")

speech_config = speechsdk.SpeechConfig(
    subscription=os.environ.get("SPEECH_KEY"), region=os.environ.get("SPEECH_REGION")
)

file_config = speechsdk.audio.AudioOutputConfig(filename="temp/audio.wav")


@st.cache_data
def list_locales() -> list[str]:
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

wavenet_description = """I had a dream we were sippin' whiskey neat
Highest floor, The Bowery, nowhere's high enough
Somewhere along the lines we stopped seein' eye to eye
You were stayin' out all night and I had enough
No, I don't wanna know where you been or where you're goin'
But I know I won't be home, and you'll be on your own
Who's gonna walk you through the dark side of the mornin'?
Who's gonna rock you when the sun won't let you sleep?
Who's wakin' up to drive you home when you're drunk and all alone?
Who's gonna walk you through the dark side of the mornin'?
It ain't me (The Bowery)
(Whiskey neat, grateful, I'm so grateful, I)
It ain't me (the Bowery)
(Whiskey neat, grateful, I'm so grateful, I)
It ain't me (the Bowery)
It ain't me (the Bowery)
(Whiskey neat, grateful, I'm so grateful, I)
It ain't me
I had a dream, we were back to 17
Summer nights and The Libertines, never growin' up
I'll take with me the Polaroids and the memories
But you know I'm gonna leave behind the worst of us
Who's gonna walk you through the dark side of the mornin'?
Who's gonna rock you when the sun won't let you sleep?
Who's wakin' up to drive you home when you're drunk and all alone?
Who's gonna walk you through the dark side of the mornin'?
It ain't me, no, no
It ain't me, no, no
It ain't me, no, no
Who's gonna walk you through the dark side of the mornin'?
It ain't me (the Bowery)
(Whiskey neat, grateful, I'm so grateful, I)
It ain't me (the Bowery)
It ain't me (grateful, I'm so grateful, I)
Ah, ooh (the Bowery)
Ah, ooh (whiskey neat, grateful, I'm so grateful, I)
Ah, ooh (it ain't me, the Bowery)
Ah, oh (whiskey neat, grateful, I'm so grateful, I)
It ain't me (the Bowery)
(Whiskey neat, grateful, I'm so grateful, I)
It ain't me, na, na, na, na-na, the Bowery
Na, na, na, na-na, whiskey neat (grateful, I'm so grateful, I)
It ain't me
"""
# The service uses deep neural networks to generate speech that is expressive and realistic, making it ideal for a wide range of applications, including virtual assistants, audiobooks, and voiceovers for movies and TV shows.

with st.sidebar:
    locales = list_locales()

    languages = sorted(set([l.split("-")[0] for l in locales]))
    language = st.selectbox("Select language", options=languages, index=languages.index("en"), key="language")

    locales2 = [l for l in locales if l.startswith(language)]
    locale = st.selectbox("Select locale", options=locales2, index=locales2.index("en-US") if language == "en" else 0, key="locale")

    voices = list_voices(locale)

    gender = st.selectbox("Select gender", options=["All", "Female", "Male"], index=0, key="gender")
    if gender != "All":
        voices = list(filter(lambda voice: voice.split(" | ")[-1] == gender, voices))

    voice_name = st.radio("Select voice", options=voices, index=0, key="voice_name")

text = st.text_area("Text to synthesize", value=wavenet_description, height=400)

audio_content = text_to_wav(voice_name=str(voice_name).split(" | ", maxsplit=1)[0], text=text)
if isinstance(audio_content, bytes):
    st.audio(audio_content, format="audio/wav")
else:
    st.error(f"Error: {audio_content}")
