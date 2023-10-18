import pyautogui
import random
import cv2
import numpy as np
from deprecated import deprecated
import easyocr
import os
from pathlib import Path
from garrator.utils.utils import loading_screen, clear_screen, closest_nodes

class OCR:
    """
    Class that captures the screen and performs OCR

    `Attributes:`
        lang: language in which the OCR will be performed
        gpu: use GPU or not (recommended to use GPU)
        imgs: List containing the filenames of the screenshots
        result: List of tuples (bbox, text, prob)
        imgs_dir: Directory where screenshots will be stored
        file_nom: Nomenclature of the screenshots

    `Methods:`
        images_dir(): Makes sure that the imgs directory exists
        take_screenshot(): Take a screenshot and save it in imgs_dir
        start(): Start OCR detection and save results
        delete_imgs(): Deletes all screenshots when the program finishes running
    """

    def __init__(self, lang="en", gpu=True):
        self.lang = lang
        self.gpu = gpu
        self.imgs = []
        self.detections = []
        self.imgs_path = Path("./garrator/.tmp_imgs/")
        self.images_dir()
        self.file_nom = "OCR_pic_"
        
        self.start()

    def images_dir(self):
        """
        Makes sure that the imgs directory exists
        """
            
        if not os.path.exists(self.imgs_path):
            os.makedirs(self.imgs_path)
        
    def take_screenshot(self, region=None):
        """
        Function that takes a screenshot and save it in imgs_dir
        :param region: (x,y,w,h) coordinates of the region to be captured
                        if None, the whole screen will be captured
        """

        if region is not None:
            myScreenshot = pyautogui.screenshot(region=region)
            # Save region data
            self.region = region
        else:
            myScreenshot = pyautogui.screenshot()

        h = str(random.getrandbits(128))
        filename = self.file_nom + h + ".png"
        myScreenshot.save(self.imgs_path / filename)
        self.imgs.append(filename)
    
    def send_screen(self, screen):
        """
        Receives the screen from the main app
        """
        self.app_screen = screen

    def start(self):
        """
        Load the OCR engine into memory
        """

        self.reader = easyocr.Reader([self.lang], gpu=self.gpu)
        
    def read(self):
        """
        Start OCR engine and save results
        """

        # Loading screen
        loading_screen(self.app_screen)
        # Get last img
        #self.last_img = self.imgs.pop()
        img = self.imgs[-1]
        # Read img
        imgf = cv2.imread((self.imgs_path / img).__str__())
        self.detections = self.reader.readtext(imgf, paragraph=True)
        # Clear loading screen
        clear_screen(self.app_screen)

    def map_coordinates_to_screen(self, detection):
        """
        Maps the coordinates of a local screenshot to the real coordinates of the screen
        :param detection: List of tuples (bbox, text, prob)
        """
        
        p_top_reg = (self.region[0], self.region[1])

        coords_arr = np.array(detection[0], dtype=np.int32)
        # mapping
        mapped_coords = coords_arr + np.array([p_top_reg[0], p_top_reg[1]])
        # convert to list
        mapped_coords_list = mapped_coords.tolist()

        detection[0] = mapped_coords_list

        return detection

    @property
    def get_detections(self):
        """
        Returns the list of all detections
        """

        return self.detections

    @deprecated(reason="Old function, not used anymore")
    def find_nearest_detections(self, mouse_pos: tuple):
        """
        Given a mouse position, this function returns the top k nearest detections
        :param mouse_pos: (x,y) coordinate of the mouse position
        :return: NOTE: This function updates the self.detections list
        """

        # Convert list of lists to list of tuples
        det_rect = [tuple(p) for det in self.detections for p in det[0]]
        # Find the closest point of the detection (rectangle) to the mouse position
        list_closest_nodes = closest_nodes(mouse_pos, det_rect)
        # Check to which detection this point corresponds
        matching_detections = [detection for detection in self.detections 
                               if any(candidate in detection[0] 
                                      for candidate in list_closest_nodes)]

        self.detections = matching_detections

    def empty_results(self):
        """
        Empty the list of results
        """

        self.detections = []
    
    def delete_imgs(self):
        """
        Deletes all screenshots taken
        """

        # empty self.imgs_path directory 

        for item in self.imgs_path.iterdir():
            if item.is_file():
                item.unlink()  # Remove file 
