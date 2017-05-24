# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inspectFeatures.ui'
#
# Created: Wed May 24 13:19:56 2017
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(850, 50)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(0, 50))
        Form.setMaximumSize(QtCore.QSize(850, 50))
        Form.setToolTip(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.inspectPushButton = QtGui.QPushButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inspectPushButton.sizePolicy().hasHeightForWidth())
        self.inspectPushButton.setSizePolicy(sizePolicy)
        self.inspectPushButton.setMinimumSize(QtCore.QSize(32, 32))
        self.inspectPushButton.setMaximumSize(QtCore.QSize(32, 32))
        self.inspectPushButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/DsgTools/icons/inspectFeatures.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.inspectPushButton.setIcon(icon)
        self.inspectPushButton.setIconSize(QtCore.QSize(28, 28))
        self.inspectPushButton.setCheckable(True)
        self.inspectPushButton.setObjectName(_fromUtf8("inspectPushButton"))
        self.gridLayout.addWidget(self.inspectPushButton, 0, 0, 1, 1)
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.mMapLayerComboBox = gui.QgsMapLayerComboBox(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mMapLayerComboBox.sizePolicy().hasHeightForWidth())
        self.mMapLayerComboBox.setSizePolicy(sizePolicy)
        self.mMapLayerComboBox.setMaximumSize(QtCore.QSize(16777215, 32))
        self.mMapLayerComboBox.setFilters(gui.QgsMapLayerProxyModel.LineLayer|gui.QgsMapLayerProxyModel.PluginLayer|gui.QgsMapLayerProxyModel.PointLayer|gui.QgsMapLayerProxyModel.PolygonLayer)
        self.mMapLayerComboBox.setObjectName(_fromUtf8("mMapLayerComboBox"))
        self.activeLayerCheckBox = QtGui.QCheckBox(self.splitter)
        self.activeLayerCheckBox.setMaximumSize(QtCore.QSize(16777215, 32))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.activeLayerCheckBox.setFont(font)
        self.activeLayerCheckBox.setObjectName(_fromUtf8("activeLayerCheckBox"))
        self.backInspectButton = QtGui.QPushButton(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backInspectButton.sizePolicy().hasHeightForWidth())
        self.backInspectButton.setSizePolicy(sizePolicy)
        self.backInspectButton.setMinimumSize(QtCore.QSize(32, 32))
        self.backInspectButton.setMaximumSize(QtCore.QSize(32, 32))
        self.backInspectButton.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/DsgTools/icons/backInspect.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backInspectButton.setIcon(icon1)
        self.backInspectButton.setIconSize(QtCore.QSize(25, 25))
        self.backInspectButton.setObjectName(_fromUtf8("backInspectButton"))
        self.label_zoom = QtGui.QLabel(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_zoom.sizePolicy().hasHeightForWidth())
        self.label_zoom.setSizePolicy(sizePolicy)
        self.label_zoom.setMinimumSize(QtCore.QSize(0, 32))
        self.label_zoom.setMaximumSize(QtCore.QSize(16777215, 32))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_zoom.setFont(font)
        self.label_zoom.setAlignment(QtCore.Qt.AlignCenter)
        self.label_zoom.setObjectName(_fromUtf8("label_zoom"))
        self.mScaleWidget = gui.QgsScaleWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mScaleWidget.sizePolicy().hasHeightForWidth())
        self.mScaleWidget.setSizePolicy(sizePolicy)
        self.mScaleWidget.setMinimumSize(QtCore.QSize(0, 32))
        self.mScaleWidget.setMaximumSize(QtCore.QSize(100, 32))
        self.mScaleWidget.setShowCurrentScaleButton(True)
        self.mScaleWidget.setObjectName(_fromUtf8("mScaleWidget"))
        self.label_id = QtGui.QLabel(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_id.sizePolicy().hasHeightForWidth())
        self.label_id.setSizePolicy(sizePolicy)
        self.label_id.setMinimumSize(QtCore.QSize(0, 32))
        self.label_id.setMaximumSize(QtCore.QSize(16777215, 32))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_id.setFont(font)
        self.label_id.setAlignment(QtCore.Qt.AlignCenter)
        self.label_id.setObjectName(_fromUtf8("label_id"))
        self.idSpinBox = QtGui.QSpinBox(self.splitter)
        self.idSpinBox.setMinimumSize(QtCore.QSize(32, 32))
        self.idSpinBox.setMaximumSize(QtCore.QSize(16777215, 32))
        self.idSpinBox.setObjectName(_fromUtf8("idSpinBox"))
        self.nextInspectButton = QtGui.QPushButton(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextInspectButton.sizePolicy().hasHeightForWidth())
        self.nextInspectButton.setSizePolicy(sizePolicy)
        self.nextInspectButton.setMinimumSize(QtCore.QSize(32, 32))
        self.nextInspectButton.setMaximumSize(QtCore.QSize(32, 32))
        self.nextInspectButton.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/DsgTools/icons/nextInspect.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextInspectButton.setIcon(icon2)
        self.nextInspectButton.setIconSize(QtCore.QSize(25, 25))
        self.nextInspectButton.setObjectName(_fromUtf8("nextInspectButton"))
        self.onlySelectedRadioButton = QtGui.QRadioButton(self.splitter)
        self.onlySelectedRadioButton.setMinimumSize(QtCore.QSize(0, 32))
        self.onlySelectedRadioButton.setMaximumSize(QtCore.QSize(16777215, 32))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.onlySelectedRadioButton.setFont(font)
        self.onlySelectedRadioButton.setObjectName(_fromUtf8("onlySelectedRadioButton"))
        self.gridLayout.addWidget(self.splitter, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.inspectPushButton.setToolTip(_translate("Form", "Inspect Features Tool", None))
        self.activeLayerCheckBox.setText(_translate("Form", "Active\n"
"Layer", None))
        self.backInspectButton.setToolTip(_translate("Form", "<html><head/><body><p>Back inspect</p><p><br/></p></body></html>", None))
        self.label_zoom.setText(_translate("Form", "Set Zoom", None))
        self.label_id.setText(_translate("Form", "Initial feat ID", None))
        self.nextInspectButton.setToolTip(_translate("Form", "<html><head/><body><p>Next inspect</p></body></html>", None))
        self.onlySelectedRadioButton.setText(_translate("Form", "Only on selected \n"
"features", None))

from qgis import gui
import resources_rc
