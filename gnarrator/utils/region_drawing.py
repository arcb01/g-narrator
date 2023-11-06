from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QRect
import cv2

class RegionMode(QWidget):
    def __init__(self, reading_engine):
        super().__init__()
        self.rectangles = []
        self.drawing = False
        self.start_point = None
        self.end_point = None
        self.reading_engine = reading_engine
        
        self.border_color = QColor(21, 93, 39)
        self.fill_color = QColor(146, 230, 167)

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

    def read_region(self):
        drawn_rect = self.rectangles.pop()
        rect_region = drawn_rect.getRect()
        try:
            self.reading_engine.read_screen(screen_region=rect_region)
        except cv2.error as e:
            print("WARNING: Trying to capture a region that is too small!")

    def draw_rectangle(self, rect):
        # Ensure left < right and top < bottom
        left = min(rect.left(), rect.right())
        top = min(rect.top(), rect.bottom())
        right = max(rect.left(), rect.right())
        bottom = max(rect.top(), rect.bottom())

        rect = QRect(left, top, right - left, bottom - top)
        self.rectangles.append(rect)
        self.update()
        # NOTE: Here starts the reading process
        self.read_region()
