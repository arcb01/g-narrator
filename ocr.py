import cv2
import easyocr
import time
from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
import sys, keyboard, pyautogui, random, string
import pygame, win32api, win32con, win32gui
import matplotlib.pyplot as plt
import matplotlib.path as mplPath
import ctypes
from scipy.spatial import KDTree
import os
import pyttsx3
from shapely.geometry import Point, Polygon


CAPTURE_KEY = 'c'
DSWITCH_KEY = 'º'
REPEAT_KEY = 'r'

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
        self.color = (170, 255, 0)
        self.rect_width = 4
        self.narrator = narrator
        pygame.init()

    def take_screenshot(self):
        myScreenshot = pyautogui.screenshot()
        filename = ''.join(random.choices(string.ascii_lowercase, k=8)) + ".png"
        myScreenshot.save(self.imgs_dir + filename)
        self.imgs.append(filename)

    def OCR(self):
        print("Reading the image content. Please wait...\n")
        # Get last img
        #self.last_img = self.imgs.pop()
        self.last_img = self.imgs[-1]
        # Read img
        imgf = cv2.imread(self.imgs_dir + self.last_img)
        # OCR
        reader = easyocr.Reader([self.lang], gpu=self.gpu)
        self.all_results = reader.readtext(imgf)
        # Avoid low accuracy detections
        self.result = list(filter(lambda x: x[2] >= 0.3, self.all_results))

    def get_disp_size(self):
        user32 = ctypes.windll.user32
        dwidth, dheight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return dwidth, dheight

    def get_mouse_pos(self):
        x_mouse_pos = pyautogui.position().x
        y_mouse_pos = pyautogui.position().y
        return x_mouse_pos, y_mouse_pos

    def closest_node(self, node, nodes):
        kdtree = KDTree(nodes)
        d, i = kdtree.query(node)
        return nodes[i]

    def find_nearest_detection(self, x, y):
        # Convert list of lists to list of tuples
        det_rect = [tuple(p) for det in self.result for p in det[0]]
        # Find the closest point of the detection (rectangle) to the mouse position
        closest_point_to_mouse = self.closest_node((x, y), det_rect)
        # Check Where is this point in the list of detections
        for i, detection in enumerate(self.result):
            rectangle = detection[0]
            for point in rectangle:
                if point[0] == closest_point_to_mouse[0] and \
                    point[1] == closest_point_to_mouse[1]:
                    index = i
        closest_detect = self.result[index]
        return closest_detect

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
            self.narrator.say("Quitting")
            sys.exit()

        if event.event_type == keyboard.KEY_DOWN and event.name == DSWITCH_KEY:
            # Switch between detections
            self.switch_detection()
            # Text to speech
            self.narrator.say(self.output_text)

        if event.event_type == keyboard.KEY_DOWN and event.name == 'm':
            x, y = self.get_mouse_pos()

            self.take_screenshot()
            self.load_display()
            self.OCR()
            
            # Find nearest detection from the mouse position
            nearest_detection = self.find_nearest_detection(x, y)
            # Draw detection
            self.draw_detection(nearest_detection)
            # Text to speech
            self.narrator.say(self.output_text)
            
        if event.event_type == keyboard.KEY_DOWN and event.name == REPEAT_KEY:
            # Repeat text a little bit slower
            self.narrator.slower_saying(self.output_text)

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

    def draw_detection(self, detection):
        
        # Draw a rectangle for every text detection
        #detection = self.result[self.p]
        #self.clear_screen()
        #for detection in self.result:
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
    # 2. Only take screenshot if the last image has changed.
    # Dont take screenshot if the mouse is the same, just switch detections
    # 3. Join sentences?

    # ========== BUG ==========
    # 2. Index out of range error
    # 3. Pressing DSWITCH_KEY too early causes an error

    # ========== FIXME ==========
    # 1. Fix the narrator variables

    # ========== FUTURE WORK ==========
    # 1. Asynchronous loading_window? line 54-56
    # 2: Speed up?
        # 2.1 https://github.com/JaidedAI/EasyOCR/issues/786
        # 2.2 https://cloudblogs.microsoft.com/opensource/2022/04/19/scaling-up-pytorch-inference-serving-billions-of-daily-nlp-inferences-with-onnx-runtime/
        # 2.3 https://github.com/Kromtar/EasyOCR-ONNX/tree/easyocr_onnx

   # ========== Other ==========
   #1. OCR2
   # https://github.com/nathanaday/RealTime-OCR
