from gnarrator.ocr import OCR
from gnarrator.TTS import Narrator
from gnarrator.app import App

def test_ocr():
    """
    Test that the reading engine works properly
    """

    ocr = OCR()

    assert ocr is not None

def test_app():
    """
    Test that the narrator works properly
    """
    
    LANGUAGE = "en"    
    VOICE_SPEED = 115 

    gnarrator = App(LANGUAGE, VOICE_SPEED)

    # FIXME: Works locally, not in github actions

    #sample_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
    #tts = Narrator(voice=sample_voice, voice_speed=115)
    
    #assert tts is not None
    assert gnarrator is not None


# NOTE: Seems like pytest doesn't work well when testing with a GUI (PyQt5)