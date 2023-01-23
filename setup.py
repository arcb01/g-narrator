

from modules.app import App, lang_settings

if __name__ == '__main__':
    # 1. Select language settings
    tts, ocr = lang_settings("en")
    # 2. Run App
    a = App(tts, ocr)
    a.run()