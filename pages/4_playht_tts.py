"""PlayHT TTS"""

import os

import httpx
import streamlit as st
from dotenv import load_dotenv
from pyht import Client, TTSOptions, Format

load_dotenv()

st.set_page_config(page_title="PlayHT TTS", page_icon="🔊", layout="wide")

with open("static/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


@st.cache_resource
def get_client():
    client = Client(
        user_id=os.getenv("PLAYHT_USER_ID"),
        api_key=os.getenv("PLAYHT_API_KEY"),
    )
    return client


@st.cache_data
def list_voices() -> list[dict[str, str]]:
    url = "https://api.play.ht/api/v2/voices"

    headers = {
        "accept": "application/json",
        "X-USER-ID": os.getenv("PLAYHT_USER_ID"),
        "AUTHORIZATION": os.getenv("PLAYHT_API_KEY"),
    }

    response = httpx.get(url, headers=headers)

    voice_list = response.json()
    voice_list = [voice for voice in voice_list if voice["id"].endswith("manifest.json")]
    return voice_list


@st.cache_data
def text_to_wav(voice_name: str = "", text: str = ""):
    client = get_client()
    options = TTSOptions(
        voice=voice_name,
        sample_rate=44_100,
        format=Format.FORMAT_WAV,
        speed=1,
    )
    byte_stream = client.tts(text=text, voice_engine="PlayHT2.0-turbo", options=options)
    audio_content = b''.join(byte_stream)
    return audio_content


def get_voice_id(voice_name: str):
    for voice in filter(lambda voice: voice["name"] == voice_name.split(" | ")[0], voice_list):
        return voice['id']


st.title("PlayHT TTS")

with st.sidebar:
    voice_list = list_voices()

    locales = sorted(set([voice["language_code"] for voice in voice_list]))
    locale = st.selectbox("Select locale", options=locales, index=locales.index("en-US"), key="locale")

    voice_list = [voice for voice in voice_list if voice["language_code"] == locale]

    gender = st.selectbox("Select gender", options=["All", "Female", "Male"], index=0, key="gender")
    if gender != "All":
        voice_list = [voice for voice in voice_list if voice["gender"].title() == gender]

    options = [f"{voice['name']} | {str(voice['age']).title()} {str(voice['accent']).title()} {str(voice['gender']).title()} | {str(voice['texture']).title()} {str(voice['style']).title()}" for voice in voice_list]

    voice_name = st.radio("Select voice", options=options, index=0, key="voice_name")

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

text = st.text_area("Text to synthesize", value=wavenet_description, height=400)

audio_content = text_to_wav(voice_name=get_voice_id(voice_name), text=text)
if isinstance(audio_content, bytes):
    st.audio(audio_content, format="audio/wav")
else:
    st.error(f"Error: {audio_content}")
