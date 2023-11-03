from os import environ
import keyboard
import json
from pathlib import Path
# Remove pygame welcome message
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QApplication, 
                            QPushButton, QWidget, qApp)
from PyQt5.QtGui import QPalette, QColor


from gnarrator.ocr import OCR
from gnarrator.TTS import Narrator
from gnarrator.utils.utils import (
                        app_print, 
                        get_mouse_pos, create_arb_reg)
from gnarrator.utils.region_drawing import RegionMode

class Window(QMainWindow):

    """
    This class creates a semi-transparent overlay for displaying the OCR detections
    as clickable buttons.

    `Attributes:`	
        overlay: semi-transparent overlay for the whole screen
    """

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.X11BypassWindowManagerHint #|
            #Qt.WindowTransparentForInput  # Transparent
        )
        self.setFocusPolicy(Qt.StrongFocus)  # Set focus policy to accept keyboard focus

        screen_geometry = qApp.desktop().availableGeometry()
        self.setGeometry(screen_geometry)

        # Set window opacity (0.5 for example, change as needed)
        self.window_opacity = 0.85
        self.setWindowOpacity(self.window_opacity)

        # Create a semi-transparent overlay for the whole screen
        self.overlay = QWidget(self)
        self.overlay.setGeometry(screen_geometry)
        self.overlay.setAutoFillBackground(True)
        overlay_palette = self.overlay.palette()
        overlay_palette.setColor(QPalette.Background, QColor(0, 0, 0, 156))
        self.overlay.setPalette(overlay_palette)
        self.overlay.show()

    def set_window_opacity(self, opacity):
        self.setWindowOpacity(opacity)

    def set_to_regional(self, screen_region=None):
        """
        Resize the window to the given region
        :param screen_region: (x,y,w,h) coordinates of the region to be captured
        """
        
        self.setGeometry(*screen_region)

    def create_button(self, coords : list, bbox_color: str, hover_color: str):
        """
        Draws a button on the screen with the given coordinates and color
        :param coords: coordinates of the button (x, y, w, h)
        :param bbox_color: color of the button
        """

        # Create button
        button = QPushButton("", self)
        # Styling
        button.setGeometry(coords[0], coords[1], coords[2], coords[3])  # Set the position and size of the button
        button.setStyleSheet(f"background-color: {bbox_color};")
        # FIXME: This doesn't work
        # button.setStyleSheet(f"QPushButton:hover {{ background-color: {hover_color}; }}")

        button.show() 

        return button

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def clear_screen(self):
        """
        Clears the screen
        """

        self.close()

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

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
        color: color of the bounding boxes
    """

    def __init__(self, settings, region_mode=False):

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
        self.app = QApplication(sys.argv)

        # Colors
        self.bbox_color = 'rgba(124, 252, 0, 224)'
        self.hover_color = None

    def get_detection_coords(self, detection : list):
        """
        For a given detection, returns the coordinates of the bounding box
        :param detection: a list containing the bounding box vertices, text, and confidence
        """
    
        bbox = detection[0]
        top = bbox[0][0]
        left = bbox[0][1]
        width = bbox[1][0] - bbox[0][0]
        height = bbox[2][1] - bbox[1][1]

        return top, left, width, height
    
    def say_content(self, content : str):
        """
        Call the TTS engine to read the content out loud
        :param content: text to be read
        """

        self.TTS.say(content)

    def read_screen(self, screen_region=None):
        """
        Main function
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
                det_coords = self.get_detection_coords(det) # x, y, w, h
                # draw button on bounding boxes coords
                button = self.window.create_button(coords=det_coords, bbox_color=self.bbox_color, hover_color=self.hover_color)
                # Associate button with bbox text
                button.clicked.connect(lambda _, text=det_text_content: self.say_content(text))

            # Launch window 
            if screen_region:
                # NOTE: This can be changed to be all screen if needed (using map_coordinates function)
                self.window.set_to_regional(screen_region=screen_region)
            self.window.show()

            # TODO: Voice comes before the window, is there any way to fix this? # pylint: disable=fixme
            #if len(self.OCR.get_detections) == 1:
                #self.say_content(det_text_content)

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
        # FIXME: The use of drawing canvas + region window pops up warning message
        self.drawing_canvas.show()
        self.app.exec_()


