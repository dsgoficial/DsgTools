# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_manageComplex.ui'
#
# Created: Fri Nov 21 14:37:02 2014
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
        Dialog.resize(539, 304)
        self.gridLayout_3 = QtGui.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tableView = QtGui.QTableView(Dialog)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.gridLayout_2.addWidget(self.tableView, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.addRow = QtGui.QPushButton(Dialog)
        self.addRow.setObjectName(_fromUtf8("addRow"))
        self.horizontalLayout_4.addWidget(self.addRow)
        self.removeRow = QtGui.QPushButton(Dialog)
        self.removeRow.setObjectName(_fromUtf8("removeRow"))
        self.horizontalLayout_4.addWidget(self.removeRow)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.updateButton = QtGui.QPushButton(Dialog)
        self.updateButton.setObjectName(_fromUtf8("updateButton"))
        self.horizontalLayout_5.addWidget(self.updateButton)
        self.cancelButton = QtGui.QPushButton(Dialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout_5.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.gridLayout_2.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Manage Complex Features", None, QtGui.QApplication.UnicodeUTF8))
        self.addRow.setText(QtGui.QApplication.translate("Dialog", "Add Complex", None, QtGui.QApplication.UnicodeUTF8))
        self.removeRow.setText(QtGui.QApplication.translate("Dialog", "Remove Complex", None, QtGui.QApplication.UnicodeUTF8))
        self.updateButton.setText(QtGui.QApplication.translate("Dialog", "Update Table", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

