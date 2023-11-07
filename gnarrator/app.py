from os import environ
import keyboard
import json
from pathlib import Path
# Remove pygame welcome message
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QMainWindow, QApplication, 
                            QPushButton, QWidget, qApp)
from PyQt5.QtGui import QPalette, QColor

from gnarrator.ocr import OCR
from gnarrator.TTS import Narrator
from gnarrator.utils.utils import app_print, create_arb_reg, get_mouse_pos
from gnarrator.utils.region_drawing import RegionMode


class Window(QMainWindow):

    """
    This class creates a semi-transparent overlay for displaying the OCR detections
    as clickable buttons.

    `Attributes:`	
        overlay: semi-transparent overlay for the whole screen
        buttons: list of buttons
        bbox_color: color of the detection boxes
        hover_color: color of the detection boxes when hovered
        border_width: width of the detection boxes border
        border_color: color of the detection boxes border
        border_radius: radius of the detection boxes border
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

        # Styling settings
        self.buttons = [] 
        self.bbox_color = "#2dc653"
        self.hover_color = "#b7efc5"
        self.border_width = 1.5
        self.border_color = "#000000"
        self.border_radius = 3

    def set_window_opacity(self, opacity):
        self.setWindowOpacity(opacity)

    def set_to_regional(self, screen_region=None):
        """
        Resize the window to the given region
        :param screen_region: (x,y,w,h) coordinates of the region to be captured
        """
        
        self.setGeometry(*screen_region)

    def create_button(self, coords : list):
        """
        Draws a button on the screen with the given coordinates and color
        :param coords: coordinates of the button (x, y, w, h)
        :param bbox_color: color of the button
        """

        # Create button
        button = QPushButton("", self)
        # Styling
        button.setGeometry(coords[0], coords[1], coords[2], coords[3])  # Set the position and size of the button
        self.buttons.append(button)  # Store a reference

        button.show() 

        return button

    def style_buttons(self):
        """
        Styles the buttons with color and border
        """

        for button in self.buttons:
            button.setStyleSheet(
                f"QPushButton {{"
                f"background-color: {self.bbox_color};"
                f"border: {self.border_width}px solid {self.border_color};"
                f"border-radius: {self.border_radius}px;"
                f"}}"
                f"QPushButton:hover {{"
                f"background-color: {self.hover_color};"
                f"}}"
            )


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

    `Methods:`
        get_detection_coords(): Returns the coordinates of the bounding box
        say_content(): Call the TTS engine to read the content out loud
        read_screen(): Read the screen content and create buttons for each detection
        read_screen_regional(): Creates a drawing canvas for selecting a region to be read
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
                det_coords = self.get_detection_coords(det)  # x, y, w, h
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

    def read_screen_quickly(self):

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
        det_coords = self.get_detection_coords(closest_det)

        button = self.window.create_button(coords=det_coords)
        button.clicked.connect(lambda _, text=det_text_content: self.say_content(text))

        self.window.style_buttons()
        
        self.window.set_to_regional(screen_region=reg)
        self.window.show()

        # 5. Read the button out loud 
        QTimer.singleShot(5, lambda: self.say_content(det_text_content))

        self.app.exec_()


class App:
    """
    Class that runs the entire application

    `Attributes:`
        clock: Pygame clock object
        app_name: Name of the application
        path: Path to the application folder
        app_logo: Application logo

    `Methods:`
        check_events(): Checks for keyboard events
        clear(): Clears the screen and deletes all screenshots taken
        run(): Main loop of the application
        set_keys(): Sets key bindings
    """

    def __init__(self, settings):
        self.app_name = "G-Narrator"
        self.path = Path("./gnarrator/")
        self.app_logo = pygame.image.load(self.path / "assets" / "logo.png")
        self.clock = pygame.time.Clock()
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
            self.FULL_SCREEN = k["FULL_SCREEN"]
            self.REGION = k["REGION"]
            self.CLEAR_KEY = k["CLEAR"]

    def clear(self):
        try:
            # Clear screen
            self.reading_engine.window.clear_screen()
        except:
            # if window is not yet loaded, ignore
            pass  

    def check_events(self):
        """
        Captures any keyboard events
        """

        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.CLEAR_KEY:
            self.clear()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.REGION:
            self.reading_engine.read_screen_regional()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.FULL_SCREEN:
            self.reading_engine.read_screen()

        # FIXME
        if event.event_type == keyboard.KEY_DOWN and event.name == "p":
            self.reading_engine.read_screen_quickly()
            # clear screen
            self.clear()

    def run(self):
        """
        Main loop of the application
        """
        
        app_print()

        while True:
            self.check_events()
            self.clock.tick(60)  