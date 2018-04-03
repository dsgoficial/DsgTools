# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dsgRasterInfoTool.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

from qgis.gui import QgsMapLayerComboBox, QgsMapLayerProxyModel
import resources_rc

class Ui_DsgRasterInfoTool(object):
    def setupUi(self, DsgRasterInfoTool):
        DsgRasterInfoTool.setObjectName(_fromUtf8("DsgRasterInfoTool"))
        DsgRasterInfoTool.resize(309, 49)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DsgRasterInfoTool.sizePolicy().hasHeightForWidth())
        DsgRasterInfoTool.setSizePolicy(sizePolicy)
        DsgRasterInfoTool.setMinimumSize(QtCore.QSize(0, 20))
        DsgRasterInfoTool.setMaximumSize(QtCore.QSize(468, 50))
        DsgRasterInfoTool.setToolTip(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(DsgRasterInfoTool)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.rasterInfoPushButton = QtGui.QPushButton(DsgRasterInfoTool)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rasterInfoPushButton.sizePolicy().hasHeightForWidth())
        self.rasterInfoPushButton.setSizePolicy(sizePolicy)
        self.rasterInfoPushButton.setMinimumSize(QtCore.QSize(32, 20))
        self.rasterInfoPushButton.setMaximumSize(QtCore.QSize(32, 32))
        self.rasterInfoPushButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/DsgTools/icons/rasterToolTip.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rasterInfoPushButton.setIcon(icon)
        self.rasterInfoPushButton.setIconSize(QtCore.QSize(20, 28))
        self.rasterInfoPushButton.setCheckable(True)
        self.rasterInfoPushButton.setObjectName(_fromUtf8("rasterInfoPushButton"))
        self.gridLayout.addWidget(self.rasterInfoPushButton, 0, 0, 1, 1)
        self.splitter = QtGui.QSplitter(DsgRasterInfoTool)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.rasterComboBox = QgsMapLayerComboBox(self.splitter)
        self.rasterComboBox.setFilters(QgsMapLayerProxyModel.RasterLayer)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rasterComboBox.sizePolicy().hasHeightForWidth())
        self.rasterComboBox.setSizePolicy(sizePolicy)
        self.rasterComboBox.setMinimumSize(QtCore.QSize(0, 20))
        self.rasterComboBox.setMaximumSize(QtCore.QSize(16777215, 32))
        self.rasterComboBox.setObjectName(_fromUtf8("rasterComboBox"))
        self.bandTooltipButton = QtGui.QPushButton(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bandTooltipButton.sizePolicy().hasHeightForWidth())
        self.bandTooltipButton.setSizePolicy(sizePolicy)
        self.bandTooltipButton.setMinimumSize(QtCore.QSize(32, 20))
        self.bandTooltipButton.setMaximumSize(QtCore.QSize(32, 32))
        self.bandTooltipButton.setToolTip(_fromUtf8(""))
        self.bandTooltipButton.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/DsgTools/icons/band_tooltip.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bandTooltipButton.setIcon(icon1)
        self.bandTooltipButton.setIconSize(QtCore.QSize(20, 20))
        self.bandTooltipButton.setCheckable(True)
        self.bandTooltipButton.setObjectName(_fromUtf8("bandTooltipButton"))
        self.dynamicHistogramButton = QtGui.QPushButton(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dynamicHistogramButton.sizePolicy().hasHeightForWidth())
        self.dynamicHistogramButton.setSizePolicy(sizePolicy)
        self.dynamicHistogramButton.setMinimumSize(QtCore.QSize(32, 20))
        self.dynamicHistogramButton.setMaximumSize(QtCore.QSize(32, 32))
        self.dynamicHistogramButton.setToolTip(_fromUtf8(""))
        self.dynamicHistogramButton.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/DsgTools/icons/dynamic_histogram_viewer.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dynamicHistogramButton.setIcon(icon2)
        self.dynamicHistogramButton.setIconSize(QtCore.QSize(20, 20))
        self.dynamicHistogramButton.setCheckable(True)
        self.dynamicHistogramButton.setObjectName(_fromUtf8("dynamicHistogramButton"))
        self.gridLayout.addWidget(self.splitter, 0, 1, 1, 1)

        self.retranslateUi(DsgRasterInfoTool)
        QtCore.QMetaObject.connectSlotsByName(DsgRasterInfoTool)

    def retranslateUi(self, DsgRasterInfoTool):
        DsgRasterInfoTool.setWindowTitle(_translate("DsgRasterInfoTool", "Form", None))
        self.rasterInfoPushButton.setToolTip(_translate("DsgRasterInfoTool", "Raster Info Tool", None))
