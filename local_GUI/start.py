"""
This script provides all functionality for the local GUI by calling
other project modules.

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
import shutil # used to recursively remove directories
from PyQt4 import QtCore, QtGui
from PIL import Image
from gui_main import Ui_Dialog
from graphzoom import GraphZoom
from batch import Batch
from help import Help

# Enable importing of other project modules
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
PRECISION = 5      # number of decimal places to show for output values
ZOOM_ICON = "./Images/zoom.png"
RGB_PLACEHOLDER = "./Images/rgb.png"
RED_PLACEHOLDER = "./Images/r.png"
GREEN_PLACEHOLDER = "./Images/g.png"
BLUE_PLACEHOLDER = "./Images/b.png"
TEMP_DIR = "./ics_tmp"

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Force consistent theme and font size
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))
        self.setStyleSheet("font-size: 11pt")

        # Disable resizing
        self.setFixedSize(self.size())
        
        # Paths to channel input files
        self.redPath = ""
        self.greenPath = ""
        self.bluePath = ""
        self.rgbPath = ""

        # Paths to grapsh
        self.autoRedGraphPath = ""
        self.autoGreenGraphPath = ""
        self.autoBlueGraphPath = ""
        self.crossRGGraphPath = ""
        self.crossRBGraphPath = ""
        self.crossGBGraphPath = ""
        self.tripleGraph1Path = ""
        self.tripleGraph2Path = ""
        self.tripleGraph3Path = ""

        # Image channel arrays
        self.redChannel = ""
        self.greenChannel = ""
        self.blueChannel = ""
        self.rgbChannel = ""
    
        # Number of steps in a given function, for updating progress bar
        self.numSteps = 1

        # Refresh the temporary directory
        self.refresh_temp()

        # Set the default parameters for the input fields
        self.set_default_parameters()

        # Load the default/placeholder images
        self.load_default_images()

        # Size of the images in pixels (e.g. 64 would mean a 64x64 image)
        self.size = 0

        # Result objects for each correlation
        self.autoResult = None
        self.crossResult = None
        self.tripleResult1 = None
        self.tripleResult2 = None
        self.tripleResult3 = None

        # Disable processing mode
        self.set_processing(False)

        # Whether or not the Graph Zoom and Help dialogs are open
        self.helpOpen = False

        #######################################################
        # Interface Object Connections                        #
        #######################################################
        clicked = QtCore.SIGNAL("clicked()")
        changed = QtCore.SIGNAL("currentChanged()")

        # Buttons
        QtCore.QObject.connect(self.ui.loadImageRed, clicked, self.load_red_image)
        QtCore.QObject.connect(self.ui.loadImageGreen, clicked, self.load_green_image)
        QtCore.QObject.connect(self.ui.loadImageBlue, clicked, self.load_blue_image)
        QtCore.QObject.connect(self.ui.loadImageRGB, clicked, self.load_RGB_image)
        QtCore.QObject.connect(self.ui.startButton, clicked,  self.start)
        QtCore.QObject.connect(self.ui.stopButton, clicked, self.stop)
        QtCore.QObject.connect(self.ui.batchModeButton, clicked, self.batch_mode)
        QtCore.QObject.connect(self.ui.saveAllButton, clicked, self.saveAll)
        QtCore.QObject.connect(self.ui.continueButton1, clicked, self.triple_process)
        QtCore.QObject.connect(self.ui.continueButton2, clicked, self.triple_complete)
        QtCore.QObject.connect(self.ui.redGraphZoom, clicked, self.zoomRed)
        QtCore.QObject.connect(self.ui.greenGraphZoom, clicked, self.zoomGreen)
        QtCore.QObject.connect(self.ui.blueGraphZoom, clicked, self.zoomBlue)
        QtCore.QObject.connect(self.ui.redGreenGraphZoom, clicked, self.zoomRedGreen)
        QtCore.QObject.connect(self.ui.redBlueGraphZoom, clicked, self.zoomRedBlue)
        QtCore.QObject.connect(self.ui.greenBlueGraphZoom, clicked, self.zoomGreenBlue)
        QtCore.QObject.connect(self.ui.tripleGraph1Zoom, clicked, self.zoomTriple1)
        QtCore.QObject.connect(self.ui.tripleGraph2Zoom, clicked, self.zoomTriple2)
        QtCore.QObject.connect(self.ui.tripleGraph3Zoom, clicked, self.zoomTriple3)
        QtCore.QObject.connect(self.ui.helpButton, clicked, self.show_help)

        # Correlation tabs
        QtCore.QObject.connect(self.ui.correlationTabWidget, changed, self.update)

    #######################################################
    # Interface Object Functions                          #
    #######################################################

    # Loads an RGB image into the interface.
    def load_RGB_image(self):
        self.message("Loading RGB Image...")
        validImage = True

        # Open the file loader and get the path of the desired image
        self.rgbPath = str(QtGui.QFileDialog.getOpenFileName())

        # Check for cancel
        if self.rgbPath == "" or self.rgbPath == None:
            validImage = False
            self.message("Image loading canceled.")

        oldPath = None
        # Call the backend to separate the image by channel
        if validImage:
            try:
                images = bimloader.load_image_mixed(str(self.rgbPath))
                image = Image.open(str(self.rgbPath))
            except bimloader.ImageFormatException:
                validImage = False
                self.msgBadFormat()
                self.rgbPath = ""
            except IOError:
                try:
                    image = bimloader.validate_image(str(self.rgbPath), True, asSciPy=False)
                    oldPath = self.rgbPath
                    self.rgbPath = os.path.join(TEMP_DIR, "rgb.png")
                    image.save(self.rgbPath)
                except Exception as e:
                    validImage = False
                    self.message(e)
                    self.rgbPath = ""
            except:
                validImage = False
                self.message("An error occurred while loading the image.")
                self.rgbPath = ""

        if validImage:
            # Update user interface with image
            if oldPath is None:
                self.message("Loaded image " + self.rgbPath)
                self.ui.rgbFile.setText(os.path.basename(self.rgbPath))
            else:
                self.message("Loaded image " + oldPath)
                self.ui.rgbFile.setText(os.path.basename(oldPath))
            self.ui.imageRgb.setPixmap(QtGui.QPixmap(self.rgbPath))

            # Save the three channel arrays
            self.redChannel = images[0]
            self.greenChannel = images[1]
            self.blueChannel = images[2]

            # Save the image dimension
            self.update_size(self.redChannel.shape[1])

            # Update the red, green, and blue paths
            self.redPath = TEMP_DIR + "/red.png"
            self.greenPath = TEMP_DIR + "/green.png"
            self.bluePath = TEMP_DIR + "/blue.png"

            # Refresh the temporary directory (delete and recreate)
            self.refresh_temp()

            # Use the arrays to generate images
            scipy.misc.imsave(self.redPath, self.redChannel)
            scipy.misc.imsave(self.greenPath, self.greenChannel)
            scipy.misc.imsave(self.bluePath, self.blueChannel)

            # Convert each monochrome image to RGB for display on the interface

            # Get rid of the green and blue channels in red image
            redImage = PIL.Image.open(self.redPath)
            redImage = redImage.convert("RGB")
            red = redImage.split()[0]
            empty = red.point(lambda i: i * 0)
            redImage = PIL.Image.merge("RGB", (red, empty, empty))
            redColorized = os.path.join(TEMP_DIR, "rc_split.png")
            redImage.save(redColorized, "PNG")

            # Get rid of red and blue channels in green image
            greenImage = PIL.Image.open(self.greenPath)
            greenImage = greenImage.convert("RGB")
            green = greenImage.split()[1]
            greenImage = PIL.Image.merge("RGB", (empty, green, empty))
            greenColorized = os.path.join(TEMP_DIR, "gc_split.png")
            greenImage.save(greenColorized, "PNG")

            # Get rid of red and green channels in blue image
            blueImage = PIL.Image.open(self.bluePath)
            blueImage = blueImage.convert("RGB")
            blue = blueImage.split()[2]
            blueImage = PIL.Image.merge("RGB", (empty, empty, blue))
            blueColorized = os.path.join(TEMP_DIR, "bc_split.png")
            blueImage.save(blueColorized, "PNG")
            
            # Load the colorized images into the interface
            self.ui.imageRed.setPixmap(QtGui.QPixmap(redColorized))
            self.ui.imageGreen.setPixmap(QtGui.QPixmap(greenColorized))
            self.ui.imageBlue.setPixmap(QtGui.QPixmap(blueColorized))

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

        # Check for cancel
        if self.redPath == "" or self.redPath == None:
            validImage = False
            self.message("Image loading canceled.")

        oldPath = None
        # Call the backend to check that the file extension is valid
        if validImage:
            try:
                self.redChannel = bimloader.load_image_split(str(self.redPath))
            except bimloader.ImageFormatException:
                validImage = False
                self.msgBadFormat()
                self.redPath = ""
            except:
                validImage = False
                self.msgBadChannels()
                self.greenPath = ""

            try:
                image = PIL.Image.open(self.redPath)
            except IOError:
                try:
                    image = bimloader.validate_image(str(self.redPath), False, asSciPy=False)
                    oldPath = self.redPath
                    self.redPath = os.path.join(TEMP_DIR, "r.png")
                    image.save(self.redPath)
                except Exception as e:
                    validImage = False
                    message = "The image could not be loaded. Please use a different format.\n"
                    message += "Exception:\n<" + str(e) + ">"
                    self.message(message)
            except e:
                validImage = False
                message = "An error occurred while loading the image.\n"
                message += "Exception:\n<" + str(e) + ">"

        if validImage:
            # Remove from the interface any images generated by splitting a loaded
            #  RGB image, in case the user has changed their mind
            self.remove_split_images()

            # Get rid of the green and blue channels
            image = PIL.Image.open(self.redPath)
            image = image.convert("RGB")
            red = image.split()[0]
            empty = red.point(lambda i: i * 0)
            redImage = PIL.Image.merge("RGB", (red, empty, empty))
            colorizedPath = os.path.join(TEMP_DIR, "rc.png")
            redImage.save(colorizedPath, "PNG")
            
            # Load the colorized image into the interface
            self.ui.imageRed.setPixmap(QtGui.QPixmap(colorizedPath))

            # Update user interface with image
            if oldPath:
                self.message("Loaded image " + oldPath)
                self.ui.redChannelFile.setText(os.path.basename(oldPath))
            else:
                self.message("Loaded image " + self.redPath)
                self.ui.redChannelFile.setText(os.path.basename(self.redPath))

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
                # Cancel image loading if the image is not monochrome
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

        # Check for cancel
        if self.greenPath == "" or self.greenPath == None:
            validImage = False
            self.message("Image loading canceled.")

        oldPath = None
        # Call the backend to load the image as an array
        if validImage:
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

            try:
                image = PIL.Image.open(self.greenPath)
            except IOError:
                try:
                    image = bimloader.validate_image(str(self.greenPath), False, asSciPy=False)
                    oldPath = self.greenPath
                    self.greenPath = os.path.join(TEMP_DIR, "g.png")
                    image.save(self.greenPath)
                except Exception as e:
                    validImage = False
                    message = "The image could not be loaded. Please use a different format.\n"
                    message += "Exception:\n<" + str(e) + ">"
                    self.message(message)
            except:
                validImage = False
                self.message("An error occurred while loading the image.")

        if validImage:
            # Remove from the interface any images generated by splitting a loaded
            #  RGB image, in case the user has changed their mind
            self.remove_split_images()

            # Get rid of the green and blue channels
            image = PIL.Image.open(self.greenPath)
            image = image.convert("RGB")
            green = image.split()[1]
            empty = green.point(lambda i: i * 0)
            greenImage = PIL.Image.merge("RGB", (empty, green, empty))
            colorizedPath = os.path.join(TEMP_DIR, "gc.png")
            greenImage.save(colorizedPath, "PNG")
            
            # Load the colorized image into the interface
            self.ui.imageGreen.setPixmap(QtGui.QPixmap(colorizedPath))

            # Update user interface with image
            if oldPath:
                self.message("Loaded image " + oldPath)
                self.ui.greenChannelFile.setText(os.path.basename(oldPath))
            else:
                self.message("Loaded image " + self.greenPath)
                self.ui.greenChannelFile.setText(os.path.basename(self.greenPath))

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

        # Check for cancel
        if self.bluePath == "" or self.bluePath == None:
            validImage = False
            self.message("Image loading canceled.")

        oldPath = None
        # Call the backend to load the image as an array
        if validImage:
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

            try:
                image = PIL.Image.open(self.bluePath)
            except IOError:
                try:
                    image = bimloader.validate_image(str(self.bluePath), False, asSciPy=False)
                    oldPath = self.bluePath
                    self.bluePath = os.path.join(TEMP_DIR, "b.png")
                    image.save(self.bluePath)
                except Exception as e:
                    validImage = False
                    message = "The image could not be loaded. Please use a different format.\n"
                    message += "Exception:\n<" + str(e) + ">"
                    self.message(message)
            except:
                validImage = False
                self.message("An error occurred while loading the image.")

        if validImage:
            # Remove from the interface any images generated by splitting a loaded
            #  RGB image, in case the user has changed their mind
            self.remove_split_images()

            # Get rid of the green and blue channels
            image = PIL.Image.open(self.bluePath)
            image = image.convert("RGB")
            blue = image.split()[2]
            empty = blue.point(lambda i: i * 0)
            blueImage = PIL.Image.merge("RGB", (empty, empty, blue))
            colorizedPath = os.path.join(TEMP_DIR, "bc.png")
            blueImage.save(colorizedPath, "PNG")
            
            # Load the colorized image into the interface
            self.ui.imageBlue.setPixmap(QtGui.QPixmap(colorizedPath))

            # Update user interface with image
            if oldPath:
                self.message("Loaded image " + oldPath)
                self.ui.blueChannelFile.setText(os.path.basename(oldPath))
            else:
                self.message("Loaded image " + self.bluePath)
                self.ui.blueChannelFile.setText(os.path.basename(self.bluePath))

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
        # Find out which correlation to do
        mode = self.get_correlation_tab()

        # Validate input
        validInput = self.validate_input(mode)

        # Continue if input is valid
        if validInput:
            # Remove values and images from output tab, if necessary
            self.clear_output_tab()

            # Remove result objects
            self.autoResult = None
            self.crossResult = None
            self.tripleResult1 = None
            self.tripleResult2 = None
            self.tripleResult3 = None

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
                
                self.allCorrelations()

            else:
                self.message("Mode error.")

    # Stop button functionality
    def stop(self):
        self.message("Correlation stopped.")

        # Reset progress bar
        self.progress(0)

        # disable processing mode
        self.set_processing(False)

        # interrupt main thread
        thread.interrupt_main()

    # Switch interface to batch mode
    def batch_mode(self):
        batch = Batch(self)
        batch.show()
        self.hide()

    # Show help dialog
    def show_help(self):
        if not self.helpOpen:
            help = Help(self)
            self.helpOpen = True
            help.show()

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
            return "<error>"

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

    # If a given string is a numeric non-blank value, returns the value as an 
    # integer; otherwise just returns the string.
    # Examples:
    #    "" ==> ""
    #    "3" ==> 3
    #    "abc" ==> "abc"
    def intify(self, num):
        if num != "":
            try:
                num = int(num)
            except:
                pass
        return num

    # Equivalent of intify for float types.
    def floatify(self, num):
        if num != "":
            try:
                num = float(num)
            except:
                pass
        return num

    ## Text inputs
    # Returns inputted Range in AC
    def get_auto_range(self):
        return self.intify(self.ui.autoRangeTextbox.text())

    # Returns inputted G(0) in AC
    def get_auto_G0(self):
        return self.floatify(self.ui.autoG0Textbox.text())

    # Returns inputted W in AC
    def get_auto_W(self):
        return self.floatify(self.ui.autoWTextbox.text())

    # Returns inputted G(Inf) in AC
    def get_auto_Ginf(self):
        return self.floatify(self.ui.autoGinfTextbox.text())

    # Returns inputted Range in XC
    def get_cross_range(self):
        return self.intify(self.ui.crossRangeTextbox.text())

    # Returns inputted G(0) in XC
    def get_cross_G0(self):
        return self.floatify(self.ui.crossG0Textbox.text())

    # Returns inputted W in XC
    def get_cross_W(self):
        return self.floatify(self.ui.crossWTextbox.text())

    # Returns inputted G(Inf) in XC
    def get_cross_Ginf(self):
        return self.floatify(self.ui.crossGinfTextbox.text())

    # Returns inputted Range in AXC
    def get_all_range(self):
        return self.intify(self.ui.allAutoCrossRangeTextbox.text())

    # Returns inputted G(0) in AXC
    def get_all_G0(self):
        return self.floatify(self.ui.allAutoCrossG0Textbox.text())

    # Returns inputted W in AXC
    def get_all_W(self):
        return self.floatify(self.ui.allAutoCrossWTextbox.text())

    # Returns inputted Ginf in AXC
    def get_all_Ginf(self):
        return self.floatify(self.ui.allAutoCrossGinfTextbox.text())

    # Returns inputted limit for TC (Output Tab)
    def get_triple_limit(self):
        return self.floatify(self.ui.startingPointInput.text())

    # Returns inputted range for TC (Output Tab)
    def get_triple_range(self):
        return self.intify(self.ui.tripleRangeTextbox.text())

    # Returns inputted G(0) for TC (Output Tab)
    def get_triple_G0(self):
        return self.floatify(self.ui.tripleG0Textbox.text())

    # Returns inputted W for TC (Output Tab)
    def get_triple_W(self):
        return self.floatify(self.ui.tripleWTextbox.text())

    # Returns inputted G(Inf) for TC (Output Tab)
    def get_triple_Ginf(self):
        return self.floatify(self.ui.tripleGinfTextbox.text())

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
            print("Limit error!")
            return -1

    # Checks if input is valid for the selected mode, and returns True only if it is.
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
                    r = int(self.get_auto_range())
                    if r <= 0:
                        self.message("Range must be greater than 0.")
                        validInput = False
                except ValueError:
                    validInput = False
                    self.message("Range must be a positive integer.")

                # non-numeric g(0)
                try:
                    g0 = float(self.get_auto_G0())
                    if g0 < 0:
                        self.message("g(0) cannot be negative.")
                        validInput = False
                except ValueError:
                    validInput = False
                    self.message("g(0) must be a number.")

                # non-numeric W
                try:
                    w = float(self.get_auto_W())
                    if w <= 0:
                        validInput = False
                        self.message("W must be  greater than 0.")
                except ValueError:
                    validInput = False
                    self.message("w must be a number.")

                # non-numeric gInf
                try:
                    ginf = float(self.get_auto_Ginf())
                    if ginf < 0:
                        self.message("gInf cannot be negative.")
                        validInput = False
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
                    r = int(self.get_cross_range())
                    if r <= 0:
                        self.message("Range must be greater than 0.")
                        validInput = False
                except ValueError:
                    validInput = False
                    self.message("Range must be a positive integer.")

                # non-numeric g(0)
                try:
                    g0 = float(self.get_cross_G0())
                    if g0 < 0:
                        self.message("g(0) cannot be negative.")
                        validInput = False
                except ValueError:
                    validInput = False
                    self.message("g(0) must be a number.")

                # non-numeric W
                try:
                    w = float(self.get_cross_W())
                    if w <= 0:
                        self.message("W must be greater than 0.")
                        validInput = False
                except ValueError:
                    validInput = False
                    self.message("W must be a number.")

                # non-numeric gInf
                try:
                    ginf = float(self.get_cross_Ginf())
                    if ginf < 0:
                        self.message("gInf cannot be negative.")
                        validInput = False
                except ValueError:
                    validInput = False
                    self.message("gInf must be a number.")

        elif mode == "triple_part3":
            if str(self.ui.tripleRangeTextbox.text()) == "":
                self.ui.tripleRangeTextbox.setFocus()
                self.message("Triple-correlation range parameter is blank.")
                validInput = False
            elif str(self.ui.tripleG0Textbox.text()) == "":
                self.ui.tripleG0Textbox.setFocus()
                self.message("Triple-correlation g(0) parameter is blank.")
                validInput = False
            elif str(self.ui.tripleWTextbox.text()) == "":
                self.ui.tripleWTextbox.setFocus()
                self.message("Triple-correlation w parameter is blank.")
                validInput = False
            elif str(self.ui.tripleGinfTextbox.text()) == "":
                self.ui.tripleGinfTextbox.setFocus()
                self.message("Triple-correlation gInf parameter is blank.")
                validInput = False
            else:
                try:
                    r = int(self.ui.tripleRangeTextbox.text())
                    if r <= 0:
                        self.message("Range must be greater than 0.")
                        validInput = False
                        self.ui.tripleRangeTextbox.clear()
                        self.ui.tripleRangeTextbox.setFocus()
                except:
                    self.message("Triple-correlation range parameter is non-numeric.")
                    self.ui.tripleRangeTextbox.clear()
                    self.ui.tripleRangeTextbox.setFocus()
                    validInput = False
                try:
                    g0 = float(self.ui.tripleG0Textbox.text())
                    if g0 < 0:
                        self.message("g(0) cannot be negative.")
                        validInput = False
                        self.ui.tripleG0Textbox.clear()
                        self.ui.tripleG0Textbox.setFocus()
                except:
                    self.message("Triple-correlation g(0) parameter is non-numeric.")
                    self.ui.tripleG0Textbox.clear()
                    self.ui.tripleG0Textbox.setFocus()
                    validInput = False
                try:
                    w = float(self.ui.tripleWTextbox.text())
                    if w <= 0:
                        self.message("W must be greater than 0.")
                        validInput = False
                        self.ui.tripleWTextbox.clear()
                        self.ui.tripleWTextbox.setFocus()
                except:
                    self.message("Triple-correlation w parameter is non-numeric.")
                    self.ui.tripleWTextbox.clear()
                    self.ui.tripleWTextbox.setFocus()
                    validInput = False
                try:
                    ginf = float(self.ui.tripleGinfTextbox.text())
                    if ginf < 0:
                        self.message("gInf cannot be negative.")
                        validInput = False
                        self.ui.tripleGinfTextbox.clear()
                        self.ui.tripleGinfTextbox.setFocus()
                except:
                    self.message("Triple-correlation gInf parameter is non-numeric.")
                    self.ui.tripleGinfTextbox.clear()
                    self.ui.tripleWTextbox.clear()
                    validInput = False
                if self.get_sample_resolution() < int(self.ui.tripleRangeTextbox.text()):
                    self.message("Sample resolution must be larger than range.")
                    self.ui.tripleRangeTextbox.clear()
                    self.ui.tripleRangeTextbox.setFocus()

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
                    r = int(self.get_all_range())
                    if r < 0:
                        self.message("Range cannot be negative")
                        validInput = False
                except ValueError:
                    validInput = False
                    self.message("Range must be a positive integer.")

                # non-numeric g(0)
                try:
                    g0 = float (self.get_all_G0())
                    if g0 < 0:
                        self.message("g(0) cannot be negative.")
                        validInput = False
                except ValueError:
                    validInput = False
                    self.message("g(0) must be a number.")

                # non-numeric W
                try:
                    w = float (self.get_all_W())
                    if w <= 0:
                        self.message("W must be greater than 0.")
                        validInput = False
                except ValueError:
                    validInput = False
                    self.message("W must be a number.")

                # non-numeric gInf
                try:
                    ginf = float (self.get_all_Ginf())
                    if ginf < 0:
                        self.message("gInf cannot be negative.")
                        validInput = False
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

    #####################################################
    # Correlation Functions                             #
    #####################################################
    
    # Performs an auto-correlation
    def autoCorrelation(self):
        # enable processing mode
        self.set_processing(True)

        # number of steps for progress tracking
        self.numSteps = 10

        self.progress(0)

        # Construct message box string and show it
        self.msgAuto()
        
        self.progress(1)

        # Make list of colors to send to midend
        colorList = []
        if self.get_red_checkbox():
            colorList.append('r')
        if self.get_green_checkbox():
            colorList.append('g')
        if self.get_blue_checkbox():
            colorList.append('b')

        self.progress(2)

        # Get input parameters
        g0 = self.get_auto_G0()
        w = self.get_auto_W()
        ginf = self.get_auto_Ginf()
        range_val = self.get_auto_range()
        deltas = self.get_auto_deltas_checkbox()

        self.progress(3)

        # Run correlation by calling midend
        result = None
        if self.get_num_images() == 1:
            # get PIL form of image from path
            pilImage = PIL.Image.open(self.rgbPath)
            self.progress(4)

            # construct inputs to send to midend
            inputs = (pilImage, colorList, g0, w, ginf, range_val, deltas)
            self.progress(5)

            # call the midend to get the result object
            result = midend.adaptor.run_dual_mixed_image(*inputs)
            self.progress(6)

        elif self.get_num_images() == 3:
            # get PIL form of images from paths
            pilR = PIL.Image.open(self.redPath)
            pilG = PIL.Image.open(self.greenPath)
            pilB = PIL.Image.open(self.bluePath)
            self.progress(4)

            # construct inputs to send to midend
            inputs = (pilR, pilG, pilB, colorList, g0, w, ginf, range_val, deltas)
            self.progress(5)

            # call the midend to get the result object
            result = midend.adaptor.run_dual_separate_image(*inputs)
            self.progress(6)
        else:
            print("Error: number of images is not 1 or 3.")

        # Save result object
        self.autoResult = result
        # Get individual channel results
        redResult = result[0]

        # update output tab with new parameters
        self.set_auto_resnorm(round(redResult.resNorm,PRECISION))
        self.set_auto_G0(round(redResult.g0,PRECISION))
        self.set_auto_W(round(redResult.w,PRECISION))
        self.set_auto_Ginf(round(redResult.ginf,PRECISION))
        self.set_auto_deltas(round(redResult.usedDeltas,PRECISION))

        self.progress(7)

        # create and display the graphs
        rPath = os.path.join(TEMP_DIR, "r_graph.png")
        gPath = os.path.join(TEMP_DIR, "g_graph.png")
        bPath = os.path.join(TEMP_DIR, "b_graph.png")
                
        for i, x in enumerate(result):
            fileLike = x.plotToStringIO()
            outFile = None
            if x.color == "r":
                outFile = open(rPath, "wb")
            elif x.color == "g":
                outFile = open(gPath, "wb")
            elif x.color == "b":
                outFile = open(bPath, "wb")
            else:
                print("Error: invalid color.")
                
            for line in fileLike.readlines():
                outFile.write(line)
            outFile.close()
        
        self.progress(9)

        if self.get_red_checkbox():
            self.ui.imageAutoRed.setPixmap(QtGui.QPixmap(rPath))
            self.autoRedGraphPath = rPath
        if self.get_green_checkbox():
            self.ui.imageAutoGreen.setPixmap(QtGui.QPixmap(gPath))
            self.autoGreenGraphPath = gPath
        if self.get_blue_checkbox():
            self.ui.imageAutoBlue.setPixmap(QtGui.QPixmap(bPath))
            self.autoBlueGraphPath = bPath

        self.progress(10)

        # Change to auto section of output tab
        self.select_tab("output", "auto")    

        # disable processing mode
        self.set_processing(False)

    # Performs a cross-correlation.
    def crossCorrelation(self):
        # enable processing mode
        self.set_processing(True)

        # number of steps for progress tracking
        self.numSteps = 10

        self.progress(0)

        # Construct message box string and show it
        self.msgCross()

        self.progress(1)

        # Make list of colors to send to midend
        colorList = []
        if self.get_red_green_checkbox():
            colorList.append('rg')
        if self.get_red_blue_checkbox():
            colorList.append('rb')
        if self.get_green_blue_checkbox():
            colorList.append('gb')

        self.progress(2)

        # Get input parameters
        g0 = self.get_cross_G0()
        w = self.get_cross_W()
        ginf = self.get_cross_Ginf()
        range_val = self.get_cross_range()
        deltas = self.get_cross_deltas_checkbox()

        self.progress(3)

        # Run correlation by calling midend
        result = None
        if self.get_num_images() == 1:
            # get PIL form of image from path
            pilImage = PIL.Image.open(self.rgbPath)
            
            self.progress(4)

            # construct inputs to send to midend
            inputs = (pilImage, colorList, g0, w, ginf, range_val, deltas)

            self.progress(5)

            # call the midend to get the result object
            result = midend.adaptor.run_dual_mixed_image(*inputs)

            self.progress(6)

        elif self.get_num_images() == 3:
            # get PIL form of images from paths
            pilR = PIL.Image.open(self.redPath)
            pilG = PIL.Image.open(self.greenPath)
            pilB = PIL.Image.open(self.bluePath)

            self.progress(4)

            # construct inputs to send to midend
            inputs = (pilR, pilG, pilB, colorList, g0, w, ginf, range_val, deltas)

            self.progress(5)

            # call the midend to get the result object
            result = midend.adaptor.run_dual_separate_image(*inputs)

            self.progress(6)

        # Save result object
        self.crossResult = result

        # Get individual channel results
        redGreenResult = result[0]

        # update output tab with new parameters
        self.set_cross_resnorm(round(redGreenResult.resNorm,PRECISION))
        self.set_cross_G0(round(redGreenResult.g0,PRECISION))
        self.set_cross_W(round(redGreenResult.w,PRECISION))
        self.set_cross_Ginf(round(redGreenResult.ginf,PRECISION))
        self.set_cross_deltas(round(redGreenResult.usedDeltas,PRECISION))

        # create and display the graphs
        rgPath = os.path.join(TEMP_DIR, "rg_graph.png")
        rbPath = os.path.join(TEMP_DIR, "rb_graph.png")
        gbPath = os.path.join(TEMP_DIR, "gb_graph.png")
        
        self.progress(7)

        for i, x in enumerate(result):
            fileLike = x.plotToStringIO()
            outFile = None
            if x.color == "rg":
                outFile = open(rgPath, "wb")
            elif x.color == "rb":
                outFile = open(rbPath, "wb")
            elif x.color == "gb":
                outFile = open(gbPath, "wb")
            else:
                print("Error: invalid color.")
                
            for line in fileLike.readlines():
                outFile.write(line)
            outFile.close()

        self.progress(9)

        if self.get_red_green_checkbox():
            self.ui.imageCrossRG.setPixmap(QtGui.QPixmap(rgPath))
            self.crossRGGraphPath = rgPath
        if self.get_red_blue_checkbox():
            self.ui.imageCrossRB.setPixmap(QtGui.QPixmap(rbPath))
            self.crossRBGraphPath = rbPath
        if self.get_green_blue_checkbox():
            self.ui.imageCrossGB.setPixmap(QtGui.QPixmap(gbPath))
            self.crossGBGraphPath = gbPath

        # Change to auto section of output tab
        self.select_tab("output", "cross")

        self.progress(10)

        # disable processing mode
        self.set_processing(False)

    # Performs a triple correlation.
    def tripleCorrelation(self):
        # enable processing mode
        self.set_processing(True)

        self.numSteps = 14

        # Construct string containing channels to be used
        self.msgTriple()

        self.progress(1)

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
        # disable inputs for parts 2 and 3 for now
        self.ui.resolution16.setEnabled(False)
        self.ui.resolution32.setEnabled(False)
        self.ui.resolution64.setEnabled(False)
        self.ui.continueButton1.setEnabled(False)
        self.ui.continueButton2.setEnabled(False)
        self.ui.tripleRangeTextbox.setEnabled(False)
        self.ui.tripleWTextbox.setEnabled(False)
        self.ui.tripleG0Textbox.setEnabled(False)
        self.ui.tripleGinfTextbox.setEnabled(False)

        result = None

        # define a path to save the image
        path = os.path.join(TEMP_DIR, "triple_1.png")

        # Save graph path
        self.tripleGraph1Path = path

        self.progress(2)

        if self.get_num_images() == 1:
            # convert the RGB image to a PIL image
            pilImage = PIL.Image.open(self.rgbPath)
            
            self.progress(3)

            # call the midend to get the result object
            result = midend.adaptor.run_triple_mixed_image_part1(pilImage)

            self.progress(4)

        elif self.get_num_images() == 3:
            # convert images to PIL images
            pilR = PIL.Image.open(self.redPath)
            pilG = PIL.Image.open(self.greenPath)
            pilB = PIL.Image.open(self.bluePath)
            
            self.progress(3)

            # call the midend to get the result object
            result = midend.adaptor.run_triple_split_image_part1(pilR, pilG, pilB)
            
            self.progress(4)

        # create the graph
        fileLike = result.plotToStringIO()
        outFile = open(path, "wb")
        for line in fileLike.readlines():
            outFile.write(line)
        outFile.close()

        self.progress(6)

        # show the graph
        self.ui.imageTripleFourier.setPixmap(QtGui.QPixmap(path))

        # save result for next part
        self.tripleResult1 = result

        self.progress(7)

        # enable sample resolution radio buttons and continue button 1
        self.ui.resolution16.setEnabled(True)
        self.ui.resolution32.setEnabled(True)
        self.ui.resolution64.setEnabled(True)
        self.ui.continueButton1.setEnabled(True)


    # Begin triple correlation process (part 2)
    def triple_process(self):
        # enable processing mode if it isn't already enabled
        self.set_processing(True)

        result = None

        # define a path to save the image
        path = os.path.join(TEMP_DIR, "triple_2.png")

        # Save graph path
        self.tripleGraph2Path = path

         # Read sample resolution (limit)
        limit = self.get_sample_resolution()

        # call the midend to get the result object
        try:
            result = midend.adaptor.run_triple_part2(self.tripleResult1, limit)
        except MemoryError:
            memMsg = ("There is not enough memory available to continue this "
                      "operation. Please ensure there is at least:\n"
                      "64x64 limit: 256 MB of memory free\n"
                      "32x32 limit: 16 MB of memory free\n"
                      "16x16 limit: 1 MB of memory free\n"
                      "or use a smaller size.")
            QtGui.QMessageBox.warning(self, "Out of Memory", memMsg)
            return

        # save result for next part
        self.tripleResult2 = result

        self.progress(8)

        # create the graph
        fileLike = result.plotToStringIO()
        outFile = open(path, "wb")
        for line in fileLike.readlines():
            outFile.write(line)
        outFile.close()
        

        self.progress(9)

        # display the graph
        self.ui.imageTripleCorrelation.setPixmap(QtGui.QPixmap(path))

        # Enable parameter inputs and continue button 2
        self.ui.tripleRangeTextbox.setEnabled(True)
        self.ui.tripleWTextbox.setEnabled(True)
        self.ui.tripleG0Textbox.setEnabled(True)
        self.ui.tripleGinfTextbox.setEnabled(True)
        self.ui.continueButton2.setEnabled(True)

        self.progress(10)

    # Finish off triple correlation process (part 3)
    def triple_complete(self):
        # enable processing mode if it isn't already enabled
        self.set_processing(True)

        # input validation
        validInput = self.validate_input("triple_part3")
        
        if validInput:
            range_val = int(self.get_triple_range())
            g0 = float(self.get_triple_G0())
            w = float(self.get_triple_W())
            gInf = float(self.get_triple_Ginf())

            self.progress(11)

            # call the midend to get the result object
            result = midend.adaptor.run_triple_part3(self.tripleResult2, range_val, g0, w, gInf)
        
            # save the result object
            self.tripleResult3 = result

            self.progress(12)

            # create the fitting curve
            path = os.path.join(TEMP_DIR, "triple_3.png")
            self.tripleGraph3Path = path
            fileLike = result.plotToStringIO()
            outFile = open(path, "wb")
            for line in fileLike.readlines():
                outFile.write(line)
            outFile.close()

            self.progress(13)

            # Show fitting curve
            self.ui.imageTripleFittingCurve.setPixmap(QtGui.QPixmap(path))

            # Show updated parameters
            self.ui.tripleResNormValue.setText(str(round(result.resNorm,PRECISION)))
            self.ui.tripleG0Value.setText(str(round(result.g0,PRECISION)))
            self.ui.tripleWValue.setText(str(round(result.w,PRECISION)))
            self.ui.tripleGinfValue.setText(str(round(result.ginf,PRECISION)))

            self.progress(14)

        # disable processing mode
        self.set_processing(False)

    # Performs all possible correlations
    def allCorrelations(self):

        # enable processing mode
        self.set_processing(True)

        self.numSteps = 12

        self.progress(0)

        # Make color lists to send to the midend
        autoColors = ['r', 'g', 'b']
        crossColors = ['rg', 'rb', 'gb']
        
        # Get input parameters
        g0 = self.get_all_G0()
        w = self.get_all_W()
        ginf = self.get_all_Ginf()
        range_val = self.get_all_range()
        deltas = self.get_all_deltas_checkbox()

        self.progress(1)

        # Run auto and cross correlations by calling the midend
        autoResult = None
        crossResult = None
        if self.get_num_images() == 1:
            pilImage = PIL.Image.open(self.rgbPath)
            self.progress(2)
            inputs = (pilImage, autoColors, g0, w, ginf, range_val, deltas)
            autoResult = midend.adaptor.run_dual_mixed_image(*inputs)
            self.progress(3)
            inputs = (pilImage, crossColors, g0, w, ginf, range_val, deltas)
            crossResult = midend.adaptor.run_dual_mixed_image(*inputs)
            self.progress(4)
        elif self.get_num_images() == 3:
            pilR = PIL.Image.open(self.redPath)
            pilG = PIL.Image.open(self.greenPath)
            pilB = PIL.Image.open(self.bluePath)
            self.progress(2)
            inputs = (pilR, pilG, pilB, autoColors, g0, w, ginf, range_val, deltas)
            autoResult = midend.adaptor.run_dual_separate_image(*inputs)
            self.progress(3)
            inputs = (pilR, pilG, pilB, crossColors, g0, w, ginf, range_val, deltas)
            crossResult = midend.adaptor.run_dual_separate_image(*inputs)
            self.progress(4)
        else:
            print("Error: number of images is not 1 or 3.")

        # Track results
        self.autoResult = autoResult
        self.crossResult = crossResult

        # Get updated parameters and update output tab
        self.set_auto_resnorm(round(autoResult[0].resNorm, PRECISION))
        self.set_auto_G0(round(autoResult[0].g0,PRECISION))
        self.set_auto_W(round(autoResult[0].w,PRECISION))
        self.set_auto_Ginf(round(autoResult[0].ginf,PRECISION))
        self.set_auto_deltas(autoResult[0].usedDeltas)

        self.progress(5)

        self.set_cross_resnorm(round(crossResult[0].resNorm, PRECISION))
        self.set_cross_G0(round(crossResult[0].g0, PRECISION))
        self.set_cross_W(round(crossResult[0].w, PRECISION))
        self.set_cross_Ginf(round(crossResult[0].ginf, PRECISION))
        self.set_cross_deltas(crossResult[0].usedDeltas)

        self.progress(6)

        # Create and display the graphs
        rPath = os.path.join(TEMP_DIR, "r_graph.png")
        gPath = os.path.join(TEMP_DIR, "g_graph.png")
        bPath = os.path.join(TEMP_DIR, "b_graph.png")
        rgPath = os.path.join(TEMP_DIR, "rg_graph.png")
        rbPath = os.path.join(TEMP_DIR, "rb_graph.png")
        gbPath = os.path.join(TEMP_DIR, "gb_graph.png")

        self.autoRedGraphPath = rPath
        self.autoGreenGraphPath = gPath
        self.autoBlueGraphPath = bPath
        self.crossRGGraphPath = rgPath
        self.crossRBGraphPath = rbPath
        self.crossGBGraphPath = gbPath

        self.progress(7)

        for i, x in enumerate(autoResult):
            fileLike = x.plotToStringIO()
            outFile = None
            if x.color == "r":
                outFile = open(rPath, "wb")
            elif x.color == "g":
                outFile = open(gPath, "wb")
            elif x.color == "b":
                outFile = open(bPath, "wb")
            else:
                print("Error: invalid color.")
                
            for line in fileLike.readlines():
                outFile.write(line)
            outFile.close()
        
        self.progress(9)

        for i, x in enumerate(crossResult):
            fileLike = x.plotToStringIO()
            outFile = None
            if x.color == "rg":
                outFile = open(rgPath, "wb")
            elif x.color == "rb":
                outFile = open(rbPath, "wb")
            elif x.color == "gb":
                outFile = open(gbPath, "wb")
            else:
                print("Error: invalid color.")

            for line in fileLike.readlines():
                outFile.write(line)
            outFile.close()

        self.progress(11)

        self.ui.imageAutoRed.setPixmap(QtGui.QPixmap(rPath))
        self.ui.imageAutoGreen.setPixmap(QtGui.QPixmap(gPath))
        self.ui.imageAutoBlue.setPixmap(QtGui.QPixmap(bPath))
        self.ui.imageCrossRG.setPixmap(QtGui.QPixmap(rgPath))
        self.ui.imageCrossRB.setPixmap(QtGui.QPixmap(rbPath))
        self.ui.imageCrossGB.setPixmap(QtGui.QPixmap(gbPath))

        # Select triple correlation tab to allow further parameter input
        self.select_tab("output", "triple")

        self.progress(12)

        # Show the Fourier transform (red) surface plot
        self.show_fourier()

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
        text += "Range = " + str(self.get_all_range()) + ", g(0) = "
        text += str(self.get_all_G0()) + ", w = " + str(self.get_all_W())
        text += ", gInf = " + str(self.get_all_Ginf()) + "],"
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
    # Graph Zoom Functions                              #
    #####################################################
    
    # Zoom functions for individual graphs
    def zoomRed(self):
        self.zoomGraph(self.autoRedGraphPath)
    def zoomGreen(self):
        self.zoomGraph(self.autoGreenGraphPath)
    def zoomBlue(self):
        self.zoomGraph(self.autoBlueGraphPath)
    def zoomRedGreen(self):
        self.zoomGraph(self.crossRGGraphPath)
    def zoomRedBlue(self):
        self.zoomGraph(self.crossRBGraphPath)
    def zoomGreenBlue(self):
        self.zoomGraph(self.crossGBGraphPath)
    def zoomTriple1(self):
        self.zoomGraph(self.tripleGraph1Path)
    def zoomTriple2(self):
        self.zoomGraph(self.tripleGraph2Path)
    def zoomTriple3(self):
        self.zoomGraph(self.tripleGraph3Path)

    # Shows a zoomed-in version of an image at a given path
    def zoomGraph(self, path):
        zoomGraph = GraphZoom(self)
        zoomGraph.show()
        zoomGraph.load_image(path)
        

    #####################################################
    # Miscellaneous Functions                           #
    #####################################################

    # Construct an RGB Image from three separate channel images (if needed)
    #  This function will also get rid of any RGB image that was previously loaded,
    #  as the user has changed their mind if they are now trying to load a monochrome
    #  image. It also gets rid of any monochrome images that have been loaded from
    #  the temporary directory as these have been split from the RGB image.
    def constructRGB(self):
        # If an RGB image has been loaded, clear it
        self.rgbPath = ""
        self.ui.imageRgb.clear()

        # If all 3 monochrome images have been loaded, combine them
        if self.redPath != "" and self.greenPath != "" and self.bluePath != "":
            self.numSteps = 5
            self.progress(0)
            rgb = numpy.dstack((self.redChannel,self.greenChannel,self.blueChannel))
            self.progress(1)
            rgb_image = PIL.Image.fromarray(numpy.uint8(rgb))
            self.progress(2)
            path = os.path.join(TEMP_DIR, "rgb_image.png")
            self.progress(3)
            scipy.misc.imsave(path, rgb_image)
            self.progress(4)
            self.ui.imageRgb.setPixmap(QtGui.QPixmap(path))
            self.progress(5)

    # Removes any images generated by splitting an RGB image.
    def remove_split_images(self):
        if str(os.path.dirname(self.redPath)) == TEMP_DIR:
            if str(os.path.basename(self.redPath)) == "blue.png":
                self.redPath = ""
                self.ui.imageRed.clear()
        if str(os.path.dirname(self.greenPath)) == TEMP_DIR:
            if str(os.path.basename(self.greenPath)) == "green.png":
                self.greenPath = ""
                self.ui.imageGreen.clear()
        if str(os.path.dirname(self.bluePath)) == TEMP_DIR:
            if str(os.path.basename(self.bluePath)) == "blue.png":
                self.bluePath = ""
                self.ui.imageBlue.clear()

    # Refreshes the temporary directory by deleting and recreating it
    def refresh_temp(self):
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR)

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
    def progress(self, value):
        self.ui.progressBar.setValue(value * 100 / self.numSteps)

    # Sets the program mode as 'processing' or 'not processing', which includes
    #  enabling/disabling of start and stop buttons and other interface features
    def set_processing(self, value):
        self.ui.startButton.setEnabled(not value)
        self.ui.stopButton.setEnabled(value)
        self.ui.batchModeButton.setEnabled(not value)
        self.ui.correlationSettingsGroup.setEnabled(not value)
        self.ui.imageSettingsGroup.setEnabled(not value)
        self.ui.progressBar.setVisible(value)

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

    # Sets the default parameters for all input fields.
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

        self.ui.tripleRangeTextbox.setPlaceholderText("16")
        self.ui.tripleGinfTextbox.setPlaceholderText("0")
        self.ui.tripleWTextbox.setPlaceholderText("10")
        self.ui.tripleG0Textbox.setPlaceholderText("1")

    # Loads the default/placeholder images into the interface
    def load_default_images(self):
        self.ui.imageRgb.setPixmap(QtGui.QPixmap(RGB_PLACEHOLDER))
        self.ui.imageRed.setPixmap(QtGui.QPixmap(RED_PLACEHOLDER))
        self.ui.imageGreen.setPixmap(QtGui.QPixmap(GREEN_PLACEHOLDER))
        self.ui.imageBlue.setPixmap(QtGui.QPixmap(BLUE_PLACEHOLDER))
        self.ui.redGraphZoom.setIcon(QtGui.QIcon(ZOOM_ICON))
        self.ui.greenGraphZoom.setIcon(QtGui.QIcon(ZOOM_ICON))
        self.ui.blueGraphZoom.setIcon(QtGui.QIcon(ZOOM_ICON))
        self.ui.redGreenGraphZoom.setIcon(QtGui.QIcon(ZOOM_ICON))
        self.ui.redBlueGraphZoom.setIcon(QtGui.QIcon(ZOOM_ICON))
        self.ui.greenBlueGraphZoom.setIcon(QtGui.QIcon(ZOOM_ICON))
        self.ui.tripleGraph1Zoom.setIcon(QtGui.QIcon(ZOOM_ICON))
        self.ui.tripleGraph2Zoom.setIcon(QtGui.QIcon(ZOOM_ICON))
        self.ui.tripleGraph3Zoom.setIcon(QtGui.QIcon(ZOOM_ICON))

    # Saves all output to a specified folder
    def saveAll(self):
        self.numSteps = 12

        # get folder from user
        saveDir = str(QtGui.QFileDialog.getExistingDirectory(self, "Export Graphs"))
        
        # enable processing mode
        self.set_processing(True)

        # export all graphs to that folder
        self.progress(0)
        self.exportFile(self.autoRedGraphPath, saveDir)
        self.progress(1)
        self.exportFile(self.autoGreenGraphPath, saveDir)
        self.progress(2)
        self.exportFile(self.autoBlueGraphPath, saveDir)
        self.progress(3)
        self.exportFile(self.crossRGGraphPath, saveDir)
        self.progress(4)
        self.exportFile(self.crossRBGraphPath, saveDir)
        self.progress(5)
        self.exportFile(self.crossGBGraphPath, saveDir)
        self.progress(6)
        self.exportFile(self.tripleGraph1Path, saveDir)
        self.progress(7)
        self.exportFile(self.tripleGraph2Path, saveDir)
        self.progress(8)
        self.exportFile(self.tripleGraph3Path, saveDir)
        self.progress(9)

        # export all text files to that folder
        resultList = []

        if self.autoResult != None:
            resultList.extend(self.autoResult)
            for x in self.autoResult:
                x.saveData(saveDir)
        self.progress(10)

        if self.crossResult != None:
            resultList.extend(self.crossResult)
            for x in self.crossResult:
                x.saveData(saveDir)
        self.progress(11)

        if self.tripleResult3 != None:
            resultList.append(self.tripleResult3)
            self.tripleResult3.saveData(saveDir)

        midend.result.saveResultsFile(saveDir, resultList)
    
        self.progress(12)

        self.set_processing(False)

    # Saves a specific file into a directory if the file exists
    def exportFile(self, filepath, destination):
        if os.path.isfile(filepath):
            dest_path = os.path.join(destination, os.path.basename(filepath))
            shutil.copyfile(filepath, dest_path)

# Program loop
def start():
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())
