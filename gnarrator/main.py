from gnarrator.app import App

if __name__ == '__main__':
    LANGUAGE = "es"     # Language for TTS
    VOICE_SPEED = 115   # Voice speed for TTS

    gnarrator = App(LANGUAGE, VOICE_SPEED)
    gnarrator.run()
