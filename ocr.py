import pyautogui
import random
import cv2
import easyocr
from scipy.spatial import KDTree
from sewar.full_ref import uqi
import time
import os, glob


class OCR:

    def __init__(self, lang="en", gpu=True):
        self.lang = lang
        self.gpu = gpu
        self.imgs = []
        self.result = []
        self.results_db = []
        self.status = True
        self.imgs_dir = "./imgs/" # NOTE: Directory where images are stored

    def take_screenshot(self):
        start = time.time()
        myScreenshot = pyautogui.screenshot()
        h = str(random.getrandbits(128))
        self.file_nom = "OCR_pic_"
        filename = self.file_nom + h + ".png"
        myScreenshot.save(self.imgs_dir + filename)
        self.imgs.append(filename)
    
    def start(self):
        # Take screenshot
        self.take_screenshot()
        print("Reading the image content. Please wait...\n")
        # Get last img
        #self.last_img = self.imgs.pop()
        img = self.imgs[-1]
        # Read img
        imgf = cv2.imread(self.imgs_dir + img)
        # OCR
        reader = easyocr.Reader([self.lang], gpu=self.gpu)
        self.all_results = reader.readtext(imgf)
        # Avoid low accuracy detections
        self.result = list(filter(lambda x: x[2] >= 0.3, self.all_results))
        # Save results
        self.results_db.append((img, self.result))

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
    
    def delete_imgs(self):
        for filename in glob.glob(self.imgs_dir + f"{self.file_nom}*"):
            os.remove(filename) 

    def check_start(self):
        # Don't start OCR if the last 2 images are the same
        if len(self.results_db) > 1:
            img1 = cv2.imread(self.imgs_dir + self.results_db[-1][0])
            img2 = cv2.imread(self.imgs_dir + self.results_db[-2][0])
            sim_score = uqi(img1, img2)
            if sim_score > 0.95:
                return False
            else:
                return True
        else:
            return True