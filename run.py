
from modules.app import App, settings
import argparse

if __name__ == '__main__':
    # Arguments for CLI
    parser = argparse.ArgumentParser(description="Gaming Narrator")
    parser.add_argument("--lang", type=str, help="Language for TTS", default="en")
    parser.add_argument("--gpu", type=bool, help="Use GPU for OCR", default=True)
    parser.add_argument("--voice_speed", type=int, help="Voice speed for TTS", default=150)
    args = parser.parse_args()

    tts, ocr = settings(args.lang, args.gpu, args.voice_speed)
    a = App(tts, ocr)
    a.run() 