from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.last_pressed = None
        self.double_click_threshold = 200  # milliseconds for double click detection
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.single_click_action)
        #self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_K:
            if not self.timer.isActive():
                # First press, start the timer
                self.timer.start(self.double_click_threshold)
                self.last_pressed = event.key()
            elif self.last_pressed == Qt.Key_K:
                # Second press and the timer is still running, must be a double click
                self.timer.stop()  # Stop the timer and handle double click
                self.double_click_action()
            else:
                # Different key pressed, reset
                self.timer.stop()
                self.single_click_action()
        else:
            super().keyPressEvent(event)

    def single_click_action(self):
        print("k was pressed once")

    def double_click_action(self):
        print("k was double clicked")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec_()

    # TODO 
