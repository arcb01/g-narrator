from garrator.app import App

if __name__ == '__main__':
    LANGUAGE = "en"     # Language for TTS
    VOICE_SPEED = 115   # Voice speed for TTS

    a = App(LANGUAGE, VOICE_SPEED)
    a.run()


    # TODO: Update documentation for this class
    # BUG: In region mode, define a minimum region if not enough pixels are selected
    # FIXME: hover color does not work
    # TODO: In region mode, clear screen when new region is selected
    # BUG: Some issue with window focus