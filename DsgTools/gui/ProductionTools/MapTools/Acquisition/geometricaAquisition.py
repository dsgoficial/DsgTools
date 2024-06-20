#! -*- coding: UTF-8 -*-
"""
/***************************************************************************
                             -------------------
        begin                : 2018-04-02
        git sha              : $Format:%H$
        copyright            : (C) 2017 by  Jossan Costa - Surveying Technician @ Brazilian Army
        email                : jossan.costa@eb.mil.br
 ***************************************************************************/
Some parts were inspired by QGIS plugin FreeHandEditting
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from builtins import range
from qgis.PyQt import QtCore
from qgis import core, gui
from qgis.PyQt.QtCore import Qt, QSettings
from qgis.PyQt.QtGui import QCursor, QPixmap, QColor
from qgis.gui import (
    QgsMapTool,
    QgsRubberBand,
    QgsAttributeDialog,
    QgsAttributeForm,
    QgsSnapIndicator,
)
from qgis.utils import iface
from qgis.core import (
    QgsPointXY,
    QgsFeature,
    QgsGeometry,
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsEditFormConfig,
    QgsWkbTypes,
    QgsProject,
    QgsPointLocator,
)

from DsgTools.gui.ProductionTools.MapTools.Acquisition.distanceToolTip import (
    DistanceToolTip,
)


class GeometricaAcquisition(QgsMapTool):
    def __init__(self, canvas, iface, action):
        super(GeometricaAcquisition, self).__init__(canvas)
        super(GeometricaAcquisition, self).__init__(canvas)
        self.iface = iface
        self.canvas = canvas
        self.rubberBand = None
        self.snapCursorRubberBand = None
        self.initVariable()
        self.setAction(action)
        self.minSegmentDistance = self.getMinSegmentDistance()
        self.decimals = self.getDecimals()
        self.distanceToolTip = DistanceToolTip(
            self.iface, self.minSegmentDistance, self.decimals
        )

    def getSuppressOption(self):
        qgisSettigns = QSettings()
        qgisSettigns.beginGroup("qgis/digitizing")
        setting = qgisSettigns.value("disable_enter_attribute_values_dialog")
        qgisSettigns.endGroup()
        return setting == "true"

    def setAction(self, action):
        self.toolAction = action
        self.toolAction.setCheckable(True)

    def canvasPressEvent(self, e):
        pass

    def activate(self):
        if self.toolAction:
            self.toolAction.setChecked(True)
        self.free = False
        self.cur = QCursor(
            QPixmap(
                [
                    "18 13 4 1",
                    "           c None",
                    "#          c #FF0000",
                    ".          c #FF0000",
                    "+          c #1210f3",
                    "                 ",
                    "   +++++++++++   ",
                    "  +     #     +  ",
                    " +      #      + ",
                    "+       #       +",
                    "+       #       +",
                    "++#############++",
                    "+       #       +",
                    "+       #       +",
                    " +      #      +",
                    "  +     #     +  ",
                    "   +++++++++++   ",
                    "                 ",
                ]
            )
        )
        self.canvas.setCursor(self.cur)

    def deactivate(self):
        self.initVariable()
        if self.toolAction:
            self.toolAction.setChecked(False)
        if self is not None:
            QgsMapTool.deactivate(self)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.initVariable()
        if event.key() == Qt.Key_Control:
            self.free = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.free = True
        if event.key() == Qt.Key_Backspace and self.geometry:
            self.geometry.pop()
            geom = QgsGeometry.fromPolygonXY([self.geometry])
            self.qntPoint -= 1
            self.rubberBand.setToGeometry(geom, self.iface.activeLayer())

    def getParametersFromConfig(self):
        # Método para obter as configurações da tool do QSettings
        # Parâmetro de retorno: parameters (Todas os parâmetros do QSettings usado na ferramenta)
        settings = QSettings()
        settings.beginGroup("PythonPlugins/DsgTools/Options")
        parameters = {
            "minSegmentDistance": settings.value("minSegmentDistance"),
            "rightAngleDecimals": settings.value("rightAngleDecimals"),
        }
        settings.endGroup()
        return parameters

    def initVariable(self):
        if self.rubberBand:
            self.rubberBand.reset(geometryType=self.iface.activeLayer().geometryType())
            self.rubberBand = None
        self.qntPoint = 0
        self.geometry = []
        # if self.snapCursorRubberBand:
        #     self.snapCursorRubberBand.reset(geometryType=QgsWkbTypes.PointGeometry)
        #     self.snapCursorRubberBand.hide()
        #     self.snapCursorRubberBand = None

    def getMinSegmentDistance(self):
        parameters = self.getParametersFromConfig()
        return float(parameters["minSegmentDistance"])

    def getDecimals(self):
        parameters = self.getParametersFromConfig()
        return (
            int(parameters["rightAngleDecimals"])
            if parameters["rightAngleDecimals"] is not None
            else 2
        )

    def completePolygon(self, geom, p4):
        filteredGeom = list(
            filter(lambda x: x is not None and isinstance(x, QgsPointXY), self.geometry)
        )
        if (len(geom) >= 2) and (len(geom) % 2 == 0):
            p1 = geom[1]
            p2 = geom[0]
            p3 = geom[-1]
            pf = self.lineIntersection(p1, p2, p3, p4)
            new_geom = QgsGeometry.fromPolygonXY([filteredGeom + [p4, pf]])
        else:
            new_geom = QgsGeometry.fromPolygonXY(
                [filteredGeom + [QgsPointXY(p4.x(), p4.y())]]
            )
            pf = p4
        return new_geom, pf

    def bufferDistanceTest(self, geom, penult, last):
        def isWithinLimits(pnt):
            """checks whether point is distant enough from proposed geom's
            ending points (penult and last)"""
            return (
                self.distanceToolTip.calculateDistance(last, pnt)
                >= self.minSegmentDistance
                and self.distanceToolTip.calculateDistance(penult, pnt)
                >= self.minSegmentDistance
            )

        for i in range(len(geom)):
            if not isWithinLimits(geom[i]):
                return False
        return True

    def distanceBetweenLinesTest(self, geom, p):
        teste_answer = True
        for i in range(len(geom) - 1):
            p1 = geom[i]
            p2 = geom[i + 1]
            projected_point = self.projectPoint(p1, p2, p)
            distance = self.distanceToolTip.calculateDistance(projected_point, p2)
            if distance > self.minSegmentDistance:
                continue
            else:
                teste_answer = False
                break
        return teste_answer

    def lineIntersection(self, p1, p2, p3, p4):
        p3Projected = p4
        if (p1.y() == p2.y()) or (p3.x() == p4.x()):
            y = p3Projected.y()
            x = p2.x()
            return QgsPointXY(x, y)
        if (p1.x() == p2.x()) or (p3.y() == p4.y()):
            y = p2.y()
            x = p3Projected.x()
            return QgsPointXY(x, y)
        else:
            m1 = (p1.y() - p2.y()) / (p1.x() - p2.x())
            a1 = p2.y() + p2.x() / m1
            m2 = (p3.y() - p4.y()) / (p3.x() - p4.x())
            # Reta perpendicular P3 P4 que passa por P4
            a2 = p4.y() + p4.x() / m2
            if abs(m1 - m2) > 0.01:
                # intersecao
                x = (a2 - a1) / (1 / m2 - 1 / m1)
                y = -x / m1 + a1
                return QgsPointXY(x, y)
            return False

    def projectPoint(self, p1, p2, p3):
        # reta P1 P2
        try:
            # p1 e p2 na vertical
            if p1.x() == p2.x():
                x = p3.x()
                y = p2.y()
            # p1 e p2 na horizontal
            elif p1.y() == p2.y():
                x = p2.x()
                y = p3.y()
            else:
                a = (p2.y() - p1.y()) / (p2.x() - p1.x())
                # reta perpendicular a P1P2 que passa por P2
                a2 = -1 / a
                b2 = p2.y() - a2 * p2.x()
                # reta paralela a P1P2 que passa por P3
                b3 = p3.y() - a * p3.x()
                # intersecao entre retas
                x = (b3 - b2) / (a2 - a)
                y = a * x + b3
            return QgsPointXY(x, y)
        except:
            return None

    def getRubberBand(self):
        geomType = self.iface.activeLayer().geometryType()
        if geomType == QgsWkbTypes.PolygonGeometry:
            rubberBand = QgsRubberBand(
                self.canvas, geometryType=QgsWkbTypes.PolygonGeometry
            )
            rubberBand.setFillColor(QColor(255, 0, 0, 40))
        elif geomType == QgsWkbTypes.LineGeometry:
            rubberBand = QgsRubberBand(
                self.canvas, geometryType=QgsWkbTypes.LineGeometry
            )
        rubberBand.setSecondaryStrokeColor(QColor(255, 0, 0, 200))
        rubberBand.setWidth(2)
        return rubberBand

    def getSnapRubberBand(self):
        rubberBand = QgsRubberBand(self.canvas, geometryType=QgsWkbTypes.PointGeometry)
        rubberBand.setFillColor(QColor(255, 0, 0, 40))
        rubberBand.setSecondaryStrokeColor(QColor(255, 0, 0, 200))
        rubberBand.setWidth(2)
        rubberBand.setIcon(QgsRubberBand.ICON_X)
        return rubberBand

    def setAllowedStyleSnapRubberBand(self):
        self.rubberBand.setLineStyle(Qt.PenStyle(Qt.SolidLine))
        self.rubberBand.setSecondaryStrokeColor(QColor(255, 0, 0, 200))
        self.rubberBand.setFillColor(QColor(255, 0, 0, 40))

    def setAvoidStyleSnapRubberBand(self):
        self.rubberBand.setLineStyle(Qt.PenStyle(Qt.DashDotLine))
        self.rubberBand.setSecondaryStrokeColor(QColor(255, 255, 0, 200))
        self.rubberBand.setFillColor(QColor(255, 0, 0, 40))

    def loadDefaultFields(self, layer, feature):
        attributesValues = {}
        primaryKeyIndexes = layer.dataProvider().pkAttributeIndexes()
        for fieldIndex in layer.attributeList():
            fieldName = layer.fields().field(fieldIndex).name()
            if fieldIndex in primaryKeyIndexes:
                continue
            attributeExpression = layer.defaultValueDefinition(fieldIndex).expression()
            if attributeExpression == "":
                continue
            evaluatedExpression = self.evaluateExpression(
                layer, layer.defaultValueDefinition(fieldIndex).expression()
            )
            if evaluatedExpression is None:
                feature[fieldName] = attributeExpression
                continue
            feature[fieldName] = evaluatedExpression

    def evaluateExpression(self, layer, expression):
        context = core.QgsExpressionContext()
        context.appendScopes(
            core.QgsExpressionContextUtils.globalProjectLayerScopes(layer)
        )
        return core.QgsExpression(expression).evaluate(context)

    def createGeometry(self, geom):
        geom = self.reprojectRubberBand(geom)
        if geom:
            layer = self.canvas.currentLayer()
            fields = layer.fields()
            feature = core.QgsFeature()
            feature.setFields(fields)
            feature.setGeometry(geom)

            feature.initAttributes(fields.count())
            provider = layer.dataProvider()
            for i in range(fields.count()):
                defaultClauseCandidate = provider.defaultValueClause(i)
                if defaultClauseCandidate:
                    feature.setAttribute(i, defaultClauseCandidate)

            self.loadDefaultFields(layer, feature)

            form = QgsAttributeDialog(layer, feature, False)
            form.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            form.setMode(int(QgsAttributeForm.AddFeatureMode))
            formSuppress = layer.editFormConfig().suppress()
            if formSuppress == QgsEditFormConfig.SuppressDefault:
                if (
                    self.getSuppressOption()
                ):  # this is calculated every time because user can switch options while using tool
                    layer.addFeature(feature)
                else:
                    form.exec_()
            elif formSuppress == QgsEditFormConfig.SuppressOff:
                form.exec_()
            else:
                layer.addFeature(feature)
            layer.endEditCommand()
            self.canvas.refresh()
            self.initVariable()

    def createSnapCursor(self, point):
        self.snapCursorRubberBand = self.getSnapRubberBand()
        self.snapCursorRubberBand.addPoint(point)

    def reprojectRubberBand(self, geom):
        """
        Reprojects the geometry
        geom: QgsGeometry
        """
        # Defining the crs from src and destiny
        epsg = self.canvas.mapSettings().destinationCrs().authid()
        crsSrc = QgsCoordinateReferenceSystem(epsg)
        # getting srid from something like 'EPSG:31983'
        layer = self.canvas.currentLayer()
        srid = layer.crs().authid()
        crsDest = QgsCoordinateReferenceSystem(
            srid
        )  # here we have to put authid, not srid
        # Creating a transformer
        coordinateTransformer = QgsCoordinateTransform(
            crsSrc, crsDest, QgsProject.instance()
        )
        lyrType = self.iface.activeLayer().geometryType()
        # Transforming the points
        if lyrType == QgsWkbTypes.LineGeometry:
            geomList = geom.asPolyline()
        elif lyrType == QgsWkbTypes.PolygonGeometry:
            geomList = geom.asPolygon()
        newGeom = []
        for idx, geomIdx in enumerate(geomList):
            if lyrType == QgsWkbTypes.LineGeometry:
                newGeom.append(coordinateTransformer.transform(geomIdx))
            elif lyrType == QgsWkbTypes.PolygonGeometry:
                line = geomIdx
                for i in range(len(line)):
                    point = line[i]
                    newGeom.append(coordinateTransformer.transform(point))
        if lyrType == QgsWkbTypes.LineGeometry:
            return QgsGeometry.fromPolylineXY(newGeom + [newGeom[0]])
        elif lyrType == QgsWkbTypes.PolygonGeometry:
            return QgsGeometry.fromPolygonXY([newGeom])
