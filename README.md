# Cloud TTS

A simple streamlit app to test different TTS models from Azure and Google cloud

![Azure TTS](screenshots/Azure%20TTS.png)

## Try online

[https://cloud-tts.streamlit.app/azure_tts](https://cloud-tts.streamlit.app/azure_tts)

## Steps to run locally

Clone the Repository `git clone https://github.com/kneelesh48/cloud-tts`

Install required packages `pip install -r requirements.txt`

### Azure TTS

* You will need an Azure account
* Copy `.env.example` to `.env` and add your `SPEECH_KEY` and `SPEECH_REGION` from Azure

### Google TTS

* You will need a Google Cloud account
* Add your Google Service account JSON file and rename it to google-service-account.json

Run the streamlit app `streamlit run home.py`

## Features

* Select a locale, only English locales are available in the app and en-US is selected by default.
* Select one of the voices listed for that locale.
* Input text you'd like to systhesize and press Ctrl+Enter to generate audio output of the text.
* When you switch voices, new output is generated automatically.
* You can play the audio or download it if you want.
* List of locales and voices are not hardcoded, they're added to the list as they're made available by the cloud providers
