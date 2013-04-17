"""
This script provides functionality for the help dialog in the local GUI.

Code for the basic framework was borrowed from:
http://www.rkblog.rk.edu.pl/w/p/simple-text-editor-pyqt4/

Code for using PyQt4 functions is from PyQt Class Reference:
http://pyqt.sourceforge.net/Docs/PyQt4/classes.html

Copyright (c) 2013 Nick Klose, Richard Leung, Cameron Mann,
Glen Nelson, Omar Qadri, and James Wang under the 401 IP License.
See LICENSE file for more details.
"""
import sys
import os.path
from PyQt4 import QtCore, QtGui
from gui_help import Ui_HelpWindow

LICENSE_FILE = "LICENSE"
README_FILE = "README.md"
HELP_FILE = "HELP"
LOGO = "icon.ico"

class Help(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.ui = Ui_HelpWindow()
        self.ui.setupUi(self)

        # Force consistent theme and font size
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))
        self.setStyleSheet("font-size: 11pt")
        
        # Disable resizing
        self.setFixedSize(self.size())

        # Load program logo
        self.ui.logo.setPixmap(QtGui.QPixmap(LOGO))

        # Show help by default
        self.help()
        
        #######################################################
        # Interface Object Connections                        #
        #######################################################
        
        clicked = QtCore.SIGNAL("clicked()")
        
        ## Buttons
        QtCore.QObject.connect(self.ui.closeButton, clicked, self.close)
        QtCore.QObject.connect(self.ui.licenseButton, clicked, self.license)
        QtCore.QObject.connect(self.ui.readmeButton, clicked, self.readme)
        QtCore.QObject.connect(self.ui.helpButton, clicked, self.help)
        QtCore.QObject.connect(self, QtCore.SIGNAL("triggered()"), self.closeEvent)

    # Loads the LICENSE file into the text window.
    def license(self):
        self.showText(LICENSE_FILE)

    # Loads the README file into the text window.
    def readme(self):
        self.showText(README_FILE)

    # Loads the HELP file into the text window.
    def help(self):
        text = open(HELP_FILE)
        lineNumber = 1
        title = ""
        version = ""
        copyright_info = ""
        license_info = ""
        displayText = ""

        for line in text:
            if lineNumber == 1:
                self.ui.title.setText(str(line)[:-1])
            elif lineNumber == 2:
                self.ui.version.setText(str(line)[:-1])
            elif lineNumber == 3:
                self.ui.copyright.setText(str(line)[:-1])
            elif lineNumber == 4:
                self.ui.license.setText(str(line)[:-1])
            elif lineNumber == 5:
                pass
            else:
                displayText += str(line)

            lineNumber += 1

        self.ui.text.setText(displayText)

    # Shows a given filename in the text window.
    def showText(self, filename):
        text = open(filename)
        displayText = ""
        for line in text:
            displayText += str(line)

        self.ui.text.setText(displayText)

    # Notify parent window that this interface is closing
    def closeEvent(self, e):
        self.parent.helpOpen = False
        self.deleteLater()
        

def start():
    app = QtGui.QApplication(sys.argv)
    help_app = Help()
    help_app.show()
    sys.exit(app.exec_())
