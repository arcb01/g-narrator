import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint

class PaintWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.rectangles = []
        self.drawing = False
        self.start_point = None
        self.end_point = None

    def paintEvent(self, event):
        qp = QPainter(self)
        pen = QPen()
        pen.setColor(QColor(144, 238, 144))  # Set outline color to light green
        pen.setWidth(3)  # Set outline width
        qp.setPen(pen)
        
        for rect in self.rectangles:
            brush = QBrush(QColor(0, 128, 0))  # Set fill color to green
            qp.setBrush(brush)
            qp.drawRect(rect)

        if self.drawing:
            pen.setColor(QColor(144, 238, 144))
            pen.setWidth(4)  # Set a thicker outline
            qp.setPen(pen)
            brush = QBrush(QColor(0, 128, 0))  # Set fill color to green
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

    def draw_rectangle(self, rect):
        self.rectangles.append(rect)
        self.update()

class PaintApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Paint Application')
        
        # Set the window opacity (0 to 1)
        self.setWindowOpacity(0.8)

        self.paint_widget = PaintWidget()
        self.setCentralWidget(self.paint_widget)

        clear_button = QPushButton('Clear', self)
        clear_button.clicked.connect(self.clear_paint)
        clear_button.move(10, 10)

    def clear_paint(self):
        self.paint_widget.rectangles = []
        self.paint_widget.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PaintApp()
    ex.show()
    sys.exit(app.exec_())
