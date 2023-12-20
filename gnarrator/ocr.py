import pyautogui
import numpy as np
from deprecated import deprecated
import easyocr

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
        find_closest_detection(): Given a mouse position, this function returns the nearest detection
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

    @deprecated(reason="Not used anymore")
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


    def find_closest_detection(self, mouse_position):
        """
        Given a mouse position, this function returns the nearest detection
        :param mouse_pos: (x,y) coordinate of the mouse position
        :return # NOTE: Updates the list of detections
        """

        # NOTE: Map mouse position to local coordinates
        mouse_position = (mouse_position[0] - self.region[0], mouse_position[1] - self.region[1])

        closest_element = min(self.detections, key=lambda element: min(np.linalg.norm(np.array(point) - np.array(mouse_position)) 
                            for point in element[0]))
        
        self.detections = [closest_element]

    def empty_detections(self):
        self.detections = []
