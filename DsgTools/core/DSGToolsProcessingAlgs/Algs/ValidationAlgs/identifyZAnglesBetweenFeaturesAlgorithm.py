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
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterNumber, QgsProject, QgsWkbTypes, 
                       QgsProcessingMultiStepFeedback)

from .validationAlgorithm import ValidationAlgorithm


class identifyZAnglesBetweenFeaturesAlgorithm(ValidationAlgorithm):

    INPUT = 'INPUT'
    ANGLE = 'ANGLE'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input'),
                [
                    QgsProcessing.TypeVectorLine,
                    QgsProcessing.TypeVectorPolygon,
                ]
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
        inputSource = self.parameterAsSource(parameters, self.INPUT, context)
        angle = self.parameterAsDouble(parameters, self.ANGLE, context)
        featsToAnalyse = list()

        crs = QgsProject.instance().crs()
        self.fields = QgsFields()
        self.fields.append(QgsField('source', QVariant.String))

        sink, dest_id = self.parameterAsSink(parameters, self.OUTPUT, context, self.fields,
            QgsWkbTypes.LineString, crs)
        
        nSteps = 2 if QgsWkbTypes.geometryType(inputSource.wkbType()) == QgsWkbTypes.LineGeometry else 1
        multiStepFeedback = feedback if nSteps == 1 else QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0

        if  QgsWkbTypes.geometryType(inputSource.wkbType()) == QgsWkbTypes.LineGeometry:
            multiStepFeedback.setProgressText(self.tr("Evaluating z within lines"))
            multiStepFeedback.setCurrentStep(currentStep)
            featsToAnalyse.extend(self.caseBetweenLines(inputSource, angle, feedback=multiStepFeedback))
            currentStep += 1
            multiStepFeedback.setProgressText(self.tr("Evaluating z within features geometries"))
            multiStepFeedback.setCurrentStep(currentStep)
            featsToAnalyse.extend(self.caseInternLine(inputSource, angle, feedback=multiStepFeedback))
            currentStep += 1
        else:
            multiStepFeedback.setProgressText(self.tr("Evaluating z within polygons"))
            featsToAnalyse.extend(self.caseInternArea(inputSource, angle, feedback=multiStepFeedback))

        sink.addFeatures(featsToAnalyse)

        return {
            self.OUTPUT: dest_id
            }

    def caseInternLine(self, lines, angle, feedback=None):
        featsToAnalyse = []
        lineCount = lines.featureCount()
        if lineCount == 0:
            return featsToAnalyse
        total = 100 / lineCount
        for current, feat in enumerate(lines.getFeatures()):
            if feedback is not None and feedback.isCanceled():
                break
            vertices = feat.geometry().vertices()
            v1 = next(vertices) if vertices.hasNext() else None
            v2 = next(vertices) if vertices.hasNext() else None
            v3 = next(vertices) if vertices.hasNext() else None
            for v4 in vertices:
                newFeat = self.checkIntersectionAndCreateFeature4p(v1, v2, v3, v4, angle) if all((v1,v2,v3,v4)) else None
                if newFeat:
                    newFeat.setAttribute('source',lines.sourceName())
                    featsToAnalyse.append(newFeat)
                v1,v2,v3 = v2,v3,v4
            if feedback is not None:
                feedback.setProgress(current * total)
        return featsToAnalyse

    def caseInternArea(self, areas, angle, feedback=None):
        featsToAnalyse = []
        areaCount = areas.featureCount()
        if areaCount == 0:
            return featsToAnalyse
        total = 100/areaCount
        for current, feat in enumerate(areas.getFeatures()):
            if feedback is not None and feedback.isCanceled():
                break
            geom = feat.geometry()
            multiPolygons = geom.asMultiPolygon()[0] if geom.isMultipart() else geom.asPolygon()
            for vertices in multiPolygons:
                for i in range(len(vertices)-3):
                    v1, v2, v3, v4 = vertices[i:i+4]
                    newFeat = self.checkIntersectionAndCreateFeature4p(v1, v2, v3, v4, angle) if all((v1,v2,v3,v4)) else None
                    if newFeat:
                        newFeat.setAttribute('source',areas.sourceName())
                        featsToAnalyse.append(newFeat)
                newFeat = self.checkIntersectionAndCreateFeature4p(vertices[-3], vertices[-2],vertices[-1], vertices[1], angle)
                if newFeat:
                    featsToAnalyse.append(newFeat)
            if feedback is not None:
                feedback.setProgress(current * total)
        return featsToAnalyse

    def caseBetweenLines(self, lines, angle, feedback=None):
        featsToAnalyse = []
        lineCount = lines.featureCount()
        if lineCount == 0:
            return featsToAnalyse
        total = 100 / lineCount
        for i, feat1 in enumerate(lines.getFeatures()):
            if feedback is not None and feedback.isCanceled():
                break
            gfeat1 = feat1.geometry()
            request = QgsFeatureRequest().setFilterRect(gfeat1.boundingBox())
            for j, feat2 in enumerate(lines.getFeatures(request)):
                if i >= j:
                    continue
                gfeat2 = feat2.geometry()
                if gfeat1.intersects(gfeat2):
                    if len(list(gfeat1.vertices())) > 2:
                        toAnalyse = self.checkIfIntersectionIsValid2g(gfeat1, gfeat2, angle)
                        if isinstance(toAnalyse, tuple):
                            toAnalyse = (x for x in toAnalyse if x)
                            for feat in toAnalyse:
                                feat.setAttribute('source',lines.sourceName())
                                featsToAnalyse.append(feat)
                        elif toAnalyse:
                            toAnalyse.setAttribute('source',lines.sourceName())
                            featsToAnalyse.append(toAnalyse)
                    # Gets the case when the z angle is created by 3 feats (at least one has only two vertices)
                    elif len(list(gfeat1.vertices())) == 2:
                        request2 = QgsFeatureRequest().setFilterRect(gfeat2.boundingBox())
                        for k, feat3 in enumerate(lines.getFeatures(request2)):
                            if any([(k > i), (k > j)]):
                                continue
                            gfeat3 = feat3.geometry()
                            if not gfeat3.touches(gfeat1):
                                toAnalyse = self.checkIfIntersectionIsValid3g(gfeat1, gfeat2, gfeat3, angle)
                                if isinstance(toAnalyse, tuple):
                                    toAnalyse = (x for x in toAnalyse if x)
                                    for feat in toAnalyse:
                                        feat.setAttribute('source',lines.sourceName())
                                        featsToAnalyse.append(feat)
                                elif toAnalyse:
                                    toAnalyse.setAttribute('source',lines.sourceName())
                                    featsToAnalyse.append(toAnalyse)
            if feedback is not None:
                feedback.setProgress(i * total)
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
        return 'identifyzanglesbetweenfeatures'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Z Angles Between Features')

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
        return QCoreApplication.translate('identifyZAnglesBetweenFeaturesAlgorithm', string)

    def createInstance(self):
        return identifyZAnglesBetweenFeaturesAlgorithm()
