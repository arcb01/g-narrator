from app import App, settings

def main():
    LANGUAGE = "en"     # Language for TTS
    GPU = True          # Use GPU for OCR
    VOICE_SPEED = 150   # Voice speed for TTS

    tts, ocr = settings(LANGUAGE, GPU, VOICE_SPEED)
    a = App(tts, ocr)
    a.run()
    
if __name__ == '__main__':
    main()