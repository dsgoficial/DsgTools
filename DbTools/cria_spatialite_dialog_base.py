# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cria_spatialite_dialog_base.ui'
#
# Created: Sun Dec 21 01:02:08 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CriaSpatialite(object):
    def setupUi(self, CriaSpatialite):
        CriaSpatialite.setObjectName(_fromUtf8("CriaSpatialite"))
        CriaSpatialite.resize(373, 135)
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
        spacerItem = QtGui.QSpacerItem(70, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pastaDestinoCriaSpatialiteLineEdit = QtGui.QLineEdit(CriaSpatialite)
        self.pastaDestinoCriaSpatialiteLineEdit.setObjectName(_fromUtf8("pastaDestinoCriaSpatialiteLineEdit"))
        self.horizontalLayout.addWidget(self.pastaDestinoCriaSpatialiteLineEdit)
        spacerItem1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonBuscarPastaDestinoCriaSpatialite = QtGui.QPushButton(CriaSpatialite)
        self.pushButtonBuscarPastaDestinoCriaSpatialite.setObjectName(_fromUtf8("pushButtonBuscarPastaDestinoCriaSpatialite"))
        self.horizontalLayout.addWidget(self.pushButtonBuscarPastaDestinoCriaSpatialite)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(CriaSpatialite)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.coordSysCriaSpatialiteLineEdit = QtGui.QLineEdit(CriaSpatialite)
        self.coordSysCriaSpatialiteLineEdit.setObjectName(_fromUtf8("coordSysCriaSpatialiteLineEdit"))
        self.horizontalLayout_2.addWidget(self.coordSysCriaSpatialiteLineEdit)
        spacerItem3 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pushButtonBuscarSistCoordCriaSpatialite = QtGui.QPushButton(CriaSpatialite)
        self.pushButtonBuscarSistCoordCriaSpatialite.setObjectName(_fromUtf8("pushButtonBuscarSistCoordCriaSpatialite"))
        self.horizontalLayout_2.addWidget(self.pushButtonBuscarSistCoordCriaSpatialite)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(CriaSpatialite)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem4 = QtGui.QSpacerItem(85, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.nomeLineEdit = QtGui.QLineEdit(CriaSpatialite)
        self.nomeLineEdit.setObjectName(_fromUtf8("nomeLineEdit"))
        self.horizontalLayout_3.addWidget(self.nomeLineEdit)
        spacerItem5 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.pushButtonOkCriaSpatialite = QtGui.QPushButton(CriaSpatialite)
        self.pushButtonOkCriaSpatialite.setObjectName(_fromUtf8("pushButtonOkCriaSpatialite"))
        self.horizontalLayout_4.addWidget(self.pushButtonOkCriaSpatialite)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem7)
        self.pushButtonCancelarCriaSpatialite = QtGui.QPushButton(CriaSpatialite)
        self.pushButtonCancelarCriaSpatialite.setObjectName(_fromUtf8("pushButtonCancelarCriaSpatialite"))
        self.horizontalLayout_4.addWidget(self.pushButtonCancelarCriaSpatialite)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(CriaSpatialite)
        QtCore.QObject.connect(self.pushButtonCancelarCriaSpatialite, QtCore.SIGNAL(_fromUtf8("clicked()")), CriaSpatialite.close)
        QtCore.QMetaObject.connectSlotsByName(CriaSpatialite)

    def retranslateUi(self, CriaSpatialite):
        CriaSpatialite.setWindowTitle(QtGui.QApplication.translate("CriaSpatialite", "Create Spatialite", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CriaSpatialite", "Select Folder", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonBuscarPastaDestinoCriaSpatialite.setText(QtGui.QApplication.translate("CriaSpatialite", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CriaSpatialite", "Coordinate System", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonBuscarSistCoordCriaSpatialite.setText(QtGui.QApplication.translate("CriaSpatialite", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("CriaSpatialite", "File Name", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOkCriaSpatialite.setText(QtGui.QApplication.translate("CriaSpatialite", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCancelarCriaSpatialite.setText(QtGui.QApplication.translate("CriaSpatialite", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

