# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dsgRasterInfoTool.ui'
#
# Created by: qgis.PyQt UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from builtins import object
from qgis.PyQt import QtCore, QtGui, QtWidgets

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

from qgis.gui import QgsMapLayerComboBox
from qgis.core import QgsMapLayerProxyModel
import resources_rc

class Ui_DsgRasterInfoTool(object):
    def setupUi(self, DsgRasterInfoTool):
        DsgRasterInfoTool.setObjectName(_fromUtf8("DsgRasterInfoTool"))
        DsgRasterInfoTool.resize(309, 49)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DsgRasterInfoTool.sizePolicy().hasHeightForWidth())
        DsgRasterInfoTool.setSizePolicy(sizePolicy)
        DsgRasterInfoTool.setMinimumSize(QtCore.QSize(0, 20))
        DsgRasterInfoTool.setMaximumSize(QtCore.QSize(468, 50))
        DsgRasterInfoTool.setToolTip(_fromUtf8(""))
        self.gridLayout = QtWidgets.QGridLayout(DsgRasterInfoTool)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.rasterInfoPushButton = QtWidgets.QPushButton(DsgRasterInfoTool)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rasterInfoPushButton.sizePolicy().hasHeightForWidth())
        self.rasterInfoPushButton.setSizePolicy(sizePolicy)
        self.rasterInfoPushButton.setMinimumSize(QtCore.QSize(16, 16))
        self.rasterInfoPushButton.setMaximumSize(QtCore.QSize(24, 24))
        self.rasterInfoPushButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/DsgTools/icons/rasterToolTip.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rasterInfoPushButton.setIcon(icon)
        self.rasterInfoPushButton.setIconSize(QtCore.QSize(16, 16))
        self.rasterInfoPushButton.setCheckable(True)
        self.rasterInfoPushButton.setObjectName(_fromUtf8("rasterInfoPushButton"))
        self.gridLayout.addWidget(self.rasterInfoPushButton, 0, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(DsgRasterInfoTool)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.rasterComboBox = QgsMapLayerComboBox(self.splitter)
        self.rasterComboBox.setFilters(QgsMapLayerProxyModel.RasterLayer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rasterComboBox.sizePolicy().hasHeightForWidth())
        self.rasterComboBox.setSizePolicy(sizePolicy)
        self.rasterComboBox.setMinimumSize(QtCore.QSize(0, 20))
        self.rasterComboBox.setMaximumSize(QtCore.QSize(16777215, 24))
        self.rasterComboBox.setObjectName(_fromUtf8("rasterComboBox"))
        self.refreshPushButton = QtWidgets.QPushButton(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshPushButton.sizePolicy().hasHeightForWidth())
        self.refreshPushButton.setSizePolicy(sizePolicy)
        self.refreshPushButton.setMinimumSize(QtCore.QSize(24, 24))
        self.refreshPushButton.setMaximumSize(QtCore.QSize(24, 24))
        self.refreshPushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/DsgTools/icons/reload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshPushButton.setIcon(icon)
        self.refreshPushButton.setIconSize(QtCore.QSize(16, 16))
        self.refreshPushButton.setObjectName("refreshPushButton")
        self.bandTooltipButton = QtWidgets.QPushButton(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bandTooltipButton.sizePolicy().hasHeightForWidth())
        self.bandTooltipButton.setSizePolicy(sizePolicy)
        self.bandTooltipButton.setMinimumSize(QtCore.QSize(16, 16))
        self.bandTooltipButton.setMaximumSize(QtCore.QSize(24, 24))
        self.bandTooltipButton.setToolTip(_fromUtf8("Show raster tooltip"))
        self.bandTooltipButton.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/DsgTools/icons/band_tooltip.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bandTooltipButton.setIcon(icon1)
        self.bandTooltipButton.setIconSize(QtCore.QSize(16, 16))
        self.bandTooltipButton.setCheckable(True)
        self.bandTooltipButton.setObjectName(_fromUtf8("bandTooltipButton"))
        self.dynamicHistogramButton = QtWidgets.QPushButton(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dynamicHistogramButton.sizePolicy().hasHeightForWidth())
        self.dynamicHistogramButton.setSizePolicy(sizePolicy)
        self.dynamicHistogramButton.setMinimumSize(QtCore.QSize(16, 16))
        self.dynamicHistogramButton.setMaximumSize(QtCore.QSize(24, 24))
        self.dynamicHistogramButton.setToolTip(_fromUtf8("Dynamic histogram view"))
        self.dynamicHistogramButton.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/DsgTools/icons/dynamic_histogram_viewer.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dynamicHistogramButton.setIcon(icon2)
        self.dynamicHistogramButton.setIconSize(QtCore.QSize(16,16))
        self.dynamicHistogramButton.setCheckable(True)
        self.dynamicHistogramButton.setObjectName(_fromUtf8("dynamicHistogramButton"))
        self.gridLayout.addWidget(self.splitter, 0, 1, 1, 1)
        self.valueSetterButton = QtWidgets.QPushButton(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valueSetterButton.sizePolicy().hasHeightForWidth())
        self.valueSetterButton.setSizePolicy(sizePolicy)
        self.valueSetterButton.setMinimumSize(QtCore.QSize(16, 16))
        self.valueSetterButton.setMaximumSize(QtCore.QSize(24, 24))
        self.valueSetterButton.setToolTip(_fromUtf8("Set Value From Raster"))
        self.valueSetterButton.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/DsgTools/icons/valueSetter.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.valueSetterButton.setIcon(icon2)
        self.valueSetterButton.setIconSize(QtCore.QSize(40, 40))
        self.valueSetterButton.setCheckable(True)
        self.valueSetterButton.setObjectName(_fromUtf8("valueSetterButton"))
        self.gridLayout.addWidget(self.splitter, 0, 2, 1, 1)

        self.retranslateUi(DsgRasterInfoTool)
        QtCore.QMetaObject.connectSlotsByName(DsgRasterInfoTool)

    def retranslateUi(self, DsgRasterInfoTool):
        DsgRasterInfoTool.setWindowTitle(_translate("DsgRasterInfoTool", "Form", None))
        self.rasterInfoPushButton.setToolTip(_translate("DsgRasterInfoTool", "Raster Info Tool", None))
