import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
import pyautogui

from garrator.ocr import OCR
from garrator.TTS import Narrator

class Window(QMainWindow):
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
        overlay_palette.setColor(QtGui.QPalette.Background, QtGui.QColor(0, 0, 0, 128))
        self.overlay.setPalette(overlay_palette)
        self.overlay.show()

    def create_button(self, coords : list, color: str):
        # Create button
        button = QPushButton("", self)
        # Styling
        button.setGeometry(coords[0], coords[1], coords[2], coords[3])  # Set the position and size of the button
        transparency = 192
        button.setStyleSheet(f"background-color: {color};")
        button.show() 

        return button

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            sys.exit()


class ReadingEngine:

    def __init__(self, lang, voice_speed):

        # Language settings for OCR and TTS
        if lang == "en":
            voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
        elif lang == "es":
            voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"

        self.OCR = OCR(lang=lang, gpu=True)
        self.TTS = Narrator(voice=voice, voice_speed=voice_speed)

        # Window
        self.app = QApplication(sys.argv)
        self.window = Window()
        self.window.show()
        
        # Read screen conrent
        # FIXME: async loading screen
        self.run()

        # Launch window 
        self.app.exec_()

    def get_detection_coords(self, detection : list):
        """
        For a given detection, draw a bounding box around the text
        :param detection: a list containing the bounding box vertices, text, and confidence
        """
    
        bbox = detection[0]
        self.output_text = detection[1]
        top = bbox[0][0]
        left = bbox[0][1]
        width = bbox[1][0] - bbox[0][0]
        height = bbox[2][1] - bbox[1][1]

        return top, left, width, height
    
    def read_content(self, content : str):
        self.TTS.say(content)

    def run(self):
        # Take screen shot
        self.OCR.take_screenshot()
        # Read screen
        self.OCR.read()
        # Detection color
        color = 'rgba(0, 255, 0, 192)'
        # Get screenshot results (bounding boxes)
        # Create a button for each bounding box
        for det in self.OCR.get_detections:
            det_text_content = det[1]
            det_coords = self.get_detection_coords(det) # x, y, w, h
            # draw button on bounding boxes coords
            button = self.window.create_button(coords=det_coords, color=color)
            # Associate button with bbox text
            button.clicked.connect(lambda _, text=det_text_content: self.read_content(text))

# NOTE: Testing
if __name__ == '__main__':
    lang = "es"
    voice_speed = 120

    r = ReadingEngine(lang="es", voice_speed=voice_speed)
    r.run()

