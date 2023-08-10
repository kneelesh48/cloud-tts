A simple streamlit app to test different TTS models from Azure and Google cloud

### Steps to run
Clone the Repository `git clone https://github.com/kneelesh48/streamlit-tts.git`

### Azure TTS
* Copy `.env.example` to `.env` and add your SPEECH_KEY and SPEECH_REGION from Azure
* Speech files will be saved as .wav files in `outputs` folder
* Run the streamlit app `streamlit run azure_tts.py`

### Google TTS
* Add your Google Service account JSON file and rename it to google-service-account.json
* Run the streamlit app `streamlit run google_tts.py`
