import cv2
import easyocr
import time
from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
import sys, keyboard, pyautogui, random, string
import pygame, win32api, win32con, win32gui
import matplotlib.pyplot as plt
import ctypes
import os
import pyttsx3


CAPTURE_KEY = 'c'
DSWITCH_KEY = 'º'
TTS_KEY = ''

class Narrator:

    def __init__(self):
        self._engine = pyttsx3.init()
        # FIXME: Temporary 
        self._engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0")
        rate = self._engine.getProperty('rate')
        self._engine.setProperty('rate', rate - 25)

    def say(self, text):
        self._engine.say(text)
        self._engine.runAndWait()

    def stop(self):
        self._engine.stop()


class Capture:

    def __init__(self, lang="en", narrator=None, gpu=True):
        self.imgs = []
        self.detections = []
        self.result = []
        self.imgs_dir = "./imgs/" # NOTE: Directory where images are stored
        self.lang = lang
        self.gpu = gpu
        self.p = 0
        self.open = True
        self.color = (88, 205, 54)
        self.rect_width = 4
        self.narrator = narrator

    def take_screenshot(self):
        myScreenshot = pyautogui.screenshot()
        filename = ''.join(random.choices(string.ascii_lowercase, k=8)) + ".png"
        myScreenshot.save(self.imgs_dir + filename)
        self.imgs.append(filename)

    def OCR(self):
        print("Reading the image content. Please wait...\n")
        # Get last img
        self.last_img = self.imgs.pop()
        # Read img
        imgf = cv2.imread(self.imgs_dir + self.last_img)
        # OCR
        reader = easyocr.Reader([self.lang], gpu=self.gpu)
        self.result = reader.readtext(imgf)

    def get_disp_size(self):
        user32 = ctypes.windll.user32
        dwidth, dheight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return dwidth, dheight

    def check_events(self):
        event = keyboard.read_event()

        # If c is pressed, take a screenshot and read the image content
        if event.event_type == keyboard.KEY_DOWN and event.name == CAPTURE_KEY:
            self.take_screenshot()
            print("\nScreenshot taken!\n")
            self.load_display()
            self.OCR()
            self.draw_detection()
            self.narrator.say(self.output_text)
            self.narrator.stop()

        if event.event_type == keyboard.KEY_DOWN and event.name == 'esc':
            print("\n ==== Stopping... ====\n")
            self.narrator.engine.say("Quitting")
            sys.exit()

        if event.event_type == keyboard.KEY_DOWN and event.name == DSWITCH_KEY:
            # Switch between detections
            self.switch_detection()
            # Text to speech
            self.narrator.say(self.output_text)


    def switch_detection(self):
        if self.p < len(self.result) - 1: 
            self.p += 1
        else: 
            self.p = 0

        self.draw_detection()


    def testing(self):
        pass

    def load_display(self):
        # https://stackoverflow.com/questions/550001/fully-transparent-windows-in-pygame
        pygame.init()
        w, h = self.get_disp_size()
        self.screen = pygame.display.set_mode((w, h)) # For borderless, use pygame.NOFRAME
        done = False
        fuchsia = (255, 0, 128)  # Transparency color
        # Keep on top
        win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        # Create layered window
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        # Set window transparency color
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

        self.screen.fill(fuchsia)  # Transparent background
        self.clear_screen = lambda : self.screen.fill(fuchsia)

        pygame.display.update()

    def draw_detection(self):
        self.clear_screen()
        # Draw a rectangle for every text detection
        detection = self.result[self.p]
        #self.clear_screen()
        bbox = detection[0]
        self.output_text = detection[1]
        top = bbox[0][0]
        left = bbox[0][1]
        width = bbox[1][0] - bbox[0][0]
        height = bbox[2][1] - bbox[1][1]
        pygame.draw.rect(self.screen, self.color,  pygame.Rect(top, left, 
                                                            width, height), 
                        self.rect_width)
        pygame.display.update()

    def run(self):
        print("\n ==== App is running... ====")
        while True:
            self.check_events()
            


if __name__ == "__main__":
    n = Narrator()
    a = Capture(lang="en", narrator=n, gpu=True)
    a.run()

    # ========== TODO ==========
    # 2. Asynchronous loading_window? line 54-56

    # ========== FIXME ==========
    # 1. View?