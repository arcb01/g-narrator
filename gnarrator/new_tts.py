# This TTS based on https://github.com/rany2/edge-tts

import tempfile
import asyncio
import edge_tts  # Assuming you have the edge_tts library installed
from pygame import mixer
import time
import os

# TTS settings
gender = "female" 
language = "es"
rate = "-50%"
volume = "-50%"

# NOTE: Add in reading engine
if gender == "male":
    if language == "es":
        VOICE = "es-ES-AlvaroNeural"
    elif language == "en":
        VOICE = "en-US-GuyNeural"
elif gender == "female":
    if language == "es":
        VOICE = "es-ES-ElviraNeural"
    elif language == "en":
        VOICE = "en-US-JennyNeural"

async def aplay(TEXT):
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE, rate=rate, volume=volume)
    output_file_path = tempfile.mktemp(suffix=".mp3")
    try:
        await communicate.save(output_file_path)
        print("Temporary MP3 file path:", output_file_path)
        # Play the MP3 file
        mixer.init()
        mixer.music.load(output_file_path)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(1)
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

if __name__ == "__main__":
    TEXT = "Este es un tts mas moderno y con una voz mas natural"
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(aplay(TEXT))
    finally:
        loop.close()
