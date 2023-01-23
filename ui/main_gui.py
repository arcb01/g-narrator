# Narrator
# Screen reader
#
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QShortcut
from PyQt5.uic import loadUi
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

import time
from ui import qt
from modules.app import App, lang_settings

class Narrator(QWidget):
    def __init__(self):
        super(Narrator, self).__init__()
        loadUi('ui/app_gui.ui', self)
        # Atributs de la classe
        self.stop_hided = True
        self.b_stop.hide()
  
        # GUI Initialitation
        self.UI()                   
    
    #  
    def UI(self):

        # Control barra de titulos
        #elf.setWindowFlag(Qt.FramelessWindowHint)        
        #self.setAtribute(Qt.WA_TranslucentBackground)
        
        # Actions Shortcuts
        #self.surt = QShortcut(QKeySequence(('Esc')), self)
        #self.surt.activated.connect(self.close)

        # Definir widgets
        self.widgets()       

        self.show()       

    def start_app(self):
        #time.sleep(1)
        #self.showMinimized()
        self.hide_stop()



    # Widgets
    def widgets(self):
        # Botons
        self.b_start.clicked.connect(self.start_app)
        self.b_stop.clicked.connect(self.close)
        self.b_tutorial.clicked.connect(self.tutorial)
        self.b_settings.clicked.connect(self.settings)
                
        # LineEdit

        # ComboBox                     

    def tutorial(self):
        self.tuto = Tutorial()
        self.tuto.show()

    def settings(self):
        self.setti = Settings()
        self.setti.show()


    def hide_stop(self):
        if self.stop_hided == True:
            self.b_stop.show()
            self.stop_hided = False



class Tutorial(QWidget):
    def __init__(self):
        super(Tutorial, self).__init__()
        loadUi('ui/app_gui_tutorial.ui', self)

        # Atributs de la classe
  
        # GUI Initialitation
        self.UI()                   
    
    #  
    def UI(self, form):
        # Control barra de titulos
        self.setWindowFlag(Qt.FramelessWindowHint)        
        
        # Actions Shortcuts
        self.surt = QShortcut(QKeySequence(('Esc')), self)
        self.surt.activated.connect(self.sortir)

    
    def sortir(self):
        self.close()



class Settings(QWidget):
    def __init__(self):
        super(Settings, self).__init__()
        loadUi('ui/app_gui_settings.ui', self)

        # Atributs de la classe
  
        # GUI Initialitation
        self.UI()                   
    
    #  
    def UI(self):
        # Control barra de titulos
        self.setWindowFlag(Qt.FramelessWindowHint)        
        
        # Actions Shortcuts
        self.surt = QShortcut(QKeySequence(('Esc')), self)
        self.surt.activated.connect(self.sortir)


    def sortir(self):
        self.close()

def main():
    app = QApplication(sys.argv)
    na = Narrator()
    sys.exit(app.exec())

"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    na = Narrator()
    sys.exit(app.exec())
"""