# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_postgisDBTool.ui'
#
# Created: Wed Mar 11 16:27:56 2015
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(291, 251)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.connectionEdit = QtGui.QLineEdit(Dialog)
        self.connectionEdit.setReadOnly(True)
        self.connectionEdit.setObjectName(_fromUtf8("connectionEdit"))
        self.horizontalLayout.addWidget(self.connectionEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.serversCombo = QtGui.QComboBox(Dialog)
        self.serversCombo.setObjectName(_fromUtf8("serversCombo"))
        self.horizontalLayout_2.addWidget(self.serversCombo)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.databaseEdit = QtGui.QLineEdit(Dialog)
        self.databaseEdit.setObjectName(_fromUtf8("databaseEdit"))
        self.horizontalLayout_3.addWidget(self.databaseEdit)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.srsButton = QtGui.QPushButton(Dialog)
        self.srsButton.setObjectName(_fromUtf8("srsButton"))
        self.horizontalLayout_4.addWidget(self.srsButton)
        self.srsEdit = QtGui.QLineEdit(Dialog)
        self.srsEdit.setReadOnly(True)
        self.srsEdit.setObjectName(_fromUtf8("srsEdit"))
        self.horizontalLayout_4.addWidget(self.srsEdit)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_7.addWidget(self.label_6)
        self.versionCombo = QtGui.QComboBox(Dialog)
        self.versionCombo.setObjectName(_fromUtf8("versionCombo"))
        self.versionCombo.addItem(_fromUtf8(""))
        self.horizontalLayout_7.addWidget(self.versionCombo)
        self.gridLayout.addLayout(self.horizontalLayout_7, 4, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.saveButton = QtGui.QPushButton(Dialog)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout_5.addWidget(self.saveButton)
        self.cancelButton = QtGui.QPushButton(Dialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout_5.addWidget(self.cancelButton)
        self.gridLayout.addLayout(self.horizontalLayout_5, 5, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Create Database", None))
        self.label.setText(_translate("Dialog", "Connection Name:", None))
        self.label_2.setText(_translate("Dialog", "Server:", None))
        self.label_3.setText(_translate("Dialog", "Database:", None))
        self.label_4.setText(_translate("Dialog", "CRS:", None))
        self.srsButton.setText(_translate("Dialog", "Search CRS", None))
        self.label_6.setText(_translate("Dialog", "EDGV version:", None))
        self.versionCombo.setItemText(0, _translate("Dialog", "2.1.3", None))
        self.saveButton.setText(_translate("Dialog", "Save", None))
        self.cancelButton.setText(_translate("Dialog", "Cancel", None))

