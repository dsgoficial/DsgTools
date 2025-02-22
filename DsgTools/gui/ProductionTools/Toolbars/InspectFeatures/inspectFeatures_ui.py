# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inspectFeatures.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(858, 36)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(0, 20))
        Form.setMaximumSize(QtCore.QSize(900, 50))
        Form.setToolTip("")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.mMapLayerComboBox = QgsMapLayerComboBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mMapLayerComboBox.sizePolicy().hasHeightForWidth()
        )
        self.mMapLayerComboBox.setSizePolicy(sizePolicy)
        self.mMapLayerComboBox.setMinimumSize(QtCore.QSize(0, 20))
        self.mMapLayerComboBox.setMaximumSize(QtCore.QSize(16777215, 32))
        self.mMapLayerComboBox.setFilters(
            core.QgsMapLayerProxyModel.HasGeometry
            | core.QgsMapLayerProxyModel.LineLayer
            | core.QgsMapLayerProxyModel.NoGeometry
            | core.QgsMapLayerProxyModel.PluginLayer
            | core.QgsMapLayerProxyModel.PointLayer
            | core.QgsMapLayerProxyModel.PolygonLayer
            | core.QgsMapLayerProxyModel.VectorLayer
        )
        self.mMapLayerComboBox.setObjectName("mMapLayerComboBox")
        self.refreshPushButton = QtWidgets.QPushButton(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.refreshPushButton.sizePolicy().hasHeightForWidth()
        )
        self.refreshPushButton.setSizePolicy(sizePolicy)
        self.refreshPushButton.setMinimumSize(QtCore.QSize(24, 24))
        self.refreshPushButton.setMaximumSize(QtCore.QSize(24, 24))
        self.refreshPushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/plugins/DsgTools/icons/reload.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.refreshPushButton.setIcon(icon)
        self.refreshPushButton.setIconSize(QtCore.QSize(16, 16))
        self.refreshPushButton.setObjectName("refreshPushButton")
        self.zoomPercentageSpinBox = QgsDoubleSpinBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.zoomPercentageSpinBox.sizePolicy().hasHeightForWidth()
        )
        self.zoomPercentageSpinBox.setSizePolicy(sizePolicy)
        self.zoomPercentageSpinBox.setMinimumSize(QtCore.QSize(0, 20))
        self.zoomPercentageSpinBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.zoomPercentageSpinBox.setObjectName("zoomPercentageSpinBox")
        self.mScaleWidget = QgsScaleWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mScaleWidget.sizePolicy().hasHeightForWidth())
        self.mScaleWidget.setSizePolicy(sizePolicy)
        self.mScaleWidget.setMinimumSize(QtCore.QSize(0, 20))
        self.mScaleWidget.setMaximumSize(QtCore.QSize(16194919, 32))
        self.mScaleWidget.setShowCurrentScaleButton(True)
        self.mScaleWidget.setObjectName("mScaleWidget")
        self.idSpinBox = QtWidgets.QSpinBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.idSpinBox.sizePolicy().hasHeightForWidth())
        self.idSpinBox.setSizePolicy(sizePolicy)
        self.idSpinBox.setMinimumSize(QtCore.QSize(40, 20))
        self.idSpinBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.idSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.idSpinBox.setSuffix("")
        self.idSpinBox.setObjectName("idSpinBox")
        self.usePanCkb = QtWidgets.QCheckBox(self.tr("Use pan"), self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usePanCkb.sizePolicy().hasHeightForWidth())
        self.usePanCkb.setSizePolicy(sizePolicy)
        self.usePanCkb.setMinimumSize(QtCore.QSize(70, 20))
        self.usePanCkb.setMaximumSize(QtCore.QSize(70, 20))
        self.usePanCkb.setObjectName("usePanCkb")
        self.backInspectButton = QtWidgets.QPushButton(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.backInspectButton.sizePolicy().hasHeightForWidth()
        )
        self.backInspectButton.setSizePolicy(sizePolicy)
        self.backInspectButton.setMinimumSize(QtCore.QSize(24, 24))
        self.backInspectButton.setMaximumSize(QtCore.QSize(24, 24))
        self.backInspectButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/plugins/DsgTools/icons/backInspect.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.backInspectButton.setIcon(icon)
        self.backInspectButton.setIconSize(QtCore.QSize(16, 16))
        self.backInspectButton.setObjectName("backInspectButton")
        self.nextInspectButton = QtWidgets.QPushButton(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.nextInspectButton.sizePolicy().hasHeightForWidth()
        )
        self.nextInspectButton.setSizePolicy(sizePolicy)
        self.nextInspectButton.setMinimumSize(QtCore.QSize(24, 24))
        self.nextInspectButton.setMaximumSize(QtCore.QSize(24, 24))
        self.nextInspectButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/plugins/DsgTools/icons/nextInspect.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.nextInspectButton.setIcon(icon1)
        self.nextInspectButton.setIconSize(QtCore.QSize(16, 16))
        self.nextInspectButton.setObjectName("nextInspectButton")
        self.mFieldExpressionWidget = QgsFieldExpressionWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mFieldExpressionWidget.sizePolicy().hasHeightForWidth()
        )
        self.mFieldExpressionWidget.setSizePolicy(sizePolicy)
        self.mFieldExpressionWidget.setMinimumSize(QtCore.QSize(0, 20))
        self.mFieldExpressionWidget.setObjectName("mFieldExpressionWidget")
        self.sortPushButton = QtWidgets.QPushButton(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sortPushButton.sizePolicy().hasHeightForWidth()
        )
        self.sortPushButton.setSizePolicy(sizePolicy)
        self.sortPushButton.setMinimumSize(QtCore.QSize(24, 24))
        self.sortPushButton.setMaximumSize(QtCore.QSize(24, 24))
        self.sortPushButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/plugins/DsgTools/icons/sort.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.sortPushButton.setIcon(icon3)
        self.sortPushButton.setCheckable(True)
        self.sortPushButton.setObjectName("sortPushButton")
        self.splitter2 = QtWidgets.QSplitter(self.splitter)
        self.splitter2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter2.setObjectName("splitter2")
        self.mFieldComboBox = QgsFieldComboBox(self.splitter2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mFieldComboBox.sizePolicy().hasHeightForWidth()
        )
        self.mFieldComboBox.setSizePolicy(sizePolicy)
        self.mFieldComboBox.setMinimumSize(QtCore.QSize(100, 0))
        self.mFieldComboBox.setObjectName("mFieldComboBox")
        self.widget = QtWidgets.QWidget(self.splitter2)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ascRadioButton = QtWidgets.QRadioButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ascRadioButton.sizePolicy().hasHeightForWidth()
        )
        self.ascRadioButton.setSizePolicy(sizePolicy)
        self.ascRadioButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/plugins/DsgTools/icons/up.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.ascRadioButton.setIcon(icon4)
        self.ascRadioButton.setChecked(True)
        self.ascRadioButton.setObjectName("ascRadioButton")
        self.horizontalLayout.addWidget(self.ascRadioButton)
        self.descRadioButton = QtWidgets.QRadioButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.descRadioButton.sizePolicy().hasHeightForWidth()
        )
        self.descRadioButton.setSizePolicy(sizePolicy)
        self.descRadioButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/plugins/DsgTools/icons/down.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.descRadioButton.setIcon(icon5)
        self.descRadioButton.setObjectName("descRadioButton")
        self.horizontalLayout.addWidget(self.descRadioButton)

        self.gridLayout.addWidget(self.splitter, 0, 2, 1, 1)
        self.inspectPushButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.inspectPushButton.sizePolicy().hasHeightForWidth()
        )
        self.inspectPushButton.setSizePolicy(sizePolicy)
        self.inspectPushButton.setMinimumSize(QtCore.QSize(24, 24))
        self.inspectPushButton.setMaximumSize(QtCore.QSize(24, 24))
        self.inspectPushButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/plugins/DsgTools/icons/inspectFeatures.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.inspectPushButton.setIcon(icon2)
        self.inspectPushButton.setIconSize(QtCore.QSize(16, 16))
        self.inspectPushButton.setCheckable(True)
        self.inspectPushButton.setObjectName("inspectPushButton")
        self.gridLayout.addWidget(self.inspectPushButton, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        # self.idSpinBox.setPrefix(_translate("Form", "ID: "))
        self.backInspectButton.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Back inspect</p><p><br/></p></body></html>",
            )
        )
        self.nextInspectButton.setToolTip(
            _translate("Form", "<html><head/><body><p>Next inspect</p></body></html>")
        )
        self.inspectPushButton.setToolTip(_translate("Form", "Inspect Features Tool"))


from qgis.gui import (
    QgsFieldExpressionWidget,
    QgsMapLayerComboBox,
    QgsScaleWidget,
    QgsDoubleSpinBox,
    QgsFieldComboBox,
)
from qgis import core
import resources_rc
