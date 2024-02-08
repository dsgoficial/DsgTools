# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-06-28
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Pedro Martins - Cartographic Engineer @ Brazilian Army
        email                : pedromartins.souza@eb.mil.br
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

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSink,
    QgsWkbTypes,
    QgsGeometry,
    QgsProcessingParameterNumber,
    QgsProcessingMultiStepFeedback,
    QgsFeedback,
    QgsProcessingContext,
    QgsVectorLayer,
    QgsProcessingParameterVectorLayer,
)

from .validationAlgorithm import ValidationAlgorithm


class IdentifyIntertwinedLinesAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    COMPARE_INPUT = "COMPARE_INPUT"
    TOLERANCE = "TOLERANCE"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT, self.tr("Input lines"), [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.COMPARE_INPUT,
                self.tr("Compare lines"),
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE,
                self.tr("Tolerance"),
                QgsProcessingParameterNumber.Integer,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.algRunner = AlgRunner()
        inputSource = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        compareInputSource = self.parameterAsVectorLayer(
            parameters, self.COMPARE_INPUT, context
        )
        tolerance = self.parameterAsInt(parameters, self.TOLERANCE, context)
        self.prepareFlagSink(parameters, inputSource, QgsWkbTypes.MultiPoint, context)
        nFeats = inputSource.featureCount()
        nCompareFeats = compareInputSource.featureCount()
        if (
            inputSource is None
            or compareInputSource is None
            or nFeats == 0
            or nCompareFeats == 0
        ):
            return {self.FLAGS: self.flag_id}
        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        inputLyr = self.makeLyrCache(inputSource, context, multiStepFeedback)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        compareLyr = self.makeLyrCache(compareInputSource, context, multiStepFeedback)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        intersectionsSet = self.getIntersections(
            inputLyr, compareLyr, tolerance, context, multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        nIntersections = len(intersectionsSet)
        if nIntersections == 0:
            return {self.FLAGS: self.flag_id}
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        stepSize = 100 / nIntersections
        for current, intersection in enumerate(intersectionsSet):
            if feedback is not None and feedback.isCanceled():
                return {self.FLAGS: self.flag_id}
            flagText = f"More than {tolerance} intersections"
            self.flagFeature(intersection, flagText)
            multiStepFeedback.setProgress(current * stepSize)
        return {self.FLAGS: self.flag_id}

    def makeLyrCache(
        self,
        layer: QgsVectorLayer,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> QgsVectorLayer:
        localCache = self.algRunner.runCreateFieldWithExpression(
            inputLyr=layer,
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=feedback,
            is_child_algorithm=False,
        )
        self.algRunner.runCreateSpatialIndex(
            localCache, context, feedback, is_child_algorithm=True
        )
        return localCache

    def getIntersections(
        self,
        layer1: QgsVectorLayer,
        layer2: QgsVectorLayer,
        tolerance,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ):
        dict1 = {feat1["featid"]: feat1 for feat1 in layer1.getFeatures()}
        dict2 = {feat2["featid"]: feat2 for feat2 in layer2.getFeatures()}
        if feedback is not None:
            multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
        else:
            multiStepFeedback = None
        joinedLyr = self.algRunner.runJoinAttributesByLocation(
            inputLyr=layer1,
            joinLyr=layer2,
            context=context,
            predicateList=[6],  # cross
            discardNonMatching=True,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        geomWkbList = []
        intersectionsSet = set()
        nFeat = joinedLyr.featureCount()
        if nFeat == 0:
            return intersectionsSet
        stepSize = 100 / nFeat
        for current, feat in enumerate(joinedLyr.getFeatures()):
            if feedback is not None and feedback.isCanceled():
                return {self.FLAGS: self.flag_id}
            feat1 = dict1[feat["featid"]]
            geom1 = feat1.geometry()
            geomWkb1 = geom1.asWkb()
            feat2 = dict2[feat["featid_2"]]
            geom2 = feat2.geometry()
            geomWkb2 = geom2.asWkb()
            geomWkbSet = {geomWkb1, geomWkb2}
            if geomWkbSet in geomWkbList:
                continue
            geomWkbList.append(geomWkbSet)
            intersections = geom1.intersection(geom2)
            intersections.convertToMultiType()
            if intersections.isEmpty():
                continue
            if intersections.wkbType() == QgsWkbTypes.MultiLineString:
                points = []
                for line in intersections.asMultiPolyline():
                    points.extend(line)
                geom = QgsGeometry()
                intersections = geom.fromMultiPointXY(points)
            multiPoint = intersections.asMultiPoint()
            if len(multiPoint) >= tolerance:
                intersectionsSet.add(intersections)
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)
        return intersectionsSet

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyintertwinedlines"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Intertwined Lines")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Line Handling")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Line Handling"

    def shortHelpString(self):
        return self.tr(
            "Verifica linhas entrelaçadas: linhas que se cruzam mais vezes que a tolerância. Retorna os pontos de interseção."
        )

    def tr(self, string):
        return QCoreApplication.translate("IdentifyIntertwinedLinesAlgorithm", string)

    def createInstance(self):
        return IdentifyIntertwinedLinesAlgorithm()
