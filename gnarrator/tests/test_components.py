from gnarrator.ocr import OCR
from gnarrator.TTS import Narrator

def test_ocr():
    """
    Test that the reading engine works properly
    """

    ocr = OCR()

    assert ocr is not None

def test_narrator():
    """
    Test that the narrator works properly
    """
    
    sample_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
    tts = Narrator(voice=sample_voice, voice_speed=115)
    
    assert tts is not None


# NOTE: Seems like pytest doesn't work well when testing with a GUI (PyQt5)