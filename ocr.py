import pyautogui
import random
import cv2
import easyocr
from scipy.spatial import KDTree
from sewar.full_ref import uqi
import time
import os, glob
from utils.utils import loading_screen, clear_screen, get_mouse_pos, get_disp_size


class OCR:
    """
    Class that captures the screen and performs OCR

    `Attributes:`
        lang: language in which the OCR will be performed
        gpu: use GPU or not (recommended to use GPU)
        imgs: List containing the filenames of the screenshots
        result: List of tuples (bbox, text, prob)
        results_db: Temporary list to store the results
        imgs_dir: Directory where screenshots will be stored
        file_nom: Nomenclature of the screenshots

    `Methods:`
        take_screenshot(): Take a screenshot and save it in imgs_dir
        start(): Start OCR detection and save results
        closest_node(): Returns the closest point of the detection to the mouse position
        find_nearest_detection(x, y): For a given mouse position, find the closest detection
        delete_imgs(): Deletes all screenshots when the program finishes running
        check_start(): Checks for repeated screenshots
    """

    def __init__(self, lang="en", gpu=True):
        self.lang = lang
        self.gpu = gpu
        self.imgs = []
        self.result = []
        #self.results_db = [] # NOTE: Not implemented
        self.imgs_dir = "./imgs/" # NOTE: Directory where images are stored
        self.file_nom = "OCR_pic_"


    def take_screenshot(self):
        """
        Function that takes a screenshot and save it in imgs_dir
        """

        myScreenshot = pyautogui.screenshot()
        h = str(random.getrandbits(128))
        filename = self.file_nom + h + ".png"
        myScreenshot.save(self.imgs_dir + filename)
        self.imgs.append(filename)
    
    def send_screen(self, screen):
        """
        Receives the screen from the main app
        """
        self.app_screen = screen

    def start(self):
        """
        Start OCR detection and save results
        """

        # Take screenshot
        self.take_screenshot()
        # Loading screen
        loading_screen(self.app_screen)
        # Get last img
        #self.last_img = self.imgs.pop()
        img = self.imgs[-1]
        # Read img
        imgf = cv2.imread(self.imgs_dir + img)
        # OCR
        reader = easyocr.Reader([self.lang], gpu=self.gpu)
        self.result = reader.readtext(imgf, paragraph=True)
        # Save results
        # NOTE: not implemented 
        # self.results_db.append((img, self.result))
        # Clear loading screen
        clear_screen(self.app_screen)

    def get_all_detections(self):
        """
        Returns the list of all detections
        """

        return self.result

    def empty_results(self):
        """
        Empty the list of results
        """

        self.result = []

    def closest_node(self, node: tuple, nodes: list):
        """
        Given a node, in this case the mouse position, this function
        returns the closest point of the detection to it.
        :param node: Tuple containing the x and y coordinates of the mouse position
        :param nodes: List of tuples containing the x and y coordinates for 
                    all points of every detection
        """

        kdtree = KDTree(nodes)
        d, i = kdtree.query(node)
        return nodes[i]

    def find_nearest_detection(self, x: int, y: int):
        """
        Given a mouse position, this function returns the closest detection
        :param x: x coordinate of the mouse position
        :param y: y coordinate of the mouse position
        """

        # Convert list of lists to list of tuples
        det_rect = [tuple(p) for det in self.result for p in det[0]]
        # Find the closest point of the detection (rectangle) to the mouse position
        closest_point_to_mouse = self.closest_node((x, y), det_rect)
        # Check to which detection this point corresponds
        for i, detection in enumerate(self.result):
            rectangle = detection[0]
            for point in rectangle:
                if point[0] == closest_point_to_mouse[0] and \
                    point[1] == closest_point_to_mouse[1]:
                    index = i
        closest_detect = self.result[index]
        return closest_detect
    
    def delete_imgs(self):
        """
        Deletes all screenshots taken
        """

        for filename in glob.glob(self.imgs_dir + f"{self.file_nom}*"):
            os.remove(filename) 

    def check_start(self):
        # NOTE: Don't implement
        pass
        """
        This function checks if the last 2 screenshots are almost identical.
        If so, it returns False, which means that OCR will not be performed.
        This is done to gain time, since OCR is a very slow process.


        if len(self.results_db) > 1:
            img1 = cv2.imread(self.imgs_dir + self.results_db[-1][0])
            img2 = cv2.imread(self.imgs_dir + self.results_db[-2][0])
            sim_score = uqi(img1, img2)
            if sim_score > 0.97:
                return False
            else:
                return True
        else:
            return True
        """