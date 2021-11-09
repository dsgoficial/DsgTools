# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-11
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Eliton - Cartographic Engineer @ Brazilian Army
        email                : eliton.filho@eb.mil.br
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

import math

from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsFeature, QgsFeatureRequest, QgsField, QgsFields,
                       QgsGeometry, QgsGeometryUtils, QgsPoint, QgsPointXY,
                       QgsProcessing, QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterNumber, QgsProject, QgsWkbTypes)

from .validationAlgorithm import ValidationAlgorithm


class identifyZAnglesBetweenLayersAlgorithm(ValidationAlgorithm):

    INPUT_LINES = 'INPUT_LINES'
    INPUT_AREAS = 'INPUT_AREAS'
    ANGLE = 'ANGLE'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LINES,
                self.tr('Select line layers to be verified'),
                layerType=QgsProcessing.TypeVectorLine,
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_AREAS,
                self.tr('Select area layers to be verified'),
                layerType=QgsProcessing.TypeVectorPolygon,
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ANGLE,
                self.tr('Minimum angle'),
                QgsProcessingParameterNumber.Double,
                defaultValue=300,
                minValue=270,
                maxValue=360
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Flags')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        lines = self.parameterAsLayerList(parameters, self.INPUT_LINES, context)
        areas = self.parameterAsLayerList(parameters, self.INPUT_AREAS, context)
        angle = self.parameterAsDouble(parameters, self.ANGLE, context)

        crs = QgsProject.instance().crs()
        self.fields = QgsFields()
        self.fields.append(QgsField('source', QVariant.String))

        sink, _ = self.parameterAsSink(parameters, self.OUTPUT, context, self.fields,
            QgsWkbTypes.LineString, crs)

        caseBetweenLines = self.caseBetweenLines(lines, angle)

        featsToAnalyse = [
            *self.caseInternLine(lines, angle),
            *self.caseInternArea(areas, angle),
            *caseBetweenLines
            ]
        sink.addFeatures(featsToAnalyse)

        return {self.OUTPUT: sink}

    def caseInternLine(self, layers, angle):
        featsToAnalyse = []
        for layer in layers:
            for feat in layer.getFeatures():
                vertices = feat.geometry().vertices()
                v1 = next(vertices) if vertices.hasNext() else None
                v2 = next(vertices) if vertices.hasNext() else None
                v3 = next(vertices) if vertices.hasNext() else None
                for v4 in vertices:
                    newFeat = self.checkIntersectionAndCreateFeature4p(v1, v2, v3, v4, angle) if all((v1,v2,v3,v4)) else None
                    if newFeat:
                        newFeat.setAttribute('source',layer.name())
                        featsToAnalyse.append(newFeat)
                    v1,v2,v3 = v2,v3,v4
        return featsToAnalyse

    def caseInternArea(self, layers, angle):
        featsToAnalyse = []
        for layer in layers:
            for feat in layer.getFeatures():
                multiPolygons = feat.geometry().asMultiPolygon()[0]
                for vertices in multiPolygons:
                    for i in range(len(vertices)-3):
                        v1, v2, v3, v4 = vertices[i:i+4]
                        newFeat = self.checkIntersectionAndCreateFeature4p(v1, v2, v3, v4, angle) if all((v1,v2,v3,v4)) else None
                        if newFeat:
                            newFeat.setAttribute('source',layer.name())
                            featsToAnalyse.append(newFeat)
                    newFeat = self.checkIntersectionAndCreateFeature4p(vertices[-3], vertices[-2],vertices[-1], vertices[1], angle)
                    if newFeat:
                        featsToAnalyse.append(newFeat)
        return featsToAnalyse

    def caseBetweenLines(self, layers, angle):
        featsToAnalyse = []
        for i in range(0, len(layers)):
            for feat1 in layers[i].getFeatures():
                gfeat1 = feat1.geometry()
                request = QgsFeatureRequest().setFilterRect(gfeat1.boundingBox())
                for j in range(i, len(layers)):
                    for feat2 in layers[j].getFeatures(request):
                        gfeat2 = feat2.geometry()
                        if gfeat1.intersects(gfeat2):
                            if len(list(gfeat1.vertices())) > 2:
                                toAnalyse = self.checkIfIntersectionIsValid2g(gfeat1, gfeat2, angle)
                                if isinstance(toAnalyse, tuple):
                                    toAnalyse = (x for x in toAnalyse if x)
                                    for feat in toAnalyse:
                                        if i==j:
                                            feat.setAttribute('source',layers[i].name())
                                        else:
                                            feat.setAttribute('source',f'{layers[i].name()}/{layers[j].name()}')
                                        featsToAnalyse.append(feat)
                                elif toAnalyse:
                                    if i==j:
                                        toAnalyse.setAttribute('source',layers[i].name())
                                    else:
                                        toAnalyse.setAttribute('source',f'{layers[i].name()}/{layers[j].name()}')
                                    featsToAnalyse.append(toAnalyse)
                            # Gets the case when the z angle is created by 3 feats (at least one has only two vertices)
                            elif len(list(gfeat1.vertices())) == 2:
                                request2 = QgsFeatureRequest().setFilterRect(gfeat2.boundingBox())
                                for k in range(i, len(layers)):
                                    for feat3 in layers[k].getFeatures(request2):
                                        gfeat3 = feat3.geometry()
                                        if not gfeat3.touches(gfeat1):
                                            toAnalyse = self.checkIfIntersectionIsValid3g(gfeat1, gfeat2, gfeat3, angle)
                                            if isinstance(toAnalyse, tuple):
                                                toAnalyse = (x for x in toAnalyse if x)
                                                for feat in toAnalyse:
                                                    if i==j:
                                                        feat.setAttribute('source',layers[i].name())
                                                    else:
                                                        feat.setAttribute('source',f'{layers[i].name()}/{layers[j].name()}')
                                                    featsToAnalyse.append(feat)
                                            elif toAnalyse:
                                                if i==j:
                                                    toAnalyse.setAttribute('source',layers[i].name())
                                                else:
                                                    toAnalyse.setAttribute('source',f'{layers[i].name()}/{layers[j].name()}')
                                                featsToAnalyse.append(toAnalyse)
        return featsToAnalyse

    def checkIntersectionAndCreateFeature4p(self, v1, v2, v3, v4, angle):
        angle1 = QgsGeometryUtils.angleBetweenThreePoints(v1.x(), v1.y(), v2.x(), v2.y(), v3.x(), v3.y())
        angle2 = QgsGeometryUtils.angleBetweenThreePoints(v2.x(), v2.y(), v3.x(), v3.y(), v4.x(), v4.y())
        angle1 = math.degrees(angle1)
        angle2 = math.degrees(angle2)
        if (angle1 > angle and angle2 < 360 - angle) or (angle1 < 360 - angle and angle2 > angle):
            newFeat = QgsFeature(self.fields)
            if isinstance(v1, QgsPoint):
                newFeat.setGeometry(QgsGeometry.fromPolyline([v1,v2,v3,v4]))
            elif isinstance(v1, QgsPointXY):
                newFeat.setGeometry(QgsGeometry.fromPolylineXY([v1,v2,v3,v4]))
            return newFeat

    def checkIfIntersectionIsValid2g(self, g1, g2, angle):
        intersection = g1.intersection(g2)
        if intersection.wkbType() != QgsWkbTypes.Point:
            return False
        intersection = intersection.asPoint()

        _, g1VertexIdx, g1PreviousVertexIdx, g1NextVertexIdx, _ = g1.closestVertex(intersection)
        _, g2VertexIdx, g2PreviousVertexIdx, g2NextVertexIdx, _ = g2.closestVertex(intersection)

        vg1 = list(g1.vertices())
        vg2 = list(g2.vertices())

        # Intersections between beginning / end of v1 and v2
        if g1NextVertexIdx == g2PreviousVertexIdx == -1:
            feat = self.checkIntersectionAndCreateFeature4p(vg1[g1PreviousVertexIdx-1], vg1[g1PreviousVertexIdx], vg1[g1VertexIdx], vg2[g2NextVertexIdx], angle)
            return feat

        elif g2NextVertexIdx == g1PreviousVertexIdx == -1:
            feat = self.checkIntersectionAndCreateFeature4p(vg2[g2PreviousVertexIdx], vg2[g2VertexIdx], vg1[g1NextVertexIdx], vg1[g1NextVertexIdx+1], angle)
            return feat

    def checkIfIntersectionIsValid3g(self, g1, g2, g3, angle):
        inter12 = g1.intersection(g2)
        inter23 = g2.intersection(g3)
        if any((inter12.wkbType() != QgsWkbTypes.Point, inter23.wkbType() != QgsWkbTypes.Point)):
            return False
        inter12 = inter12.asPoint()
        inter23 = inter23.asPoint()

        _, g1VertexIdx, g1PreviousVertexIdx, g1NextVertexIdx, _ = g1.closestVertex(inter12)
        _, g3VertexIdx, g3PreviousVertexIdx, g3NextVertexIdx, _ = g3.closestVertex(inter23)

        vg1 = list(g1.vertices())
        vg3 = list(g3.vertices())

        # Intersections between beginning / end of v1 and v2
        if g1NextVertexIdx == g3PreviousVertexIdx == -1:
            feat = self.checkIntersectionAndCreateFeature4p(vg1[g1PreviousVertexIdx], vg1[g1VertexIdx], vg3[g3VertexIdx], vg3[g3NextVertexIdx], angle)
            return feat

        elif g3NextVertexIdx == g1PreviousVertexIdx == -1:
            feat = self.checkIntersectionAndCreateFeature4p(vg3[g3PreviousVertexIdx], vg3[g3VertexIdx], vg1[g1VertexIdx], vg1[g1NextVertexIdx], angle)
            return feat


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifyzanglesbetweenlayersalgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Z angles Between Layers')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Quality Assurance Tools (Identification Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Quality Assurance Tools (Identification Processes)'

    def tr(self, string):
        return QCoreApplication.translate('identifyZAnglesBetweenLayersAlgorithm', string)

    def createInstance(self):
        return identifyZAnglesBetweenLayersAlgorithm()
