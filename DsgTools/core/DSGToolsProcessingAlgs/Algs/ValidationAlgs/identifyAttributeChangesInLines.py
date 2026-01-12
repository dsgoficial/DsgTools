# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-28
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Pedro Martins- Cartographic Engineer @ Brazilian Army
        email                : souza.pedromartins@eb.mil.br
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
from typing import List
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSink,
    QgsPointXY,
    QgsFeature,
    QgsProcessingParameterVectorLayer,
    QgsFeatureRequest,
    QgsGeometryUtils,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsGeometry,
    QgsLineString,
    QgsExpression,
    QgsWkbTypes,
    QgsVectorLayer,
    QgsProcessingContext,
    QgsFeedback,
    QgsProcessingMultiStepFeedback,
)
import math
from .validationAlgorithm import ValidationAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class IdentifyAttributeChangesInLines(ValidationAlgorithm):

    INPUT_LAYER = "INPUT_LAYER"
    INPUT_FIELDS = "INPUT_FIELDS"
    INPUT_ANGLE = "INPUT_ANGLE"
    INPUT_MAX_SIZE = "INPUT_MAX_SIZE"
    FLAGS = "OUTPUT"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LAYER,
                self.tr("Input Layer"),
                types=[QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.INPUT_FIELDS,
                self.tr("Fields to consider"),
                type=QgsProcessingParameterField.Any,
                parentLayerParameterName="INPUT_LAYER",
                allowMultiple=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_ANGLE,
                self.tr("Maximum angle between lines"),
                type=QgsProcessingParameterNumber.Double,
                minValue=0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_MAX_SIZE,
                self.tr("Maximum size"),
                type=QgsProcessingParameterNumber.Double,
                optional=True,
                minValue=0,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        inputFields = self.parameterAsFields(parameters, self.INPUT_FIELDS, context)
        angle = self.parameterAsDouble(parameters, self.INPUT_ANGLE, context)
        maxLength = self.parameterAsDouble(parameters, self.INPUT_MAX_SIZE, context)
        algRunner = AlgRunner()
        self.prepareFlagSink(parameters, layer, QgsWkbTypes.MultiPoint, context)
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        inputLyr = self.makeLyrCache(layer, algRunner, context, multiStepFeedback)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        currentStep += 1
        nFeats = inputLyr.featureCount()
        if inputLyr is None or nFeats == 0:
            return {self.FLAGS: self.flag_id}
        if feedback is not None:
            stepSize = 100 / nFeats
        if maxLength > 0:
            expr = QgsExpression("$length < " + str(maxLength))
            allFeatures = inputLyr.getFeatures(QgsFeatureRequest(expr))
        else:
            allFeatures = inputLyr.getFeatures()
        pointsAndFields = []
        for current, feature in enumerate(allFeatures):
            if multiStepFeedback.isCanceled():
                return {self.FLAGS: self.flag_id}
            featGeom = feature.geometry()
            geometry = featGeom.constGet()
            if featGeom.isMultipart():
                for line in geometry:
                    ptFin = QgsGeometry.fromPointXY(QgsPointXY(line[-1]))
            else:
                ptFin = QgsGeometry.fromPointXY(QgsPointXY(geometry[-1]))
            lineTouched = self.linesTouchedOnPoint(inputLyr, feature, ptFin)
            if len(lineTouched) == 0:
                continue
            smallerAngle = 360
            for lineToBeSelected in lineTouched:
                angMinus180 = abs(
                    self.anglesBetweenLines(feature, lineToBeSelected, ptFin) - 180
                )
                if angMinus180 < smallerAngle:
                    smallerAngle = angMinus180
                    line = lineToBeSelected
            changedFields = []
            if self.anglesBetweenLines(feature, line, ptFin) < (
                180 + angle
            ) and self.anglesBetweenLines(feature, line, ptFin) > (180 - angle):
                changedFields = self.getChangedFields(inputFields, feature, line)
                FieldsNames = self.getFieldsNames(changedFields, feature, line)
                if len(changedFields) == 0:
                    continue
                if [ptFin, FieldsNames] not in pointsAndFields:
                    pointsAndFields.append([ptFin, FieldsNames])
            multiStepFeedback.setProgress(current * stepSize)
        multiStepFeedback.setCurrentStep(currentStep)
        currentStep += 1
        newPointsAndFields = self.filterFlagsInMultipleIntersectionsCenario(
            pointsAndFields, inputLyr, inputFields, multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(currentStep)
        if len(newPointsAndFields) == 0:
            return {self.FLAGS: self.flag_id}
        for ptAndF in newPointsAndFields:
            pt = ptAndF[0]
            flagText = ptAndF[1]
            self.flagFeature(pt, flagText)
        return {self.FLAGS: self.flag_id}

    def makeLyrCache(
        self,
        layer: QgsVectorLayer,
        algRunner: AlgRunner,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> QgsVectorLayer:
        localCache = algRunner.runCreateFieldWithExpression(
            inputLyr=layer,
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=feedback,
            is_child_algorithm=False,
        )
        algRunner.runCreateSpatialIndex(
            localCache, context, feedback, is_child_algorithm=True
        )
        return localCache

    def linesTouchedOnPoint(
        self, layer: QgsVectorLayer, feature: QgsFeature, point
    ) -> List[QgsFeature]:
        lines = []
        geomFeature = feature.geometry()
        AreaOfInterest = geomFeature.boundingBox()
        request = QgsFeatureRequest().setFilterRect(AreaOfInterest)
        for feat in layer.getFeatures(request):
            geomFeat = feat.geometry()
            if geomFeat.intersects(point):
                wktFeature = geomFeature.asWkt()
                wktFeat = geomFeat.asWkt()
                if wktFeat == wktFeature:
                    continue
                lines.append(feat)
        return lines

    def adjacentPoint(self, line: QgsFeature, point) -> QgsPointXY:
        if isinstance(line, QgsFeature):
            geometry = line.geometry()
        elif isinstance(line, QgsLineString):
            geometry = QgsGeometry(line)
        else:
            print('oi')
            pass
        vertexPoint = geometry.closestVertexWithContext(point)[1]
        adjpoints = geometry.adjacentVertices(vertexPoint)
        adjptvertex = adjpoints[0]
        if adjptvertex < 0:
            adjptvertex = adjpoints[1]
        adjpt = geometry.vertexAt(adjptvertex)
        return QgsPointXY(adjpt)

    def anglesBetweenLines(
        self, line1: QgsFeature, line2: QgsFeature, point: QgsGeometry
    ):
        pointB = QgsPointXY(point.asPoint())
        pointA = self.adjacentPoint(line1, pointB)
        pointC = self.adjacentPoint(line2, pointB)
        angleRad = QgsGeometryUtils().angleBetweenThreePoints(
            pointA.x(), pointA.y(), pointB.x(), pointB.y(), pointC.x(), pointC.y()
        )
        angle = math.degrees(angleRad)

        return abs(angle)

    def getChangedFields(self, inputFields, feature1, feature2):
        changedFields = []
        for field in inputFields:
            if not feature1[field] == feature2[field]:
                changedFields.append(field)
        return changedFields

    def getFieldsNames(self, inputFields, feature1, feature2):
        text = ""
        for field in inputFields:
            value1 = feature1[field]
            value2 = feature2[field]
            if text == "":
                text = str(field) + ": " + str(value1) + " e " + str(value2)
            else:
                text += ", " + str(field) + ": " + str(value1) + " e " + str(value2)
        return text

    def filterFlagsInMultipleIntersectionsCenario(
        self,
        pointsAndFields,
        lineLayer: QgsVectorLayer,
        inputFields,
        feedback: QgsFeedback = None,
    ):
        pointsToBeRemoved = []
        if feedback is not None:
            stepSize = 100 / len(pointsAndFields) if len(pointsAndFields) else 0
        for current, point in enumerate(pointsAndFields):
            if feedback is not None and feedback.isCanceled():
                break
            lineAndPointArray = []
            for line in lineLayer.getFeatures():
                lineGeom = line.geometry()
                geometry = lineGeom.constGet()
                if lineGeom.isMultipart():
                    for l in geometry:
                        ptFin = QgsGeometry.fromPointXY(QgsPointXY(l[-1]))
                        ptIni = QgsGeometry.fromPointXY(QgsPointXY(l[0]))
                else:
                    ptFin = QgsGeometry.fromPointXY(QgsPointXY(geometry[-1]))
                    ptIni = QgsGeometry.fromPointXY(QgsPointXY(geometry[0]))
                if ptFin.intersects(point[0]):
                    lineAndPointArray.append([line, ptFin])
                if ptIni.intersects(point[0]):
                    lineAndPointArray.append([line, ptIni])
            smallerAngle = 360
            for i in range(len(lineAndPointArray) - 1):
                lineA = lineAndPointArray[i][0]
                for j in range(i + 1, len(lineAndPointArray)):
                    lineB = lineAndPointArray[j][0]
                    angMinus180 = abs(
                        self.anglesBetweenLines(lineA, lineB, lineAndPointArray[i][1])
                        - 180
                    )
                    if angMinus180 < smallerAngle:
                        smallerAngle = angMinus180
                        line1 = lineA
                        line2 = lineB
            fieldsChanged = []
            fieldsChanged = self.getChangedFields(inputFields, line1, line2)
            if len(fieldsChanged) == 0:
                pointsToBeRemoved.append(point)
            if feedback is not None:
                feedback.setProgress(current * stepSize)
        newPoints = [pt for pt in pointsAndFields if pt not in pointsToBeRemoved]
        return newPoints

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return IdentifyAttributeChangesInLines()

    def name(self):
        """
        Here is where the processing itself takes place.
        """
        return "identifyattributechangesinlines"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Attribute Changes In Lines")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Attribute Handling")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Attribute Handling"

    def shortHelpString(self):
        return self.tr(
            "O algoritmo identifica se existe alguma mudança de atributos entre linhas nos campos escolhidos e dentro da tolerância para continuidade"
        )
