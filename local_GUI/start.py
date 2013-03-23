"""
This script loads up the local GUI and calls the backend.

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
import shutil # used to recursively remove directories
from PyQt4 import QtCore, QtGui
from PIL import Image
from main_ICS import Ui_Dialog

# Enable backend importing
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(CUR_DIR)
sys.path.append(ROOT_DIR)

# Import backend modules
import backend.bimloader as bimloader
import backend.dual as dual
import backend.triple as triple

# Import midend modules
import midend.adaptor

# Global constants
PRECISION = 6      # number of decimal places to show for output values


class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # Force theme
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))
        self.setStyleSheet("font-size: 11pt")

        # Interface variables
        self.redPath = ""
        self.greenPath = ""
        self.bluePath = ""
        self.rgbPath = ""

        # Image arrays
        self.redChannel = ""
        self.greenChannel = ""
        self.blueChannel = ""
        self.rgbChannel = ""

        # Temporary file directory (used during runtime only)
        self.temp_dir = "./ics_tmp"

        # Size of the images in pixels (e.g. 64 would mean a 64x64 image)
        self.size = 0

        # Result of most recent triple correlation part, used for next part
        self.tripleResult = None

        #######################################################
        # Interface Object Connections                        #
        #######################################################

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

        # Correlation tabs
        QtCore.QObject.connect(self.ui.correlationTabWidget,
                               QtCore.SIGNAL("currentChanged()"),
                               self.update)

        # Start Button
        QtCore.QObject.connect(self.ui.startButton,
                               QtCore.SIGNAL("clicked()"),
                               self.start)

        # Stop BUtton
        QtCore.QObject.connect(self.ui.stopButton,
                               QtCore.SIGNAL("clicked()"),
                               self.stop)

        # Continue Button 1
        QtCore.QObject.connect(self.ui.continueButton1,
                               QtCore.SIGNAL("clicked()"),
                               self.triple_process)

        # Continue Button 2
        QtCore.QObject.connect(self.ui.continueButton2,
                               QtCore.SIGNAL("clicked()"),
                               self.triple_complete)


    #######################################################
    # Interface Object Functions                          #
    #######################################################

    # Loads an RGB image into the interface.
    def load_RGB_image(self):
        self.message("Loading RGB Image...")
        validImage = True

        # Open the file loader and get the path of the desired image
        self.rgbPath = str(QtGui.QFileDialog.getOpenFileName())

        # Call the backend to separate the image by channel
        try:
            images = bimloader.load_image_mixed(str(self.rgbPath))
        except bimloader.ImageFormatException:
            validImage = False
            self.msgBadFormat()
            self.rgbPath = ""

        if validImage:
            # Update user interface with image
            self.message("Loaded image " + self.rgbPath)
            self.ui.rgbFile.setText(os.path.basename(self.rgbPath))
            self.ui.imageRgb.setPixmap(QtGui.QPixmap(self.rgbPath))

            # Save the three channel arrays
            self.redChannel = images[0]
            self.greenChannel = images[1]
            self.blueChannel = images[2]

            # Save the image dimension
            self.update_size(self.redChannel.shape[1])

            # Update the red, green, and blue paths
            self.redPath = self.temp_dir + "/red.png"
            self.greenPath = self.temp_dir + "/green.png"
            self.bluePath = self.temp_dir + "/blue.png"

            # Refresh the temporary directory (delete and recreate)
            self.refresh_temp()

            # Use the arrays to generate images
            scipy.misc.imsave(self.redPath, self.redChannel)
            scipy.misc.imsave(self.greenPath, self.greenChannel)
            scipy.misc.imsave(self.bluePath, self.blueChannel)

            # Load the images into the interface
            self.ui.imageRed.setPixmap(QtGui.QPixmap(self.redPath))
            self.ui.imageGreen.setPixmap(QtGui.QPixmap(self.greenPath))
            self.ui.imageBlue.setPixmap(QtGui.QPixmap(self.bluePath))

            # Calculate the average intensity per pixel of each channel
            redAvgInt = self.aipp(self.redPath, self.size)
            greenAvgInt = self.aipp(self.greenPath, self.size)
            blueAvgInt = self.aipp(self.bluePath, self.size)

            # Update the interface with average intensities per pixel
            self.ui.redIntensityText.setText(str(redAvgInt))
            self.ui.greenIntensityText.setText(str(greenAvgInt))
            self.ui.blueIntensityText.setText(str(blueAvgInt))

    # Loads a red channel image into the interface.
    def load_red_image(self):
        self.message("Loading red image...")
        validImage = True

        # Open the file loader to get the path of the desired image
        self.redPath = str(QtGui.QFileDialog.getOpenFileName())

        # Call the backend to check that the file extension is valid
        try:
            self.redChannel = bimloader.load_image_split(str(self.redPath))
        except bimloader.ImageFormatException:
            validImage = False
            self.msgBadFormat()
            self.redPath = ""

        if validImage:
            # Clear RGB path, since the user has opted to use single-channel images
            self.rgbPath = ""

            # Update user interface with image
            self.message("Loaded image " + self.redPath)
            self.ui.redChannelFile.setText(os.path.basename(self.redPath))
            self.ui.imageRed.setPixmap(QtGui.QPixmap(self.redPath))

            # Remove any temporary images from the interface
            self.refresh_temp()
            #self.refresh_paths()

            # Remember old size in case something bad happens
            oldSize = self.size

            # Update image size
            self.update_size(self.redChannel.shape[1])

            # Calculate average intensity per pixel
            monochrome = True
            redAvgInt = 0
            try:
                redAvgInt = self.aipp(self.redPath, self.size)
            except:
                self.msgBadChannels()
                self.ui.imageRed.clear()
                self.redPath = ""
                self.redChannel = ""
                monochrome = False
                self.update_size(oldSize)

            if monochrome:
                self.ui.redIntensityText.setText(str(redAvgInt))

                # Construct an RGB image from three channel images, if possible
                self.constructRGB()

    # Loads a green channel image into the interface.
    def load_green_image(self):
        self.message("Loading green image...")
        validImage = True

        # Open the file loader to get the path of the desired image
        self.greenPath = str(QtGui.QFileDialog.getOpenFileName())

        # Call the backend to load the image as an array
        try:
            self.greenChannel = bimloader.load_image_split(str(self.greenPath))

        except bimloader.ImageFormatException:
            validImage = False
            self.msgBadFormat()
            self.greenPath = ""
        except:
            validImage = False
            self.msgBadChannels()
            self.greenPath = ""

        if validImage:
            # Update user interface with image
            self.message("Loaded image " + self.greenPath)
            self.ui.greenChannelFile.setText(os.path.basename(self.greenPath))
            self.ui.imageGreen.setPixmap(QtGui.QPixmap(self.greenPath))

            # Clear RGB path, since the user has opted to use single-channel images
            self.rgbPath = ""

            # Remove any temporary images from the interface
            self.refresh_temp()

            # Remember old size in case something bad happens
            oldSize = self.size

            # Update image size
            self.update_size(self.greenChannel.shape[1])

            # Calculate average intensity per pixel
            monochrome = True
            greenAvgInt = 0
            try:
                greenAvgInt = self.aipp(self.greenPath, self.size)
            except:
                self.msgBadChannels()
                self.ui.imageGreen.clear()
                self.greenPath = ""
                self.greenChannel = ""
                monochrome = False
                self.update_size(oldSize)

            if monochrome:
                self.ui.greenIntensityText.setText(str(greenAvgInt))

                # Construct an RGB image from three channel images, if possible
                self.constructRGB()# Update average intensity per pixel

    # Loads a blue channel image into the interface
    def load_blue_image(self):
        self.message("Loading blue image...")
        validImage = True

        # Open the file loader to get the path of the desired image
        self.bluePath = str(QtGui.QFileDialog.getOpenFileName())

        # Call the backend to load the image as an array
        try:
            self.blueChannel = bimloader.load_image_split(str(self.bluePath))
        except bimloader.ImageFormatException:
            validImage = False
            self.msgBadFormat()
            self.bluePath = ""
        except:
            validImage = False
            self.msgBadChannels()
            self.bluePath = ""

        if validImage:
            # Update user interface with image
            self.message("Loaded image " + self.bluePath)
            self.ui.blueChannelFile.setText(os.path.basename(self.bluePath))
            self.ui.imageBlue.setPixmap(QtGui.QPixmap(self.bluePath))

            # Clear RGB path, since the user has opted to use single-channel images
            self.rgbPath = ""

            # Remove any temporary images from the interface
            self.refresh_temp()

            # Remember old size in case something bad happens
            oldSize = self.size

            # Update image size
            self.update_size(self.blueChannel.shape[1])

            # Calculate average intensity per pixel
            monochrome = True
            blueAvgInt = 0
            try:
                blueAvgInt = self.aipp(self.bluePath, self.size)
            except:
                self.msgBadChannels()
                self.ui.imageBlue.clear()
                self.bluePath = ""
                monochrome = False
                self.update_size(oldSize)

            if monochrome:
                self.ui.blueIntensityText.setText(str(blueAvgInt))

                # Construct an RGB image from three channel images, if possible
                self.constructRGB()


    # Start button functionality
    def start(self):
        # Disable start button and batch button and enable stop button
        self.ui.startButton.setEnabled(False)
        self.ui.stopButton.setEnabled(True)
        self.ui.batchModeButton.setEnabled(False)

        # Find out which correlation to do
        mode = self.get_correlation_tab()

        # Validate input
        validInput = self.validate_input(mode)

        # Continue if input is valid
        if validInput:

            # Remove values and images from output tab, if necessary
            self.clear_output_tab()

            # Update message bar with input parameters
            text = ""
            if mode == "auto":
                self.autoCorrelation()

            elif mode == "cross":
                self.crossCorrelation()

            elif mode == "triple":
                self.tripleCorrelation()

            elif mode == "all":
                # Construct string containing channels to be used
                self.msgAll()
                red = self.redChannel
                green = self.greenChannel
                blue = self.blueChannel
                result = self.correlate_all(red, green, blue)
                redAuto = result[0]
                greenAuto = result[1]
                blueAuto = result[2]
                redGreenCross = result[3]
                redBlueCross = result[4]
                greenBlueCross = result[5]
                self.select_tab("output", "triple")
                self.show_fourier()
            else:
                self.message("Mode error.")

        # Disable stop button and re-enable start button and batch button
        self.ui.startButton.setEnabled(True)
        self.ui.batchModeButton.setEnabled(True)
        self.ui.stopButton.setEnabled(False)

    # Stop button functionality
    def stop(self):
        self.message("Stopping correlation.")

        # Reset progress bar
        self.progress(0)

        # Enable start button and batch mode button, and disable stop button
        self.ui.startButton.setEnabled(True)
        self.ui.stopButton.setEnabled(False)
        self.ui.batchModeButton.setEnabled(True)


    ######################################################
    # Interface Input Functions                          #
    ######################################################

    # Returns 'input' or 'output' depending on current tab
    def get_main_tab(self):
        cur = self.ui.mainTabWidget.currentIndex()
        if cur == 0:
            return "input"
        elif cur == 1:
            return "output"
        else:
            return "<error in mainTabWidget>"

    # Returns "three" or "one" depending on which tab the
    #  user has selected in Image Settings
    def get_image_tab(self):
        cur = self.ui.imageSettingsTabWidget.currentIndex()
        if cur == 0:
            return "three"
        elif cur == 1:
            return "one"
        else:
            return "<error in imageSettingsTabWidget>"

    # Returns "auto", "cross", "triple", or "all" depending on
    #  which correlation settings tab the user has selected.
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
            return "<error in correlationTabWidget>"

    ## Checkboxes
    # Returns state of AC Red checkbox
    def get_red_checkbox(self):
        if self.ui.redCheckbox.checkState() != 0:
            return True
        else:
            return False

    # Returns state of AC Green checkbox
    def get_green_checkbox(self):
        if self.ui.greenCheckbox.checkState() != 0:
            return True
        else:
            return False

    # Returns state of AC Blue checkbox
    def get_blue_checkbox(self):
        if self.ui.blueCheckbox.checkState() != 0:
            return True
        else:
            return False

    # Returns state of XC-RG checkbox
    def get_red_green_checkbox(self):
        if self.ui.redGreenCheckbox.checkState() != 0:
            return True
        else:
            return False

    # Returns state of XC-RB checkbox
    def get_red_blue_checkbox(self):
        if self.ui.redBlueCheckbox.checkState() != 0:
            return True
        else:
            return False

    # Returns state of XC-GB checkbox
    def get_green_blue_checkbox(self):
        if self.ui.greenBlueCheckbox.checkState() != 0:
            return True
        else:
            return False

    # Returns state of AC Consider Deltas checkbox
    def get_auto_deltas_checkbox(self):
        if self.ui.autoDeltasCheckbox.checkState() != 0:
            return True
        else:
            return False

    # Returns the state of the XC Consider Deltas checkbox
    def get_cross_deltas_checkbox(self):
        if self.ui.crossDeltasCheckbox.checkState() != 0:
            return True
        else:
            return False

    # Returns the state of the All Correlations Consider Deltas checkbox
    def get_all_deltas_checkbox(self):
        if self.ui.allDeltasCheckbox.checkState() != 0:
            return True
        else:
            return False

    # Returns the state of the TC Consider Deltas checkbox
    def get_triple_deltas_checkbox(self):
        if self.ui.allDeltasCheckbox.checkState() != 0:
            return True
        else:
            return False

    ## Text inputs
    # Returns inputted Range in AC
    def get_auto_range(self):
        return int(self.ui.autoRangeTextbox.text())

    # Returns inputted G(0) in AC
    def get_auto_G0(self):
        return float(self.ui.autoG0Textbox.text())

    # Returns inputted W in AC
    def get_auto_W(self):
        return float(self.ui.autoWTextbox.text())

    # Returns inputted G(Inf) in AC
    def get_auto_Ginf(self):
        return float(self.ui.autoGinfTextbox.text())

    # Returns inputted Range in XC
    def get_cross_range(self):
        return int(self.ui.crossRangeTextbox.text())

    # Returns inputted G(0) in XC
    def get_cross_G0(self):
        return float(self.ui.crossG0Textbox.text())

    # Returns inputted W in XC
    def get_cross_W(self):
        return float(self.ui.crossWTextbox.text())

    # Returns inputted G(Inf) in XC
    def get_cross_Ginf(self):
        return float(self.ui.crossGinfTextbox.text())

    # Returns inputted Range in AXC
    def get_all_range(self):
        return int(self.ui.allAutoCrossRangeTextbox.text())

    # Returns inputted G(0) in AXC
    def get_all_G0(self):
        return float(self.ui.allAutoCrossG0Textbox.text())

    # Returns inputted W in AXC
    def get_all_W(self):
        return float(self.ui.allAutoCrossWTextbox.text())

    # Returns inputted Ginf in AXC
    def get_all_Ginf(self):
        return float(self.ui.allAutoCrossGinfTextbox.text())

    # Returns inputted limit for TC (Output Tab)
    def get_triple_limit(self):
        return float(self.ui.startingPointInput.text())

    # Returns inputted range for TC (Output Tab)
    def get_triple_range(self):
        return int(self.ui.tripleRangeTextbox.text())

    # Returns inputted G(0) for TC (Output Tab)
    def get_triple_G0(self):
        return float(self.ui.tripleG0Textbox.text())

    # Returns inputted W for TC (Output Tab)
    def get_triple_W(self):
        return float(self.ui.tripleWTextbox.text())

    # Returns inputted G(Inf) for TC (Output Tab)
    def get_triple_Ginf(self):
        return float(self.ui.tripleGinfTextbox.text())

    ## Radio buttons

    # Returns sample resolution (32, 48, or 64)
    def get_sample_resolution(self):
        if self.ui.resolution16.isChecked() != 0:
            return 16
        elif self.ui.resolution32.isChecked() != 0:
            return 32
        elif self.ui.resolution64.isChecked() != 0:
            return 64
        else:
            return -1

    # Validate interface input
    def validate_input(self, mode):
        validInput = True
        # Make sure a file has been loaded
        if self.rgbPath == "":
            if self.redPath == "" or self.greenPath == "" or self.bluePath == "":
                validInput = False
                text = "Load either one RGB image, or three "
                text += "monochrome images\nbefore starting the "
                text += "correlation process."
                self.message(text)

        if mode == "auto":
            # no channels selected
            none_checked = True
            if self.get_red_checkbox() == True:
                none_checked = False
            elif self.get_green_checkbox() == True:
                none_checked = False
            elif self.get_blue_checkbox() == True:
                none_checked = False

            if none_checked:
                self.message("You must select at least one channel.")
                validInput = False

            # blank range
            elif self.get_auto_range() == "":
                self.message("Range parameter missing.")
                validInput = False

            # blank g(0)
            elif self.get_auto_G0() == "":
                self.message("g(0) parameter missing.")
                validInput = False

            # blank W
            elif self.get_auto_W() == "":
                self.message("W parameter missing.")
                validInput = False

            # blank gInf
            elif self.get_auto_Ginf() == "":
                self.message("gInf parameter missing.")
                validInput = False

            else:
                # non-numeric range
                try:
                    float(self.get_auto_range())
                except ValueError:
                    validInput = False
                    self.message("Range must be a number.")

                # non-numeric g(0)
                try:
                    float(self.get_auto_G0())
                except ValueError:
                    validInput = False
                    self.message("g(0) must be a number.")

                # non-numeric W
                try:
                    float(self.get_auto_W())
                except ValueError:
                    validInput = False
                    self.message("w must be a number.")

                # non-numeric gInf
                try:
                    float(self.get_auto_Ginf())
                except ValueError:
                    validInput = False
                    self.message("gInf must be a number.")

        elif mode == "cross":
            # no channels selected
            none_checked = True
            if self.get_red_green_checkbox() == True:
                none_checked = False
            elif self.get_red_blue_checkbox() == True:
                none_checked = False
            elif self.get_green_blue_checkbox() == True:
                none_checked = False

            if none_checked:
                validInput = False
                self.message("You must select at least one channel pair.")

            # blank range
            elif self.get_cross_range() == "":
                validInput = False
                self.message("Range parameter missing.")

            # blank g(0)
            elif self.get_cross_G0() == "":
                validInput = False
                self.message("g(0) parameter missing.")

            # blank W
            elif self.get_cross_W() == "":
                validInput = False
                self.message("W parameter missing.")

            # blank gInf
            elif self.get_cross_Ginf() == "":
                validInput = False
                self.message("Ginf parameter missing.")

            else:
                # non-numeric range
                try:
                    float(self.get_cross_range())
                except ValueError:
                    validInput = False
                    self.message("Range must be a number.")

                # non-numeric g(0)
                try:
                    float(self.get_cross_G0())
                except ValueError:
                    validInput = False
                    self.message("g(0) must be a number.")

                # non-numeric W
                try:
                    float(self.get_cross_W())
                except ValueError:
                    validInput = False
                    self.message("W must be a number.")

                # non-numeric gInf
                try:
                    float(self.get_cross_Ginf())
                except ValueError:
                    validInput = False
                    self.message("gInf must be a number.")

        elif mode == "all":
            # blank range
            if self.get_all_range() == "":
                validInput = False
                self.message("Range parameter missing.")

            # blank g(0)
            elif self.get_all_G0() == "":
                validInput = False
                self.message("g(0) parameter missing.")

            # blank W
            elif self.get_all_W() == "":
                validInput = False
                self.message("W parameter missing.")

            # blank gInf
            elif self.get_all_Ginf() == "":
                validInput = False
                self.message("gInf parameter missing.")

            else:
                # non-numeric range
                try:
                    float (self.get_all_range())
                except ValueError:
                    validInput = False
                    self.message("Range must be a number.")

                # non-numeric g(0)
                try:
                    float (self.get_all_G0())
                except ValueError:
                    validInput = False
                    self.message("g(0) must be a number.")

                # non-numeric W
                try:
                    float (self.get_all_W())
                except ValueError:
                    validInput = False
                    self.message("W must be a number.")

                # non-numeric gInf
                try:
                    float (self.get_all_Ginf())
                except ValueError:
                    validInput = False
                    self.message("gInf must be a number.")

        return validInput

    ######################################################
    # Interface Output Functions                         #
    ######################################################

    # Set the Res. Norm. value on the auto tab
    def set_auto_resnorm(self, value):
        self.ui.autoResNormValue.setText(str(value))

    # Set the g0 value on the auto tab
    def set_auto_G0(self, value):
        self.ui.autoG0Value.setText(str(value))

    # Set the W value on the auto tab
    def set_auto_W(self, value):
        self.ui.autoWValue.setText(str(value))

    # Set the gInf value on the auto tab
    def set_auto_Ginf(self, value):
        self.ui.autoGinfValue.setText(str(value))

    # Set the deltas checkbox on the auto tab
    def set_auto_deltas(self, value):
        self.ui.autoDeltasUsedCheckbox.setChecked(bool(value))

    # Set the Res. Norm. value on the cross tab
    def set_cross_resnorm(self, value):
        self.ui.crossResNormValue.setText(str(value))

    # Set the g0 value on the cross tab
    def set_cross_G0(self, value):
        self.ui.crossG0Value.setText(str(value))

    # set the W value on the cross tab
    def set_cross_W(self, value):
        self.ui.crossWValue.setText(str(value))

    # Set the gInf value on the cross tab
    def set_cross_Ginf(self, value):
        self.ui.crossGinfValue.setText(str(value))

    # Set the deltas checkbox on the cross tab
    def set_cross_deltas(self, value):
        self.ui.crossDeltasUsedCheckbox.setChecked(bool(value))

    # Set the Res. Norm. value on the triple tab
    def set_triple_resnorm(self, value):
        self.ui.tripleResNormValue.setText(str(value))

    # Set the g0 value on the triple tab
    def set_triple_G0(self, value):
        self.ui.tripleG0Value.setText(str(value))

    # Set the w value on the triple tab
    def set_triple_W(self, value):
        self.ui.tripleWValue.setText(str(value))

    # Set the gInf value on the triple tab
    def set_triple_Ginf(self, value):
        self.ui.tripleGinfValue.setText(str(value))

    # Set the deltas checkbox on the triple tab
    def set_triple_deltas(self, value):
        self.ui.tripleDeltasUsedCheckbox.setChecked(bool(value))

    #####################################################
    # Correlation Functions                             #
    #####################################################
    
    # Performs an auto-correlation
    def autoCorrelation(self):
        # Construct message box string and show it
        self.msgAuto()

        # Make list of colors to send to midend
        colorList = []
        if self.get_red_checkbox():
            colorList.append('r')
        if self.get_green_checkbox():
            colorList.append('g')
        if self.get_blue_checkbox():
            colorList.append('b')

        # Get input parameters
        g0 = self.get_auto_G0()
        w = self.get_auto_W()
        ginf = self.get_auto_Ginf()
        range_val = self.get_auto_range()
        deltas = self.get_auto_deltas_checkbox()

        # Run correlation by calling midend
        result = None
        if self.get_num_images() == 1:
            # get PIL form of image from path
            pilImage = PIL.Image.open(self.rgbPath)

            # construct inputs to send to midend
            inputs = (pilImage, colorList, g0, w, ginf, range_val, deltas)

            # call the midend to get the result object
            result = midend.adaptor.run_dual_mixed_image(*inputs)

        elif self.get_num_images() == 3:
            # get PIL form of images from paths
            pilR = PIL.Image.open(self.redPath)
            pilG = PIL.Image.open(self.greenPath)
            pilB = PIL.Image.open(self.bluePath)

            # construct inputs to send to midend
            inputs = (pilR, pilG, pilB, colorList, g0, w, ginf, range_val, deltas)

            # call the midend to get the result object
            result = midend.adaptor.run_dual_separate_image(*inputs)

        else:
            print("Error: number of images is not 1 or 3.")
        # Get individual channel results
        redResult = result[0]

        # update output tab with new parameters
        self.set_auto_resnorm(round(redResult.resNorm,PRECISION))
        self.set_auto_G0(round(redResult.g0,PRECISION))
        self.set_auto_W(round(redResult.w,PRECISION))
        self.set_auto_Ginf(round(redResult.ginf,PRECISION))
        self.set_auto_deltas(round(redResult.usedDeltas,PRECISION))

        # create and display the graphs
        rPath = os.path.join(self.temp_dir, "r_graph.png")
        gPath = os.path.join(self.temp_dir, "g_graph.png")
        bPath = os.path.join(self.temp_dir, "b_graph.png")
                
        for i, x in enumerate(result):
            fileLike = x.plotToStringIO()
            outFile = None
            if x.color == "r":
                outFile = open(rPath, "w")
            elif x.color == "g":
                outFile = open(gPath, "w")
            elif x.color == "b":
                outFile = open(bPath, "w")
            else:
                print("Error: invalid color.")
                
            for line in fileLike.readlines():
                outFile.write(line)
            outFile.close()

        if self.get_red_checkbox():
            self.ui.imageAutoRed.setPixmap(QtGui.QPixmap(rPath))
        if self.get_green_checkbox():
            self.ui.imageAutoGreen.setPixmap(QtGui.QPixmap(gPath))
        if self.get_blue_checkbox():
            self.ui.imageAutoBlue.setPixmap(QtGui.QPixmap(bPath))

        # Change to auto section of output tab
        self.select_tab("output", "auto")

    # Performs a cross-correlation.
    def crossCorrelation(self):
        # Construct message box string and show it
        self.msgCross()

        # Make list of colors to send to midend
        colorList = []
        if self.get_red_green_checkbox():
            colorList.append('rg')
        if self.get_red_blue_checkbox():
            colorList.append('rb')
        if self.get_green_blue_checkbox():
            colorList.append('gb')

        # Get input parameters
        g0 = self.get_cross_G0()
        w = self.get_cross_W()
        ginf = self.get_cross_Ginf()
        range_val = self.get_cross_range()
        deltas = self.get_cross_deltas_checkbox()

        # Run correlation by calling midend
        result = None
        if self.get_num_images() == 1:
            # get PIL form of image from path
            pilImage = PIL.Image.open(self.rgbPath)

            # construct inputs to send to midend
            inputs = (pilImage, colorList, g0, w, ginf, range_val, deltas)

            # call the midend to get the result object
            result = midend.adaptor.run_dual_mixed_image(*inputs)

        elif self.get_num_images() == 3:
            # get PIL form of images from paths
            pilR = PIL.Image.open(self.redPath)
            pilG = PIL.Image.open(self.greenPath)
            pilB = PIL.Image.open(self.bluePath)

            # construct inputs to send to midend
            inputs = (pilR, pilG, pilB, colorList, g0, w, ginf, range_val, deltas)

            # call the midend to get the result object
            result = midend.adaptor.run_dual_separate_image(*inputs)

        # Get individual channel results
        redGreenResult = result[0]

        # update output tab with new parameters
        self.set_cross_resnorm(round(redGreenResult.resNorm,PRECISION))
        self.set_cross_G0(round(redGreenResult.g0,PRECISION))
        self.set_cross_W(round(redGreenResult.w,PRECISION))
        self.set_cross_Ginf(round(redGreenResult.ginf,PRECISION))
        self.set_cross_deltas(round(redGreenResult.usedDeltas,PRECISION))

        # create and display the graphs
        rgPath = os.path.join(self.temp_dir, "rg_graph.png")
        rbPath = os.path.join(self.temp_dir, "rb_graph.png")
        gbPath = os.path.join(self.temp_dir, "gb_graph.png")
                
        for i, x in enumerate(result):
            fileLike = x.plotToStringIO()
            outFile = None
            if x.color == "rg":
                outFile = open(rgPath, "w")
            elif x.color == "rb":
                outFile = open(rbPath, "w")
            elif x.color == "gb":
                outFile = open(gbPath, "w")
            else:
                print("Error: invalid color.")
                
            for line in fileLike.readlines():
                outFile.write(line)
            outFile.close()

        if self.get_red_green_checkbox():
            self.ui.imageCrossRG.setPixmap(QtGui.QPixmap(rgPath))
        if self.get_red_blue_checkbox():
            self.ui.imageCrossRB.setPixmap(QtGui.QPixmap(rbPath))
        if self.get_green_blue_checkbox():
            self.ui.imageCrossGB.setPixmap(QtGui.QPixmap(gbPath))

        # Change to auto section of output tab
        self.select_tab("output", "cross")

    # Performs a triple correlation.
    def tripleCorrelation(self):
        # Construct string containing channels to be used
        self.msgTriple()

        # Change to triple section of output tab
        self.select_tab("output", "triple")

        # Show Fourier transform (red) surface plot
        self.show_fourier()

    # Returns the number of images to use (0, 1, or 3). 0 means
    # the user hasn't yet loaded all required channels, 1 means
    # the user has loaded one RGB image, and 3 means the user
    # has loaded 3 individual monochrome images.
    def get_num_images(self):
        if self.rgbPath != "":
            return 1
        elif self.redPath != "" and self.greenPath != "" and self.bluePath != "":
            return 3
        else:
            print("No image loaded.")
            return 0

    # Show Fourier transform (red) surface plot (part 1)
    def show_fourier(self):
        result = None

        # define a path to save the image
        path = os.path.join(self.temp_dir, "triple_1.png")

        if self.get_num_images() == 1:
            # convert the RGB image to a PIL image
            pilImage = PIL.Image.open(self.rgbPath)

            # call the midend to get the result object
            result = midend.adaptor.run_triple_mixed_image_part1(pilImage)

        elif self.get_num_images() == 3:
            # convert images to PIL images
            pilR = PIL.Image.open(self.redPath)
            pilG = PIL.Image.open(self.greenPath)
            pilB = PIL.Image.open(self.bluePath)
            
            # call the midend to get the result object
            result = midend.adaptor.run_triple_split_image_part1(pilR, pilG, pilB)

        # create the graph
        fileLike = result.plotToStringIO()
        outFile = open(path, "w")
        for line in fileLike.readlines():
            outFile.write(line)
        outFile.close()

        # show the graph
        self.ui.imageTripleFourier.setPixmap(QtGui.QPixmap(path))

        # save result for next part
        self.tripleResult = result

        # enable sample resolution radio buttons and continue button 1
        self.ui.resolution16.setEnabled(True)
        self.ui.resolution32.setEnabled(True)
        self.ui.resolution64.setEnabled(True)
        self.ui.continueButton1.setEnabled(True)


    # Begin triple correlation process (part 2)
    def triple_process(self):
        result = None

        # define a path to save the image
        path = os.path.join(self.temp_dir, "triple_2.png")

         # Read sample resolution (limit)
        limit = self.get_sample_resolution()

        # call the midend to get the result object
        result = midend.adaptor.run_triple_part2(self.tripleResult, limit)

        # save result for next part
        self.tripleResult = result

        # create the graph
        fileLike = result.plotToStringIO()
        outFile = open(path, "w")
        for line in fileLike.readlines():
            outFile.write(line)
        outFile.close()
        
        # display the graph
        self.ui.imageTripleCorrelation.setPixmap(QtGui.QPixmap(path))

        # disable sample resolution radio buttons and continue button 1
        self.ui.resolution16.setEnabled(False)
        self.ui.resolution32.setEnabled(False)
        self.ui.resolution64.setEnabled(False)
        self.ui.continueButton1.setEnabled(False)

        # Enable parameter inputs and continue button 2
        self.ui.tripleRangeTextbox.setEnabled(True)
        self.ui.tripleWTextbox.setEnabled(True)
        self.ui.tripleG0Textbox.setEnabled(True)
        self.ui.tripleGinfTextbox.setEnabled(True)
        self.ui.tripleDeltasCheckbox.setEnabled(True)
        self.ui.continueButton2.setEnabled(True)

    # Finish off triple correlation process (part 3)
    def triple_complete(self):
        # disable parameter inputs and continue button 2
        self.ui.tripleRangeTextbox.setEnabled(False)
        self.ui.tripleWTextbox.setEnabled(False)
        self.ui.tripleG0Textbox.setEnabled(False)
        self.ui.tripleGinfTextbox.setEnabled(False)
        self.ui.tripleDeltasCheckbox.setEnabled(False)
        self.ui.continueButton2.setEnabled(False)

        self.progress(10)
        range = 0.0
        g0 = 0.0
        w = 0.0
        gInf = 0.0
        deltas = False
        if self.get_triple_range() != "":
            range = float(self.get_triple_range())
            g0 = float(self.get_triple_G0())
            w = float(self.get_triple_W())
            gInf = float(self.get_triple_Ginf())
            deltas = self.get_triple_deltas_checkbox()
        else:
            range = float(self.get_all_range())
            g0 = float(self.get_all_G0())
            w = float(self.get_all_W())
            gInf = float(self.get_all_Ginf())
            deltas = self.get_all_deltas_checkbox()

        self.progress(25)
        # Do triple correlation

        self.progress(75)
        # Show fitting curve

        self.progress(95)
        # Show res. norm. and whether deltas were used

        self.progress(100)

    #####################################################
    # Message Box Functions                             #
    #####################################################

    # Message Box functionality
    def message(self, text):
        self.ui.messageBox.setText(str(text))

    # Informs the user that they have selected an invalid file format
    def msgBadFormat(self):
        self.message("Invalid file format. Please use a different type of file.")

    # Informs the user that they have selected a non-monochrome image
    def msgBadChannels(self):
        self.message("Image has too many channels. Please use a monochrome image.")

    # Construct message to show user when autocorrelation is selected
    def msgAuto(self):
        channels = ""
        if self.get_red_checkbox():
            if self.get_green_checkbox():
                if self.get_blue_checkbox():
                    channels = "red, green, and blue channels"
                else:
                    channels = "red and green channels"
            else:
                if self.get_blue_checkbox():
                    channels = "red and blue channels"
                else:
                    channels = "red channel"
        else:
            if self.get_green_checkbox():
                if self.get_blue_checkbox():
                    channels = "green and blue channels"
                else:
                    channels = "green channel"
            else:
                channels = "blue channel"

        # Construct output string
        text = "Starting auto-correlation using " + channels
        text += " and parameters\n[range = " + str(self.get_auto_range())
        text += ", g(0) = " + str(self.get_auto_G0()) +", w = "
        text += str(self.get_auto_W()) + ", gInf = " + str(self.get_auto_Ginf())
        text += "],"
        if self.get_auto_deltas_checkbox() == False:
            text += " do not"
        text += " consider deltas, S.R. "
        res = str(self.get_sample_resolution())
        text += str(res) + " x " + str(res) + "."
        self.message(text)

    # Construct message to show user when cross-correlation is selected
    def msgCross(self):
        channels = ""
        if self.get_red_green_checkbox():
            if self.get_red_blue_checkbox():
                if self.get_green_blue_checkbox():
                    channels = "RG, RB, and GB channel pairs"
                else:
                    channels = "RG and RB channel pairs"
            else:
                if self.get_green_blue_checkbox():
                    channels = "RG and GB channel pairs"
                else:
                    channels = "RG channel pair"
        else:
            if self.get_red_blue_checkbox():
                if self.get_green_blue_checkbox():
                    channels = "RB and GB channel pairs"
                else:
                    channels = "RB channel pair"
            else:
                channels = "GB channel pair"

        text = "Starting cross-correlation using " + channels
        text += " and parameters\n[Range = "
        text += str(self.get_cross_range()) + ", g(0) = "
        text += str(self.get_cross_G0()) + ", w = "
        text += str(self.get_cross_W()) + ", gInf = "
        text += str(self.get_cross_Ginf()) + "],"
        if self.get_cross_deltas_checkbox() == False:
            text+= " do not"
        text += " consider deltas, S.R. "
        res = str(self.get_sample_resolution())
        text += res + " x " + res + "."
        self.message(text)

    # Construct message to show user when triple-correlation is selected
    def msgTriple(self):
        res = str(self.get_sample_resolution())
        text = "Starting triple correlation with sample resolution "
        text += res + " x " + res + "."
        # Do triple correlation
        self.message(text)

    # Constructive message to show user when all correlations are selected
    def msgAll(self):
        text = "Running all possible correlations using parameters ["
        text += "Range = " + self.get_all_range() + ", g(0) = "
        text += self.get_all_G0() + ", w = " + self.get_all_W()
        text += ", gInf = " + self.get_all_Ginf() + "],"
        if self.get_all_deltas_checkbox() == False:
            text += " do not"
            text += " consider deltas, using sample resolution "
            res = str(self.get_sample_resolution())
            text += res + " x " + res + "."
        # Do all correlations
        self.message(text)


    #####################################################
    # Interface Update Functions                        #
    #####################################################
    # Selects a specific tab on the interface
    def select_tab(self, mainTab, subTab=None):
        if mainTab == "input":
            self.ui.mainTabWidget.setCurrentIndex(0)
            if subTab == "auto":
                self.ui.correlationTabWidget.setCurrentIndex(0)
            elif subTab == "cross":
                self.ui.correlationTabWidget.setCurrentIndex(1)
            elif subTab == "triple":
                self.ui.correlationTabWidget.setCurrentIndex(2)
        else:
            self.ui.mainTabWidget.setCurrentIndex(1)
            if subTab == "auto":
                self.ui.outputCorrelationTabWidget.setCurrentIndex(0)
            elif subTab == "cross":
                self.ui.outputCorrelationTabWidget.setCurrentIndex(1)
            elif subTab == "triple":
                self.ui.outputCorrelationTabWidget.setCurrentIndex(2)

        if subTab == "three":
            self.ui.imageSettingsTabWidget.setCurrentIndex(0)
        elif subTab == "single":
            self.ui.imageSettingsTabWidget.setCurrentIndex(1)
        elif subTab == "all":
            self.ui.correlationTabWidget.setCurrentIndex(3)

    #####################################################
    # Miscellaneous Functions                           #
    #####################################################

    # Construct an RGB Image from three separate channel images
    def constructRGB(self):
        if self.redPath != "" and self.greenPath != "" and self.bluePath != "":
            print('hello')

    # Refreshes the temporary directory by deleting and recreating it
    def refresh_temp(self):
        self.remove_temp()
        self.create_temp()

    # Creates the temporary directory if it does not exist.
    def create_temp(self):
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    # Removes the temporary directory if it exists.
    def remove_temp(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    # Updates the size of the image internally and on the GUI label.
    def update_size(self, size):
        self.size = size
        sizeStr = str(size) + " x " + str(size)
        self.ui.imageSizeText.setText(sizeStr)

    # Calculates the average intensity per pixel given an image
    def aipp(self, path, dim):
        image  = Image.open(path)
        sum = 0
        num = 0
        for x in range(0, dim):
            for y in range(0, dim):
                pixel = image.load()
                sum += pixel[x,y]
                num += 1
        return sum / num

    # Updates the progress bar
    def progress(self, percent):
        self.ui.progressBar.setValue(percent)

    # Remove paths for any nonexistent images
    def remove_paths(self):
        if not os.path.isfile(self.rgbPath):
            self.ui.imageRgb.clear()
            self.rgbPath = ""
        if not os.path.isfile(self.greenPath):
            self.ui.imageGreen.clear()
            self.greenPath = ""
        if not os.path.isfile(self.bluePath):
            self.ui.imageBlue.clear()
            self.bluePath = ""

    # Clears any images and parameters in the output tab from previous correlation.
    def clear_output_tab(self):
        # Clear autocorrelation images
        self.ui.imageAutoRed.clear()
        self.ui.imageAutoGreen.clear()
        self.ui.imageAutoBlue.clear()

        # Clear autocorrelation parameters
        self.ui.autoResNormValue.clear()
        self.ui.autoG0Value.clear()
        self.ui.autoWValue.clear()
        self.ui.autoGinfValue.clear()

        # Clear cross-correlation images
        self.ui.imageCrossRG.clear()
        self.ui.imageCrossRB.clear()
        self.ui.imageCrossGB.clear()

        # Clear cross-correlation parameters
        self.ui.crossResNormValue.clear()
        self.ui.crossG0Value.clear()
        self.ui.crossWValue.clear()
        self.ui.crossGinfValue.clear()

        # Clear triple correlation images
        self.ui.imageTripleFourier.clear()
        self.ui.imageTripleCorrelation.clear()
        self.ui.imageTripleFittingCurve.clear()

        # Clear triple correlation parameters
        self.ui.tripleResNormValue.clear()
        self.ui.tripleRangeTextbox.clear()
        self.ui.tripleWTextbox.clear()
        self.ui.tripleG0Textbox.clear()
        self.ui.tripleGinfTextbox.clear()

def start():
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())
