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

from functools import partial
from typing import Tuple
from DsgTools.gui.ProductionTools.MapTools.GenericSelectionTool.genericSelectionTool import AbstractSelectionTool

from qgis.core import (
    QgsVectorLayer,
    QgsWkbTypes,
    Qgis,
    QgsGeometry,
    QgsPointXY,
    QgsFeature,
)

from qgis.gui import QgisInterface
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QMenu, QApplication

class TrimExtendTool(AbstractSelectionTool):
    TRIM, EXTEND = range(2)
    def __init__(self, iface: QgisInterface):
        self.iface = iface
        self.toolAction = None
        self.canvas = self.iface.mapCanvas()
        super(TrimExtendTool, self).__init__(self.iface)

    def addTool(self, manager, callback, parentMenu, iconBasePath):
        icon_path = iconBasePath + "/trim_extend_icon.png"
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
            isCheckable=True,
        )
        self.setAction(action)
    
    def setAction(self, action) -> None:
        self.toolAction = action

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

    def getNearestVertexOnSelectedObject(self, referenceFeat: QgsVectorLayer, destinationFeature: QgsFeature):
        destinationGeom = destinationFeature.geometry()
        verticesreferenceFeatList = list(referenceFeat.geometry().vertices())
        firstVertex, lastVertex = verticesreferenceFeatList[0], verticesreferenceFeatList[-1]
        if firstVertex == lastVertex:
            QMessageBox.warning(
                self.iface.mainWindow(),
                self.tr("Warning!"),
                self.tr(
                    "The referenceFeat is closed, it must be open."
                ),
            )
            return
        distanceFirstVertexdestinationFeat = QgsGeometry.fromPointXY(QgsPointXY(firstVertex)).distance(destinationGeom)
        distanceLastVertexdestinationFeat = QgsGeometry.fromPointXY(QgsPointXY(lastVertex)).distance(destinationGeom)
        if distanceFirstVertexdestinationFeat < distanceLastVertexdestinationFeat:
            return firstVertex, 0
        return lastVertex, -1
    
    def getClosestVertexInDestination(self, referenceFeat, destinationFeat):
        # TODO: tratar caso de destino polígono
        destinationGeom = destinationFeat.geometry()
        closestVertexToReferenceGeom, firstOrLasterVertexInreferenceFeat = self.getNearestVertexOnSelectedObject(referenceFeat, destinationFeat)
        if destinationGeom.type() == QgsWkbTypes.GeometryType.PolygonGeometry:
            distanceVertexToreferenceFeat = QgsGeometry(destinationGeom.constGet().boundary()).lineLocatePoint(QgsGeometry(closestVertexToReferenceGeom))
        else:
            distanceVertexToreferenceFeat = destinationGeom.lineLocatePoint(QgsGeometry(closestVertexToReferenceGeom))
        pointIndestinationFeat = destinationGeom.interpolate(distanceVertexToreferenceFeat)
        return pointIndestinationFeat, firstOrLasterVertexInreferenceFeat
    
    def addVertexOnDestinationFeature(
        self,
        referenceFeat: QgsFeature,
        destinationFeat: QgsFeature,
        destinationLyr: QgsVectorLayer
    ) -> Tuple[QgsPointXY, int]:
        destinationPointGeom, firstOrLasterVertexInreferenceFeat = self.getClosestVertexInDestination(referenceFeat, destinationFeat)
        destinationPointXY = destinationPointGeom.asPoint()
        geomdestinationFeat = destinationFeat.geometry()
        _, _, positionInsertPoint, _ = geomdestinationFeat.closestSegmentWithContext(destinationPointXY)
        geomdestinationFeat.insertVertex(destinationPointXY.x(), destinationPointXY.y(), positionInsertPoint)
        destinationLyr.changeGeometry(destinationFeat.id(), geomdestinationFeat) # Camada depende de qual vai ser a feição a ser ligada
        return destinationPointXY, firstOrLasterVertexInreferenceFeat
    
    def getMode(self, referenceFeat: QgsFeature, destinationFeat: QgsFeature) -> int:
        geomreferenceFeat = referenceFeat.geometry()
        geomdestinationFeat = destinationFeat.geometry()
        if geomreferenceFeat.intersects(geomdestinationFeat):
            return self.TRIM
        return self.EXTEND

    def get_closest_boundary_line(self, polygon, reference_point):
        """
        Get the closest boundary line from a polygon (exterior or interior ring)
        
        Args:
            polygon: QgsPolygon object
            reference_point: QgsPoint or QgsGeometry to measure distance from
        
        Returns:
            tuple: (closest_linestring, distance, is_exterior)
        """
        
        min_distance = float('inf')
        
        # Check exterior ring
        exterior_ring = polygon.exteriorRing()
        if exterior_ring:
            exterior_geom = QgsGeometry(exterior_ring.clone())
            distance = reference_point.distance(exterior_geom)
            
            if distance < min_distance:
                min_distance = distance
        
        # Check all interior rings (holes)
        for i in range(polygon.numInteriorRings()):
            interior_ring = polygon.interiorRing(i)
            if interior_ring:
                interior_geom = QgsGeometry(interior_ring.clone())
                distance = reference_point.distance(interior_geom)
                
                if distance < min_distance:
                    min_distance = distance
        
        return min_distance

    def trimExtendFeatures(self, destinationLyr: QgsVectorLayer, destinationFeat: QgsFeature):
        layer = self.iface.mapCanvas().currentLayer()
        numberSelectedFeatures = layer.selectedFeatureCount()
        if numberSelectedFeatures != 1:
            self.iface.messageBar().pushMessage(
                self.tr("Error"),
                self.tr("Select only one feature on the origin layer"),
                level=Qgis.Critical, 
                duration=5
            )
            return
        referenceFeat = [i for i in layer.getSelectedFeatures()][0]
        trimOrExtend = self.getMode(referenceFeat, destinationFeat)
        newVertex, firstOrLasterVertexInreferenceFeat = self.addVertexOnDestinationFeature(referenceFeat, destinationFeat, destinationLyr)
        referenceGeom = referenceFeat.geometry()
        geomdestinationFeat = destinationFeat.geometry()
        if trimOrExtend == self.EXTEND:
            pointsGeomreferenceFeat = referenceGeom.asPolyline() if not referenceGeom.isMultipart() else referenceGeom.asMultiPolyline()[0] # tem que resolver o caso de multipart
            if firstOrLasterVertexInreferenceFeat == 0:
                pointsGeomreferenceFeat.insert(0, newVertex)
            else:
                pointsGeomreferenceFeat.append(newVertex)
            newReferenceGeom = QgsGeometry.fromPolylineXY(pointsGeomreferenceFeat)
        else:
            _, _, positionInsertPoint, _ = geomdestinationFeat.closestSegmentWithContext(newVertex)
            referenceGeom.insertVertex(newVertex.x(), newVertex.y(), positionInsertPoint)
            resultProcess, newGeomsreferenceFeat, _ = referenceGeom.splitGeometry([newVertex], False)
            if resultProcess == 0 and newReferenceGeom:
                part1 = referenceGeom
                part2 = newGeomsreferenceFeat[0]
                newReferenceGeom = part1 if part1.length() > part2.length() else part2
            else:
                print("Algum erro aconteceu!")
                return
        if QgsWkbTypes.isMultiType(layer.wkbType()):
            newReferenceGeom.convertToMultiType()
        layer.changeGeometry(referenceFeat.id(), newReferenceGeom)
    
    def createContextMenu(self, e, geometryFilter=None):
        super().createContextMenu(
            e=e,
            geometryFilter=[
                QgsWkbTypes.LineGeometry, QgsWkbTypes.PolygonGeometry
            ] 
        )
    
    def performTask(self, e, lyrFeatDict):
        moreThanOneFeat = (
            len(list(lyrFeatDict.values())) > 1
            or len(list(lyrFeatDict.values())[0]) > 1
        )
        if moreThanOneFeat:
            # if there are overlapping features (valid candidates only)
            (
                selectedFeaturesDict,
                notSelectedFeaturesDict,
            ) = self.checkSelectedFeaturesOnDict(menuDict=lyrFeatDict)
            self.setContextMenuStyle(
                e=e,
                dictMenuSelected=selectedFeaturesDict,
                dictMenuNotSelected=notSelectedFeaturesDict,
            )
        else:
            layer = list(lyrFeatDict.keys())[0]
            feature = lyrFeatDict[layer][0]
            self.trimExtendFeatures(
                destinationFeat=feature,
                destinationLyr=layer,
            )
    
    def setContextMenuStyle(self, e, dictMenuSelected, dictMenuNotSelected):
        """
        Defines how many "submenus" the context menu should have.
        There are 3 context menu scenarios to be handled:
        :param e: (QMouseEvent) mouse event on canvas.
        :param dictMenuSelected: (dict) dictionary of classes and its selected features being treatead.
        :param dictMenuNotSelected: (dict) dictionary of classes and its non selected features being treatead.
        """
        # finding out filling conditions
        menuDict = dictMenuNotSelected
        menu = QMenu()
        self.createSubmenu(
            e=e,
            parentMenu=menu,
            menuDict=menuDict,
            genericAction=None,
            selectAll=False,
        )
        menu.exec_(self.canvas.viewport().mapToGlobal(e.pos()))
    
    def getCallbackMultipleFeatures(self, e, dictLayerFeature, selectAll=True):
        """
        Sets the callback of an action with a list features as target.
        :param e: (QMouseEvent) mouse event on canvas.
        :param dictLayerFeature: (dict) dictionary containing layers/features to be treated.
        :return: (tuple-of function_lambda) callbacks for triggered and hovered signals.
        """
        triggeredAction = partial(
            lambda x: print("hop"),
            dictLayerFeature=dictLayerFeature,
        )
        # to trigger "Hover" signal on QMenu for the multiple options
        hoveredAction = partial(
            self.createMultipleRubberBand, dictLayerFeature=dictLayerFeature
        )
        return triggeredAction, hoveredAction

    def getCallback(self, e, layer, feature, geomType=None, selectAll=True):
        """
        Gets the callback for an action.
        :param e: (QMouseEvent) mouse event on canvas.
        :param layer: (QgsVectorLayer) layer to be treated.
        :param feature: (QgsFeature) feature to be treated.
        :param geomType: (int) code indicating layer geometry type. It is retrieved OTF in case it's not given.
        :return: (tuple-of function_lambda) callbacks for triggered and hovered signals.
        """
        triggeredAction = partial(
            self.trimExtendFeatures,
            destinationLyr=layer,
            destinationFeat=feature,
        )
        hoveredAction = partial(
            self.createRubberBand, feature=feature, layer=layer, geom=geomType
        )
        return triggeredAction, hoveredAction
    
    def removeSelection(self, e, hasControlModifier, lyr):
        return

    def unload(self):
        pass