# emoji_haikus
The podcast where humans and machines speak freely. 

How it will work?
The `main.py` file in the root of the project will coordinate the creation of the podcast episode based on the episode name and theme.

### Installation and Usage using UV
Have UV installed:

run `uv sync`

### generate scripts
Run the main.py file with the `EPISODE_NAME` and `EPISODE_THEME` env variables set.
This will generate a script based on the instructions in the `base`folder.

### text_to_speech
This module uses Google CHIRP to generate voice from a given input text.
The function `process_script` will read the script generated and create multiple .mp3 files for each participant of the episode.
If the `generate_host`argument is set to `False`, it will not generate the Host lines.

### Sample
You can find the first episode after being editted in CapCut in the `samples` folder. The name of the file is `final_version.mp3`.

### TODO

- [x] Script generation
- [x] Text to Speech
- [ ] Automatic episode edition

### References

Langchain Google AI - https://python.langchain.com/docs/integrations/chat/google_generative_ai/
Write to Cloud Storage 
https://cloud.google.com/appengine/docs/legacy/standard/python/googlecloudstorageclient/read-write-to-cloud-storage
https://cloud.google.com/storage/docs/uploading-objects-from-memory
List of Google Supported Voices - https://cloud.google.com/text-to-speech/docs/list-voices-and-types#list_of_all_supported_languages
Text to Speech sample 
https://cloud.google.com/text-to-speech/docs/create-audio-text-client-libraries#create_audio_data
https://cloud.google.com/text-to-speech/docs/samples/tts-quickstart?hl=en