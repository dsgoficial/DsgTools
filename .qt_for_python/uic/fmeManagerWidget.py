# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\camello\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\DsgTools\gui\CustomWidgets\ProcessingParameterWidgets\fmeManagerWidget.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FMEManagerWidget(object):
    def setupUi(self, FMEManagerWidget):
        FMEManagerWidget.setObjectName("FMEManagerWidget")
        FMEManagerWidget.resize(448, 164)
        self.gridLayout = QtWidgets.QGridLayout(FMEManagerWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(FMEManagerWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(FMEManagerWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.versionComboBox = QtWidgets.QComboBox(FMEManagerWidget)
        self.versionComboBox.setObjectName("versionComboBox")
        self.gridLayout.addWidget(self.versionComboBox, 1, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout.addLayout(self.verticalLayout_2, 5, 0, 1, 5)
        self.workspaceComboBox = QtWidgets.QComboBox(FMEManagerWidget)
        self.workspaceComboBox.setObjectName("workspaceComboBox")
        self.gridLayout.addWidget(self.workspaceComboBox, 3, 0, 1, 5)
        self.serverLineEdit = QtWidgets.QLineEdit(FMEManagerWidget)
        self.serverLineEdit.setObjectName("serverLineEdit")
        self.gridLayout.addWidget(self.serverLineEdit, 1, 0, 1, 1)
        self.loadPushButton = QtWidgets.QPushButton(FMEManagerWidget)
        self.loadPushButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.loadPushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/DsgTools/icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loadPushButton.setIcon(icon)
        self.loadPushButton.setObjectName("loadPushButton")
        self.gridLayout.addWidget(self.loadPushButton, 1, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(FMEManagerWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(FMEManagerWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)
        self.sslCheckBox = QtWidgets.QCheckBox(FMEManagerWidget)
        self.sslCheckBox.setChecked(False)
        self.sslCheckBox.setObjectName("sslCheckBox")
        self.gridLayout.addWidget(self.sslCheckBox, 1, 2, 1, 1)
        self.proxyCheckBox = QtWidgets.QCheckBox(FMEManagerWidget)
        self.proxyCheckBox.setObjectName("proxyCheckBox")
        self.gridLayout.addWidget(self.proxyCheckBox, 1, 3, 1, 1)

        self.retranslateUi(FMEManagerWidget)
        QtCore.QMetaObject.connectSlotsByName(FMEManagerWidget)

    def retranslateUi(self, FMEManagerWidget):
        _translate = QtCore.QCoreApplication.translate
        FMEManagerWidget.setWindowTitle(_translate("FMEManagerWidget", "Form"))
        self.label.setText(_translate("FMEManagerWidget", "Server Address"))
        self.label_3.setText(_translate("FMEManagerWidget", "Parameters"))
        self.loadPushButton.setToolTip(_translate("FMEManagerWidget", "Load / Reload"))
        self.label_2.setText(_translate("FMEManagerWidget", "Workspace"))
        self.label_4.setText(_translate("FMEManagerWidget", "Version"))
        self.sslCheckBox.setText(_translate("FMEManagerWidget", "Use SSL"))
        self.proxyCheckBox.setText(_translate("FMEManagerWidget", "Use proxy"))

import resources_rc
