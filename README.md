A simple streamlit app to test different TTS models from Google cloud and Azure

### Google TTS
* You will need a Google Cloud account
* git clone the repo
* Add your Google Service account JSON file and rename it to google-service-account.json
* streamlit run google_tts.py


### Azure TTS
* You will need an Azure account
* git clone the repo
* copy .env.example to .env and add your SPEECH_KEY and SPEECH_REGION from Azure
* Create output folder. This is where speech files will be saved as .wav files
* streamlit run azure_tts.py
