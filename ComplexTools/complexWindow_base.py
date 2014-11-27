# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'complexWindow_base.ui'
#
# Created: Wed Nov 26 18:34:16 2014
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
        DockWidget.resize(280, 468)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.dbCombo = QtGui.QComboBox(self.dockWidgetContents)
        self.dbCombo.setObjectName(_fromUtf8("dbCombo"))
        self.horizontalLayout.addWidget(self.dbCombo)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.complexCombo = QtGui.QComboBox(self.dockWidgetContents)
        self.complexCombo.setObjectName(_fromUtf8("complexCombo"))
        self.horizontalLayout_2.addWidget(self.complexCombo)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.dbButton = QtGui.QPushButton(self.dockWidgetContents)
        self.dbButton.setObjectName(_fromUtf8("dbButton"))
        self.horizontalLayout_3.addWidget(self.dbButton)
        self.managePushButton = QtGui.QPushButton(self.dockWidgetContents)
        self.managePushButton.setObjectName(_fromUtf8("managePushButton"))
        self.horizontalLayout_3.addWidget(self.managePushButton)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.associatePushButton = QtGui.QPushButton(self.dockWidgetContents)
        self.associatePushButton.setObjectName(_fromUtf8("associatePushButton"))
        self.horizontalLayout_4.addWidget(self.associatePushButton)
        self.disassociatePushButton = QtGui.QPushButton(self.dockWidgetContents)
        self.disassociatePushButton.setObjectName(_fromUtf8("disassociatePushButton"))
        self.horizontalLayout_4.addWidget(self.disassociatePushButton)
        self.zoomButton = QtGui.QPushButton(self.dockWidgetContents)
        self.zoomButton.setObjectName(_fromUtf8("zoomButton"))
        self.horizontalLayout_4.addWidget(self.zoomButton)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)
        self.treeWidget = QtGui.QTreeWidget(self.dockWidgetContents)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.gridLayout.addWidget(self.treeWidget, 4, 0, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(QtGui.QApplication.translate("DockWidget", "Complex", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DockWidget", "Database:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DockWidget", "Complex Class:", None, QtGui.QApplication.UnicodeUTF8))
        self.dbButton.setText(QtGui.QApplication.translate("DockWidget", "Load DB\'s", None, QtGui.QApplication.UnicodeUTF8))
        self.managePushButton.setText(QtGui.QApplication.translate("DockWidget", "Manage", None, QtGui.QApplication.UnicodeUTF8))
        self.associatePushButton.setText(QtGui.QApplication.translate("DockWidget", "Associate", None, QtGui.QApplication.UnicodeUTF8))
        self.disassociatePushButton.setText(QtGui.QApplication.translate("DockWidget", "Disassociate", None, QtGui.QApplication.UnicodeUTF8))
        self.zoomButton.setText(QtGui.QApplication.translate("DockWidget", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(0, QtGui.QApplication.translate("DockWidget", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(1, QtGui.QApplication.translate("DockWidget", "Value", None, QtGui.QApplication.UnicodeUTF8))

