# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2021-06-08
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Jossan Costa - Surveying Technician @ Brazilian Army
                               (C) 2022 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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
from qgis import core
from qgis.gui import QgsMapTool
from qgis.utils import iface
from qgis.PyQt.QtCore import QObject


class FilterTools(QgsMapTool):
    def __init__(self, iface):
        """
        Hides or show active layers labels.
        """
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        super(FilterTools, self).__init__(self.canvas)
        self.actionList = []

    def addTool(self, manager, callback, parentToolbar, stackButton, iconBasePath):
        self.stackButton = stackButton
        icon_path = iconBasePath + "/filter.svg"
        toolTip = self.tr("DSGTools: Filter Selected")
        action = manager.add_action(
            icon_path,
            text=self.tr("DSGTools: Filter Selected"),
            callback=self.filterSelections,
            add_to_menu=False,
            add_to_toolbar=False,
            withShortcut=True,
            tooltip=toolTip,
            parentButton=stackButton,
            isCheckable=False,
        )
        self.actionList.append(action)

        icon_path = iconBasePath + "/filterByGeomtries.png"
        toolTip = self.tr("DSGTools: Filter All Using the Selected Feature's Geometry")
        action = manager.add_action(
            icon_path,
            text=self.tr("DSGTools: Filter All Using the Selected Feature's Geometry"),
            callback=self.filterBySelectedGeometries,
            add_to_menu=False,
            add_to_toolbar=False,
            withShortcut=True,
            tooltip=toolTip,
            parentButton=stackButton,
            isCheckable=False,
        )
        self.actionList.append(action)

        icon_path = iconBasePath + "/removeSpatialFilter.png"
        toolTip = self.tr("DSGTools: Remove Filters")
        action = manager.add_action(
            icon_path,
            text=self.tr("DSGTools: Remove Filters"),
            callback=self.cleanAllFilters,
            add_to_menu=False,
            add_to_toolbar=False,
            withShortcut=True,
            tooltip=toolTip,
            parentButton=stackButton,
            isCheckable=False,
        )
        self.actionList.append(action)

    def unload(self):
        for action in self.actionList:
            self.iface.unregisterMainWindowAction(action)
        del self

    def setCurrentActionOnStackButton(self):
        try:
            self.stackButton.setDefaultAction(self.sender())
        except:
            pass

    def cleanAllFilters(self):
        self.setCurrentActionOnStackButton()
        loadedLayers = core.QgsProject.instance().mapLayers().values()
        showMessage = False
        for layer in loadedLayers:
            if layer.isEditable():
                showMessage = True
            layer.setSubsetString("")
        iface.mapCanvas().refresh()
        if showMessage:
            iface.messageBar().pushMessage(
                "Attention",
                "Enabled layers for edition have not been unfiltered.",
                level=core.Qgis.Info,
                duration=3,
            )

    def filterBySelectedGeometries(self):
        self.setCurrentActionOnStackButton()
        layer = iface.activeLayer()
        if not layer:
            return
        selectedFeatures = layer.selectedFeatures()
        if not selectedFeatures:
            return
        if not (layer.geometryType() == core.QgsWkbTypes.PolygonGeometry):
            return
        multiPolygon = core.QgsMultiPolygon()
        for feature in selectedFeatures:
            for geometry in feature.geometry().asGeometryCollection():
                multiPolygon.addGeometry(geometry.constGet().clone())
        multiPolygon = core.QgsGeometry(multiPolygon).makeValid()
        textFilter = "(geom && st_geomfromewkt('SRID={0};{1}') ) AND st_relate(geom, st_geomfromewkt('SRID={0};{1}'), 'T********')".format(
            layer.crs().authid().split(":")[-1], multiPolygon.asWkt()
        )
        layersBacklist = ["aux_moldura_a"]
        loadedLayers = core.QgsProject.instance().mapLayers().values()
        for loadedLayer in loadedLayers:
            if (
                not isinstance(loadedLayer, core.QgsVectorLayer)
                or loadedLayer.dataProvider().name() != "postgres"
                or loadedLayer.dataProvider().uri().table() in layersBacklist
            ):
                continue
            loadedLayer.setSubsetString(textFilter)
        iface.mapCanvas().refresh()

    def filterSelections(self):
        self.setCurrentActionOnStackButton()
        layer = iface.activeLayer()
        if not layer:
            return
        selectedFeatures = layer.selectedFeatures()
        if not selectedFeatures:
            return
        primaryKeyIndex = layer.primaryKeyAttributes()[0]
        primaryKeyName = layer.fields().names()[primaryKeyIndex]
        layer.setSubsetString(
            '"{0}" in ({1})'.format(
                primaryKeyName,
                ",".join(
                    [
                        "'{}'".format(str(i[primaryKeyName]))
                        if not isinstance(i[primaryKeyName], int)
                        else str(i[primaryKeyName])
                        for i in selectedFeatures
                    ]
                ),
            )
        )
