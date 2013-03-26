"""
This script allows for zoomed-in viewing of images in the local GUI.

Code for the basic framework was borrowed from:
http://www.rkblog.rk.edu.pl/w/p/simple-text-editor-pyqt4/

Code for using PyQt4 functions is from PyQt Class Reference:
http://pyqt.sourceforge.net/Docs/PyQt4/classes.html

Copyright (c) 2013 Nick Klose, Richard Leung, Cameron Mann,
Glen Nelson, Omar Qadri, and James Wang under the 401 IP License.
See LICENSE file for more details.
"""

# Import python modules
import sys
import os.path
from PyQt4 import QtCore, QtGui
from gui_graphzoom import Ui_graphZoomWindow

class GraphZoom(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.ui = Ui_graphZoomWindow()
        self.ui.setupUi(self)
        self.imagePath = None

        # Force consistent theme and font size
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))
        self.setStyleSheet("font-size: 11pt")
    
        # Map close button
        QtCore.QObject.connect(self.ui.closeButton,
                               QtCore.SIGNAL("clicked()"),
                               self.close)

    # Loads an image from the given path into the interface
    def load_image(self, path):
        print("Loading image from path " + path)
        self.ui.image.setPixmap(QtGui.QPixmap(path))
        self.imagePath = path

def start():
    app = QtGui.QApplication(sys.argv)
    myapp = GraphZoom()
    myapp.show()
    sys.exit(app.exec_())
