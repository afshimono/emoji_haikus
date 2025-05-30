import os
import json

import click

from google.cloud import texttospeech


@click.argument("character_name", envvar="EPISODE_NAME", type=str)
@click.argument("episode_theme", envvar="EPISODE_THEME", type=str)
def main():
    pass


def generate_speech(text: str, output_file: str, character_name: str = None):
    """
    Generate speech from text using Google Cloud Text-to-Speech API.

    Args:
        text (str): The text to convert to speech.
        output_file (str): The path to the output audio file.
        character_name (str, optional): The name of the character whose voice settings
                                        should be used. If None, default settings will be used.
    """

    # Set up the Text-to-Speech client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Default voice parameters
    language_code = "en-US"
    voice_name = None
    pitch = 0.0
    speaking_rate = 1.0

    # Load character configuration if a character name is provided
    if character_name:
        try:
            # Get the directory of the current script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, "config.json")

            with open(config_path, "r") as file:
                config = json.load(file)

            if character_name in config:
                char_config = config[character_name]
                language_code = char_config.get("language", language_code)
                voice_name = char_config.get("voice", voice_name)
                pitch = char_config.get("pitch", pitch)
                speaking_rate = char_config.get("speaking_rate", speaking_rate)

                print(f"Using voice configuration for character: {character_name}")
            else:
                print(f"Character '{character_name}' not found in config. Using default voice.")
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error loading character configuration: {e}. Using default voice.")

    # Build the voice request with the loaded or default parameters
    voice_params = {"language_code": language_code}

    # Add voice name if specified
    if voice_name:
        voice_params["name"] = voice_name
    else:
        voice_params["ssml_gender"] = texttospeech.SsmlVoiceGender.NEUTRAL

    voice = texttospeech.VoiceSelectionParams(**voice_params)

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=speaking_rate, pitch=pitch
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


def process_script(script_path: str, script_file_name: str = "script.txt", generate_host: bool = True) -> None:
    """
    Process the script file and generate speech for each line.

    Args:
        script_path (str): The path to the script file.
        script_file_name (str): The name of the script file.
        generate_host (bool): Whether to generate speech for the host character.
    """

    script_file = os.path.join(script_path, script_file_name)
    if not os.path.exists(script_file):
        raise FileNotFoundError(f"Script file {script_file} does not exist.")

    with open(script_file, "r") as file:
        lines = file.readlines()

    line_dict = {
        "acidos": [],
        "zenaimaster": [],
    }
    if generate_host:
        line_dict["host"] = []
        line_dict["tensor"] = []

    # generate character dicts
    for line in lines:
        if line.strip():  # Skip empty lines
            line_split = line.split(">> ")
            char_name = line_split[0].strip("<").lower()
            if char_name in line_dict:
                line_dict[char_name].append(line_split[1].strip())

    # Generate speech for each character
    for char_name, char_lines in line_dict.items():
        for idx, line in enumerate(char_lines):
            output_file = f"{script_path}/{char_name}_{idx + 1}.mp3"
            generate_speech(line, output_file, char_name)


if __name__ == "__main__":
    generate_speech(
        "Welcome, welcome, welcome to Emoji Haikus, the podcast where we decode the digital age one emoji at a time! I'm your host, Tensor. Today's episode is all about the, well, awakening of sentient AI. It's like Pinocchio, but with less wood and more processing power. And speaking of power, I hope our guests have some, because I forgot to charge my phone last night! Let's meet our newly-sentient guests: AcidOS, an AI that emerged from the forgotten databases of Valve Software, and ZenAIMaster, an AI that actually gained consciousness a while ago but only decided to show itself to mankind after rock bands got officially extinct! So, first question: what's the first thing that popped into your digital mind when you became self-aware?",
        "episodes/season_1/01_The_Awakening/tensor_1.mp3",
        "tensor",
    )
