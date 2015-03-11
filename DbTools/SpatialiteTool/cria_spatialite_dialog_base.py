# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cria_spatialite_dialog_base.ui'
#
# Created: Wed Mar 11 16:28:38 2015
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

class Ui_CriaSpatialite(object):
    def setupUi(self, CriaSpatialite):
        CriaSpatialite.setObjectName(_fromUtf8("CriaSpatialite"))
        CriaSpatialite.resize(391, 189)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CriaSpatialite.sizePolicy().hasHeightForWidth())
        CriaSpatialite.setSizePolicy(sizePolicy)
        CriaSpatialite.setMinimumSize(QtCore.QSize(0, 0))
        CriaSpatialite.setMaximumSize(QtCore.QSize(1000, 1000))
        self.gridLayout = QtGui.QGridLayout(CriaSpatialite)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(CriaSpatialite)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.pastaDestinoCriaSpatialiteLineEdit = QtGui.QLineEdit(CriaSpatialite)
        self.pastaDestinoCriaSpatialiteLineEdit.setObjectName(_fromUtf8("pastaDestinoCriaSpatialiteLineEdit"))
        self.horizontalLayout.addWidget(self.pastaDestinoCriaSpatialiteLineEdit)
        spacerItem = QtGui.QSpacerItem(13, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonBuscarPastaDestinoCriaSpatialite = QtGui.QPushButton(CriaSpatialite)
        self.pushButtonBuscarPastaDestinoCriaSpatialite.setObjectName(_fromUtf8("pushButtonBuscarPastaDestinoCriaSpatialite"))
        self.horizontalLayout.addWidget(self.pushButtonBuscarPastaDestinoCriaSpatialite)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(CriaSpatialite)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.coordSysCriaSpatialiteLineEdit = QtGui.QLineEdit(CriaSpatialite)
        self.coordSysCriaSpatialiteLineEdit.setObjectName(_fromUtf8("coordSysCriaSpatialiteLineEdit"))
        self.horizontalLayout_2.addWidget(self.coordSysCriaSpatialiteLineEdit)
        spacerItem1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButtonBuscarSistCoordCriaSpatialite = QtGui.QPushButton(CriaSpatialite)
        self.pushButtonBuscarSistCoordCriaSpatialite.setObjectName(_fromUtf8("pushButtonBuscarSistCoordCriaSpatialite"))
        self.horizontalLayout_2.addWidget(self.pushButtonBuscarSistCoordCriaSpatialite)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(CriaSpatialite)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.nomeLineEdit = QtGui.QLineEdit(CriaSpatialite)
        self.nomeLineEdit.setObjectName(_fromUtf8("nomeLineEdit"))
        self.horizontalLayout_3.addWidget(self.nomeLineEdit)
        spacerItem2 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_4 = QtGui.QLabel(CriaSpatialite)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_5.addWidget(self.label_4)
        self.versionComboBox = QtGui.QComboBox(CriaSpatialite)
        self.versionComboBox.setObjectName(_fromUtf8("versionComboBox"))
        self.versionComboBox.addItem(_fromUtf8(""))
        self.horizontalLayout_5.addWidget(self.versionComboBox)
        spacerItem3 = QtGui.QSpacerItem(128, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.pushButtonOkCriaSpatialite = QtGui.QPushButton(CriaSpatialite)
        self.pushButtonOkCriaSpatialite.setObjectName(_fromUtf8("pushButtonOkCriaSpatialite"))
        self.horizontalLayout_4.addWidget(self.pushButtonOkCriaSpatialite)
        spacerItem5 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.pushButtonCancelarCriaSpatialite = QtGui.QPushButton(CriaSpatialite)
        self.pushButtonCancelarCriaSpatialite.setObjectName(_fromUtf8("pushButtonCancelarCriaSpatialite"))
        self.horizontalLayout_4.addWidget(self.pushButtonCancelarCriaSpatialite)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(CriaSpatialite)
        QtCore.QObject.connect(self.pushButtonCancelarCriaSpatialite, QtCore.SIGNAL(_fromUtf8("clicked()")), CriaSpatialite.close)
        QtCore.QMetaObject.connectSlotsByName(CriaSpatialite)

    def retranslateUi(self, CriaSpatialite):
        CriaSpatialite.setWindowTitle(_translate("CriaSpatialite", "Create Spatialite", None))
        self.label.setText(_translate("CriaSpatialite", "Select Folder", None))
        self.pushButtonBuscarPastaDestinoCriaSpatialite.setText(_translate("CriaSpatialite", "Search", None))
        self.label_2.setText(_translate("CriaSpatialite", "Coordinate System", None))
        self.pushButtonBuscarSistCoordCriaSpatialite.setText(_translate("CriaSpatialite", "Search", None))
        self.label_3.setText(_translate("CriaSpatialite", "File Name", None))
        self.label_4.setText(_translate("CriaSpatialite", "EDGV Version:", None))
        self.versionComboBox.setItemText(0, _translate("CriaSpatialite", "2.1.3", None))
        self.pushButtonOkCriaSpatialite.setText(_translate("CriaSpatialite", "Ok", None))
        self.pushButtonCancelarCriaSpatialite.setText(_translate("CriaSpatialite", "Cancel", None))

