# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graphzoom.ui'
#
# Created: Tue Mar 26 10:08:36 2013
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

class Ui_graphZoomWindow(object):
    def setupUi(self, graphZoomWindow):
        graphZoomWindow.setObjectName(_fromUtf8("graphZoomWindow"))
        graphZoomWindow.resize(670, 670)
        self.centralwidget = QtGui.QWidget(graphZoomWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.image = QtGui.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(40, 10, 591, 591))
        self.image.setFrameShape(QtGui.QFrame.Panel)
        self.image.setFrameShadow(QtGui.QFrame.Raised)
        self.image.setLineWidth(2)
        self.image.setText(_fromUtf8(""))
        self.image.setScaledContents(True)
        self.image.setObjectName(_fromUtf8("image"))
        self.closeButton = QtGui.QPushButton(self.centralwidget)
        self.closeButton.setGeometry(QtCore.QRect(400, 610, 211, 51))
        self.closeButton.setDefault(True)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.saveButton = QtGui.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(60, 610, 211, 51))
        self.saveButton.setDefault(False)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        graphZoomWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(graphZoomWindow)
        QtCore.QMetaObject.connectSlotsByName(graphZoomWindow)

    def retranslateUi(self, graphZoomWindow):
        graphZoomWindow.setWindowTitle(_translate("graphZoomWindow", "Graph Zoom", None))
        self.closeButton.setText(_translate("graphZoomWindow", "Close Window", None))
        self.saveButton.setText(_translate("graphZoomWindow", "Save Image", None))

