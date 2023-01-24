
from modules.app import App, settings

if __name__ == '__main__':
    # 1. Settings
    lang = "en"
    gpu = True
    voice_speed = 150
    # 2. Run App
    tts, ocr = settings(lang, gpu, voice_speed)
    a = App(tts, ocr)
    a.run() 