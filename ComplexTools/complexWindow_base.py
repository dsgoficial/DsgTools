# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'complexWindow_base.ui'
#
# Created: Wed Nov 19 18:38:15 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(217, 338)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.managePushButton = QtGui.QPushButton(self.dockWidgetContents)
        self.managePushButton.setObjectName(_fromUtf8("managePushButton"))
        self.gridLayout.addWidget(self.managePushButton, 0, 0, 1, 1)
        self.associatePushButton = QtGui.QPushButton(self.dockWidgetContents)
        self.associatePushButton.setObjectName(_fromUtf8("associatePushButton"))
        self.gridLayout.addWidget(self.associatePushButton, 0, 1, 1, 1)
        self.treeView = QtGui.QTreeView(self.dockWidgetContents)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.gridLayout.addWidget(self.treeView, 1, 0, 1, 2)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(QtGui.QApplication.translate("DockWidget", "Complex", None, QtGui.QApplication.UnicodeUTF8))
        self.managePushButton.setText(QtGui.QApplication.translate("DockWidget", "Manage", None, QtGui.QApplication.UnicodeUTF8))
        self.associatePushButton.setText(QtGui.QApplication.translate("DockWidget", "Associate", None, QtGui.QApplication.UnicodeUTF8))

