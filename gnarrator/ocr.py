import pyautogui
import numpy as np
from deprecated import deprecated
import easyocr

from gnarrator.utils.utils import closest_nodes

class OCR:
    """
    Class that captures the screen and performs OCR

    `Attributes:`
        lang: language in which the OCR will be performed
        gpu: use GPU or not (recommended to use GPU)
        imgs: List containing the filenames of the screenshots
        detections: List of tuples (bbox, text, prob)

    `Methods:`
        take_screenshot(): Take a screenshot and save it in imgs_dir
        start(): Loads the OCR engine into memory
        read(): Start OCR engine and save results
        get_detections(): Returns the list of all detections
    """

    def __init__(self, lang="en", gpu=True):
        self.lang = lang
        self.gpu = gpu
        self.imgs = []
        self.detections = []
        self.region = None
        
        self.start()
        
    def take_screenshot(self, screen_region=None):
        """
        Function that takes a screenshot and save it in imgs_dir
        :param screen_region: (x,y,w,h) coordinates of the region to be captured
                        if None, the whole screen will be captured
        """

        if screen_region is not None:
            myScreenshot = pyautogui.screenshot(region=screen_region)
            # Save region data
            self.region = screen_region
        else:
            myScreenshot = pyautogui.screenshot()

        self.imgs.append(np.array(myScreenshot))

    def start(self):
        """
        Load the OCR engine into memory
        """

        self.reader = easyocr.Reader([self.lang], gpu=self.gpu)
        
    def read(self):
        """
        Start OCR engine and save results
        """

        # Delete if previous detections
        self.empty_detections()
        # Get last img
        img = self.imgs[-1]
        # Fill all detections info
        self.detections = self.reader.readtext(img, paragraph=True)

    def map_coordinates_to_screen(self, detection):
        """
        Maps the coordinates of a local screenshot to the real coordinates of the screen
        :param detection: List of tuples (bbox, text, prob)
        """
        
        p_top_reg = (self.region[0], self.region[1])

        coords_arr = np.array(detection[0], dtype=np.int32)
        # mapping
        mapped_coords = coords_arr - np.array([p_top_reg[0], p_top_reg[1]])
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

    def find_closest_detection(self, mouse_position):
        closest_element = None
        closest_distance = float('inf')

        for element in self.detections:
            points = element[0]
            label = element[1]

            for point in points:
                distance = np.linalg.norm(np.array(point) - np.array(mouse_position))

                if distance < closest_distance:
                    closest_distance = distance
                    closest_element = element

        f = self.map_coordinates_to_screen(closest_element)

        return f

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
        print("closnode", list_closest_nodes)
        # Check to which detection this point corresponds
        matching_detections = [detection for detection in self.detections 
                               if any(candidate in detection[0] 
                                      for candidate in list_closest_nodes)]

        self.detections = matching_detections

    def empty_detections(self):
        """
        Empty the list of detections
        """

        self.detections = []
