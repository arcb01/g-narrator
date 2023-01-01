
import pyautogui
import random
import string
import cv2
import easyocr
from scipy.spatial import KDTree
import numpy as np


class OCR:

    def __init__(self, lang="en", gpu=True):
        self.lang = lang
        self.gpu = gpu
        self.imgs = []
        self.result = []
        self.imgs_dir = "./imgs/" # NOTE: Directory where images are stored

    def take_screenshot(self):
        myScreenshot = pyautogui.screenshot()
        filename = ''.join(random.choices(string.ascii_lowercase, k=8)) + ".png"
        myScreenshot.save(self.imgs_dir + filename)
        self.imgs.append(filename)
    
    def start(self):
        # Take screenshot
        self.take_screenshot()
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