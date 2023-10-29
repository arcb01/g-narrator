import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import Qt

from garrator.ocr import OCR

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
        self.setWindowOpacity(0.5)

        # Create a semi-transparent overlay for the whole screen
        self.overlay = QtWidgets.QWidget(self)
        self.overlay.setGeometry(screen_geometry)
        self.overlay.setAutoFillBackground(True)
        overlay_palette = self.overlay.palette()
        overlay_palette.setColor(QtGui.QPalette.Background, QtGui.QColor(0, 0, 0, 128))
        self.overlay.setPalette(overlay_palette)
        self.overlay.show()


    def draw_button_on_coords(self, coors):
        button = QPushButton("", self)
        button.setGeometry(coors[0], coors[1], 100, 50)  # Set the position and size of the button
        button.setStyleSheet("background-color: black;")  # Set button style
        text_to_print = "Hello, World!"  # Define the text to print
        button.clicked.connect(lambda: self.on_button_clicked(text_to_print))
        button.show()  # Make sure to show the button

    def on_button_clicked(self, text_to_print):
        print(text_to_print)
        sys.exit()

    def closeEvent(self, event):
        # Override the close event to prevent the window from closing
        event.ignore()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            sys.exit()

    def run_scan(self):
        self.draw_button_on_coords((100, 100))
        # FIXME: Fix mouse lost control (when not available such as shooting camera)

        # TODO:
        # Call the OCR object/engine
        # Take screen shot
        # Get screenshot results (bounding boxes)
        # Create a button for each bounding box
        # draw button on bounding boxes coords
        # when button clicked read out loud text content
        # button asthetics
        pass

def read_screen():
    app = QApplication(sys.argv)
    mywindow = Window()
    mywindow.show()
    mywindow.run_scan()
    app.exec_()


# NOTE: Testing
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = Window()
    mywindow.show()
    mywindow.read_screen()
    #mywindow.draw_button_on_coords((100, 100))
    app.exec_()


