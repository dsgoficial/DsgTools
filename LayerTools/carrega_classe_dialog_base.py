# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'carrega_classe_dialog_base.ui'
#
# Created: Thu Nov 06 19:18:18 2014
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

class Ui_CarregaClasse(object):
    def setupUi(self, CarregaClasse):
        CarregaClasse.setObjectName(_fromUtf8("CarregaClasse"))
        CarregaClasse.resize(400, 600)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CarregaClasse.sizePolicy().hasHeightForWidth())
        CarregaClasse.setSizePolicy(sizePolicy)
        CarregaClasse.setMinimumSize(QtCore.QSize(400, 600))
        CarregaClasse.setMaximumSize(QtCore.QSize(400, 600))
        self.horizontalLayoutWidget = QtGui.QWidget(CarregaClasse)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 361, 51))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.arquivoLineEditCarregaClasse = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.arquivoLineEditCarregaClasse.setObjectName(_fromUtf8("arquivoLineEditCarregaClasse"))
        self.horizontalLayout.addWidget(self.arquivoLineEditCarregaClasse)
        spacerItem1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonBuscarArquivo = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonBuscarArquivo.setObjectName(_fromUtf8("pushButtonBuscarArquivo"))
        self.horizontalLayout.addWidget(self.pushButtonBuscarArquivo)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(CarregaClasse)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 90, 361, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.coordSysLineEditCarregaClasse = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.coordSysLineEditCarregaClasse.setObjectName(_fromUtf8("coordSysLineEditCarregaClasse"))
        self.horizontalLayout_2.addWidget(self.coordSysLineEditCarregaClasse)
        spacerItem2 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.groupBox = QtGui.QGroupBox(CarregaClasse)
        self.groupBox.setGeometry(QtCore.QRect(10, 150, 381, 331))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayoutWidget_3 = QtGui.QWidget(self.groupBox)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 361, 311))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.listWidgetOrigemCategoriaCarregaClasse = QtGui.QListWidget(self.horizontalLayoutWidget_3)
        self.listWidgetOrigemCategoriaCarregaClasse.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWidgetOrigemCategoriaCarregaClasse.setObjectName(_fromUtf8("listWidgetOrigemCategoriaCarregaClasse"))
        self.horizontalLayout_3.addWidget(self.listWidgetOrigemCategoriaCarregaClasse)
        self.horizontalLayoutWidget_4 = QtGui.QWidget(CarregaClasse)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(20, 540, 351, 44))
        self.horizontalLayoutWidget_4.setObjectName(_fromUtf8("horizontalLayoutWidget_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.pushButtonOkCarregaClasse = QtGui.QPushButton(self.horizontalLayoutWidget_4)
        self.pushButtonOkCarregaClasse.setObjectName(_fromUtf8("pushButtonOkCarregaClasse"))
        self.horizontalLayout_4.addWidget(self.pushButtonOkCarregaClasse)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.pushButtonCancelarCarregaClasse = QtGui.QPushButton(self.horizontalLayoutWidget_4)
        self.pushButtonCancelarCarregaClasse.setObjectName(_fromUtf8("pushButtonCancelarCarregaClasse"))
        self.horizontalLayout_4.addWidget(self.pushButtonCancelarCarregaClasse)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayoutWidget_2 = QtGui.QWidget(CarregaClasse)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 490, 186, 42))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.checkBoxTodosCarregaClasse = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBoxTodosCarregaClasse.setObjectName(_fromUtf8("checkBoxTodosCarregaClasse"))
        self.verticalLayout_2.addWidget(self.checkBoxTodosCarregaClasse)

        self.retranslateUi(CarregaClasse)
        QtCore.QObject.connect(self.pushButtonCancelarCarregaClasse, QtCore.SIGNAL(_fromUtf8("clicked()")), CarregaClasse.close)
        QtCore.QMetaObject.connectSlotsByName(CarregaClasse)

    def retranslateUi(self, CarregaClasse):
        CarregaClasse.setWindowTitle(_translate("CarregaClasse", "Load by Class", None))
        self.label.setText(_translate("CarregaClasse", "File                    ", None))
        self.pushButtonBuscarArquivo.setText(_translate("CarregaClasse", "Search", None))
        self.label_2.setText(_translate("CarregaClasse", "Coordinate System", None))
        self.groupBox.setTitle(_translate("CarregaClasse", "Select the classes", None))
        self.pushButtonOkCarregaClasse.setText(_translate("CarregaClasse", "Ok", None))
        self.pushButtonCancelarCarregaClasse.setText(_translate("CarregaClasse", "Cancel", None))
        self.checkBoxTodosCarregaClasse.setText(_translate("CarregaClasse", "Select All", None))

