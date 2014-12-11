# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_postgisDBTool.ui'
#
# Created: Thu Dec 11 10:20:01 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(292, 171)
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
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.serversCombo = QtGui.QComboBox(Dialog)
        self.serversCombo.setObjectName(_fromUtf8("serversCombo"))
        self.horizontalLayout_2.addWidget(self.serversCombo)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)
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
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 2)
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
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 0, 1, 2)
        self.saveButton = QtGui.QPushButton(Dialog)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.gridLayout.addWidget(self.saveButton, 4, 0, 1, 1)
        self.cancelButton = QtGui.QPushButton(Dialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.gridLayout.addWidget(self.cancelButton, 4, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Create Database", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Connection Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Server:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Database:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "SRS:", None, QtGui.QApplication.UnicodeUTF8))
        self.srsButton.setText(QtGui.QApplication.translate("Dialog", "Search SRS", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("Dialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

