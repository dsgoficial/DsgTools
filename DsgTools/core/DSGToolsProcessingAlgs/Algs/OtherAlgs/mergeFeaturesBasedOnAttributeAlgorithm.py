# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-06-13
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Pedro Martins - Cartographic Engineer @ Brazilian Army
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

import re
from datetime import datetime

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsCoordinateTransform,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterField,
    QgsProcessingParameterString,
    QgsProcessingParameterVectorLayer,
    QgsProject,
    QgsProcessingParameterFeatureSink,
)

from ...algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler


class MergeFeaturesBasedOnAttributeAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    MERGE = "MERGE"
    MATCH_FIELD_1 = "MATCH_FIELD_1"
    MATCH_FIELD_2 = "MATCH_FIELD_2"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input Layer"),
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.MATCH_FIELD_1,
                self.tr("Match field 1"),
                parentLayerParameterName=self.INPUT,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.MERGE,
                self.tr("Merge Layer"),
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.MATCH_FIELD_2,
                self.tr("Match field 2"),
                parentLayerParameterName=self.MERGE,
            )
        )

        # self.addParameter(
        #     QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Merged Layer"))
        # )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        matchField1 = self.parameterAsFields(parameters, self.MATCH_FIELD_1, context)[0]
        mergeLyr = self.parameterAsVectorLayer(parameters, self.MERGE, context)
        if mergeLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.MERGE)
            )
        matchField2 = self.parameterAsFields(parameters, self.MATCH_FIELD_2, context)[0]
        algRunner = AlgRunner()
        nSteps = 3
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Preparing data"))
        dictFeatureMerge = {feat[matchField2]: feat for feat in mergeLyr.getFeatures()}
        inputFields = inputLyr.fields()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating new features"))

        nFeats = inputLyr.featureCount()
        if nFeats == 0:
            return {}
        stepSize = 100 / nFeats
        featuresToAdd = set()
        inputLyr.startEditing()
        inputLyr.beginEditCommand(self.tr("Merge features"))
        for current, feat in enumerate(inputLyr.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            if feat[matchField1] not in dictFeatureMerge:
                continue
            feat2 = dictFeatureMerge[feat[matchField1]]
            newFeature = QgsFeature(inputFields)
            for field in inputFields:
                newFeature[field.name()] = feat[field.name()]
            newFeature.setGeometry(feat2.geometry())
            featuresToAdd |= {newFeature}
            multiStepFeedback.setProgress(current * stepSize)
        inputLyr.addFeatures(list(featuresToAdd))
        inputLyr.endEditCommand()

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Dissolving"))
        attributeBlackList = [
            field.name() for field in inputLyr.fields() if field.name() != matchField1
        ]

        algRunner.runDSGToolsDissolvePolygonsWithSameAttributeSet(
            inputLyr=inputLyr,
            # attributeBlackList=attributeBlackList,
            context=context,
            feedback=multiStepFeedback,
        )

        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "mergefeaturesbasedonattribute"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Merge Features Based On Attribute")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Utils")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Utils"

    def tr(self, string):
        return QCoreApplication.translate(
            "MergeFeaturesBasedOnAttributeAlgorithm", string
        )

    def createInstance(self):
        return MergeFeaturesBasedOnAttributeAlgorithm()
