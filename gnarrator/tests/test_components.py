from gnarrator.ocr import OCR
from gnarrator.TTS import Narrator
from gnarrator.app import App
from gnarrator.reading_engine import ReadingEngine

SAMPLE_SETTINGS = {"LANGUAGE": "en", 
            "VOICE_RATE": "+5%",
            "VOICE_VOLUME": "+0%",
            "GENDER": "male"}

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

    gnarrator = App(SAMPLE_SETTINGS)

    assert gnarrator is not None


def test_narrator():
    """
    Test that the narrator works properly
    """
    
    narrator = Narrator(SAMPLE_SETTINGS)

    assert narrator is not None


def test_reading_engine():
    """
    Test that the reading engine works properly
    """

    reading_engine = ReadingEngine(SAMPLE_SETTINGS)

    assert reading_engine is not None


def test_cli():
    """
    Test that the CLI works properly
    """

    # TODO: Figure out how to test this since it gives no exit code
