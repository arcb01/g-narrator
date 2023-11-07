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

    def __init__(self, settings):

        # Language settings for OCR and TTS
        if settings["GENDER"] == "male":
            if settings["LANGUAGE"] == "es":
                VOICE = "es-ES-AlvaroNeural"
            elif settings["LANGUAGE"]  == "en":
                VOICE = "en-US-GuyNeural"
        elif settings["GENDER"] == "female":
            if settings["LANGUAGE"] == "es":
                VOICE = "es-ES-ElviraNeural"
            elif settings["LANGUAGE"] == "en":
                VOICE = "en-US-JennyNeural"

        # OCR and TTS engines
        self.OCR = OCR(lang=settings["LANGUAGE"], gpu=True)
        settings["VOICE"] = VOICE
        self.TTS = Narrator(settings)

        # Window app
        self.window = None
        self.drawing_canvas = None
        self.app = QApplication(sys.argv)
    
    def say_content(self, content : str):
        """
        Call the TTS engine to read the content out loud
        :param content: text to be read
        """

        self.TTS.say(content)

    def read_screen(self, screen_region=None):
        """
        Read the screen content and create buttons for each detection
        """

        # Create window
        # NOTE: This needs to be here in order to make the screenshot loop process to work.
        #       otherwise the program will only run once.
        self.window = Window()

        if screen_region:
            # Take regional screen shot
            self.OCR.take_screenshot(screen_region=screen_region)
        else:
            # Take full screen shot
            self.OCR.take_screenshot()

        # Read textual elements
        self.OCR.read()
        # Get screenshot results (bounding boxes)
        # Create a button for each bounding box
        if len(self.OCR.get_detections) > 0:
            for det in self.OCR.get_detections:
                det_text_content = det[1]
                det_coords = get_detection_coords(det)  # x, y, w, h
                # draw button on bounding boxes coords
                button = self.window.create_button(coords=det_coords)
                # Associate button with bbox text
                button.clicked.connect(lambda _, text=det_text_content: self.say_content(text))

            # Give buttons style
            self.window.style_buttons()

            # Launch window 
            if screen_region:
                # NOTE: This can be changed to be all screen if needed (using map_coordinates function)
                self.window.set_to_regional(screen_region=screen_region)
            self.window.show()

            # if only 1 detection was found, read it directly
            if len(self.OCR.get_detections) == 1:
                QTimer.singleShot(5, lambda: self.say_content(det_text_content))
    
            self.app.exec_()

    def read_screen_regional(self):
        """
        Creates a drawing canvas for selecting a region to be read
        The RegionMode object will read the content of the delimited region after its drawn.
        """

        # open region canvas for drawing
        self.drawing_canvas = Window()
        region_window = RegionMode(reading_engine=self)
        self.drawing_canvas.setCentralWidget(region_window)
        self.drawing_canvas.set_window_opacity(0.35)
        # NOTE: The use of drawing canvas + region window pops up warning message
        self.drawing_canvas.show()
        self.app.exec_()

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
