from garrator.app import App

if __name__ == '__main__':
    LANGUAGE = "en"     # Language for TTS
    VOICE_SPEED = 115   # Voice speed for TTS

    a = App(LANGUAGE, VOICE_SPEED)
    a.run()

    # BUG: In region mode, define a minimum region if not enough pixels are selected
    # BUG: Some issue with window focus
    # BUG: Sometimes can ocurr that the language from the keybaord changes and therefore keyboard input stops working
    # BUG: If you click the window while narrator is reading the program crashes
    
    # FIXME: hover color does not work
    # FIXME: Maybe adding quit to the main app fixes the issue of not being able to clear the screen unless clicked

    # TODO: Update documentation
    # TODO: In region mode, clear screen when new region is selected
    # TODO: Read actumatically if  only 1 box
    # TODO: Mouse key bindings
    