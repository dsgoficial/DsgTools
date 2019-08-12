# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2019-08-12
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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
from functools import partial

from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.core import QgsProject, QgsVectorLayer
from qgis.PyQt.QtCore import Qt, QSettings
from qgis.PyQt.QtGui import QColor, QCursor
from qgis.PyQt.QtWidgets import QMenu, QApplication

from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler

class LabelTogglingTool(QgsMapTool):
    def __init__(self, iface):
        """
        Hides or show active layers labels.
        """
        self.iface = iface       
        self.canvas = self.iface.mapCanvas()
        QgsMapTool.__init__(self, self.canvas)
         
    
    def addTool(self, manager, callback, parentMenu, iconBasePath):
        icon_path = iconBasePath + '/toggleLabels.png'
        toolTip = self.tr("DSGTools: Toggle all labels visibility")
        action = manager.add_action(
            icon_path,
            text=self.tr('DSGTools: Toggle all labels visibility'),
            callback=self.run,
            add_to_menu=False,
            add_to_toolbar=True,
            withShortcut = True,
            tooltip = toolTip,
            parentToolbar =parentMenu,
            isCheckable = False
        )
        self.setAction(action)    

    def setAction(self, action):
        self.toolAction = action
            
    def deactivate(self):
        """
        Deactivate tool.
        """
        try:
            if self is not None:
                QgsMapTool.deactivate(self)
        except:
            pass

    def run(self):
        """
        Activate tool.
        """
        visibleLayers = QgsProject.instance().layerTreeRoot().checkedLayers()
        for lyr in self.iface.mapCanvas().layers(): #ordered layers
            if not isinstance(lyr, QgsVectorLayer) or lyr not in visibleLayers:
                continue
            lyr.setLabelsEnabled(not lyr.labelsEnabled())
        self.iface.mapCanvas().refresh()

    def unload(self):
        self.deactivate()
