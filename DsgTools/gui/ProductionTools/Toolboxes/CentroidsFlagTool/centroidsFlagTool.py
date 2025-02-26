# -*- coding: utf-8 -*-
"""
/***************************************************************************
InspectFeatures
                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2025-02-26
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Matheus Alves Silva @ Brazilian Army
        email                : matheus.alvessilva@eb.mil.br
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
from qgis.PyQt.QtWidgets import QMessageBox, QSpinBox, QAction, QDockWidget
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QSettings, pyqtSignal, pyqtSlot, QObject, Qt
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.Qt import QObject

from qgis.core import (
    QgsMapLayer,
    Qgis,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeatureRequest,
    QgsWkbTypes,
    QgsProject,
)
from qgis.gui import QgsMessageBar

from .centroidsFlagTool_ui import Ui_CentroidFlagsDockWidget


class CentroidFlagsDockWidget(QDockWidget, Ui_CentroidFlagsDockWidget):
    def __init__(self, iface, parent=None):
        """
        Constructor
        """
        super(CentroidFlagsDockWidget, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.iface = iface


    def unload(self):
        pass

    def getToolState(self) -> dict:
        pass

    def setToolState(self, stateDict: dict) -> bool:
        pass
