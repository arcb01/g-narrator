from gnarrator.ocr import OCR
from gnarrator.TTS import Narrator
from gnarrator.app import App, ReadingEngine
import subprocess

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

    try:
        subprocess.run(['gnarrator'], stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Subprocess failed with return code {e.returncode}, stderr output: {e.stderr}")
        raise
