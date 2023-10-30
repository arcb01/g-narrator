from garrator.ocr import OCR
from garrator.narrator import Narrator

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
    # TODO
    pass