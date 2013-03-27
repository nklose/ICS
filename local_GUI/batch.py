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
import shutil
from PyQt4 import QtCore, QtGui
from gui_batch import Ui_Dialog

# Enable importing of other project modules
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(CUR_DIR)
sys.path.append(ROOT_DIR)

# Global constants
TEMP_DIR = "./ics_tmp"
RGB_PLACEHOLDER = "./Images/rgb.png"
RED_PLACEHOLDER = "./Images/r.png"
GREEN_PLACEHOLDER = "./Images/g.png"
BLUE_PLACEHOLDER = "./Images/b.png"

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

        self.path = None      # directory containing all images
        self.rgbImages = []   # list containing RGB image paths
        self.monoImages = []  # list containing monochrome image paths
        self.extensions = []  # list of file extensions in directory
        self.numSteps = 0     # number of steps in current process
        self.rgbCount = 0     # number of RGB images in current directory
        self.monoCount = 0    # number of monochrome images in current directory

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
        self.set_processing(True)

    # Stops the current operation
    def stop(self):
        self.set_processing(False)

    # Loads a folder into the interface
    def load(self):
        self.set_processing(True)

        self.message("Loading directory and detecting images.")

        self.path = str(QtGui.QFileDialog.getExistingDirectory(self, "Load"))

        if self.path != None and self.path != "":
            self.ui.folderLabel.setText(os.path.basename(self.path))
            files = os.listdir(self.path)

            self.rgbImages = []
            self.monoImages = []
            self.extensions = []
    
            # iterate through all files
            for image in files:
                image = str(image)
                channels = self.get_channels(image)
                if channels == "rgb":
                    self.rgbImages.append(image)
                elif channels == "r":
                    self.monoImages.append(image)
                elif channels == "g":
                    self.monoImages.append(image)
                elif channels == "b":
                    self.monoImages.append(image)
                else:
                    self.message("Warning: improperly formatted filename(s) found.")
                if str(os.path.splitext(image)[1]) not in self.extensions:
                    self.extensions.append(str(os.path.splitext(image)[1]))

            # update file counts
            self.ui.rgbCount.setText(str(len(self.rgbImages)))
            self.ui.monoCount.setText(str(len(self.monoImages)) + " (" + str(len(self.monoImages)/3) + ")")
            self.ui.fileCount.setText(str(len(self.rgbImages) + len(self.monoImages)))

            # convert extension list to string and display it
            extList = ""
            for ext in self.extensions:
                extList += str(ext)[1:] + ", "
            extList = extList[:-2]
            self.ui.formatsList.setText(extList.upper())
                

        self.set_processing(False)

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
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR)
        
    # Shows default parameters on all input fields
    def set_default_parameters(self):
        self.ui.autoRangeTextbox.setPlaceholderText("20")
        self.ui.autoGinfTextbox.setPlaceholderText("0")
        self.ui.autoWTextbox.setPlaceholderText("10")
        self.ui.autoG0Textbox.setPlaceholderText("1")
        
        self.ui.crossRangeTextbox.setPlaceholderText("20")
        self.ui.crossGinfTextbox.setPlaceholderText("0")
        self.ui.crossWTextbox.setPlaceholderText("10")
        self.ui.crossG0Textbox.setPlaceholderText("1")

        self.ui.allAutoCrossRangeTextbox.setPlaceholderText("20")
        self.ui.allAutoCrossGinfTextbox.setPlaceholderText("0")
        self.ui.allAutoCrossWTextbox.setPlaceholderText("10")
        self.ui.allAutoCrossG0Textbox.setPlaceholderText("1")

        self.ui.allTripleRangeTextbox.setPlaceholderText("20")
        self.ui.allTripleGinfTextbox.setPlaceholderText("0")
        self.ui.allTripleWTextbox.setPlaceholderText("10")
        self.ui.allTripleG0Textbox.setPlaceholderText("1")

        self.ui.tripleRangeTextbox.setPlaceholderText("20")
        self.ui.tripleGinfTextbox.setPlaceholderText("0")
        self.ui.tripleWTextbox.setPlaceholderText("10")
        self.ui.tripleG0Textbox.setPlaceholderText("1")

    # Shows default placeholder images
    def load_default_images(self):
        self.ui.imageRgb.setPixmap(QtGui.QPixmap(RGB_PLACEHOLDER))
        self.ui.imageRed.setPixmap(QtGui.QPixmap(RED_PLACEHOLDER))
        self.ui.imageGreen.setPixmap(QtGui.QPixmap(GREEN_PLACEHOLDER))
        self.ui.imageBlue.setPixmap(QtGui.QPixmap(BLUE_PLACEHOLDER))

    # Enables or disables processing mode
    def set_processing(self, value):
        self.ui.startButton.setEnabled(not value)
        self.ui.stopButton.setEnabled(value)
        self.ui.singleModeButton.setEnabled(not value)
        self.ui.correlationSettingsGroup.setEnabled(not value)
        self.ui.imageParametersGroup.setEnabled(not value)
        self.ui.progressBar.setVisible(value)

    # Sets the progress bar based on the current step in the process and the
    #  total number of steps. The current step is passed to the function, and
    #  the total number is stored in self.numSteps and updated each process.
    def progress(self, value):
        self.ui.progressBar.setValue(value * 100 / self.numSteps)

    # Updates the message bar with some text.
    def message(self, text):
        self.ui.messageBox.setText(str(text))

    # Returns the channels contained in an image as a string by grabbing the
    #  text before the underscore of a filename. For example, if the filename
    #  is g_024.png, the string "g" will be returned.
    def get_channels(self, filename):
        prefix = True
        file_prefix = ""
        for c in filename:
            if c == "_":
                prefix = False
            if prefix:
                file_prefix += c
        return file_prefix

    # Returns the number of an image by grabbing the text after the underscore.
    #  for example, a filename of b_003.png will return 3 as an integer.
    def get_number(self, filename):
        number = False
        file_number = 0
        for c in filename:
            if number:
                file_number += c
            if c == "_":
                number = True
            elif c == ".":
                number = False

        return int(file_number)
                
# Program loop
def start():
    app = QtGui.QApplication(sys.argv)
    batch_app = Batch()
    batch_app.show()
    sys.exit(app.exec_())
