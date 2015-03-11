# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_about.ui'
#
# Created: Wed Mar 11 19:39:18 2015
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName(_fromUtf8("AboutDialog"))
        AboutDialog.resize(586, 210)
        self.buttonBox = QtGui.QDialogButtonBox(AboutDialog)
        self.buttonBox.setGeometry(QtCore.QRect(420, 180, 160, 25))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(AboutDialog)
        self.label.setGeometry(QtCore.QRect(430, 10, 151, 161))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/DsgTools/icons/dsg.png")))
        self.label.setScaledContents(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(AboutDialog)
        self.label_2.setGeometry(QtCore.QRect(9, 9, 121, 161))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/DsgTools/icons/eb.jpg")))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.textBrowser = QtGui.QTextBrowser(AboutDialog)
        self.textBrowser.setEnabled(True)
        self.textBrowser.setGeometry(QtCore.QRect(140, 9, 281, 161))
        self.textBrowser.setFrameShape(QtGui.QFrame.NoFrame)
        self.textBrowser.setFrameShadow(QtGui.QFrame.Sunken)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))

        self.retranslateUi(AboutDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AboutDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AboutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About", None))
        self.textBrowser.setHtml(_translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:600;\">Brazilian Army</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:600;\">Geographic Service Bureau</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:600;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:600;\">This plugin was developed in accordance with the Technical Specifications of Brazilian National Spatial Data Infrastructure.</span></p></body></html>", None))

import resources_rc
