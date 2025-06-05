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
    QgsProject,
    QgsCoordinateTransform,
)
from qgis.gui import (
    QgisInterface, 
    QgsMapMouseEvent
)
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.PyQt.QtGui import QPixmap, QPainter, QPen, QCursor
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QMenu, QApplication

class TrimExtendTool(AbstractSelectionTool):
    TRIM, EXTEND = range(2)
    def __init__(self, iface: QgisInterface):
        self.iface = iface
        self.toolAction = None
        self.canvas = self.iface.mapCanvas()
        super(TrimExtendTool, self).__init__(self.iface)
        self.setCursor(self.createColoredCursor(Qt.yellow, 32))
    
    def createColoredCursor(self, color, size=16):
        """Create a colored crosshair cursor"""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        pen = QPen(color, 2)
        painter.setPen(pen)
        
        # Draw crosshair
        center = size // 2
        painter.drawLine(center, 2, center, size - 2)
        painter.drawLine(2, center, size - 2, center)
        
        painter.end()
        
        return QCursor(pixmap, center, center)

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

    def getNearestVertexOnSelectedObject(
            self, 
            referenceFeat: QgsVectorLayer, 
            destinationFeature: QgsFeature
    ) -> Tuple[QgsPointXY, int]:
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
    
    def crsProjectToLayer(self) -> QgsCoordinateTransform:
        projectCrs = QgsProject.instance().crs()
        lyrCrs = self.iface.activeLayer().crs()
        if projectCrs == lyrCrs:
            return None
        coordinateTransform = QgsCoordinateTransform(
            projectCrs,
            lyrCrs,
            QgsProject.instance()
        )
        return coordinateTransform

    def getClosestVertexInDestination(
            self, 
            referenceFeat: QgsFeature, 
            destinationFeat: QgsFeature, 
            clickEvent: QgsMapMouseEvent,
    ) -> Tuple[QgsGeometry, int]:
        # TODO: tratar caso de destino polígono]
        clickPoint = self.canvas.getCoordinateTransform().toMapCoordinates(
            clickEvent.x(), clickEvent.y()
        )
        trimOrExtend = self.getMode(referenceFeat, destinationFeat)
        clickPoint = QgsGeometry.fromPointXY(clickPoint)
        rect = self.getCursorRect(clickEvent)
        rect = QgsGeometry.fromRect(rect)
        coordinateTransform = self.crsProjectToLayer()
        if coordinateTransform is not None:
            clickPoint.transform(coordinateTransform)
            rect.transform(coordinateTransform)
        referenceGeom = referenceFeat.geometry()
        destinationGeom = destinationFeat.geometry()
        closestVertexToReferenceGeom, firstOrLasterVertexInreferenceFeat = self.getNearestVertexOnSelectedObject(referenceFeat, destinationFeat)
        boundary = QgsGeometry(destinationGeom.constGet().boundary()) if destinationGeom.type() == QgsWkbTypes.GeometryType.PolygonGeometry else destinationGeom
        pointInDestinationFeat = boundary.nearestPoint(clickPoint) if trimOrExtend == self.EXTEND else referenceGeom.intersection(boundary)
        return pointInDestinationFeat, firstOrLasterVertexInreferenceFeat, rect
    
    def addVertexOnDestinationFeature(
        self,
        referenceFeat: QgsFeature,
        destinationFeat: QgsFeature,
        destinationLyr: QgsVectorLayer,
        clickEvent: QgsMapMouseEvent,
    ) -> Tuple[QgsPointXY, int]:
        trimOrExtend = self.getMode(referenceFeat, destinationFeat)
        destinationPointGeom, firstOrLasterVertexInreferenceFeat, rect = self.getClosestVertexInDestination(referenceFeat, destinationFeat, clickEvent)
        destinationGeom = destinationFeat.geometry()
        if trimOrExtend == self.TRIM:
            destinationPointGeom = destinationGeom.nearestPoint(destinationPointGeom)
        destinationPointXY = destinationPointGeom.asPoint()
        _, _, positionInsertPoint, __ = destinationGeom.closestSegmentWithContext(destinationPointXY)
        closestVertexOnDestinationGeom = QgsGeometry(destinationGeom.vertexAt(positionInsertPoint))
        if trimOrExtend == self.TRIM:
            if closestVertexOnDestinationGeom.asPoint() != destinationPointXY:
                destinationGeom.insertVertex(destinationPointXY.x(), destinationPointXY.y(), positionInsertPoint)
                destinationLyr.changeGeometry(destinationFeat.id(), destinationGeom)
            return destinationPointXY, firstOrLasterVertexInreferenceFeat
        else:
            if closestVertexOnDestinationGeom.intersects(rect):
                return closestVertexOnDestinationGeom.asPoint(), firstOrLasterVertexInreferenceFeat
            destinationGeom.insertVertex(destinationPointXY.x(), destinationPointXY.y(), positionInsertPoint)
            destinationLyr.changeGeometry(destinationFeat.id(), destinationGeom)
            return destinationPointXY, firstOrLasterVertexInreferenceFeat
    
    def getMode(self, referenceFeat: QgsFeature, destinationFeat: QgsFeature) -> int:
        geomreferenceFeat = referenceFeat.geometry()
        destinationGeom = destinationFeat.geometry()
        if geomreferenceFeat.intersects(destinationGeom):
            return self.TRIM
        return self.EXTEND

    def trimExtendFeatures(
            self, 
            destinationLyr: QgsVectorLayer, 
            destinationFeat: QgsFeature, 
            clickEvent: QgsMapMouseEvent,
    ):
        layer = self.iface.mapCanvas().currentLayer()
        if layer.crs() != destinationLyr.crs():
            self.iface.messageBar().pushMessage(
                self.tr("Error"),
                self.tr("The reference system of origin layer is difference of destination layer"),
                level=Qgis.Critical,
                duration=5
            )
            return
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
        referenceGeom = referenceFeat.geometry()
        destinationPointXY, firstOrLasterVertexInreferenceFeat = self.addVertexOnDestinationFeature(
            referenceFeat, 
            destinationFeat, 
            destinationLyr, 
            clickEvent,
        )
        if trimOrExtend == self.EXTEND:
            pointsGeomReferenceFeat = referenceGeom.asPolyline() if not referenceGeom.isMultipart() else referenceGeom.asMultiPolyline()[0] # tem que resolver o caso de multipart
            if firstOrLasterVertexInreferenceFeat == 0:
                pointsGeomReferenceFeat.insert(0, destinationPointXY)
            else:
                pointsGeomReferenceFeat.append(destinationPointXY)
            newReferenceGeom = QgsGeometry.fromPolylineXY(pointsGeomReferenceFeat)
        else:
            resultProcess, newGeomsreferenceFeat, _ = referenceGeom.splitGeometry([destinationPointXY], False)
            if resultProcess == 0 and newGeomsreferenceFeat:
                part1 = referenceGeom
                part2 = newGeomsreferenceFeat[0]
                newReferenceGeom = part1 if part1.length() > part2.length() else part2
            else:
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
                clickEvent=e,
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
            clickEvent=e,
        )
        hoveredAction = partial(
            self.createRubberBand, feature=feature, layer=layer, geom=geomType
        )
        return triggeredAction, hoveredAction
    
    def removeSelection(self, e, hasControlModifier, lyr):
        return

    def unload(self):
        pass