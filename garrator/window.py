import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import Qt

from garrator.ocr import OCR
from garrator.TTS import Narrator

class Window(QMainWindow):
    """
    This class creates a semi-transparent overlay for displaying the OCR detections
    as clickable buttons.
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
        self.setGeometry(*screen_region)

    def create_button(self, coords : list, color: str):
        """
        Draws a button on the screen with the given coordinates and color
        :param coords: coordinates of the button (x, y, w, h)
        :param color: color of the button
        """

        # Create button
        button = QPushButton("", self)
        # Styling
        button.setGeometry(coords[0], coords[1], coords[2], coords[3])  # Set the position and size of the button
        button.setStyleSheet(f"background-color: {color};")
        button.show() 

        return button

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


class ReadingEngine:

    def __init__(self, lang, voice_speed):
        """
        This class runs the OCR and TTS engines into the Window class to be able to 
        read the screen content.

        :param lang: language for OCR and TTS
        :param voice_speed: speed of the TTS voice
        """

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
        # Bboxes color
        self.color = 'rgba(0, 255, 0, 192)'

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
                button = self.window.create_button(coords=det_coords, color=self.color)
                # Associate button with bbox text
                button.clicked.connect(lambda _, text=det_text_content: self.say_content(text))

            # Launch window 
            if screen_region:
                self.window.set_to_regional(screen_region=screen_region)
            self.window.show()
            self.app.exec_()