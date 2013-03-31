# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help.ui'
#
# Created: Sat Mar 30 21:20:20 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_HelpWindow(object):
    def setupUi(self, HelpWindow):
        HelpWindow.setObjectName(_fromUtf8("HelpWindow"))
        HelpWindow.resize(900, 600)
        self.centralwidget = QtGui.QWidget(HelpWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.title = QtGui.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(0, 10, 901, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName(_fromUtf8("title"))
        self.version = QtGui.QLabel(self.centralwidget)
        self.version.setGeometry(QtCore.QRect(0, 30, 901, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.version.setFont(font)
        self.version.setAlignment(QtCore.Qt.AlignCenter)
        self.version.setObjectName(_fromUtf8("version"))
        self.copyright = QtGui.QLabel(self.centralwidget)
        self.copyright.setGeometry(QtCore.QRect(0, 50, 901, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.copyright.setFont(font)
        self.copyright.setAlignment(QtCore.Qt.AlignCenter)
        self.copyright.setObjectName(_fromUtf8("copyright"))
        self.license = QtGui.QLabel(self.centralwidget)
        self.license.setGeometry(QtCore.QRect(0, 70, 901, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.license.setFont(font)
        self.license.setAlignment(QtCore.Qt.AlignCenter)
        self.license.setObjectName(_fromUtf8("license"))
        self.closeButton = QtGui.QPushButton(self.centralwidget)
        self.closeButton.setGeometry(QtCore.QRect(710, 550, 181, 41))
        self.closeButton.setDefault(True)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.licenseButton = QtGui.QPushButton(self.centralwidget)
        self.licenseButton.setGeometry(QtCore.QRect(410, 550, 181, 41))
        self.licenseButton.setObjectName(_fromUtf8("licenseButton"))
        self.helpButton = QtGui.QPushButton(self.centralwidget)
        self.helpButton.setGeometry(QtCore.QRect(10, 550, 181, 41))
        self.helpButton.setObjectName(_fromUtf8("helpButton"))
        self.readmeButton = QtGui.QPushButton(self.centralwidget)
        self.readmeButton.setGeometry(QtCore.QRect(210, 550, 181, 41))
        self.readmeButton.setObjectName(_fromUtf8("readmeButton"))
        self.text = QtGui.QTextBrowser(self.centralwidget)
        self.text.setGeometry(QtCore.QRect(10, 100, 881, 441))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(10)
        self.text.setFont(font)
        self.text.setObjectName(_fromUtf8("text"))
        self.logo = QtGui.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(850, 10, 41, 41))
        self.logo.setFrameShape(QtGui.QFrame.NoFrame)
        self.logo.setFrameShadow(QtGui.QFrame.Plain)
        self.logo.setText(_fromUtf8(""))
        self.logo.setScaledContents(True)
        self.logo.setObjectName(_fromUtf8("logo"))
        HelpWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(HelpWindow)
        QtCore.QMetaObject.connectSlotsByName(HelpWindow)

    def retranslateUi(self, HelpWindow):
        HelpWindow.setWindowTitle(_translate("HelpWindow", "MainWindow", None))
        self.title.setText(_translate("HelpWindow", "Image Correlation Spectroscopy (ICS)", None))
        self.version.setText(_translate("HelpWindow", "Version 2.1 Beta", None))
        self.copyright.setText(_translate("HelpWindow", "Copyright (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson, Omar Qadri, and James Wang.", None))
        self.license.setText(_translate("HelpWindow", "Released under the GPL-compatible 401 IP License.", None))
        self.closeButton.setText(_translate("HelpWindow", "Close Window", None))
        self.licenseButton.setText(_translate("HelpWindow", "View License", None))
        self.helpButton.setText(_translate("HelpWindow", "View Help", None))
        self.readmeButton.setText(_translate("HelpWindow", "View Readme", None))
        self.text.setHtml(_translate("HelpWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Courier New\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:11pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:11pt;\"><br /></p></body></html>", None))

