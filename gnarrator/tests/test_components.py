from gnarrator.ocr import OCR
from gnarrator.TTS import Narrator
from gnarrator.app import App, ReadingEngine

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




    assert gnarrator is not None


def test_narrator():
    """
    Test that the narrator works properly
    """
    
    VOICE = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
    VOICE_SPEED = 115 

    narrator = Narrator(VOICE, VOICE_SPEED)

    assert narrator is not None


def test_reading_engine():
    """
    Test that the reading engine works properly
    """

    LANGUAGE = "en"    
    VOICE_SPEED = 115 

    reading_engine = ReadingEngine(LANGUAGE, VOICE_SPEED)

    assert reading_engine is not None


# FIXME: Works locally, not in github actions
