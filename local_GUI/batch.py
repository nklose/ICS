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
from help import Help

# Enable importing of other project modules
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(CUR_DIR)
sys.path.append(ROOT_DIR)

# Import midend modules
import midend.batchRunner

# Global constants
TEMP_DIR = "./ics_tmp"
PLACEHOLDER = "./Images/rgb.png"

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
        self.size = 0         # length in pixels of one size of an image
        self.numImages = 0    # total number of images to run
        self.numProcessed = 0 # number of images processed so far
        self.imageType = None # current type of image being processed
        self.splitMin = None  # minimum image number for split images
        self.splitMax = None  # maximum image number for split images
        self.mixedMin = None  # minimum image number for mixed images
        self.mixedMax = None  # maximum image number for mixed images

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
        QtCore.QObject.connect(self.ui.helpButton, clicked, self.show_help)

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
            mixedBR = None
            splitBR = None

            if len(self.rgbImages) != 0:
                self.imageType = "mixed"
                mixedConfig = self.get_config(True)
                mixedBR = midend.batchRunner.BatchRunner(mixedConfig)
                mixedBR.runAll(self.update_batch_progress)
                mixedBR.outputAllFiles()

            if len(self.monoImages) != 0:
                self.imageType = "split"
                splitConfig = self.get_config(False)                
                splitBR = midend.batchRunner.BatchRunner(splitConfig)
                splitBR.runAll(self.update_batch_progress)
                splitBR.outputAllFiles()

            outputDirectory = str(self.path) + "_output"
            self.message(str(len(self.rgbImages) + len(self.monoImages) / 3) + " correlations performed. Results outputted to " + outputDirectory + ".")

        self.set_processing(False)

    # Stops the current operation
    def stop(self):
        self.set_processing(False)

    # Loads a folder into the interface
    def load(self):
        self.set_processing(True)
        
        self.size = 0
        self.numProcessed = 0
        self.numImages = 0

        self.message("Loading directory and detecting images.")

        self.path = str(QtGui.QFileDialog.getExistingDirectory(self, "Load"))

        if self.path != None and self.path != "":
            self.ui.folderLabel.setText(os.path.basename(self.path))
            files = os.listdir(self.path)

            self.rgbImages = []
            self.monoImages = []
            self.extensions = []

            self.mixedMin = None
            self.mixedMax = None
            self.splitMin = None
            self.splitMax = None
    
            # iterate through all files
            for image in files:
                if self.get_number(image) != "IGNORE":
                    if self.size == 0:
                        i = PIL.Image.open(os.path.join(self.path,str(image)))
                        self.size = i.size[0]
                    image = str(image)
                    channels = self.get_channels(image)
                    if channels == "rgb":
                        self.rgbImages.append(image)
                        if self.mixedMin == None:
                            self.mixedMin = self.get_number(image)
                        elif self.mixedMax == None:
                            self.mixedMax = self.get_number(image)
                        else:
                            if self.get_number(image) < self.mixedMin:
                                self.mixedMin = self.get_number(image)
                            if self.get_number(image) > self.mixedMax:
                                self.mixedMax = self.get_number(image)
                    else:
                        if self.splitMin == None:
                            self.splitMin = self.get_number(image)
                        elif self.splitMax == None:
                            self.splitMax = self.get_number(image)
                        else:
                            if self.get_number(image) < self.splitMin:
                                self.splitMin = self.get_number(image)
                            if self.get_number(image) > self.splitMax:
                                self.splitMax = self.get_number(image)
                        if channels == "r":
                            self.monoImages.append(image)
                        elif channels == "g":
                            self.monoImages.append(image)
                        elif channels == "b":
                            self.monoImages.append(image)
                        else:
                            self.message("Warning: improperly formatted filename(s) found.")
                    if str(os.path.splitext(image)[1]) not in self.extensions:
                        self.extensions.append(str(os.path.splitext(image)[1]))
                
            # Sort the resulting lists
            self.rgbImages.sort()
            self.monoImages.sort()

            # update file counts
            self.ui.rgbCount.setText(str(len(self.rgbImages)))
            self.ui.monoCount.setText(str(len(self.monoImages)) + " (" + str(len(self.monoImages)/3) + ")")
            self.ui.fileCount.setText(str(len(self.rgbImages) + len(self.monoImages)))

            self.numImages = (len(self.monoImages) / 3) + len(self.rgbImages)

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

    # Shows the help dialog
    def show_help(self):
        help = Help(self)
        help.show()

    #######################################################
    # Miscellaneous Functions                             #
    #######################################################

    # Updates the interface to reflect the current batch state. Called whenever
    # a new image is being correlated.
    def update_batch_progress(self, numFinished, numTotal):
        outputString = "Running " + str(numFinished) + " of " + str(numTotal)
        currentPath = None
        if self.imageType == "mixed":
            outputString += " mixed images."
            currentImage = self.rgbImages[self.numProcessed + self.mixedMin]
            currentPath = os.path.join(self.path, currentImage)

        elif self.imageType == "split":
            outputString += " split images."
            currentImage = self.monoImages[self.numProcessed + self.splitMin - len(self.rgbImages)]
            currentPath = os.path.join(self.path, currentImage)
        
        # Show the current image in the interface
        self.ui.image.setPixmap(QtGui.QPixmap(currentPath))
        self.ui.imagePath.setText(currentPath)

        self.message(outputString)
        self.numSteps = self.numImages
        self.numProcessed += 1
        self.progress(self.numProcessed)

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
        self.ui.dualRange.setPlaceholderText("20")
        self.ui.dualGinf.setPlaceholderText("0")
        self.ui.dualW.setPlaceholderText("10")
        self.ui.dualG0.setPlaceholderText("1")
        
        self.ui.tripleRange.setPlaceholderText("20")
        self.ui.tripleGinf.setPlaceholderText("0")
        self.ui.tripleW.setPlaceholderText("10")
        self.ui.tripleG0.setPlaceholderText("1")

    # Shows default placeholder image
    def load_default_images(self):
        self.ui.image.setPixmap(QtGui.QPixmap(PLACEHOLDER))

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
        file_number = ""
        for c in filename:
            if number:
                file_number += c
            if c == "_":
                number = True
            elif c == ".":
                number = False

        try:
            return int(file_number[:-1])
        except:
            return "IGNORE" # ignore this file as it doesn't follow syntax
 
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
        # read values from inputs
        dual_range = str(self.ui.dualRange.text())
        dual_g0 = str(self.ui.dualG0.text())
        dual_w = str(self.ui.dualW.text())
        dual_ginf = str(self.ui.dualGinf.text())
        triple_range = str(self.ui.tripleRange.text())
        triple_g0 = str(self.ui.tripleG0.text())
        triple_w = str(self.ui.tripleW.text())
        triple_ginf = str(self.ui.tripleGinf.text())

        validInput = True

        # Check if input is valid
        if dual_range == "" or dual_g0 == "" or dual_w == "" or dual_ginf == "" or triple_range == "" or triple_g0 == "" or triple_w == "" or triple_ginf == "":
            self.message("Some parameters are missing; aborting.")
            validInput = False
        else:
            try:
                dr = int(dual_range)
                tr = int(triple_range)
                dg0 = float(dual_g0)
                tg0 = float(triple_g0)
                dw = float(dual_w)
                tw = float(triple_w)
                dginf = float(dual_ginf)
                tginf = float(triple_ginf)
                if dg0 < 0 or tg0 < 0 or dginf < 0 or tginf < 0:
                    validInput = False
                    self.message("Some parameters are negative; aborting.")
                elif dr <= 0 or tr <= 0:
                    validInput = False
                    self.message("Range must be greater than 0; aborting.")
                elif dw <= 0 or tw <= 0:
                    validInput = False
                    self.message("W parmeter must be greater than 0; aborting.")
                elif tr > self.get_limit():
                    self.message("Triple range cannot be larger than the sample resolution.")
                    validInput = False
            except ValueError:
                validInput = False
                self.message("Some parameters are non-numeric; aborting.")
        return validInput
    
    # Returns the selected limit for triple correlations.
    def get_limit(self):
        if bool(self.ui.resolution16.isChecked()):
            return 16
        elif bool(self.ui.resolution64.isChecked()):
            return 64
        else:
            return 32

    # Creates a mixed image config object for BatchRunner using the current program 
    # state. If the mixed input parameter is true, the config object will be set up 
    # for single RGB images; otherwise, split monochrome images will be used.
    def get_config(self, mixed):
        config = Config()
        config.side = self.size
        config.input_directory = self.path
        config.output_directory = os.path.join(os.path.dirname(self.path), 
                                               os.path.basename(self.path) + "_output")
        config.dual_range = int(self.ui.dualRange.text())
        config.triple_range = int(self.ui.tripleRange.text())
        config.auto_consider_deltas = bool(self.ui.considerAutoDeltas.isChecked())
        config.cross_consider_deltas = bool(self.ui.considerCrossDeltas.isChecked())
        config.dual_initial = numpy.array([self.ui.dualG0.text(),
                                           self.ui.dualW.text(),
                                           self.ui.dualGinf.text(),0,0], dtype = numpy.float)
        config.triple_initial = numpy.array([self.ui.tripleG0.text(),
                                             self.ui.tripleW.text(),
                                             self.ui.tripleGinf.text()], dtype = numpy.float)
        config.triple_lim = self.get_limit()
        if mixed:
            config.input_type = "mixed"
            config.name_format = "rgb_{:03d}.bmp"
            config.output_type = "full"
            config.name_min = self.mixedMin
            config.name_max = self.mixedMax
        else:
            config.input_type = "split"
            config.name_format = "{:s}_{:03d}.bmp"
            config.output_type = "full"
            config.name_min = self.splitMin
            config.name_max = self.splitMax
        config.output_numbering = "{:03d}"

        return config
        
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
