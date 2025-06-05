# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2021-06-08
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Matheus Alves Silva - Cartographic Engineer @ Brazilian Army
        email                :  matheus.alvessilva@eb.mil.br
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
from qgis.PyQt import QtCore
from typing import Set
from qgis.core import (
    Qgis,
    QgsVectorLayer,
    QgsWkbTypes,
)
from qgis.gui import QgsMapTool
from qgis.utils import iface

class SmoothLinesTool(QgsMapTool):
    def __init__(self, iface):
        self.iface = iface
        self.toolAction = None
        self.canvas = self.iface.mapCanvas()
        super(SmoothLinesTool, self).__init__(self.canvas)

    def addTool(
            self, 
            manager, 
            callback, 
            parentMenu, 
            iconBasePath,
            parentButton=None,
            defaultButton=False,
        ):
        self.parentButton=parentButton
        icon_path = iconBasePath + "/smoothLines.png"
        toolTip = self.tr("DSGTools: Smooth Selected Lines")
        action = manager.add_action(
            icon_path,
            text=self.tr("DSGTools: Smooth Selected Lines"),
            callback=callback,
            add_to_menu=False,
            add_to_toolbar=False,
            withShortcut=True,
            tooltip=toolTip,
            parentToolbar=parentMenu,
            parentButton=parentButton,
        )
        self.setAction(action)
        if defaultButton:
            self.parentButton.setDefaultAction(action)

    def activate(self):
        """
        Activates tool.
        """
        if self.toolAction:
            self.toolAction.setChecked(False)

    def setAction(self, action):
        """
        Defines an action for tool.
        action: QAction to be set.
        """
        self.toolAction = action

    def setToolEnabled(self, layer=None):
        """
        Checks if it is possible to use tool given layer editing conditions and type.
        :param layer: (QgsVectorLayer) layer that may have its lines closed.
        :return: (bool) whether tool may be used.
        """
        if not isinstance(layer, QgsVectorLayer):
            layer = self.iface.mapCanvas().currentLayer()
        if (
            not layer
            or not isinstance(layer, QgsVectorLayer)
            or layer.geometryType() != QgsWkbTypes.LineGeometry
            or not layer.isEditable()
        ):
            enabled = False
        else:
            enabled = True
        self.toolAction.setEnabled(enabled) if self.toolAction else None
        return enabled
    
    def getParametersFromConfig(self):
        # Método para obter as configurações da tool do QSettings
        # Parâmetro de retorno: parameters (Todas os parâmetros do QSettings usado na ferramenta)
        settings = QtCore.QSettings()
        settings.beginGroup("PythonPlugins/DsgTools/Options")
        numberSmoothingIterations = settings.value("numberSmoothingIterations")
        fractionLineCreateNewVertices = settings.value("fractionLineCreateNewVertices")
        settings.endGroup()
        return int(numberSmoothingIterations), float(fractionLineCreateNewVertices)

    def smoothSelectedLines(self):
        layer = iface.activeLayer()
        if not layer:
            iface.messageBar().pushMessage(
                self.tr("Error"), 
                self.tr("Select a valid layer"), 
                level=Qgis.Critical, 
                duration=5
            )
            return
        selectedFeatures = layer.selectedFeatureCount()
        if selectedFeatures == 0:
            iface.messageBar().pushMessage(
                self.tr("Error"),
                self.tr("Select at least one feature in the source layer"), 
                level=Qgis.Critical, 
                duration=5
            )
            return
        numberSmoothingIterations, fractionLineCreateNewVertices = self.getParametersFromConfig()
        for feat in layer.selectedFeatures():
            geom = feat.geometry()
            geom_smooth = geom.smooth(numberSmoothingIterations, fractionLineCreateNewVertices)
            feat.setGeometry(geom_smooth)
            layer.updateFeature(feat)
        iface.mapCanvas().refresh()
        return (True, '')
    
    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.canvas.unsetMapTool(self)

    def unload(self):
        self.deactivate()
        try:
            self.iface.unregisterMainWindowAction(self.toolAction)
        except:
            pass