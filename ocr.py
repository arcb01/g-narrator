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


CAPTURE_KEY = 'c'
MOVE_KEY = ''
READ_KEY = ''


class Capture:

    def __init__(self, lang="en", gpu=True):
        self.imgs = []
        self.imgs_dir = "./imgs/" # NOTE: Directory where images are stored
        self.lang = lang
        self.gpu = gpu

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

    def show_results(self):
        text_results = list(map(lambda x: x[1], self.result))
        print(text_results)

    def get_disp_size(self):
        user32 = ctypes.windll.user32
        dwidth, dheight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return dwidth, dheight

    def check_events(self):
        # If c is pressed, take a screenshot and read the image content
        if keyboard.KEY_DOWN and keyboard.is_pressed(CAPTURE_KEY):
            self.take_screenshot()
            print("\nScreenshot taken!\n")
            self.load_display()
            self.OCR()
            self.draw_detection()

        if keyboard.KEY_DOWN and keyboard.is_pressed('esc'):
            print("\n ==== Stopping... ====\n")
            sys.exit()

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
        pygame.display.update()

    def draw_detection(self):
        color = (88, 205, 54)
        # Draw a rectangle for every text detection 
        for detection in self.result:
            bbox = detection[0]
            text = detection[1]
            top = bbox[0][0]
            left = bbox[0][1]
            width = bbox[1][0] - bbox[0][0]
            height = bbox[2][1] - bbox[1][1]
            pygame.draw.rect(self.screen, color,  pygame.Rect(top, left, width, height), 2)
            pygame.display.update()


    def run(self):
        print("\n ==== App is running... ====")
        while True:
            self.check_events()
            

if __name__ == "__main__":
    a = Capture()
    a.run()

    # ========== TODO ==========
    # 1. Set queueing system, for every detection, and switch between them
    # 2. Asynchronous loading_window? line 54-56
    # 2. Screen reader https://github.com/nateshmbhat/pyttsx3