# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2023-05-17
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
                                   2023 by Pedro Martins - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
                               pedromartins.souza@eb.mil.br
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


from PyQt5.QtWidgets import QToolTip
from qgis.core import (QgsCoordinateTransformContext, QgsDistanceArea,
                       QgsGeometry, QgsProject, QgsUnitTypes, QgsVectorLayer,
                       QgsWkbTypes)
from qgis.gui import QgisInterface, QgsMapToolDigitizeFeature
from qgis.PyQt.QtCore import QEvent, QObject, QRect, Qt
from qgis.PyQt.QtWidgets import QPushButton


class MeasureTool(QObject):
    def __init__(self, iface: QgisInterface):
        """
        Hides or show active layers labels.
        """
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        super(MeasureTool, self).__init__()
        self.toolAction = None
        self.distance_area = QgsDistanceArea()
        self.acquisitionTooltipButton = QPushButton()
        self.acquisitionTooltipButton.setToolTip(self.tr("Show acquisition tooltip"))
        self.pointList = PointList()
        self.eventFilter = None

    def addTool(self, manager, callback, parentToolbar, stackButton, iconBasePath):
        self.stackButton = stackButton
        icon_path = iconBasePath + "/measure_tool.png"
        toolTip = self.tr("DSGTools: Measure while digitizing")
        action = manager.add_action(
            icon_path,
            text=self.tr("DSGTools: Measure while digitizing"),
            callback=self.activateTool,
            add_to_menu=False,
            add_to_toolbar=True,
            withShortcut=True,
            tooltip=toolTip,
            parentButton=stackButton,
            isCheckable=True,
        )
        self.setAction(action)

    def activateTool(self):
        state = self.toolAction.isChecked()
        if state:
            self.canvas.mapToolSet.connect(self.activateFilterMapTool)
            if not isinstance(self.canvas.mapTool(), QgsMapToolDigitizeFeature):
                return
        else:
            try:
                self.canvas.mapToolSet.disconnect(self.activateFilterMapTool)
            except TypeError:
                pass
        self.activateFilter(state)

    def activateFilterMapTool(self, mapTool):
        state = isinstance(mapTool, QgsMapToolDigitizeFeature)
        self.activateFilter(state)

    def setToolEnabled(self):
        layer = self.iface.activeLayer()
        if (
            not isinstance(layer, QgsVectorLayer)
            or layer.geometryType() == QgsWkbTypes.PointGeometry
            or not layer.isEditable()
        ):
            enabled = False
        else:
            enabled = True
        if not enabled:
            self.closeAndRemoveEventFilter()
            self.toolAction.setChecked(False)
        self.toolAction.setEnabled(enabled)
        return enabled

    def activateFilter(self, state: bool):
        if state:
            self.eventFilter = EventFilter(self.iface, self.pointList)
            self.canvas.viewport().setMouseTracking(True)
            self.canvas.viewport().installEventFilter(self.eventFilter)
            self.canvas.installEventFilter(self.eventFilter)
        else:
            self.closeAndRemoveEventFilter()

    def setAction(self, action):
        self.toolAction = action
        self.toolAction.setCheckable(True)
        self.setToolEnabled()

    def closeAndRemoveEventFilter(self):
        if self.eventFilter is None:
            return
        self.eventFilter.close()
        self.canvas.viewport().removeEventFilter(self.eventFilter)
        self.canvas.removeEventFilter(self.eventFilter)
        self.eventFilter = None
        try:
            self.canvas.mapToolSet.disconnect(self.activateFilterMapTool)
        except TypeError:
            pass

    def unload(self):
        self.closeAndRemoveEventFilter()

class PointList(list):
    def __init__(self):
        list.__init__(self)

    def empty(self):
        self[:] = []

    def newPoint(self):
        if len(self) > 0:
            self.insert(0, self[0])

    def updateCurrentPoint(self, point):
        if len(self) > 0:
            self[0] = point
        else:
            self.insert(0, point)

    def previousPoint(self):
        if len(self) > 1:
            return self[1]
        else:
            return None

    def removeLastPoint(self):
        if len(self) > 1:
            del self[1]

