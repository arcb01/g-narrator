from gnarrator.app import App
import click


@click.command()
@click.option('--language', default="en", help="Language setting")
@click.option('--voice-rate', default="+0%", help="Voice rate setting")
@click.option('--voice-volume', default="+0%", help="Voice volume setting")
@click.option('--gender', default="male", help="Gender setting")
def _main(language, voice_rate, voice_volume, gender):
    """
    Main function
    """
    
    settings = {
                "LANGUAGE": language,
                "VOICE_RATE": voice_rate,
                "VOICE_VOLUME": voice_volume,
                "GENDER": gender
                }

    # Start the app
    gnarrator = App(settings)
    gnarrator.run()


if __name__ == '__main__':
    _main()
    
  
