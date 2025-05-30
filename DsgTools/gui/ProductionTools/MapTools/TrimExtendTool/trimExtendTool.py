# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2025-05-27
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Matheus Alves Silva - Cartographic Engineer @ Brazilian Army
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

from qgis.PyQt.QtCore import QSettings, QObject

from qgis.core import (
    QgsVectorLayer,
    QgsWkbTypes,
    Qgis,
    QgsGeometry,
    QgsPointXY,
)

from qgis.gui import QgisInterface, QgsMapTool

class TrimExtendTool(QgsMapTool):
    def __init__(self, iface: QgisInterface):
        self.iface = iface
        self.toolAction = None
        self.canvas = self.iface.mapCanvas()
        super(TrimExtendTool, self).__init__(self.canvas)

    def addTool(self, manager, callback, parentMenu, iconBasePath):
        icon_path = iconBasePath + "/closedLines.png"
        toolTip = self.tr("DSGTools: Trim Extend")
        action = manager.add_action(
            icon_path,
            text=toolTip,
            callback=callback,
            add_to_menu=False,
            add_to_toolbar=True,
            withShortcut=True,
            tooltip=toolTip,
            parentToolbar=parentMenu,
        )
        self.setAction(action)
    
    def setAction(self, action) -> None:
        self.toolAction = action
    
    def activate(self):
        """
        Activates tool.
        """
        if self.toolAction:
            self.toolAction.setChecked(False)
    
    def setToolEnabled(self, layer: QgsVectorLayer=None) -> bool:
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
    
    def checkFirstLastVertexEquals(self, firstVertex, lastVertex):
        if firstVertex == lastVertex:
            QMessageBox.warning(
                self.iface.mainWindow(),
                self.tr("Warning!"),
                self.tr(
                    "The baseline is closed, it must be open."
                ),
            )
            return

    def vertexBaseLineCloser(self, baseLine, featConnected):
        geomFeatConnected = featConnected.geometry()
        verticesBaseLineList = list(baseLine.vertices())
        firstVertex = verticesBaseLineList[0]
        lastVertex = verticesBaseLineList[-1]
        self.checkFirstLastVertexEquals(firstVertex, lastVertex)
        distanceFirstVertexFeatConnected = QgsGeometry.fromPointXY(QgsPointXY(firstVertex)).distance(geomFeatConnected)
        distanceLastVertexFeatConnected = QgsGeometry.fromPointXY(QgsPointXY(lastVertex)).distance(geomFeatConnected)
        if distanceFirstVertexFeatConnected < distanceLastVertexFeatConnected:
            return firstVertex, 'FIRST'
        return lastVertex, 'LAST'
    
    def pointInLineClosestVertex(self, baseLine, featConnected):
        geomFeatConnected = featConnected.geometry()
        vertexClosestBaseLine, firstOrLasterVertexInBaseLine = self.vertexBaseLineCloser(baseLine, featConnected)
        distanceVertexToBaseLine = geomFeatConnected.lineLocatePoint(vertexClosestBaseLine)
        pointInFeatConnected = geomFeatConnected.interpolate(distanceVertexToBaseLine)
        return pointInFeatConnected, firstOrLasterVertexInBaseLine
    
    def addAndReturnVertex(self, baseLine, featConnected):
        pointInFeatConnectedXY, firstOrLasterVertexInBaseLine = self.pointInLineClosestVertex(baseLine, featConnected).asPoint()
        geomFeatConnected = featConnected.geometry()
        _, _, positionInsertPoint, _ = geomFeatConnected.closestSegmentWithContext(pointInFeatConnectedXY)
        geomFeatConnected.insertVertex(pointInFeatConnectedXY.x(), pointInFeatConnectedXY.y(), positionInsertPoint)
        layerConnected.changeGeometry(featConnected.id(), geomFeatConnected) # Camada depende de qual vai ser a feição a ser ligada
        return pointInFeatConnectedXY, firstOrLasterVertexInBaseLine
    
    def checkTrimOrExtend(self, baseLine, featConnected):
        geomBaseLine = baseLine.geometry()
        geomFeatConnected = featConnected.geometry()
        if geomBaseLine.intersects(geomFeatConnected):
            return 'TRIM'
        return 'EXTEND'
    
    def connectFeatures(self, baseLine, featConnected):
        trimOrExtend = self.checkTrimOrExtend(baseLine, featConnected)
        newVertex, firstOrLasterVertexInBaseLine = self.addAndReturnVertex(baseLine, featConnected)
        geomBaseLine = baseLine.geometry()
        geomFeatConnected = featConnected.geometry()
        if trimOrExtend == "EXTEND":
            pointsGeomBaseLine = geomBaseLine.asPolyline()
            if firstOrLasterVertexInBaseLine == 'FIRST':
                pointsGeomBaseLine.insert(0, newVertex)
            else:
                pointsGeomBaseLine.append(newVertex)
            newGeomBaseLine = QgsGeometry.fromPolylineXY(pointsGeomBaseLine)
        else:
            _, _, positionInsertPoint, _ = geomFeatConnected.closestSegmentWithContext(newVertex)
            geomBaseLine.insertVertex(newVertex.x(), newVertex.y(), positionInsertPoint)
            resultProcess, newGeomsBaseLine, _ = geomBaseLine.splitGeometry([newVertex], False)
            if resultProcess == 0 and newGeomBaseLine:
                part1 = geomBaseLine
                part2 = newGeomsBaseLine[0]
                if part1.length() > part2.length():
                    newGeomBaseLine = part1
                else:
                    newGeomBaseLine = part2
            else:
                print("Algum erro aconteceu!")
                return
        layerBaseLine.changeGeometry(baseLine.id(), newGeomBaseLine)

    def verifyOneFeatureSelected(self):
        layer = self.iface.mapCanvas().currentLayer()
        numberSelectedFeatures = layer.selectedFeatureCount()
        if numberSelectedFeatures != 1:
            self.iface.messageBar().pushMessage(
                self.tr("Error"),
                self.tr("Select only one feature"),
                level=Qgis.Critical, 
                duration=5
            )
            return

    def trimExtendFeatures(self):
        self.verifyOneFeatureSelected()
        # self.connectFeatures(baseLine, featConnected)

    def unload(self):
        pass