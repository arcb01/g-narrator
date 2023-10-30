from garrator.app import App

if __name__ == '__main__':
    LANGUAGE = "en"     # Language for TTS
    VOICE_SPEED = 115   # Voice speed for TTS

    a = App(LANGUAGE, VOICE_SPEED)
    a.run()