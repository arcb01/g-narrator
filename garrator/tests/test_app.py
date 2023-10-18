from ..app import App, settings

def test_app_init():
    """
    Test that the App object initialises properly
    """

    LANGUAGE = "en"     # Language for TTS
    GPU = True          # Use GPU for OCR
    VOICE_SPEED = 150   # Voice speed for TTS

    tts, ocr = settings(LANGUAGE, GPU, VOICE_SPEED)
    a = App(tts, ocr)

    assert a is not None