class App:
    """
    Class that runs the entire application

    # TODO: Update doc

    `Attributes:`
        clock: Pygame clock object
        switch_detection: Boolean that enables swtiching between detections
        det_idx: Index of the current detection
        highlighted_color: Color that highlights the current bounding box
        dimmed_color: Color of the unselected bounding boxes
        start_x: Starting x coordinate of the region to be read
        start_y: Starting y coordinate of the region to be read
        n_pressed: Boolean that checks if the n key is pressed

    `Methods:`
        check_events(): Checks for keyboard events
        clear(): Clears the screen and deletes all screenshots taken
        end_of_list(): Checks if the current detection is the last one
        run(): Main loop of the application
        set_keys(): Sets key bindings
    """

    def __init__(self, settings):
        self.app_name = "G-Narrator"
        self.path = Path("./gnarrator/")
        self.app_logo = pygame.image.load(self.path / "assets" / "logo.png")
        self.clock = pygame.time.Clock()
        self.switch_detection = False
        self.engaging = False
        self.dimmed_color = (102, 153, 0)
        self.highlighted_color = (170, 255, 0)
        self.n_pressed = False
        self.start_x, self.start_y = 0, 0
        self.set_keys()
        pygame.init()

        self.reading_engine = ReadingEngine(settings)

    def set_keys(self):
        """
        Set key bindings
        """

        # Read json file containing key bindings
        with open(self.path / "config" / "keys.json", encoding="utf-8") as json_file:
            k = json.load(json_file)
            self.CAPTURE = k["CAPTURE"]
            self.SWITCH_DET_FORWARD = k["SWITCH_FORWARD"]
            self.SWITCH_DET_BACKWARD = k["SWITCH_BACKWARD"]
            self.REPEAT_KEY = k["REPEAT"]
            self.READ_NEAREST = k["READ_NEAREST"]
            self.READ_OUT_LOUD = k["READ_OUT_LOUD"]
            self.CLEAR_KEY = k["CLEAR"]

    def clear(self):
        try:
            # Clear screen
            self.reading_engine.window.clear_screen()
        except:
            # if window is not yet loaded, ignore
            pass  

    # TODO: This will be removed
    def end_of_list(self):
        return True if self.det_idx == len(self.OCR.get_detections) - 1 else False

    def check_events(self):
        """
        Captures any keyboard events
        """

        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.CLEAR_KEY:
            self.clear()

        # TODO: Define exit key
        if event.event_type == keyboard.KEY_DOWN and event.name == "":
            pass
            # TODO: sys.exit()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.READ_NEAREST:
            self.reading_engine.read_screen_regional()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.CAPTURE:
            self.reading_engine.read_screen()

        # TODO: Refactor to circular doubly linked list # pylint: disable=fixme
        if event.event_type == keyboard.KEY_DOWN and event.name in [self.SWITCH_DET_FORWARD, self.SWITCH_DET_BACKWARD]:
            
            assert len(self.OCR.get_detections) > 0, "No detections found yet. Please start scanning first."

            if not self.end_of_list():
                if event.name == self.SWITCH_DET_BACKWARD:
                    if self.det_idx == 0: # The first bbox
                        self.draw_detection(self.OCR.get_detections[self.det_idx], color=self.dimmed_color)
                        self.det_idx = len(self.OCR.get_detections) - 1
                        self.draw_detection(self.OCR.get_detections[self.det_idx], color=self.highlighted_color)
                    elif self.det_idx > 0: # Not the first bbox
                        self.draw_detection(self.OCR.get_detections[self.det_idx], color=self.dimmed_color)
                        self.draw_detection(self.OCR.get_detections[self.det_idx - 1], color=self.highlighted_color)
                        self.det_idx  -= 1
                elif event.name == self.SWITCH_DET_FORWARD:
                    self.draw_detection(self.OCR.get_detections[self.det_idx], color=self.dimmed_color)
                    self.draw_detection(self.OCR.get_detections[self.det_idx + 1], color=self.highlighted_color)
                    self.det_idx  += 1
            else:
                if event.name == self.SWITCH_DET_FORWARD:
                    # Loop back to start
                    self.draw_detection(self.OCR.get_detections[self.det_idx], color=self.dimmed_color)
                    self.det_idx = 0
                    self.draw_detection(self.OCR.get_detections[self.det_idx], color=self.highlighted_color)
                else:
                    self.draw_detection(self.OCR.get_detections[self.det_idx], color=self.dimmed_color)
                    self.draw_detection(self.OCR.get_detections[self.det_idx - 1], color=self.highlighted_color)
                    self.det_idx  -= 1

        # TODO: This needs to be updated # pylint: disable=fixme
        if event.event_type == keyboard.KEY_DOWN and event.name == self.READ_OUT_LOUD:
            if len(self.OCR.get_detections) > 0:
                pass
                #self.read_out_loud()

        # TODO: This needs to be updated # pylint: disable=fixme
        if event.event_type == keyboard.KEY_DOWN and event.name == self.REPEAT_KEY:
            pass
            #self.read_out_loud(slow=True)

    def run(self):
        """
        Main loop of the application
        """
        
        app_print()

        while True:
            self.check_events()
            self.clock.tick(60)  