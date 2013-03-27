"""
This script provides functionality for batch mode in the local GUI.

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
import scipy
import numpy
import PIL
import thread
from PyQt4 import QtCore, QtGui
from gui_batch import Ui_Dialog

# Enable importing of other project modules
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(CUR_DIR)
sys.path.append(ROOT_DIR)

# Global constants
TEMP_DIR = "./ics_tmp"

class Batch(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Force consistent theme and font size
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))
        self.setStyleSheet("font-size: 11pt")

        # Run startup functions
        self.initialize()

        # Current directory path
        self.path = None

        # Track parent window
        self.parent = parent
        
        #######################################################
        # Interface Object Connections                        #
        #######################################################

        clicked = QtCore.SIGNAL("clicked()")
        
        ## Buttons
        QtCore.QObject.connect(self.ui.startButton, clicked, self.start)
        QtCore.QObject.connect(self.ui.stopButton, clicked, self.stop)
        QtCore.QObject.connect(self.ui.loadButton, clicked, self.load)
        QtCore.QObject.connect(self.ui.singleModeButton, clicked, self.single_mode)

    #######################################################
    # Connection Functions                                #
    #######################################################

    # Starts the selected correlation
    def start(self):
        pass

    # Stops the current operation
    def stop(self):
        pass

    # Loads a folder into the interface
    def load(self):
        pass

    # Switches to single mode
    def single_mode(self):
        self.parent.show()
        self.close()

    #######################################################
    # Miscellaneous Functions                             #
    #######################################################

    # Runs any functions needed upon program startup
    def initialize(self):
        self.refresh_temp()             # delete and recreate temp directory
        self.set_default_parameters()   # show default parameters in input fields
        self.load_default_images()      # show default placeholder images
        self.set_processing(False)      # disable processing mode

    # Deletes and recreates the temporary directory
    def refresh_temp(self):
        pass
    
    # Shows default parameters on all input fields
    def set_default_parameters(self):
        pass

    # Shows default placeholder images
    def load_default_images(self):
        pass

    # Enables or disables processing mode
    def set_processing(self, value):
        pass

# Program loop
def start():
    app = QtGui.QApplication(sys.argv)
    batch_app = Batch()
    batch_app.show()
    sys.exit(app.exec_())
