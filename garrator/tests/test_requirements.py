import chardet

def test_req_encoding(file_path='./requirements.txt'):
    """
    Test if the encoding of requirements.txt is utf-8 or utf-8-sig
    """

    with open(file_path, 'rb') as file:
        detector = chardet.universaldetector.UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()

    assert detector.result["encoding"].lower() in ["utf-8", "utf-8-sig"], "requirements.txt encoding error"