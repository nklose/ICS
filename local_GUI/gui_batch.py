# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'batch.ui'
#
# Created: Sat Mar 30 21:23:54 2013
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1024, 670)
        Dialog.setAutoFillBackground(False)
        self.startButton = QtGui.QPushButton(Dialog)
        self.startButton.setGeometry(QtCore.QRect(10, 620, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.startButton.setFont(font)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.singleModeButton = QtGui.QPushButton(Dialog)
        self.singleModeButton.setGeometry(QtCore.QRect(740, 620, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.singleModeButton.setFont(font)
        self.singleModeButton.setObjectName(_fromUtf8("singleModeButton"))
        self.stopButton = QtGui.QPushButton(Dialog)
        self.stopButton.setGeometry(QtCore.QRect(140, 620, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.stopButton.setFont(font)
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.imageGroup = QtGui.QGroupBox(Dialog)
        self.imageGroup.setGeometry(QtCore.QRect(10, 20, 1001, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.imageGroup.setFont(font)
        self.imageGroup.setFlat(False)
        self.imageGroup.setCheckable(False)
        self.imageGroup.setObjectName(_fromUtf8("imageGroup"))
        self.labelRGB = QtGui.QLabel(self.imageGroup)
        self.labelRGB.setGeometry(QtCore.QRect(80, 220, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelRGB.setFont(font)
        self.labelRGB.setObjectName(_fromUtf8("labelRGB"))
        self.labelRed = QtGui.QLabel(self.imageGroup)
        self.labelRed.setGeometry(QtCore.QRect(360, 220, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelRed.setFont(font)
        self.labelRed.setObjectName(_fromUtf8("labelRed"))
        self.labelGreen = QtGui.QLabel(self.imageGroup)
        self.labelGreen.setGeometry(QtCore.QRect(600, 220, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelGreen.setFont(font)
        self.labelGreen.setObjectName(_fromUtf8("labelGreen"))
        self.labelBlue = QtGui.QLabel(self.imageGroup)
        self.labelBlue.setGeometry(QtCore.QRect(860, 220, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelBlue.setFont(font)
        self.labelBlue.setObjectName(_fromUtf8("labelBlue"))
        self.imageRgb = QtGui.QLabel(self.imageGroup)
        self.imageRgb.setGeometry(QtCore.QRect(30, 30, 191, 191))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.imageRgb.setFont(font)
        self.imageRgb.setFrameShape(QtGui.QFrame.Panel)
        self.imageRgb.setFrameShadow(QtGui.QFrame.Sunken)
        self.imageRgb.setText(_fromUtf8(""))
        self.imageRgb.setObjectName(_fromUtf8("imageRgb"))
        self.imageRed = QtGui.QLabel(self.imageGroup)
        self.imageRed.setGeometry(QtCore.QRect(280, 30, 191, 191))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.imageRed.setFont(font)
        self.imageRed.setFrameShape(QtGui.QFrame.Panel)
        self.imageRed.setFrameShadow(QtGui.QFrame.Sunken)
        self.imageRed.setText(_fromUtf8(""))
        self.imageRed.setObjectName(_fromUtf8("imageRed"))
        self.imageGreen = QtGui.QLabel(self.imageGroup)
        self.imageGreen.setGeometry(QtCore.QRect(530, 30, 191, 191))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.imageGreen.setFont(font)
        self.imageGreen.setFrameShape(QtGui.QFrame.Panel)
        self.imageGreen.setFrameShadow(QtGui.QFrame.Sunken)
        self.imageGreen.setText(_fromUtf8(""))
        self.imageGreen.setObjectName(_fromUtf8("imageGreen"))
        self.imageBlue = QtGui.QLabel(self.imageGroup)
        self.imageBlue.setGeometry(QtCore.QRect(780, 30, 191, 191))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.imageBlue.setFont(font)
        self.imageBlue.setFrameShape(QtGui.QFrame.Panel)
        self.imageBlue.setFrameShadow(QtGui.QFrame.Sunken)
        self.imageBlue.setText(_fromUtf8(""))
        self.imageBlue.setObjectName(_fromUtf8("imageBlue"))
        self.imageParametersGroup = QtGui.QGroupBox(Dialog)
        self.imageParametersGroup.setGeometry(QtCore.QRect(10, 270, 311, 341))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.imageParametersGroup.setFont(font)
        self.imageParametersGroup.setObjectName(_fromUtf8("imageParametersGroup"))
        self.loadButton = QtGui.QPushButton(self.imageParametersGroup)
        self.loadButton.setGeometry(QtCore.QRect(30, 50, 261, 41))
        self.loadButton.setObjectName(_fromUtf8("loadButton"))
        self.fileCountLabel = QtGui.QLabel(self.imageParametersGroup)
        self.fileCountLabel.setGeometry(QtCore.QRect(10, 140, 141, 21))
        self.fileCountLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fileCountLabel.setObjectName(_fromUtf8("fileCountLabel"))
        self.imageFormatLabel = QtGui.QLabel(self.imageParametersGroup)
        self.imageFormatLabel.setGeometry(QtCore.QRect(10, 250, 141, 21))
        self.imageFormatLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.imageFormatLabel.setObjectName(_fromUtf8("imageFormatLabel"))
        self.fileCount = QtGui.QLabel(self.imageParametersGroup)
        self.fileCount.setGeometry(QtCore.QRect(160, 140, 131, 21))
        self.fileCount.setFrameShape(QtGui.QFrame.Box)
        self.fileCount.setFrameShadow(QtGui.QFrame.Sunken)
        self.fileCount.setText(_fromUtf8(""))
        self.fileCount.setObjectName(_fromUtf8("fileCount"))
        self.formatsList = QtGui.QLabel(self.imageParametersGroup)
        self.formatsList.setGeometry(QtCore.QRect(160, 230, 131, 61))
        self.formatsList.setFrameShape(QtGui.QFrame.Box)
        self.formatsList.setFrameShadow(QtGui.QFrame.Sunken)
        self.formatsList.setText(_fromUtf8(""))
        self.formatsList.setAlignment(QtCore.Qt.AlignCenter)
        self.formatsList.setWordWrap(True)
        self.formatsList.setObjectName(_fromUtf8("formatsList"))
        self.rgbCount = QtGui.QLabel(self.imageParametersGroup)
        self.rgbCount.setGeometry(QtCore.QRect(160, 170, 131, 21))
        self.rgbCount.setFrameShape(QtGui.QFrame.Box)
        self.rgbCount.setFrameShadow(QtGui.QFrame.Sunken)
        self.rgbCount.setText(_fromUtf8(""))
        self.rgbCount.setObjectName(_fromUtf8("rgbCount"))
        self.numRgbLabel = QtGui.QLabel(self.imageParametersGroup)
        self.numRgbLabel.setGeometry(QtCore.QRect(10, 170, 141, 21))
        self.numRgbLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.numRgbLabel.setObjectName(_fromUtf8("numRgbLabel"))
        self.numMonochromeLabel = QtGui.QLabel(self.imageParametersGroup)
        self.numMonochromeLabel.setGeometry(QtCore.QRect(10, 200, 141, 21))
        self.numMonochromeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.numMonochromeLabel.setObjectName(_fromUtf8("numMonochromeLabel"))
        self.monoCount = QtGui.QLabel(self.imageParametersGroup)
        self.monoCount.setGeometry(QtCore.QRect(160, 200, 131, 21))
        self.monoCount.setFrameShape(QtGui.QFrame.Box)
        self.monoCount.setFrameShadow(QtGui.QFrame.Sunken)
        self.monoCount.setText(_fromUtf8(""))
        self.monoCount.setObjectName(_fromUtf8("monoCount"))
        self.folderLabel = QtGui.QLabel(self.imageParametersGroup)
        self.folderLabel.setGeometry(QtCore.QRect(50, 100, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.folderLabel.setFont(font)
        self.folderLabel.setFrameShape(QtGui.QFrame.Box)
        self.folderLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.folderLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.folderLabel.setObjectName(_fromUtf8("folderLabel"))
        self.correlationSettingsGroup = QtGui.QGroupBox(Dialog)
        self.correlationSettingsGroup.setGeometry(QtCore.QRect(340, 270, 671, 251))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.correlationSettingsGroup.setFont(font)
        self.correlationSettingsGroup.setObjectName(_fromUtf8("correlationSettingsGroup"))
        self.allTripleParametersGroup = QtGui.QGroupBox(self.correlationSettingsGroup)
        self.allTripleParametersGroup.setGeometry(QtCore.QRect(320, 30, 311, 201))
        self.allTripleParametersGroup.setFlat(False)
        self.allTripleParametersGroup.setCheckable(False)
        self.allTripleParametersGroup.setObjectName(_fromUtf8("allTripleParametersGroup"))
        self.tripleRangeLabel = QtGui.QLabel(self.allTripleParametersGroup)
        self.tripleRangeLabel.setGeometry(QtCore.QRect(10, 30, 51, 31))
        self.tripleRangeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tripleRangeLabel.setObjectName(_fromUtf8("tripleRangeLabel"))
        self.tripleG0Label = QtGui.QLabel(self.allTripleParametersGroup)
        self.tripleG0Label.setGeometry(QtCore.QRect(10, 70, 51, 31))
        self.tripleG0Label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tripleG0Label.setObjectName(_fromUtf8("tripleG0Label"))
        self.tripleWLabel = QtGui.QLabel(self.allTripleParametersGroup)
        self.tripleWLabel.setGeometry(QtCore.QRect(180, 30, 21, 31))
        self.tripleWLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tripleWLabel.setObjectName(_fromUtf8("tripleWLabel"))
        self.tripleGinfLabel = QtGui.QLabel(self.allTripleParametersGroup)
        self.tripleGinfLabel.setGeometry(QtCore.QRect(150, 70, 51, 31))
        self.tripleGinfLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tripleGinfLabel.setObjectName(_fromUtf8("tripleGinfLabel"))
        self.tripleRange = QtGui.QLineEdit(self.allTripleParametersGroup)
        self.tripleRange.setGeometry(QtCore.QRect(70, 30, 91, 31))
        self.tripleRange.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.tripleRange.setCursorPosition(0)
        self.tripleRange.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.tripleRange.setObjectName(_fromUtf8("tripleRange"))
        self.tripleG0 = QtGui.QLineEdit(self.allTripleParametersGroup)
        self.tripleG0.setGeometry(QtCore.QRect(70, 70, 91, 31))
        self.tripleG0.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.tripleG0.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.tripleG0.setObjectName(_fromUtf8("tripleG0"))
        self.tripleW = QtGui.QLineEdit(self.allTripleParametersGroup)
        self.tripleW.setGeometry(QtCore.QRect(210, 30, 91, 31))
        self.tripleW.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.tripleW.setCursorPosition(0)
        self.tripleW.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.tripleW.setObjectName(_fromUtf8("tripleW"))
        self.tripleGinf = QtGui.QLineEdit(self.allTripleParametersGroup)
        self.tripleGinf.setGeometry(QtCore.QRect(210, 70, 91, 31))
        self.tripleGinf.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.tripleGinf.setCursorPosition(0)
        self.tripleGinf.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.tripleGinf.setObjectName(_fromUtf8("tripleGinf"))
        self.tripleG0Label_2 = QtGui.QLabel(self.allTripleParametersGroup)
        self.tripleG0Label_2.setGeometry(QtCore.QRect(0, 100, 151, 31))
        self.tripleG0Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tripleG0Label_2.setObjectName(_fromUtf8("tripleG0Label_2"))
        self.resolution16 = QtGui.QRadioButton(self.allTripleParametersGroup)
        self.resolution16.setGeometry(QtCore.QRect(20, 130, 116, 22))
        self.resolution16.setObjectName(_fromUtf8("resolution16"))
        self.resolution32 = QtGui.QRadioButton(self.allTripleParametersGroup)
        self.resolution32.setGeometry(QtCore.QRect(20, 150, 116, 22))
        self.resolution32.setChecked(True)
        self.resolution32.setObjectName(_fromUtf8("resolution32"))
        self.resolution64 = QtGui.QRadioButton(self.allTripleParametersGroup)
        self.resolution64.setGeometry(QtCore.QRect(20, 170, 116, 22))
        self.resolution64.setObjectName(_fromUtf8("resolution64"))
        self.allAutoCrossGroup = QtGui.QGroupBox(self.correlationSettingsGroup)
        self.allAutoCrossGroup.setGeometry(QtCore.QRect(10, 30, 311, 201))
        self.allAutoCrossGroup.setFlat(False)
        self.allAutoCrossGroup.setCheckable(False)
        self.allAutoCrossGroup.setObjectName(_fromUtf8("allAutoCrossGroup"))
        self.dualRangeLabel = QtGui.QLabel(self.allAutoCrossGroup)
        self.dualRangeLabel.setGeometry(QtCore.QRect(10, 30, 51, 31))
        self.dualRangeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dualRangeLabel.setObjectName(_fromUtf8("dualRangeLabel"))
        self.dualG0Label = QtGui.QLabel(self.allAutoCrossGroup)
        self.dualG0Label.setGeometry(QtCore.QRect(10, 70, 51, 31))
        self.dualG0Label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dualG0Label.setObjectName(_fromUtf8("dualG0Label"))
        self.dualWLabel = QtGui.QLabel(self.allAutoCrossGroup)
        self.dualWLabel.setGeometry(QtCore.QRect(180, 30, 21, 31))
        self.dualWLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dualWLabel.setObjectName(_fromUtf8("dualWLabel"))
        self.dualGinfLabel = QtGui.QLabel(self.allAutoCrossGroup)
        self.dualGinfLabel.setGeometry(QtCore.QRect(150, 70, 51, 31))
        self.dualGinfLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dualGinfLabel.setObjectName(_fromUtf8("dualGinfLabel"))
        self.considerAutoDeltas = QtGui.QCheckBox(self.allAutoCrossGroup)
        self.considerAutoDeltas.setGeometry(QtCore.QRect(20, 110, 301, 20))
        self.considerAutoDeltas.setObjectName(_fromUtf8("considerAutoDeltas"))
        self.considerCrossDeltas = QtGui.QCheckBox(self.allAutoCrossGroup)
        self.considerCrossDeltas.setGeometry(QtCore.QRect(20, 140, 301, 20))
        self.considerCrossDeltas.setObjectName(_fromUtf8("considerCrossDeltas"))
        self.dualRange = QtGui.QLineEdit(self.allAutoCrossGroup)
        self.dualRange.setGeometry(QtCore.QRect(70, 30, 91, 31))
        self.dualRange.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.dualRange.setCursorPosition(0)
        self.dualRange.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.dualRange.setObjectName(_fromUtf8("dualRange"))
        self.dualG0 = QtGui.QLineEdit(self.allAutoCrossGroup)
        self.dualG0.setGeometry(QtCore.QRect(70, 70, 91, 31))
        self.dualG0.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.dualG0.setCursorPosition(0)
        self.dualG0.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.dualG0.setObjectName(_fromUtf8("dualG0"))
        self.dualW = QtGui.QLineEdit(self.allAutoCrossGroup)
        self.dualW.setGeometry(QtCore.QRect(210, 30, 91, 31))
        self.dualW.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.dualW.setCursorPosition(0)
        self.dualW.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.dualW.setObjectName(_fromUtf8("dualW"))
        self.dualGinf = QtGui.QLineEdit(self.allAutoCrossGroup)
        self.dualGinf.setGeometry(QtCore.QRect(210, 70, 91, 31))
        self.dualGinf.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.dualGinf.setCursorPosition(0)
        self.dualGinf.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.dualGinf.setObjectName(_fromUtf8("dualGinf"))
        self.messageBox = QtGui.QLabel(Dialog)
        self.messageBox.setGeometry(QtCore.QRect(340, 530, 671, 81))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Consolas"))
        font.setPointSize(10)
        self.messageBox.setFont(font)
        self.messageBox.setFrameShape(QtGui.QFrame.WinPanel)
        self.messageBox.setFrameShadow(QtGui.QFrame.Sunken)
        self.messageBox.setLineWidth(1)
        self.messageBox.setAlignment(QtCore.Qt.AlignCenter)
        self.messageBox.setWordWrap(True)
        self.messageBox.setObjectName(_fromUtf8("messageBox"))
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(270, 630, 461, 23))
        self.progressBar.setAutoFillBackground(False)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.helpButton = QtGui.QPushButton(Dialog)
        self.helpButton.setGeometry(QtCore.QRect(820, 0, 191, 27))
        self.helpButton.setObjectName(_fromUtf8("helpButton"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Image Correlation Spectroscopy", None))
        self.startButton.setText(_translate("Dialog", "START", None))
        self.singleModeButton.setText(_translate("Dialog", "SWITCH TO SINGLE IMAGE MODE", None))
        self.stopButton.setText(_translate("Dialog", "STOP", None))
        self.imageGroup.setTitle(_translate("Dialog", "Current Image", None))
        self.labelRGB.setText(_translate("Dialog", "All Channels", None))
        self.labelRed.setText(_translate("Dialog", "Red", None))
        self.labelGreen.setText(_translate("Dialog", "Green", None))
        self.labelBlue.setText(_translate("Dialog", "Blue", None))
        self.imageParametersGroup.setTitle(_translate("Dialog", "Image Parameters", None))
        self.loadButton.setText(_translate("Dialog", "Load Images Folder", None))
        self.fileCountLabel.setText(_translate("Dialog", "Total File Count:", None))
        self.imageFormatLabel.setText(_translate("Dialog", "Image Format(s):", None))
        self.numRgbLabel.setText(_translate("Dialog", "# of RGBs:", None))
        self.numMonochromeLabel.setText(_translate("Dialog", "# of Monochromes:", None))
        self.folderLabel.setText(_translate("Dialog", "<no directory loaded>", None))
        self.correlationSettingsGroup.setTitle(_translate("Dialog", "Correlation Settings", None))
        self.allTripleParametersGroup.setTitle(_translate("Dialog", "Triple Parameters", None))
        self.tripleRangeLabel.setText(_translate("Dialog", "Range:", None))
        self.tripleG0Label.setText(_translate("Dialog", "g(0):", None))
        self.tripleWLabel.setText(_translate("Dialog", "w:", None))
        self.tripleGinfLabel.setText(_translate("Dialog", "gInf:", None))
        self.tripleG0Label_2.setText(_translate("Dialog", "Sample Resolution:", None))
        self.resolution16.setText(_translate("Dialog", "16 x 16", None))
        self.resolution32.setText(_translate("Dialog", "32 x 32", None))
        self.resolution64.setText(_translate("Dialog", "64 x 64", None))
        self.allAutoCrossGroup.setTitle(_translate("Dialog", "Auto/Cross Parameters", None))
        self.dualRangeLabel.setText(_translate("Dialog", "Range:", None))
        self.dualG0Label.setText(_translate("Dialog", "g(0):", None))
        self.dualWLabel.setText(_translate("Dialog", "w:", None))
        self.dualGinfLabel.setText(_translate("Dialog", "gInf:", None))
        self.considerAutoDeltas.setText(_translate("Dialog", "Consider Autocorrelation Deltas", None))
        self.considerCrossDeltas.setText(_translate("Dialog", "Consider Cross-correlation Deltas", None))
        self.messageBox.setText(_translate("Dialog", "Ready.", None))
        self.helpButton.setText(_translate("Dialog", "Help/About", None))

