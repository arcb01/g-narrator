from gnarrator.app import App

if __name__ == '__main__':
    # Settings for TTS and OCR
    settings = {"LANGUAGE": "en", 
                "VOICE_RATE": "+5%",
                "VOICE_VOLUME": "+0%",
                "GENDER": "male"}
    
    gnarrator = App(settings)
    gnarrator.run()
