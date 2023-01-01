
import pyttsx3


class Narrator:

    def __init__(self):
        self._engine = pyttsx3.init()
        # FIXME: Temporary 
        self._engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0")
        self.voice_default_rate = 170

    def say(self, text):
        self._engine.setProperty('rate', self.voice_default_rate)
        self._engine.say(text)
        self._engine.runAndWait()

    def stop(self):
        self._engine.stop()

    def slower_saying(self, text):
        self._engine.stop()
        self._engine.setProperty('rate', self.voice_default_rate * 0.5)
        self._engine.say(text)
        self._engine.runAndWait()