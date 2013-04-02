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
import shutil
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

        # Prevent resizing
        self.setFixedSize(self.size())

        # Close Window Button
        QtCore.QObject.connect(self.ui.closeButton,
                               QtCore.SIGNAL("clicked()"),
                               self.close)

        # Save Image Button
        QtCore.QObject.connect(self.ui.saveButton,
                               QtCore.SIGNAL("clicked()"),
                               self.save)

    # Loads an image from the given path into the interface
    def load_image(self, path):
        self.ui.image.setPixmap(QtGui.QPixmap(path))
        self.imagePath = path

    # Saves an image to a path of the user's choice
    def save(self):
        if self.imagePath != "" and self.imagePath != None:
            # get the path to save the image to
            savePath = QtGui.QFileDialog.getSaveFileName(self,
                                                         "Save File",
                                                         "",
                                                         "PNG Image (*.png)")
            # copy the image to the chosen destination
            shutil.copyfile(self.imagePath, savePath)

def start():
    app = QtGui.QApplication(sys.argv)
    myapp = GraphZoom()
    myapp.show()
    sys.exit(app.exec_())
