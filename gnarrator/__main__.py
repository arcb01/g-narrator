from gnarrator.app import App
import click


@click.command()
@click.option('--language', default="en", help="Language of the voice")
@click.option('--voice-rate', default="+0%", help="Voice speed")
@click.option('--voice-volume', default="+0%", help="Voice volume setting")
@click.option('--gender', default="male", help="Voice gender setting")
@click.option('--apperance', default="light", help="Apperance setting")
def _main(language="en", voice_rate="+0%", voice_volume="+0%", gender="male", apperance="light"):
    
    settings = {
                "LANGUAGE": language,
                "VOICE_RATE": voice_rate,
                "VOICE_VOLUME": voice_volume,
                "GENDER": gender,
                "APPERANCE": apperance
                }

    # Start the app
    gnarrator = App(settings)
    gnarrator.run()


if __name__ == '__main__':
    _main()
    
  
