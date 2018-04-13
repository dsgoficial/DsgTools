# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inspectFeatures.ui'
#
# Created: Wed Jul 26 08:46:19 2017
#      by: qgis.PyQt UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from builtins import object
from qgis.PyQt import QtCore, QtWidgets, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(625, 24)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(0, 50))
        Form.setMaximumSize(QtCore.QSize(900, 50))
        Form.setToolTip(_fromUtf8(""))
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.mMapLayerComboBox = gui.QgsMapLayerComboBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mMapLayerComboBox.sizePolicy().hasHeightForWidth())
        self.mMapLayerComboBox.setSizePolicy(sizePolicy)
        self.mMapLayerComboBox.setMaximumSize(QtCore.QSize(16777215, 24))
        self.mMapLayerComboBox.setFilters(core.QgsMapLayerProxyModel.HasGeometry|core.QgsMapLayerProxyModel.LineLayer|core.QgsMapLayerProxyModel.NoGeometry|core.QgsMapLayerProxyModel.PluginLayer|core.QgsMapLayerProxyModel.PointLayer|core.QgsMapLayerProxyModel.PolygonLayer|core.QgsMapLayerProxyModel.VectorLayer)
        self.mMapLayerComboBox.setObjectName(_fromUtf8("mMapLayerComboBox"))
        self.label_zoom = QtWidgets.QLabel(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_zoom.sizePolicy().hasHeightForWidth())
        self.label_zoom.setSizePolicy(sizePolicy)
        self.label_zoom.setMinimumSize(QtCore.QSize(0, 0))
        self.label_zoom.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_zoom.setFont(font)
        self.label_zoom.setAlignment(QtCore.Qt.AlignCenter)
        self.label_zoom.setObjectName(_fromUtf8("label_zoom"))
        self.mScaleWidget = gui.QgsScaleWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mScaleWidget.sizePolicy().hasHeightForWidth())
        self.mScaleWidget.setSizePolicy(sizePolicy)
        self.mScaleWidget.setMinimumSize(QtCore.QSize(0, 24))
        self.mScaleWidget.setMaximumSize(QtCore.QSize(16194919, 24))
        self.mScaleWidget.setShowCurrentScaleButton(True)
        self.mScaleWidget.setObjectName(_fromUtf8("mScaleWidget"))
        self.idSpinBox = QtWidgets.QSpinBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.idSpinBox.sizePolicy().hasHeightForWidth())
        self.idSpinBox.setSizePolicy(sizePolicy)
        self.idSpinBox.setMinimumSize(QtCore.QSize(40, 24))
        self.idSpinBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.idSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.idSpinBox.setSuffix(_fromUtf8(""))
        self.idSpinBox.setObjectName(_fromUtf8("idSpinBox"))
        self.backInspectButton = QtWidgets.QPushButton(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backInspectButton.sizePolicy().hasHeightForWidth())
        self.backInspectButton.setSizePolicy(sizePolicy)
        self.backInspectButton.setMinimumSize(QtCore.QSize(24, 24))
        self.backInspectButton.setMaximumSize(QtCore.QSize(24, 24))
        self.backInspectButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/DsgTools/icons/backInspect.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backInspectButton.setIcon(icon)
        self.backInspectButton.setIconSize(QtCore.QSize(16, 16))
        self.backInspectButton.setObjectName(_fromUtf8("backInspectButton"))
        self.nextInspectButton = QtWidgets.QPushButton(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextInspectButton.sizePolicy().hasHeightForWidth())
        self.nextInspectButton.setSizePolicy(sizePolicy)
        self.nextInspectButton.setMinimumSize(QtCore.QSize(24, 24))
        self.nextInspectButton.setMaximumSize(QtCore.QSize(24, 24))
        self.nextInspectButton.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/DsgTools/icons/nextInspect.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextInspectButton.setIcon(icon1)
        self.nextInspectButton.setIconSize(QtCore.QSize(16, 16))
        self.nextInspectButton.setObjectName(_fromUtf8("nextInspectButton"))
        self.mFieldExpressionWidget = gui.QgsFieldExpressionWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mFieldExpressionWidget.sizePolicy().hasHeightForWidth())
        self.mFieldExpressionWidget.setSizePolicy(sizePolicy)
        self.mFieldExpressionWidget.setObjectName(_fromUtf8("mFieldExpressionWidget"))
        self.gridLayout.addWidget(self.splitter, 0, 1, -1, -1)
        self.inspectPushButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inspectPushButton.sizePolicy().hasHeightForWidth())
        self.inspectPushButton.setSizePolicy(sizePolicy)
        self.inspectPushButton.setMinimumSize(QtCore.QSize(24, 24))
        self.inspectPushButton.setMaximumSize(QtCore.QSize(24, 24))
        self.inspectPushButton.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/DsgTools/icons/inspectFeatures.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.inspectPushButton.setIcon(icon2)
        self.inspectPushButton.setIconSize(QtCore.QSize(16, 16))
        self.inspectPushButton.setCheckable(True)
        self.inspectPushButton.setObjectName(_fromUtf8("inspectPushButton"))
        self.gridLayout.addWidget(self.inspectPushButton, 0, 0, -1, -1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_zoom.setText(_translate("Form", "Scale", None))
        self.idSpinBox.setPrefix(_translate("Form", "ID: ", None))
        self.backInspectButton.setToolTip(_translate("Form", "<html><head/><body><p>Back inspect</p><p><br/></p></body></html>", None))
        self.nextInspectButton.setToolTip(_translate("Form", "<html><head/><body><p>Next inspect</p></body></html>", None))
        self.inspectPushButton.setToolTip(_translate("Form", "Inspect Features Tool", None))

from qgis import gui, core  
import resources_rc
