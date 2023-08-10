A simple streamlit app to test different TTS models from Azure and Google cloud

### Try online
* Azure TTS [https://azure-tts.streamlit.app/](https://azure-tts.streamlit.app/)
* Google TTS [https://gcloud-tts.streamlit.app/](https://gcloud-tts.streamlit.app/)

### Steps to run locally
Clone the Repository `git clone https://github.com/kneelesh48/streamlit-tts.git`

#### Azure TTS
* Copy `.env.example` to `.env` and add your `SPEECH_KEY` and `SPEECH_REGION` from Azure
* Speech files will be saved as .wav files in `outputs` folder
* Run the streamlit app `streamlit run azure_tts.py`

#### Google TTS
* Add your Google Service account JSON file and rename it to google-service-account.json
* Run the streamlit app `streamlit run google_tts.py`

### Features
* Select a locale, only English locales are available in the app and en-US is selected by default.
* Select one of the voices listed for that locale.
* Input test you'd like to systhesize and press Ctrl+Enter to generate audio output of the text
* When you switch voices, new output is generated automatically
* You play play the audio or download it if you want