class EventFilter(QObject):
    def __init__(self, iface: QgisInterface, pointList: PointList):
        QObject.__init__(self)
        self.iface = iface
        self.mapCanvas = iface.mapCanvas()
        self.pointList = pointList
        self.dist_area = QgsDistanceArea()
        projCrs = QgsProject.instance().crs()
        self.dist_area.setSourceCrs(projCrs, QgsCoordinateTransformContext())
        ellipsoidAcronym = projCrs.ellipsoidAcronym()
        if ellipsoidAcronym != "":
            self.dist_area.setEllipsoid(ellipsoidAcronym)

    def close(self):
        pass

    def eventFilter(self, obj, event):
        if not event.spontaneous():
            return QObject.eventFilter(self, obj, event)
        if (
            (
                event.type() == QEvent.MouseButtonPress
                and event.button() == Qt.LeftButton
            )
            or (
                event.type() == QEvent.MouseButtonRelease
                and event.button() == Qt.LeftButton
            )
            or (event.type() == QEvent.MouseMove and event.button() != Qt.MidButton)
        ):
            curPoint = (
                self.iface.mapCanvas()
                .getCoordinateTransform()
                .toMapCoordinates(event.pos())
            )
            self.updateMeasure()
            self.pointList.updateCurrentPoint(curPoint)
        if (
            event.type() == QEvent.MouseButtonRelease
            and event.button() == Qt.LeftButton
        ):
            self.pointList.newPoint()
        elif event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
                self.pointList.removeLastPoint()
            elif event.key() == Qt.Key_Escape:
                self.pointList.empty()
        elif (
            event.type() == QEvent.MouseButtonRelease
            and event.button() == Qt.RightButton
        ):
            self.pointList.empty()
        return QObject.eventFilter(self, obj, event)

    def updateMeasure(self):
        length, distAcum = None, None
        area = None
        if (
            self.iface.mapCanvas().currentLayer().geometryType()
            == QgsWkbTypes.LineGeometry
        ):
            if len(self.pointList) > 1:
                line_dist = QgsGeometry.fromPolylineXY(self.pointList[:2])
                length = line_dist.length()
            line_acum = QgsGeometry.fromPolylineXY(self.pointList)
            measure_distAcum = self.dist_area.measureLength(line_acum)
            distAcum = self.dist_area.convertLengthMeasurement(
                measure_distAcum, QgsUnitTypes.DistanceMeters
            )
            tooltip = QToolTip
            if length != None or length == 0:
                measure_dist = self.dist_area.measureLength(line_dist)
                dist = self.dist_area.convertLengthMeasurement(
                    measure_dist, QgsUnitTypes.DistanceMeters
                )
                txt = f"<b>Parcial: {dist:.3f} m</b><br/><b>Total: {distAcum:.3f} m</b></p>"
                tooltip.showText(
                    self.mapCanvas.mapToGlobal(self.mapCanvas.mouseLastXY()),
                    txt,
                    self.mapCanvas,
                    QRect(),
                    5000,
                )
            else:
                tooltip.hideText()
        elif (
            self.iface.mapCanvas().currentLayer().geometryType()
            == QgsWkbTypes.PolygonGeometry
        ):
            tempPointList = []
            if len(self.pointList) > 2:
                tempPointList = self.pointList[:]
                tempPointList.append(self.pointList[0])
                polygon = QgsGeometry.fromPolygonXY([tempPointList])
                area = polygon.area()
            if area != None:
                measure_area = self.dist_area.measureArea(polygon)
                area = self.dist_area.convertAreaMeasurement(
                    measure_area, QgsUnitTypes.AreaSquareMeters
                )
                txt = f"<b>Area: {area:.3f}m²</b></p>"
                QToolTip.showText(
                    self.mapCanvas.mapToGlobal(self.mapCanvas.mouseLastXY()),
                    txt,
                    self.mapCanvas,
                )
            else:
                QToolTip.hideText()
