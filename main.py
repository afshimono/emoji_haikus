import click

from text_to_speech.main import generate_speech

@click.command()
@click.argument('episode_name', envvar='EPISODE_NAME', type=str)
@click.argument('episode_theme', envvar='EPISODE_THEME', type=str)
def main(episode_name:str, episode_theme:str):
    print(f"Today in our episode {episode_name} Emoji-Haikus, we will write about {episode_theme}")


if __name__ == "__main__":
    main()
