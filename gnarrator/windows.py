from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QRect
import cv2
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QWidget, qApp)
from gnarrator.utils.utils import map_rgb_string_to_qcolor


class RegionMode(QWidget):
    """
    Class for the drawing of the region to be captured
    """

    def __init__(self, window, reading_engine, settings):
        super().__init__()
        self.rectangles = []
        self.drawing = False
        self.start_point = None
        self.end_point = None
        self.settings = settings
        self.reading_engine = reading_engine
    
        # Load settings
        try:
            self.border_color = map_rgb_string_to_qcolor(self.settings["rect_reg_border_color"])
            self.fill_color = map_rgb_string_to_qcolor(self.settings["rect_reg_fill_color"])
        except:
            print("WARNING: Regional rectangle colors MUST be in rgb(r,g,b) format!")

        self.window = window

    def paintEvent(self, event):
        qp = QPainter(self)
        pen = QPen()
        pen.setColor(self.border_color)  # Set outline color to light green
        pen.setWidth(3)  # Set outline width
        qp.setPen(pen)
        
        for rect in self.rectangles:
            brush = QBrush(self.fill_color)  # Set fill color to green
            qp.setBrush(brush)
            qp.drawRect(rect)

        if self.drawing:
            pen.setColor(self.border_color)
            pen.setWidth(8)  # Set a thicker outline
            qp.setPen(pen)
            brush = QBrush(self.fill_color)  # Set fill color to green
            qp.setBrush(brush)
            qp.drawRect(QRect(self.start_point, self.end_point))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.start_point = event.pos()
            self.end_point = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            end_point = event.pos()
            rect = QRect(self.start_point, end_point)
            self.draw_rectangle(rect)
            self.drawing = False

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_point = event.pos()
            self.update()

    def start_reading(self):
        """
        When a rectangle is drawn, send the region to the reading engine
        """

        # Get rectangle region
        drawn_rect = self.rectangles.pop()
        rect_region = drawn_rect.getRect()
        try:
            # Read region
            self.reading_engine.read_screen(mode="regional", window=self.window, 
                                            screen_region=rect_region)
        except cv2.error as e:
            print("WARNING: Trying to capture a region that is too small!")

    def draw_rectangle(self, rect):
        # Ensure multidirectional drawing
        left = min(rect.left(), rect.right())
        top = min(rect.top(), rect.bottom())
        right = max(rect.left(), rect.right())
        bottom = max(rect.top(), rect.bottom())

        rect = QRect(left, top, right - left, bottom - top)
        self.rectangles.append(rect)
        self.update()
        # NOTE: When a rectangled region is defined, then the reading process starts here
        self.start_reading()


class Window(QMainWindow):

    """
    This class creates a semi-transparent overlay for displaying the OCR detections
    as clickable buttons.

    `Attributes:`	
        overlay: semi-transparent overlay for the whole screen
        ov_bck_color: color of the overlay
        buttons: list of buttons
        bbox_color: color of the detection boxes
        hover_color: color of the detection boxes when hovered
        border_width: width of the detection boxes border
        border_color: color of the detection boxes border
        border_radius: radius of the detection boxes border
    """

    def __init__(self, settings, mode):
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
        self.settings = settings

        # Set window opacity 
        if mode == "full":
            self.window_opacity = settings["op_full_mode"]
        elif mode == "regional":
            self.window_opacity = settings["op_regional_mode"]
        elif mode == "snq":
            self.window_opacity = settings["op_snq_mode"]

        self.setWindowOpacity(self.window_opacity)

        # Create a semi-transparent overlay for the whole screen
        self.overlay = QWidget(self)
        self.ov_bck_color = settings["ov_bck_color"]
        self.overlay.setGeometry(screen_geometry)
        self.overlay.setAutoFillBackground(True)
        self.overlay.setStyleSheet(f"background-color: {self.ov_bck_color};")
        self.overlay.show()

        # Styling settings
        self.buttons = [] 
        self.bbox_color = settings["bbox_color"]
        self.hover_color = settings["hover_color"]
        self.border_width = 1.5
        self.border_color = settings["border_color"]
        self.border_radius = 3

    def set_window_opacity(self, opacity):
        self.setWindowOpacity(opacity)

    def reset_opacity(self):
        # Set window opacity back to normal
        self.setWindowOpacity(self.settings["op_full_mode"])

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
        self.close()

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass