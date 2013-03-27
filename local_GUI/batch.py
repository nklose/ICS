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

# Import midend modules
import midend.batchRunner

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
        validInput = self.validate_input()
        if validInput:
            # begin process
            self.message("Beginning batch correlation process.")
            
            # create config object
            config = Config()
            br = midend.batchRunner.BatchRunner(config)

        self.set_processing(False)

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
 
    # Returns the selected correlation mode by reading which tab the user has open
    def get_correlation_tab(self):
        cur = self.ui.correlationTabWidget.currentIndex()
        if cur == 0:
            return "auto"
        elif cur == 1:
            return "cross"
        elif cur == 2:
            return "triple"
        elif cur == 3:
            return "all"
        else:
            return "<error>"

    # Validates input parameters. Returns True only if parameters are valid.
    def validate_input(self):
        mode = self.get_correlation_tab()
        # auto, cross, and triple-correlation parameters
        mode = self.get_correlation_tab()
        range_val = None
        g0 = None
        w = None
        ginf = None
        none_checked = True
        # all correlations - extra parameters
        range_val2 = None
        g02 = None
        w2 = None
        ginf = None
        # get input depending on current mode
        if mode == "auto":
            if self.ui.redCheckbox.isChecked():
                none_checked = False
            elif self.ui.greenCheckbox.isChecked():
                none_checked = False
            elif self.ui.blueCheckbox.isChecked():
                none_checked = False
            range_val = str(self.ui.autoRangeTextbox.text())
            g0 = str(self.ui.autoG0Textbox.text())
            w = str(self.ui.autoWTextbox.text())
            ginf = str(self.ui.autoGinfTextbox.text())
        elif mode == "cross":
            if self.ui.redGreenCheckbox.isChecked():
                none_checked = False
            elif self.ui.redBlueCheckbox.isChecked():
                none_checked = False
            elif self.ui.greenBlueCheckbox.isChecked():
                none_checked = False
            range_val = str(self.ui.crossRangeTextbox.text())
            g0 = str(self.ui.crossG0Textbox.text())
            w = str(self.ui.crossWTextbox.text())
            ginf = str(self.ui.crossGinfTextbox.text())
        elif mode == "triple":
            none_checked = False
            range_val = str(self.ui.tripleRangeTextbox.text())
            g0 = str(self.ui.tripleG0Textbox.text())
            w = str(self.ui.tripleWTextbox.text())
            ginf = str(self.ui.tripleGinfTextbox.text())
        elif mode == "all":
            none_checked = False
            range_val = str(self.ui.allAutoCrossRangeTextbox.text())
            g0 = str(self.ui.allAutoCrossG0Textbox.text())
            w = str(self.ui.allAutoCrossWTextbox.text())
            ginf = str(self.ui.allAutoCrossGinfTextbox.text())
            range_val2 = str(self.ui.allTripleRangeTextbox.text())
            g02 = str(self.ui.allTripleG0Textbox.text())
            w2 = str(self.ui.allTripleWTextbox.text())
            ginf2 = str(self.ui.allTripleGinfTextbox.text())
        # Check if input is valid
        validInput = True
        if none_checked:
            self.message("At least one checkbox is needed; aborting.")
            validInput = False
        elif range_val == "" or g0 == "" or ginf == "" or w == "":
            self.message("Some parameters are missing; aborting.")
            validInput = False
        else:
            try:
                int(range_val)
                float(g0)
                float(w)
                float(ginf)
            except ValueError:
                validInput = False
                self.message("Some parameters are non-numeric; aborting.")
            if mode == "all":
                if range_val2 == "" or g02 == "" or ginf2 == "" or w2 == "":
                    self.message("Some parameters are missing; aborting.")
                    validInput = False
                else:
                    try:
                        int(range_val2)
                        float(g02)
                        float(w2)
                        float(ginf2)
                    except ValueError:
                        validInput = False
                        self.message("Some parameters are non-numeric; aborting.")

        return validInput
                          
# Program loop
def start():
    app = QtGui.QApplication(sys.argv)
    batch_app = Batch()
    batch_app.show()
    sys.exit(app.exec_())

# Configuration object for doing batch operations on
class Config:
    side = None
    input_directory = None
    output_directory = None
    name_min = None
    name_max = None
    name_format = None
    dual_range = None
    triple_range = None
    auto_consider_deltas = None
    cross_consider_deltas = None
    dual_initial = numpy.array([1, 10, 0, 0, 0], dtype = numpy.float)
    triple_initial = numpy.array([50, 2, 0], dtype = numpy.float)
    triple_lim = 32
    input_type = 'mixed'
    output_type = 'full'
    output_numbering = 'none'
