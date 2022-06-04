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

from functools import partial

from qgis.gui import QgsMapTool
from qgis.core import QgsProject, QgsVectorLayer

class LabelTogglingTool(QgsMapTool):
    AllLayers, SelectedLayers, ActiveLayer = range(3)
    def __init__(self, iface):
        """
        Hides or show active layers labels.
        """
        self.iface = iface       
        self.canvas = self.iface.mapCanvas()
        super(LabelTogglingTool, self).__init__(self.canvas)
    
    def addTool(self, manager, callback, parentToolbar, stackButton, iconBasePath):
        self.stackButton = stackButton

        icon_path = iconBasePath + '/toggleAllLabels.png'
        toolTip = self.tr("DSGTools: Toggle all labels visibility")
        action = manager.add_action(
            icon_path,
            text=self.tr('DSGTools: Toggle all labels visibility'),
            callback=partial(self.run, mode=LabelTogglingTool.AllLayers, iface=self.iface),
            add_to_menu=False,
            add_to_toolbar=False,
            withShortcut=True,
            tooltip=toolTip,
            parentButton=self.stackButton,
            isCheckable=False
        )
        self.setAction(action)
        self.stackButton.setDefaultAction(action)

        icon_path = iconBasePath + '/toggleSelectedLayersLabel.png'
        toolTip = self.tr("DSGTools: Toggle selected layers' labels visibility")
        action = manager.add_action(
            icon_path,
            text=self.tr("DSGTools: Toggle selected layers' label visibility"),
            callback=partial(self.run, mode=LabelTogglingTool.SelectedLayers, iface=self.iface),
            add_to_menu=False,
            add_to_toolbar=False,
            withShortcut=True,
            tooltip=toolTip,
            parentButton=self.stackButton,
            isCheckable=False
        )
        self.setAction(action) 

        icon_path = iconBasePath + '/toggleActiveLayerLabel.png'
        toolTip = self.tr("DSGTools: Toggle active layer' label visibility")
        action = manager.add_action(
            icon_path,
            text=self.tr("DSGTools: Toggle active layer' label visibility"),
            callback=partial(self.run, mode=LabelTogglingTool.ActiveLayer, iface=self.iface),
            add_to_menu=False,
            add_to_toolbar=False,
            withShortcut=True,
            tooltip=toolTip,
            parentButton=self.stackButton,
            isCheckable=False
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
                self.deactivate()
        except:
            pass

    def run(self, iface, mode=None):
        """
        Activate tool.
        """
        mode = LabelTogglingTool.AllLayers if mode is None else mode
        try:
            self.stackButton.setDefaultAction(self.sender())
        except:
            pass
        for lyr in self.getLayers(iface, mode): #ordered layers
            if not isinstance(lyr, QgsVectorLayer):
                continue
            lyr.setLabelsEnabled(not lyr.labelsEnabled())
        self.canvas.refresh()

    def getLayers(self, iface, mode):
        if mode == LabelTogglingTool.AllLayers:
            return QgsProject.instance().layerTreeRoot().checkedLayers()
        elif mode == LabelTogglingTool.SelectedLayers:
            return self.iface.layerTreeView().selectedLayers()
        elif mode == LabelTogglingTool.ActiveLayer:
            return [iface.activeLayer()]
        else:
            return []

    def unload(self):
        self.deactivate()
        del self
