import streamlit as st

st.set_page_config(page_title="Cloud TTS", page_icon="🔊", layout="wide")

with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Cloud TTS")

st.write("Synthesize Text to Speech using latest models from Google Cloud and Azure.")
st.write("Select azure tts or google tts from the sidebar, to get started")
st.write("Select a language and voice from the sidebar, then enter some text to synthesize.")
