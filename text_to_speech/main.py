from google.cloud import texttospeech


def generate_speech(text:str, output_file:str):
    """
    Generate speech from text using Google Cloud Text-to-Speech API.

    Args:
        text (str): The text to convert to speech.
        output_file (str): The path to the output audio file.
    """
    # Set up the Text-to-Speech client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_file, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f"Audio content written to file {output_file}")

if __name__ == "__main__":
    # Example usage
    text = 'Hello, Mr. Fodson, how are you doing <prosody rate="0.8x">today?'
    output_file = "output.mp3"
    generate_speech(text, output_file)