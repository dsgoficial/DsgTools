# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-05-11
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Marcel Fernandes - Cartographic Engineer @ Brazilian Army
        email                :
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os
from typing import List, Optional

from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeatureRequest,
    QgsMapLayer,
    QgsProject,
    QgsRectangle,
    QgsVectorLayer,
    QgsWkbTypes,
    QgsFeature,
)
from qgis.gui import QgsMapTool, QgsMessageBar, QgisInterface
from qgis.PyQt import QtCore, QtGui, uic
from qgis.PyQt.Qt import QObject, QVariant
from qgis.PyQt.QtCore import QObject, QSettings, Qt, pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QSpinBox, QWidget
from qgis.PyQt.QtXml import QDomDocument
from qgis.core.additions.edit import edit

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "centerPointAndBoundaries.ui")
)


class CenterPointAndBoundariesToolbar(QWidget, FORM_CLASS):
    def __init__(self, iface: QgisInterface, parent: Optional[QWidget] = None):
        """
        Constructor
        """
        super(CenterPointAndBoundariesToolbar, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.splitter.hide()
        self.iface = iface

        self.canvas = self.iface.mapCanvas()

        icon_path = ":/plugins/DsgTools/icons/centroid.png"
        text = self.tr("DSGTools: Run add centroids")
        self.runPushButtonAction = self.add_action(
            icon_path, text, self.runPushButton.click, parent=self.parent
        )
        self.iface.registerMainWindowAction(self.runPushButtonAction, "")

        self.lineLayerDict = dict()

        self.iface.newProjectCreated.connect(self.resetTool)
        QgsProject.instance().layersWillBeRemoved.connect(self.syncLayers)
        self.enableTool(enabled=False)

    def add_action(
        self,
        icon_path: str,
        text: str,
        callback: QAction,
        parent: Optional[QWidget] = None,
    ) -> QAction:
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        if parent:
            parent.addAction(action)
        return action

    def enableTool(self, enabled: bool = True) -> None:
        allowed = False if self.lineLayerDict == dict() else True
        toggled = self.runPushButton.isChecked()
        enabled = allowed and toggled
        self.runPushButton.setEnabled(enabled)

    @pyqtSlot(bool, name="on_centerPointPushButton_toggled")
    def toggleBar(self, toggled: Optional[bool] = None) -> None:
        """
        Shows/Hides the tool bar
        """
        toggled = self.centerPointPushButton.isChecked() if toggled is None else toggled
        if toggled:
            self.splitter.show()
        else:
            self.splitter.hide()

    def resetTool(self):
        self.lineLayerDict = dict()

    def syncLayers(self, layerids):
        for lyrid in layerids:
            if lyrid not in self.lineLayerDict:
                continue
            self.lineLayerDict.pop(lyrid)

    @pyqtSlot(bool)
    def on_runPushButton_clicked(self) -> None:
        pass

    @pyqtSlot(bool)
    def on_configPushButton_clicked(self) -> None:
        pass

    def unload(self) -> None:
        self.iface.unregisterMainWindowAction(self.runPushButtonAction)
        self.iface.newProjectCreated.disconnect(self.resetTool)
        QgsProject.instance().layersWillBeRemoved.disconnect(self.syncLayers)
