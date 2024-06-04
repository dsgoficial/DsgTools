# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-04-12
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luizclaudio.andrade@eb.mil.br
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

from collections import Counter, defaultdict
from PyQt5.QtCore import QCoreApplication
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from qgis.core import (
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsFeature,
    QgsDataSourceUri,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingParameterBoolean,
    QgsProcessingFeatureSourceDefinition,
    QgsProcessingMultiStepFeedback,
)

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.GeometricTools.featureHandler import FeatureHandler


class DeaggregatorAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input layer"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)

        algRunner = AlgRunner()
        paramDict = LayerHandler().getDestinationParameters(inputLyr)
        featHandler = FeatureHandler()

        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)

        cacheLyr = algRunner.runCreateFieldWithExpression(
            inputLyr=inputLyr
            if not onlySelected
            else QgsProcessingFeatureSourceDefinition(inputLyr.id(), True),
            expression="$id",
            fieldType=1,
            fieldName="_featid",
            feedback=multiStepFeedback,
            context=context,
        )

        nFeats = cacheLyr.featureCount()
        if nFeats == 0:
            return {}
        
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        deaggregatedLyr = algRunner.runMultipartToSingleParts(
            inputLayer=cacheLyr,
            context=context,
            feedback=multiStepFeedback
        )

        deaggregatedFeatureCount = deaggregatedLyr.featureCount()
        if deaggregatedFeatureCount == nFeats or deaggregatedFeatureCount == 0:
            return {}

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        itemCounter = Counter(f["_featid"] for f in deaggregatedLyr.getFeatures())
        candidateIdList = [k for k, v in itemCounter.items() if v > 1]
        nCandidates = len(candidateIdList)
        if nCandidates == 0:
            return {}

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        inputLyr.startEditing()
        inputLyr.beginEditCommand(f"Updating layer {inputLyr.name()}")
        stepSize = 100 / nCandidates
        featuresToAdd = []
        for current, feature in enumerate(inputLyr.getFeatures(candidateIdList)):
            if multiStepFeedback.isCanceled():
                return {}
            if not feature.geometry():
                inputLyr.deleteFeature(feature.id())
                feedback.setProgress(int(current * stepSize))
                continue
            updtGeom, newFeatList, update = featHandler.handleFeature(
                [feature], feature, inputLyr, paramDict
            )
            if not update:
                feature.setGeometry(updtGeom)
                inputLyr.updateFeature(feature)
                featuresToAdd += newFeatList
            feedback.setProgress(int(current * stepSize))
        if featuresToAdd:
            inputLyr.addFeatures(featuresToAdd, QgsFeatureSink.FastInsert)
        inputLyr.endEditCommand()
        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "deaggregategeometries"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Deaggregate Geometries")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Geometric Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Geometric Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("DeaggregatorAlgorithm", string)

    def createInstance(self):
        return DeaggregatorAlgorithm()
