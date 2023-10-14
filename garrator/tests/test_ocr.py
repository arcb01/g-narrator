from garrator.modules.ocr import OCR

def test_ocr_init():
    """
    Test that the OCR object initialises properly
    """

    ocr = OCR()
    assert ocr is not None