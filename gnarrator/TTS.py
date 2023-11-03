import tempfile
import asyncio
import edge_tts  # Assuming you have the edge_tts library installed
from pygame import mixer
import time
import os

class Narrator:
    """
    Class used to read text

    `Attributes:`
        settings: Settings dictionary for the narrator

    `Methods:`
        say(): Playsback the text
        aplay(): Async playback of the text
        stop(): Stop playback
    """

    def __init__(self, settings):
        self.gender = settings["GENDER"]
        self.voice = settings["VOICE"]
        self.rate = settings["VOICE_RATE"]
        self.volume = settings["VOICE_VOLUME"]

    async def aplay(self, text : str):
        """
        Given a text, read it out loud
        :param text: Text to be read
        """

        communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, volume=self.volume)
        output_file_path = tempfile.mktemp(suffix=".mp3")
        try:
            await communicate.save(output_file_path)
            #print("Temporary MP3 file path:", output_file_path)
            # Play the MP3 file
            mixer.init()
            mixer.music.load(output_file_path)
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(.01)
        except Exception as e:
            print("Error while playing the audio:", str(e))
        finally:
            # Stop the mixer and ensure the file is closed
            mixer.music.stop()
            mixer.quit()
            # Clean up the temporary file after playback
            try:
                os.remove(output_file_path)
            except Exception as e:
                print("Error while deleting the file:", str(e))

    def say(self, text: str):
        """
        Given a text, read it out loud
        :param text: Text to be read
        """

        loop = asyncio.get_event_loop_policy().get_event_loop()
        try:
            loop.run_until_complete(self.aplay(text))
        finally:
            #loop.close()
            pass

    def stop(self):
        """
        Stop the voice engine
        """
        pass