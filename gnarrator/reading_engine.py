from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import sys
from gnarrator.utils.utils import get_mouse_pos, create_arb_reg, get_detection_coords
from gnarrator.windows import Window, RegionMode
from gnarrator.ocr import OCR
from gnarrator.TTS import Narrator


class ReadingEngine:

    """
    This class runs the OCR and TTS engines into the Window class to be able to 
    read the screen content.

    `Attributes:`
        lang: language for OCR and TTS
        voice_speed: speed of the TTS voice
        OCR: OCR engine
        TTS: TTS engine
        app: Window app

    `Methods:`
        get_detection_coords(): Returns the coordinates of the bounding box
        say_content(): Call the TTS engine to read the content out loud
        read_screen(): Read the screen content and create buttons for each detection
        read_screen_regional(): Creates a drawing canvas for selecting a region to be read
        read_screen_small_n_quick(): Finds the closest detection to the mouse pointer and reads it out loud
    """

    def __init__(self, settings=None):

        # Language settings for OCR and TTS
        self.settings = settings
        if self.settings["GENDER"] == "male":
            if self.settings["LANGUAGE"] == "es":
                VOICE = "es-ES-AlvaroNeural"
            elif self.settings["LANGUAGE"]  == "en":
                VOICE = "en-US-GuyNeural"
        elif self.settings["GENDER"] == "female":
            if self.settings["LANGUAGE"] == "es":
                VOICE = "es-ES-ElviraNeural"
            elif self.settings["LANGUAGE"] == "en":
                VOICE = "en-US-JennyNeural"

        # OCR and TTS engines
        self.OCR = OCR(lang=self.settings["LANGUAGE"], gpu=True)
        self.settings["VOICE"] = VOICE
        self.TTS = Narrator(self.settings)

        # Window app
        self.app = QApplication(sys.argv)
    
    def say_content(self, content : str):
        """
        Call the TTS engine to read the content out loud
        :param content: text to be read
        """

        self.TTS.say(content)

    def read_screen(self, mode, window, screen_region=None):
        """
        Read the screen content and create buttons for each detection
        :param window: Window where the buttons will be displayed
        :param mode: mode of reading (full, regional, small_n_quick)
        :param screen_region: (x,y,w,h) coordinates of the region to be captured
                        if None, the whole screen will be captured
        """

        if mode == "full":
            # Take full screen shot
            self.OCR.take_screenshot()
        elif mode == "regional" or mode == "regional_n_quick":
            # Take regional screen shot
            self.OCR.take_screenshot(screen_region=screen_region)
            
        # Read textual elements
        self.OCR.read()

        # Get screenshot results (bounding boxes)
        # Create a button for each bounding box
        if len(self.OCR.get_detections) > 0:
            for det in self.OCR.get_detections:
                det_text_content = det[1]
                det_coords = get_detection_coords(det)  # x, y, w, h
                # draw button on bounding boxes coords
                button = window.create_button(coords=det_coords)
                # Associate button with bbox text
                button.clicked.connect(lambda _, text=det_text_content: self.say_content(text))

            # Give buttons style
            window.style_buttons()

            # Launch window 
            if screen_region:
                # NOTE: This can be changed to be all screen if needed (using map_coordinates function)
                window.set_to_regional(screen_region=screen_region)

            # if only 1 detection was found, read it directly
            #if len(self.OCR.get_detections) == 1:
                #QTimer.singleShot(5, lambda: self.say_content(det_text_content))

            return window

    def read_screen_regional(self):
        """
        Creates a drawing canvas for selecting a region to be read
        The RegionMode object will read the content of the delimited region after its drawn.
        """

        

    def read_screen_small_n_quick(self):
        """
        Finds the closest detection to the mouse pointer and 
        reads it out loud
        """

        self.window = Window()
        # 1. Create arbitrary region from mouse point
        xmouse, ymouse = get_mouse_pos()
        reg = create_arb_reg(cp=(xmouse, ymouse), w=540, h=320)
        # 2. Take a screenshot of the arbitrary region
        self.OCR.take_screenshot(screen_region=reg)
        self.OCR.read()
        # 3. Find the nearest detection
        closest_det = self.OCR.find_closest_detection((xmouse, ymouse))
        # 4. Draw the button
        det_text_content = closest_det[1]
        det_coords = get_detection_coords(closest_det)

        button = self.window.create_button(coords=det_coords)
        button.clicked.connect(lambda _, text=det_text_content: self.say_content(text))

        self.window.style_buttons()
        
        self.window.set_to_regional(screen_region=reg)
        self.window.show()

        # 5. Read the button out loud 
        QTimer.singleShot(5, lambda: self.say_content(det_text_content))

        self.app.exec_()
