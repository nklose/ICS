"""
This program acts as a start point for the local GUI.

Code for the basic framework was borrowed from:
http://www.rkblog.rk.edu.pl/w/p/simple-text-editor-pyqt4/
"""

import sys
from PyQt4 import QtCore, QtGui
from main_ICS import Ui_Dialog

# Globals
singleImage = False
mode = "auto"

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        ## Interface Object Connections

        # Image Settings Buttons
        QtCore.QObject.connect(self.ui.loadImageRed,
                               QtCore.SIGNAL("clicked()"),
                               self.load_red_image)
        
        QtCore.QObject.connect(self.ui.loadImageGreen,
                               QtCore.SIGNAL("clicked()"),
                               self.load_green_image)

        QtCore.QObject.connect(self.ui.loadImageBlue,
                               QtCore.SIGNAL("clicked()"),
                               self.load_blue_image)

        QtCore.QObject.connect(self.ui.loadImageRGB,
                               QtCore.SIGNAL("clicked()"),
                               self.load_RGB_image)

        # Start Button
        QtCore.QObject.connect(self.ui.startButton,
                               QtCore.SIGNAL("clicked()"),
                               self.start)

    ## Interface Functions

    # Loads an RGB image into the interface.
    def load_RGB_image(self):
        print("Loading RGB Image...")

    # Loads a red channel image into the interface.
    def load_red_image(self):
        print("Loading red image...")

    # Loads a green channel image into the interface.
    def load_green_image(self):
        print("Loading green image...")
 
    # Loads a blue channel image into the interface.
    def load_blue_image(self):
        print("Loading blue image...")

    # Start button functionality
    def start(self):
        if mode == "auto":
            print("Auto mode")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())
