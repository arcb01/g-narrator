from os import environ
import keyboard
import json
from pathlib import Path
# Remove pygame welcome message
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import Qt

from garrator.ocr import OCR
from garrator.TTS import Narrator
from garrator.utils.utils import (
                        get_disp_size, app_print, 
                        get_mouse_pos)
from garrator.window import Window, ReadingEngine


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
        quit(): Clears the screen and deletes all screenshots taken
        end_of_list(): Checks if the current detection is the last one
        run(): Main loop of the application
        set_keys(): Sets key bindings
    """

    def __init__(self, lang, voice_speed):
        self.app_name = "Garrator"
        self.path = Path("./garrator/")
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

        self.reading_engine = ReadingEngine(lang, voice_speed)

    def set_keys(self):
        """
        Set key bindings
        """

        # Read json file containing key bindings
        with open(self.path / "config" / "keys.json") as json_file:
            k = json.load(json_file)
            self.CAPTURE = k["CAPTURE"]
            self.SWITCH_DET_FORWARD = k["SWITCH_FORWARD"]
            self.SWITCH_DET_BACKWARD = k["SWITCH_BACKWARD"]
            self.REPEAT_KEY = k["REPEAT"]
            self.READ_NEAREST = k["READ_NEAREST"]
            self.READ_OUT_LOUD = k["READ_OUT_LOUD"]
            self.QUIT_KEY = k["QUIT"]

    def quit(self):
        # TODO: Add a confirmation message
        pass

    # FIXME: This will be removed
    def end_of_list(self):
        return True if self.det_idx == len(self.OCR.get_detections) - 1 else False

    def check_events(self):
        """
        Captures any keyboard events
        """

        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.QUIT_KEY:
            self.quit()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.READ_NEAREST and not self.n_pressed:
            self.start_x, self.start_y = get_mouse_pos()
            self.n_pressed = True

        if event.event_type == keyboard.KEY_UP and event.name == self.READ_NEAREST:
            self.end_x, self.end_y = get_mouse_pos()
            #print("n released")
            self.n_pressed = False

            region = (
                min(self.start_x, self.end_x),
                min(self.start_y, self.end_y),
                abs(self.end_x - self.start_x),
                abs(self.end_y - self.start_y)
            )

            # Launch reading engine
            self.reading_engine.read_screen(screen_region=region)

        if event.event_type == keyboard.KEY_DOWN and event.name == self.CAPTURE:
            self.reading_engine.read_screen()

        # FIXME: Refactor to circular doubly linked list
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

        # FIXME: This needs to be updated
        if event.event_type == keyboard.KEY_DOWN and event.name == self.READ_OUT_LOUD:
            if len(self.OCR.get_detections) > 0:
                self.read_out_loud()

        # FIXME: This needs to be updated
        if event.event_type == keyboard.KEY_DOWN and event.name == self.REPEAT_KEY:
            self.read_out_loud(slow=True)

    def run(self):
        """
        Main loop of the application
        """
        
        app_print()

        while True:
            self.check_events()
            self.clock.tick(60)


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
        self.setFocusPolicy(QtCore.Qt.StrongFocus)  # Set focus policy to accept keyboard focus

        screen_geometry = QtWidgets.qApp.desktop().availableGeometry()
        self.setGeometry(screen_geometry)

        # Set window opacity (0.5 for example, change as needed)
        self.setWindowOpacity(0.7)

        # Create a semi-transparent overlay for the whole screen
        self.overlay = QtWidgets.QWidget(self)
        self.overlay.setGeometry(screen_geometry)
        self.overlay.setAutoFillBackground(True)
        overlay_palette = self.overlay.palette()
        overlay_palette.setColor(QtGui.QPalette.Background, QtGui.QColor(0, 0, 0, 156))
        self.overlay.setPalette(overlay_palette)
        self.overlay.show()

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
        # BUG: This doesn't work
        # button.setStyleSheet(f"QPushButton:hover {{ background-color: {hover_color}; }}")

        button.show() 

        return button

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


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

    def __init__(self, lang, voice_speed):

        # FIXME: Maybe this could be changed when new TTS engine is added
        # Language settings for OCR and TTS
        if lang == "en":
            voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
        elif lang == "es":
            voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"

        # OCR and TTS engines
        self.OCR = OCR(lang=lang, gpu=True)
        self.TTS = Narrator(voice=voice, voice_speed=voice_speed)

        # Window app
        self.app = QApplication(sys.argv)
        # Colors
        self.bbox_color = 'rgba(124, 252, 0, 224)'
        self.hover_color = None

        # TODO: async loading screen

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
                self.window.set_to_regional(screen_region=screen_region)
            self.window.show()
            self.app.exec_()

