# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_associateWithComplex.ui'
#
# Created: Fri Nov 21 14:36:43 2014
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
        Dialog.resize(602, 473)
        self.gridLayout_4 = QtGui.QGridLayout(Dialog)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tableView = QtGui.QTableView(Dialog)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.gridLayout_2.addWidget(self.tableView, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.selectedFeaturesTreeWidget = QtGui.QTreeWidget(Dialog)
        self.selectedFeaturesTreeWidget.setObjectName(_fromUtf8("selectedFeaturesTreeWidget"))
        self.selectedFeaturesTreeWidget.header().setVisible(True)
        self.horizontalLayout_3.addWidget(self.selectedFeaturesTreeWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.selectAllButton = QtGui.QPushButton(Dialog)
        self.selectAllButton.setObjectName(_fromUtf8("selectAllButton"))
        self.verticalLayout.addWidget(self.selectAllButton)
        self.selectOneButton = QtGui.QPushButton(Dialog)
        self.selectOneButton.setObjectName(_fromUtf8("selectOneButton"))
        self.verticalLayout.addWidget(self.selectOneButton)
        self.deselectOneButton = QtGui.QPushButton(Dialog)
        self.deselectOneButton.setObjectName(_fromUtf8("deselectOneButton"))
        self.verticalLayout.addWidget(self.deselectOneButton)
        self.deselectAllButton = QtGui.QPushButton(Dialog)
        self.deselectAllButton.setObjectName(_fromUtf8("deselectAllButton"))
        self.verticalLayout.addWidget(self.deselectAllButton)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.componentFeaturesTreeWidget = QtGui.QTreeWidget(Dialog)
        self.componentFeaturesTreeWidget.setObjectName(_fromUtf8("componentFeaturesTreeWidget"))
        self.horizontalLayout_3.addWidget(self.componentFeaturesTreeWidget)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.associateButton = QtGui.QPushButton(Dialog)
        self.associateButton.setObjectName(_fromUtf8("associateButton"))
        self.horizontalLayout_5.addWidget(self.associateButton)
        self.cancelButton = QtGui.QPushButton(Dialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout_5.addWidget(self.cancelButton)
        self.gridLayout_4.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Associate Selected Features with Complex", None, QtGui.QApplication.UnicodeUTF8))
        self.selectedFeaturesTreeWidget.headerItem().setText(0, QtGui.QApplication.translate("Dialog", "Selected Features", None, QtGui.QApplication.UnicodeUTF8))
        self.selectAllButton.setText(QtGui.QApplication.translate("Dialog", ">>", None, QtGui.QApplication.UnicodeUTF8))
        self.selectOneButton.setText(QtGui.QApplication.translate("Dialog", ">", None, QtGui.QApplication.UnicodeUTF8))
        self.deselectOneButton.setText(QtGui.QApplication.translate("Dialog", "<", None, QtGui.QApplication.UnicodeUTF8))
        self.deselectAllButton.setText(QtGui.QApplication.translate("Dialog", "<<", None, QtGui.QApplication.UnicodeUTF8))
        self.componentFeaturesTreeWidget.headerItem().setText(0, QtGui.QApplication.translate("Dialog", "Component Features", None, QtGui.QApplication.UnicodeUTF8))
        self.associateButton.setText(QtGui.QApplication.translate("Dialog", "Associate", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

