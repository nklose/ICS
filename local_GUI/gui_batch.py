# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'batchv2.ui'
#
# Created: Wed Mar 27 11:23:01 2013
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
        self.imageGroup.setGeometry(QtCore.QRect(10, 10, 1001, 251))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.imageGroup.setFont(font)
        self.imageGroup.setFlat(False)
        self.imageGroup.setCheckable(False)
        self.imageGroup.setObjectName(_fromUtf8("imageGroup"))
        self.imageRGB = QtGui.QGraphicsView(self.imageGroup)
        self.imageRGB.setGeometry(QtCore.QRect(30, 30, 192, 192))
        self.imageRGB.setObjectName(_fromUtf8("imageRGB"))
        self.imageRed = QtGui.QGraphicsView(self.imageGroup)
        self.imageRed.setGeometry(QtCore.QRect(280, 30, 192, 192))
        self.imageRed.setObjectName(_fromUtf8("imageRed"))
        self.imageGreen = QtGui.QGraphicsView(self.imageGroup)
        self.imageGreen.setGeometry(QtCore.QRect(530, 30, 192, 192))
        self.imageGreen.setObjectName(_fromUtf8("imageGreen"))
        self.imageBlue = QtGui.QGraphicsView(self.imageGroup)
        self.imageBlue.setGeometry(QtCore.QRect(780, 30, 192, 192))
        self.imageBlue.setObjectName(_fromUtf8("imageBlue"))
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
        self.imageSettingsGroup = QtGui.QGroupBox(Dialog)
        self.imageSettingsGroup.setGeometry(QtCore.QRect(10, 270, 311, 341))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.imageSettingsGroup.setFont(font)
        self.imageSettingsGroup.setObjectName(_fromUtf8("imageSettingsGroup"))
        self.loadButton = QtGui.QPushButton(self.imageSettingsGroup)
        self.loadButton.setGeometry(QtCore.QRect(30, 50, 261, 41))
        self.loadButton.setObjectName(_fromUtf8("loadButton"))
        self.fileCountLabel = QtGui.QLabel(self.imageSettingsGroup)
        self.fileCountLabel.setGeometry(QtCore.QRect(10, 140, 141, 21))
        self.fileCountLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fileCountLabel.setObjectName(_fromUtf8("fileCountLabel"))
        self.imageFormatLabel = QtGui.QLabel(self.imageSettingsGroup)
        self.imageFormatLabel.setGeometry(QtCore.QRect(10, 230, 141, 21))
        self.imageFormatLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.imageFormatLabel.setObjectName(_fromUtf8("imageFormatLabel"))
        self.fileCount = QtGui.QLabel(self.imageSettingsGroup)
        self.fileCount.setGeometry(QtCore.QRect(160, 140, 131, 21))
        self.fileCount.setFrameShape(QtGui.QFrame.Box)
        self.fileCount.setFrameShadow(QtGui.QFrame.Sunken)
        self.fileCount.setObjectName(_fromUtf8("fileCount"))
        self.formatsList = QtGui.QLabel(self.imageSettingsGroup)
        self.formatsList.setGeometry(QtCore.QRect(160, 230, 131, 21))
        self.formatsList.setFrameShape(QtGui.QFrame.Box)
        self.formatsList.setFrameShadow(QtGui.QFrame.Sunken)
        self.formatsList.setObjectName(_fromUtf8("formatsList"))
        self.rgbCount = QtGui.QLabel(self.imageSettingsGroup)
        self.rgbCount.setGeometry(QtCore.QRect(160, 170, 131, 21))
        self.rgbCount.setFrameShape(QtGui.QFrame.Box)
        self.rgbCount.setFrameShadow(QtGui.QFrame.Sunken)
        self.rgbCount.setObjectName(_fromUtf8("rgbCount"))
        self.numRgbLabel = QtGui.QLabel(self.imageSettingsGroup)
        self.numRgbLabel.setGeometry(QtCore.QRect(10, 170, 141, 21))
        self.numRgbLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.numRgbLabel.setObjectName(_fromUtf8("numRgbLabel"))
        self.numMonochromeLabel = QtGui.QLabel(self.imageSettingsGroup)
        self.numMonochromeLabel.setGeometry(QtCore.QRect(10, 200, 141, 21))
        self.numMonochromeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.numMonochromeLabel.setObjectName(_fromUtf8("numMonochromeLabel"))
        self.monoCount = QtGui.QLabel(self.imageSettingsGroup)
        self.monoCount.setGeometry(QtCore.QRect(160, 200, 131, 21))
        self.monoCount.setFrameShape(QtGui.QFrame.Box)
        self.monoCount.setFrameShadow(QtGui.QFrame.Sunken)
        self.monoCount.setObjectName(_fromUtf8("monoCount"))
        self.folderLabel = QtGui.QLabel(self.imageSettingsGroup)
        self.folderLabel.setGeometry(QtCore.QRect(50, 100, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.folderLabel.setFont(font)
        self.folderLabel.setFrameShape(QtGui.QFrame.Box)
        self.folderLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.folderLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.folderLabel.setObjectName(_fromUtf8("folderLabel"))
        self.correlationSettingsGroup = QtGui.QGroupBox(Dialog)
        self.correlationSettingsGroup.setGeometry(QtCore.QRect(340, 270, 671, 221))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.correlationSettingsGroup.setFont(font)
        self.correlationSettingsGroup.setObjectName(_fromUtf8("correlationSettingsGroup"))
        self.correlationTabWidget = QtGui.QTabWidget(self.correlationSettingsGroup)
        self.correlationTabWidget.setGeometry(QtCore.QRect(10, 30, 651, 181))
        self.correlationTabWidget.setObjectName(_fromUtf8("correlationTabWidget"))
        self.autoCorrelationTab = QtGui.QWidget()
        self.autoCorrelationTab.setObjectName(_fromUtf8("autoCorrelationTab"))
        self.autoChannelsGroup = QtGui.QGroupBox(self.autoCorrelationTab)
        self.autoChannelsGroup.setGeometry(QtCore.QRect(10, 10, 121, 131))
        self.autoChannelsGroup.setObjectName(_fromUtf8("autoChannelsGroup"))
        self.redCheckbox = QtGui.QCheckBox(self.autoChannelsGroup)
        self.redCheckbox.setGeometry(QtCore.QRect(10, 30, 70, 17))
        self.redCheckbox.setChecked(True)
        self.redCheckbox.setObjectName(_fromUtf8("redCheckbox"))
        self.greenCheckbox = QtGui.QCheckBox(self.autoChannelsGroup)
        self.greenCheckbox.setGeometry(QtCore.QRect(10, 60, 70, 17))
        self.greenCheckbox.setChecked(True)
        self.greenCheckbox.setObjectName(_fromUtf8("greenCheckbox"))
        self.blueCheckbox = QtGui.QCheckBox(self.autoChannelsGroup)
        self.blueCheckbox.setGeometry(QtCore.QRect(10, 90, 70, 17))
        self.blueCheckbox.setChecked(True)
        self.blueCheckbox.setObjectName(_fromUtf8("blueCheckbox"))
        self.autoGroup = QtGui.QGroupBox(self.autoCorrelationTab)
        self.autoGroup.setGeometry(QtCore.QRect(140, 10, 341, 131))
        self.autoGroup.setFlat(False)
        self.autoGroup.setCheckable(False)
        self.autoGroup.setObjectName(_fromUtf8("autoGroup"))
        self.autoRangeLabel = QtGui.QLabel(self.autoGroup)
        self.autoRangeLabel.setGeometry(QtCore.QRect(10, 30, 61, 31))
        self.autoRangeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.autoRangeLabel.setObjectName(_fromUtf8("autoRangeLabel"))
        self.autoG0Label = QtGui.QLabel(self.autoGroup)
        self.autoG0Label.setGeometry(QtCore.QRect(10, 70, 61, 31))
        self.autoG0Label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.autoG0Label.setObjectName(_fromUtf8("autoG0Label"))
        self.autoWLabel = QtGui.QLabel(self.autoGroup)
        self.autoWLabel.setGeometry(QtCore.QRect(200, 30, 21, 31))
        self.autoWLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.autoWLabel.setObjectName(_fromUtf8("autoWLabel"))
        self.autoGinfLabel = QtGui.QLabel(self.autoGroup)
        self.autoGinfLabel.setGeometry(QtCore.QRect(180, 70, 41, 31))
        self.autoGinfLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.autoGinfLabel.setObjectName(_fromUtf8("autoGinfLabel"))
        self.autoRangeTextbox = QtGui.QLineEdit(self.autoGroup)
        self.autoRangeTextbox.setGeometry(QtCore.QRect(80, 30, 91, 31))
        self.autoRangeTextbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.autoRangeTextbox.setObjectName(_fromUtf8("autoRangeTextbox"))
        self.autoG0Textbox = QtGui.QLineEdit(self.autoGroup)
        self.autoG0Textbox.setGeometry(QtCore.QRect(80, 70, 91, 31))
        self.autoG0Textbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.autoG0Textbox.setObjectName(_fromUtf8("autoG0Textbox"))
        self.autoWTextbox = QtGui.QLineEdit(self.autoGroup)
        self.autoWTextbox.setGeometry(QtCore.QRect(230, 30, 91, 31))
        self.autoWTextbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.autoWTextbox.setObjectName(_fromUtf8("autoWTextbox"))
        self.autoGinfTextbox = QtGui.QLineEdit(self.autoGroup)
        self.autoGinfTextbox.setGeometry(QtCore.QRect(230, 70, 91, 31))
        self.autoGinfTextbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.autoGinfTextbox.setObjectName(_fromUtf8("autoGinfTextbox"))
        self.autoDeltasCheckbox = QtGui.QCheckBox(self.autoGroup)
        self.autoDeltasCheckbox.setGeometry(QtCore.QRect(150, 110, 171, 17))
        self.autoDeltasCheckbox.setObjectName(_fromUtf8("autoDeltasCheckbox"))
        self.correlationTabWidget.addTab(self.autoCorrelationTab, _fromUtf8(""))
        self.crossCorrelationTab = QtGui.QWidget()
        self.crossCorrelationTab.setObjectName(_fromUtf8("crossCorrelationTab"))
        self.crossGroup = QtGui.QGroupBox(self.crossCorrelationTab)
        self.crossGroup.setGeometry(QtCore.QRect(140, 10, 341, 131))
        self.crossGroup.setFlat(False)
        self.crossGroup.setCheckable(False)
        self.crossGroup.setObjectName(_fromUtf8("crossGroup"))
        self.crossRangeLabel = QtGui.QLabel(self.crossGroup)
        self.crossRangeLabel.setGeometry(QtCore.QRect(10, 30, 61, 31))
        self.crossRangeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.crossRangeLabel.setObjectName(_fromUtf8("crossRangeLabel"))
        self.crossG0Label = QtGui.QLabel(self.crossGroup)
        self.crossG0Label.setGeometry(QtCore.QRect(-20, 70, 91, 31))
        self.crossG0Label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.crossG0Label.setObjectName(_fromUtf8("crossG0Label"))
        self.crossWLabel = QtGui.QLabel(self.crossGroup)
        self.crossWLabel.setGeometry(QtCore.QRect(190, 30, 31, 31))
        self.crossWLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.crossWLabel.setObjectName(_fromUtf8("crossWLabel"))
        self.crossGinfLabel = QtGui.QLabel(self.crossGroup)
        self.crossGinfLabel.setGeometry(QtCore.QRect(180, 70, 41, 31))
        self.crossGinfLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.crossGinfLabel.setObjectName(_fromUtf8("crossGinfLabel"))
        self.crossRangeTextbox = QtGui.QLineEdit(self.crossGroup)
        self.crossRangeTextbox.setGeometry(QtCore.QRect(80, 30, 91, 31))
        self.crossRangeTextbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.crossRangeTextbox.setObjectName(_fromUtf8("crossRangeTextbox"))
        self.crossG0Textbox = QtGui.QLineEdit(self.crossGroup)
        self.crossG0Textbox.setGeometry(QtCore.QRect(80, 70, 91, 31))
        self.crossG0Textbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.crossG0Textbox.setObjectName(_fromUtf8("crossG0Textbox"))
        self.crossWTextbox = QtGui.QLineEdit(self.crossGroup)
        self.crossWTextbox.setGeometry(QtCore.QRect(230, 30, 91, 31))
        self.crossWTextbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.crossWTextbox.setObjectName(_fromUtf8("crossWTextbox"))
        self.crossGinfTextbox = QtGui.QLineEdit(self.crossGroup)
        self.crossGinfTextbox.setGeometry(QtCore.QRect(230, 70, 91, 31))
        self.crossGinfTextbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.crossGinfTextbox.setObjectName(_fromUtf8("crossGinfTextbox"))
        self.crossChannelsGroup = QtGui.QGroupBox(self.crossCorrelationTab)
        self.crossChannelsGroup.setGeometry(QtCore.QRect(10, 10, 121, 131))
        self.crossChannelsGroup.setObjectName(_fromUtf8("crossChannelsGroup"))
        self.redGreenCheckbox = QtGui.QCheckBox(self.crossChannelsGroup)
        self.redGreenCheckbox.setGeometry(QtCore.QRect(10, 30, 111, 17))
        self.redGreenCheckbox.setChecked(True)
        self.redGreenCheckbox.setObjectName(_fromUtf8("redGreenCheckbox"))
        self.redBlueCheckbox = QtGui.QCheckBox(self.crossChannelsGroup)
        self.redBlueCheckbox.setGeometry(QtCore.QRect(10, 60, 91, 17))
        self.redBlueCheckbox.setChecked(True)
        self.redBlueCheckbox.setObjectName(_fromUtf8("redBlueCheckbox"))
        self.greenBlueCheckbox = QtGui.QCheckBox(self.crossChannelsGroup)
        self.greenBlueCheckbox.setGeometry(QtCore.QRect(10, 90, 111, 17))
        self.greenBlueCheckbox.setChecked(True)
        self.greenBlueCheckbox.setObjectName(_fromUtf8("greenBlueCheckbox"))
        self.crossDeltasCheckbox = QtGui.QCheckBox(self.crossCorrelationTab)
        self.crossDeltasCheckbox.setGeometry(QtCore.QRect(290, 120, 171, 17))
        self.crossDeltasCheckbox.setObjectName(_fromUtf8("crossDeltasCheckbox"))
        self.correlationTabWidget.addTab(self.crossCorrelationTab, _fromUtf8(""))
        self.tripleCorrelationTab = QtGui.QWidget()
        self.tripleCorrelationTab.setObjectName(_fromUtf8("tripleCorrelationTab"))
        self.tripleParametersGroup = QtGui.QGroupBox(self.tripleCorrelationTab)
        self.tripleParametersGroup.setGeometry(QtCore.QRect(140, 10, 311, 131))
        self.tripleParametersGroup.setFlat(False)
        self.tripleParametersGroup.setCheckable(False)
        self.tripleParametersGroup.setObjectName(_fromUtf8("tripleParametersGroup"))
        self.tripleRangeLabel = QtGui.QLabel(self.tripleParametersGroup)
        self.tripleRangeLabel.setGeometry(QtCore.QRect(10, 30, 51, 31))
        self.tripleRangeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tripleRangeLabel.setObjectName(_fromUtf8("tripleRangeLabel"))
        self.tripleG0Label = QtGui.QLabel(self.tripleParametersGroup)
        self.tripleG0Label.setGeometry(QtCore.QRect(10, 70, 51, 31))
        self.tripleG0Label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tripleG0Label.setObjectName(_fromUtf8("tripleG0Label"))
        self.tripleWLabel = QtGui.QLabel(self.tripleParametersGroup)
        self.tripleWLabel.setGeometry(QtCore.QRect(180, 30, 21, 31))
        self.tripleWLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tripleWLabel.setObjectName(_fromUtf8("tripleWLabel"))
        self.tripleGinfLabel = QtGui.QLabel(self.tripleParametersGroup)
        self.tripleGinfLabel.setGeometry(QtCore.QRect(150, 70, 51, 31))
        self.tripleGinfLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tripleGinfLabel.setObjectName(_fromUtf8("tripleGinfLabel"))
        self.tripleRangeTextbox = QtGui.QLineEdit(self.tripleParametersGroup)
        self.tripleRangeTextbox.setGeometry(QtCore.QRect(70, 30, 91, 31))
        self.tripleRangeTextbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.tripleRangeTextbox.setObjectName(_fromUtf8("tripleRangeTextbox"))
        self.tripleG0Textbox = QtGui.QLineEdit(self.tripleParametersGroup)
        self.tripleG0Textbox.setGeometry(QtCore.QRect(70, 70, 91, 31))
        self.tripleG0Textbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.tripleG0Textbox.setObjectName(_fromUtf8("tripleG0Textbox"))
        self.tripleWTextbox = QtGui.QLineEdit(self.tripleParametersGroup)
        self.tripleWTextbox.setGeometry(QtCore.QRect(210, 30, 91, 31))
        self.tripleWTextbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.tripleWTextbox.setObjectName(_fromUtf8("tripleWTextbox"))
        self.tripleGinfTextbox = QtGui.QLineEdit(self.tripleParametersGroup)
        self.tripleGinfTextbox.setGeometry(QtCore.QRect(210, 70, 91, 31))
        self.tripleGinfTextbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.tripleGinfTextbox.setObjectName(_fromUtf8("tripleGinfTextbox"))
        self.frame = QtGui.QFrame(self.tripleCorrelationTab)
        self.frame.setGeometry(QtCore.QRect(470, 10, 161, 131))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.sampleResolutionLabel = QtGui.QLabel(self.frame)
        self.sampleResolutionLabel.setGeometry(QtCore.QRect(10, 10, 141, 21))
        self.sampleResolutionLabel.setWordWrap(True)
        self.sampleResolutionLabel.setObjectName(_fromUtf8("sampleResolutionLabel"))
        self.resolution16 = QtGui.QRadioButton(self.frame)
        self.resolution16.setGeometry(QtCore.QRect(30, 50, 82, 17))
        self.resolution16.setChecked(False)
        self.resolution16.setObjectName(_fromUtf8("resolution16"))
        self.resolution32 = QtGui.QRadioButton(self.frame)
        self.resolution32.setGeometry(QtCore.QRect(30, 70, 82, 17))
        self.resolution32.setChecked(True)
        self.resolution32.setObjectName(_fromUtf8("resolution32"))
        self.resolution64 = QtGui.QRadioButton(self.frame)
        self.resolution64.setGeometry(QtCore.QRect(30, 90, 82, 17))
        self.resolution64.setObjectName(_fromUtf8("resolution64"))
        self.correlationTabWidget.addTab(self.tripleCorrelationTab, _fromUtf8(""))
        self.allCorrelationsTab = QtGui.QWidget()
        self.allCorrelationsTab.setObjectName(_fromUtf8("allCorrelationsTab"))
        self.allAutoCrossGroup = QtGui.QGroupBox(self.allCorrelationsTab)
        self.allAutoCrossGroup.setGeometry(QtCore.QRect(10, 10, 311, 131))
        self.allAutoCrossGroup.setFlat(False)
        self.allAutoCrossGroup.setCheckable(False)
        self.allAutoCrossGroup.setObjectName(_fromUtf8("allAutoCrossGroup"))
        self.allAutoCrossRangeLabel = QtGui.QLabel(self.allAutoCrossGroup)
        self.allAutoCrossRangeLabel.setGeometry(QtCore.QRect(10, 30, 51, 31))
        self.allAutoCrossRangeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.allAutoCrossRangeLabel.setObjectName(_fromUtf8("allAutoCrossRangeLabel"))
        self.allAutoCrossG0Label = QtGui.QLabel(self.allAutoCrossGroup)
        self.allAutoCrossG0Label.setGeometry(QtCore.QRect(10, 70, 51, 31))
        self.allAutoCrossG0Label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.allAutoCrossG0Label.setObjectName(_fromUtf8("allAutoCrossG0Label"))
        self.allAutoCrossWLabel = QtGui.QLabel(self.allAutoCrossGroup)
        self.allAutoCrossWLabel.setGeometry(QtCore.QRect(180, 30, 21, 31))
        self.allAutoCrossWLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.allAutoCrossWLabel.setObjectName(_fromUtf8("allAutoCrossWLabel"))
        self.allAutoCrossGinfLabel = QtGui.QLabel(self.allAutoCrossGroup)
        self.allAutoCrossGinfLabel.setGeometry(QtCore.QRect(150, 70, 51, 31))
        self.allAutoCrossGinfLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.allAutoCrossGinfLabel.setObjectName(_fromUtf8("allAutoCrossGinfLabel"))
        self.allAutoCrossRangeTextbox = QtGui.QLineEdit(self.allAutoCrossGroup)
        self.allAutoCrossRangeTextbox.setGeometry(QtCore.QRect(70, 30, 91, 31))
        self.allAutoCrossRangeTextbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.allAutoCrossRangeTextbox.setObjectName(_fromUtf8("allAutoCrossRangeTextbox"))
        self.allAutoCrossG0Textbox = QtGui.QLineEdit(self.allAutoCrossGroup)
        self.allAutoCrossG0Textbox.setGeometry(QtCore.QRect(70, 70, 91, 31))
        self.allAutoCrossG0Textbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.allAutoCrossG0Textbox.setObjectName(_fromUtf8("allAutoCrossG0Textbox"))
        self.allAutoCrossWTextbox = QtGui.QLineEdit(self.allAutoCrossGroup)
        self.allAutoCrossWTextbox.setGeometry(QtCore.QRect(210, 30, 91, 31))
        self.allAutoCrossWTextbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.allAutoCrossWTextbox.setObjectName(_fromUtf8("allAutoCrossWTextbox"))
        self.allAutoCrossGinfTextbox = QtGui.QLineEdit(self.allAutoCrossGroup)
        self.allAutoCrossGinfTextbox.setGeometry(QtCore.QRect(210, 70, 91, 31))
        self.allAutoCrossGinfTextbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.allAutoCrossGinfTextbox.setObjectName(_fromUtf8("allAutoCrossGinfTextbox"))
        self.allDeltasCheckbox = QtGui.QCheckBox(self.allAutoCrossGroup)
        self.allDeltasCheckbox.setGeometry(QtCore.QRect(150, 110, 171, 17))
        self.allDeltasCheckbox.setObjectName(_fromUtf8("allDeltasCheckbox"))
        self.allTripleParametersGroup = QtGui.QGroupBox(self.allCorrelationsTab)
        self.allTripleParametersGroup.setGeometry(QtCore.QRect(320, 10, 311, 131))
        self.allTripleParametersGroup.setFlat(False)
        self.allTripleParametersGroup.setCheckable(False)
        self.allTripleParametersGroup.setObjectName(_fromUtf8("allTripleParametersGroup"))
        self.allTripleRangeLabel = QtGui.QLabel(self.allTripleParametersGroup)
        self.allTripleRangeLabel.setGeometry(QtCore.QRect(10, 30, 51, 31))
        self.allTripleRangeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.allTripleRangeLabel.setObjectName(_fromUtf8("allTripleRangeLabel"))
        self.allTripleG0Label = QtGui.QLabel(self.allTripleParametersGroup)
        self.allTripleG0Label.setGeometry(QtCore.QRect(10, 70, 51, 31))
        self.allTripleG0Label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.allTripleG0Label.setObjectName(_fromUtf8("allTripleG0Label"))
        self.allTripleWLabel = QtGui.QLabel(self.allTripleParametersGroup)
        self.allTripleWLabel.setGeometry(QtCore.QRect(180, 30, 21, 31))
        self.allTripleWLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.allTripleWLabel.setObjectName(_fromUtf8("allTripleWLabel"))
        self.allTripleGinfLabel = QtGui.QLabel(self.allTripleParametersGroup)
        self.allTripleGinfLabel.setGeometry(QtCore.QRect(150, 70, 51, 31))
        self.allTripleGinfLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.allTripleGinfLabel.setObjectName(_fromUtf8("allTripleGinfLabel"))
        self.allTripleRangeTextbox = QtGui.QLineEdit(self.allTripleParametersGroup)
        self.allTripleRangeTextbox.setGeometry(QtCore.QRect(70, 30, 91, 31))
        self.allTripleRangeTextbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.allTripleRangeTextbox.setObjectName(_fromUtf8("allTripleRangeTextbox"))
        self.allTripleG0Textbox = QtGui.QLineEdit(self.allTripleParametersGroup)
        self.allTripleG0Textbox.setGeometry(QtCore.QRect(70, 70, 91, 31))
        self.allTripleG0Textbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.allTripleG0Textbox.setObjectName(_fromUtf8("allTripleG0Textbox"))
        self.allTripleWTextbox = QtGui.QLineEdit(self.allTripleParametersGroup)
        self.allTripleWTextbox.setGeometry(QtCore.QRect(210, 30, 91, 31))
        self.allTripleWTextbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.allTripleWTextbox.setObjectName(_fromUtf8("allTripleWTextbox"))
        self.allTripleGinfTextbox = QtGui.QLineEdit(self.allTripleParametersGroup)
        self.allTripleGinfTextbox.setGeometry(QtCore.QRect(210, 70, 91, 31))
        self.allTripleGinfTextbox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.allTripleGinfTextbox.setObjectName(_fromUtf8("allTripleGinfTextbox"))
        self.correlationTabWidget.addTab(self.allCorrelationsTab, _fromUtf8(""))
        self.messageBox = QtGui.QLabel(Dialog)
        self.messageBox.setGeometry(QtCore.QRect(340, 500, 671, 81))
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

        self.retranslateUi(Dialog)
        self.correlationTabWidget.setCurrentIndex(0)
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
        self.imageSettingsGroup.setTitle(_translate("Dialog", "Image Settings", None))
        self.loadButton.setText(_translate("Dialog", "Load Images Folder", None))
        self.fileCountLabel.setText(_translate("Dialog", "Total File Count:", None))
        self.imageFormatLabel.setText(_translate("Dialog", "Image Format(s):", None))
        self.fileCount.setText(_translate("Dialog", "100", None))
        self.formatsList.setText(_translate("Dialog", "JPG, TIF, BMP", None))
        self.rgbCount.setText(_translate("Dialog", "100", None))
        self.numRgbLabel.setText(_translate("Dialog", "# of RGBs:", None))
        self.numMonochromeLabel.setText(_translate("Dialog", "# of Monochromes:", None))
        self.monoCount.setText(_translate("Dialog", "100", None))
        self.folderLabel.setText(_translate("Dialog", "<no file>", None))
        self.correlationSettingsGroup.setTitle(_translate("Dialog", "Correlation Settings", None))
        self.autoChannelsGroup.setTitle(_translate("Dialog", "Channels", None))
        self.redCheckbox.setText(_translate("Dialog", "Red", None))
        self.greenCheckbox.setText(_translate("Dialog", "Green", None))
        self.blueCheckbox.setText(_translate("Dialog", "Blue", None))
        self.autoGroup.setTitle(_translate("Dialog", "Auto-Correlation Parameters", None))
        self.autoRangeLabel.setText(_translate("Dialog", "Range:", None))
        self.autoG0Label.setText(_translate("Dialog", "g(0):", None))
        self.autoWLabel.setText(_translate("Dialog", "w:", None))
        self.autoGinfLabel.setText(_translate("Dialog", "gInf:", None))
        self.autoDeltasCheckbox.setText(_translate("Dialog", "Consider Deltas", None))
        self.correlationTabWidget.setTabText(self.correlationTabWidget.indexOf(self.autoCorrelationTab), _translate("Dialog", "Auto-Correlation", None))
        self.crossGroup.setTitle(_translate("Dialog", "Cross-Correlation Parameters", None))
        self.crossRangeLabel.setText(_translate("Dialog", "Range:", None))
        self.crossG0Label.setText(_translate("Dialog", "g(0):", None))
        self.crossWLabel.setText(_translate("Dialog", "w:", None))
        self.crossGinfLabel.setText(_translate("Dialog", "gInf:", None))
        self.crossChannelsGroup.setTitle(_translate("Dialog", "Channels", None))
        self.redGreenCheckbox.setText(_translate("Dialog", "Red-Green", None))
        self.redBlueCheckbox.setText(_translate("Dialog", "Red-Blue", None))
        self.greenBlueCheckbox.setText(_translate("Dialog", "Green-Blue", None))
        self.crossDeltasCheckbox.setText(_translate("Dialog", "Consider Deltas", None))
        self.correlationTabWidget.setTabText(self.correlationTabWidget.indexOf(self.crossCorrelationTab), _translate("Dialog", "Cross-Correlation", None))
        self.tripleParametersGroup.setTitle(_translate("Dialog", "Triple Parameters", None))
        self.tripleRangeLabel.setText(_translate("Dialog", "Range:", None))
        self.tripleG0Label.setText(_translate("Dialog", "g(0):", None))
        self.tripleWLabel.setText(_translate("Dialog", "w:", None))
        self.tripleGinfLabel.setText(_translate("Dialog", "gInf:", None))
        self.sampleResolutionLabel.setText(_translate("Dialog", "Sample Resolution:", None))
        self.resolution16.setText(_translate("Dialog", "16 x 16", None))
        self.resolution32.setText(_translate("Dialog", "32 x 32", None))
        self.resolution64.setText(_translate("Dialog", "64 x 64", None))
        self.correlationTabWidget.setTabText(self.correlationTabWidget.indexOf(self.tripleCorrelationTab), _translate("Dialog", "Triple-Correlation", None))
        self.allAutoCrossGroup.setTitle(_translate("Dialog", "Auto/Cross Parameters", None))
        self.allAutoCrossRangeLabel.setText(_translate("Dialog", "Range:", None))
        self.allAutoCrossG0Label.setText(_translate("Dialog", "g(0):", None))
        self.allAutoCrossWLabel.setText(_translate("Dialog", "w:", None))
        self.allAutoCrossGinfLabel.setText(_translate("Dialog", "gInf:", None))
        self.allDeltasCheckbox.setText(_translate("Dialog", "Consider Deltas", None))
        self.allTripleParametersGroup.setTitle(_translate("Dialog", "Triple Parameters", None))
        self.allTripleRangeLabel.setText(_translate("Dialog", "Range:", None))
        self.allTripleG0Label.setText(_translate("Dialog", "g(0):", None))
        self.allTripleWLabel.setText(_translate("Dialog", "w:", None))
        self.allTripleGinfLabel.setText(_translate("Dialog", "gInf:", None))
        self.correlationTabWidget.setTabText(self.correlationTabWidget.indexOf(self.allCorrelationsTab), _translate("Dialog", "All", None))
        self.messageBox.setText(_translate("Dialog", "Ready.", None))

