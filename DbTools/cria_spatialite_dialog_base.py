# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cria_spatialite_dialog_base.ui'
#
# Created: Thu Nov 06 19:17:00 2014
#      by: PyQt4 UI code generator 4.10.2
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
        CriaSpatialite.resize(500, 250)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CriaSpatialite.sizePolicy().hasHeightForWidth())
        CriaSpatialite.setSizePolicy(sizePolicy)
        CriaSpatialite.setMinimumSize(QtCore.QSize(500, 250))
        CriaSpatialite.setMaximumSize(QtCore.QSize(500, 250))
        self.horizontalLayoutWidget = QtGui.QWidget(CriaSpatialite)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 440, 51))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pastaDestinoCriaSpatialiteLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.pastaDestinoCriaSpatialiteLineEdit.setObjectName(_fromUtf8("pastaDestinoCriaSpatialiteLineEdit"))
        self.horizontalLayout.addWidget(self.pastaDestinoCriaSpatialiteLineEdit)
        spacerItem1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonBuscarPastaDestinoCriaSpatialite = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonBuscarPastaDestinoCriaSpatialite.setObjectName(_fromUtf8("pushButtonBuscarPastaDestinoCriaSpatialite"))
        self.horizontalLayout.addWidget(self.pushButtonBuscarPastaDestinoCriaSpatialite)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(CriaSpatialite)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(30, 90, 440, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.coordSysCriaSpatialiteLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.coordSysCriaSpatialiteLineEdit.setObjectName(_fromUtf8("coordSysCriaSpatialiteLineEdit"))
        self.horizontalLayout_2.addWidget(self.coordSysCriaSpatialiteLineEdit)
        spacerItem3 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pushButtonBuscarSistCoordCriaSpatialite = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButtonBuscarSistCoordCriaSpatialite.setObjectName(_fromUtf8("pushButtonBuscarSistCoordCriaSpatialite"))
        self.horizontalLayout_2.addWidget(self.pushButtonBuscarSistCoordCriaSpatialite)
        self.horizontalLayoutWidget_4 = QtGui.QWidget(CriaSpatialite)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(30, 210, 441, 31))
        self.horizontalLayoutWidget_4.setObjectName(_fromUtf8("horizontalLayoutWidget_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.pushButtonOkCriaSpatialite = QtGui.QPushButton(self.horizontalLayoutWidget_4)
        self.pushButtonOkCriaSpatialite.setObjectName(_fromUtf8("pushButtonOkCriaSpatialite"))
        self.horizontalLayout_4.addWidget(self.pushButtonOkCriaSpatialite)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.pushButtonCancelarCriaSpatialite = QtGui.QPushButton(self.horizontalLayoutWidget_4)
        self.pushButtonCancelarCriaSpatialite.setObjectName(_fromUtf8("pushButtonCancelarCriaSpatialite"))
        self.horizontalLayout_4.addWidget(self.pushButtonCancelarCriaSpatialite)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.horizontalLayoutWidget_3 = QtGui.QWidget(CriaSpatialite)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(30, 150, 361, 41))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(self.horizontalLayoutWidget_3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.nomeLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_3)
        self.nomeLineEdit.setObjectName(_fromUtf8("nomeLineEdit"))
        self.horizontalLayout_3.addWidget(self.nomeLineEdit)
        spacerItem8 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)

        self.retranslateUi(CriaSpatialite)
        QtCore.QObject.connect(self.pushButtonCancelarCriaSpatialite, QtCore.SIGNAL(_fromUtf8("clicked()")), CriaSpatialite.close)
        QtCore.QMetaObject.connectSlotsByName(CriaSpatialite)

    def retranslateUi(self, CriaSpatialite):
        CriaSpatialite.setWindowTitle(_translate("CriaSpatialite", "Create Spatialite", None))
        self.label.setText(_translate("CriaSpatialite", "Select Folder                        ", None))
        self.pushButtonBuscarPastaDestinoCriaSpatialite.setText(_translate("CriaSpatialite", "Search", None))
        self.label_2.setText(_translate("CriaSpatialite", "Coordinate System", None))
        self.pushButtonBuscarSistCoordCriaSpatialite.setText(_translate("CriaSpatialite", "Search", None))
        self.pushButtonOkCriaSpatialite.setText(_translate("CriaSpatialite", "Ok", None))
        self.pushButtonCancelarCriaSpatialite.setText(_translate("CriaSpatialite", "Cancel", None))
        self.label_3.setText(_translate("CriaSpatialite", "File Name            ", None))

