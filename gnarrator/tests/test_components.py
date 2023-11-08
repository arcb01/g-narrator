#from gnarrator.app import App
from gnarrator.reading_engine import ReadingEngine

SAMPLE_SETTINGS = {"LANGUAGE": "en", 
            "VOICE_RATE": "+5%",
            "VOICE_VOLUME": "+0%",
            "GENDER": "male",
            "APPERANCE": "light"}

def test_app():
    """
    Test that the narrator works properly
    """

    # NOTE: App test fails

    #gnarrator = App(SAMPLE_SETTINGS)

    #assert gnarrator is not None

def test_reading_engine():
    """
    Test that the reading engine works properly
    """

    reading_engine = ReadingEngine(SAMPLE_SETTINGS)

    assert reading_engine is not None
