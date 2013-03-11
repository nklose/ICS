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

import sys
from PyQt4 import QtCore, QtGui
from local_GUI.main_ICS import Ui_Dialog
from os.path import basename

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        # Interface variables
        self.redPath = ""
        self.greenPath = ""
        self.bluePath = ""
        self.rgbPath = ""

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

        # Restart Button
        QtCore.QObject.connect(self.ui.restartButton,
                               QtCore.SIGNAL("clicked()"),
                               self.restart)


    # Loads an RGB image into the interface.
    def load_RGB_image(self):
        self.message("Loading RGB Image...")
        self.rgbPath = str(QtGui.QFileDialog.getOpenFileName())
        self.message("Loaded image " + self.rgbPath)
        self.ui.rgbFile.setText(basename(self.rgbPath))
        self.ui.imageRgb.setPixmap(QtGui.QPixmap(self.rgbPath))

    # Loads a red channel image into the interface.
    def load_red_image(self):
        self.message("Loading red image...")
        self.redPath = str(QtGui.QFileDialog.getOpenFileName())
        self.message("Loaded image " + self.redPath)
        self.ui.redChannelFile.setText(basename(self.redPath))
        self.ui.imageRed.setPixmap(QtGui.QPixmap(self.redPath))

    # Loads a green channel image into the interface.
    def load_green_image(self):
        self.message("Loading green image...")
        self.greenPath = str(QtGui.QFileDialog.getOpenFileName())
        self.message("Loaded image " + self.greenPath)
        self.ui.greenChannelFile.setText(basename(self.greenPath))
        self.ui.imageGreen.setPixmap(QtGui.QPixmap(self.greenPath))
 
    # Loads a blue channel image into the interface.
    def load_blue_image(self):
        self.message("Loading blue image...")
        self.bluePath = str(QtGui.QFileDialog.getOpenFileName())
        self.message("Loaded image " + self.bluePath)
        self.ui.blueChannelFile.setText(basename(self.bluePath))
        self.ui.imageBlue.setPixmap(QtGui.QPixmap(self.bluePath))

    # Start button functionality
    def start(self):
        
        # Find out which correlation to do
        mode = self.get_correlation_tab()
            
        # Input Checking
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
        
        # Continue if input is valid
        if validInput:
            # Update message bar with input parameters
            text = ""
            if mode == "auto":
                # Construct string containing channels to be used
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
                text += " and parameters\n[range = " + self.get_auto_range()
                text += ", g(0) = " + self.get_auto_G0() +", w = "
                text += self.get_auto_W() + ", gInf = " + self.get_auto_Ginf() 
                text += "],"
                if self.get_auto_deltas_checkbox() == False:
                    text += " do not"
                text += " consider deltas, S.R. "
                res = str(self.get_sample_resolution())
                text += res + " x " + res + "."
                self.message(text)
                 # Do auto-correlation
            
            elif mode == "cross":
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
                text += self.get_cross_range() + ", g(0) = " 
                text += self.get_cross_G0() + ", w = "
                text += self.get_cross_W() + ", gInf = "
                text += self.get_cross_Ginf() + "],"
                if self.get_cross_deltas_checkbox() == False:
                    text+= " do not"
                text += " consider deltas, S.R. " 
                res = str(self.get_sample_resolution())
                text += res + " x " + res + "."
                # Do cross-correlation
                self.message(text)

            elif mode == "triple":
                res = str(self.get_sample_resolution())
                text = "Starting triple correlation with sample resolution "
                text += res + " x " + res + "."
                # Do triple correlation
                self.message(text)

            elif mode == "all":
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
                        


    # Restart button functionality (unused currently)
    def restart(self):
        self.message("Restarting.")
        
    ######################################################
    # Functions to get the current state of the program  #
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

    ## Text inputs
    # Returns inputted Range in AC
    def get_auto_range(self):
        return str(self.ui.autoRangeTextbox.text())

    # Returns inputted G(0) in AC
    def get_auto_G0(self):
        return str(self.ui.autoG0Textbox.text())

    # Returns inputted W in AC
    def get_auto_W(self):
        return str(self.ui.autoWTextbox.text())

    # Returns inputted G(Inf) in AC
    def get_auto_Ginf(self):
        return str(self.ui.autoGinfTextbox.text())

    # Returns inputted Range in XC
    def get_cross_range(self):
        return str(self.ui.crossRangeTextbox.text())
    
    # Returns inputted G(0) in XC
    def get_cross_G0(self):
        return str(self.ui.crossG0Textbox.text())

    # Returns inputted W in XC
    def get_cross_W(self):
        return str(self.ui.crossWTextbox.text())
    
    # Returns inputted G(Inf) in XC
    def get_cross_Ginf(self):
        return str(self.ui.crossGinfTextbox.text())

    # Returns inputted Range in AXC
    def get_all_range(self):
        return str(self.ui.allAutoCrossRangeTextbox.text())
    
    # Returns inputted G(0) in AXC
    def get_all_G0(self):
        return str(self.ui.allAutoCrossG0Textbox.text())
    
    # Returns inputted W in AXC
    def get_all_W(self):
        return str(self.ui.allAutoCrossWTextbox.text())

    # Returns inputted Ginf in AXC
    def get_all_Ginf(self):
        return str(self.ui.allAutoCrossGinfTextbox.text())

    # Returns inputted limit for TC (Output Tab)
    def get_TC_limit(self):
        return str(self.ui.startingPointInput.text())

    # Returns inputted range for TC (Output Tab)
    def get_TC_range(self):
        return str(self.ui.tripleRangeTextbox.text())

    # Returns inputted G(0) for TC (Output Tab)
    def get_TC_G0(self):
        return str(self.ui.tripleG0Textbox.text())

    # Returns inputted W for TC (Output Tab)
    def get_TC_W(self):
        return str(self.ui.tripleWTextbox.text())

    # Returns inputted G(Inf) for TC (Output Tab)
    def get_TC_Ginf(self):
        return str(self.ui.tripleGinfTextbox.text())

    ## Radio buttons

    # Returns sample resolution (32, 48, or 64)
    def get_sample_resolution(self):
        if self.ui.resolution32.isChecked() != 0:
            return 32
        elif self.ui.resolution48.isChecked() != 0:
            return 48
        elif self.ui.resolution64.isChecked() != 0:
            return 64
        else:
            return -1
    
    #####################################################
    # Miscellaneous Functions                           #
    #####################################################

    # Message Box functionality
    def message(self, text):
        self.ui.messageBox.setText(str(text))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())
