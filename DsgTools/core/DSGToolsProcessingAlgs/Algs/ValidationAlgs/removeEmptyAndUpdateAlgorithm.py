# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-24
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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
from PyQt5.QtCore import QCoreApplication

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterVectorLayer,
    QgsProcessingFeatureSourceDefinition,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class RemoveEmptyAndUpdateAlgorithm(ValidationAlgorithm):
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
        layerHandler = LayerHandler()
        algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            return {}
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)

        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
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
        if nFeats == 0 or multiStepFeedback.isCanceled():
            return {}

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(
            self.tr("Removing empty geometries from layer {input}...").format(
                input=inputLyr.name()
            )
        )
        notNullLayer = algRunner.runRemoveNull(
            cacheLyr, context, feedback=multiStepFeedback
        )

        notNullCount = notNullLayer.featureCount()
        if notNullCount == nFeats or multiStepFeedback.isCanceled():
            return {}

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Updating original layer..."))
        idsToDeleteSet = set(f["_featid"] for f in cacheLyr.getFeatures()) - set(
            f["_featid"] for f in notNullLayer.getFeatures()
        )
        idsToDeleteSet = idsToDeleteSet | set(f["_featid"] for f in cacheLyr.getFeatures() if 'Too few points in geometry component' in f.geometry().constGet().isValid()[1])
        inputLyr.startEditing()
        inputLyr.beginEditCommand(f"Deleting null values from {inputLyr.name()}")
        inputLyr.deleteFeatures(list(idsToDeleteSet))
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
        return "removeemptyandupdate"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Remove empty and update")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Basic Geometry Construction Issues Handling")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Basic Geometry Construction Issues Handling"

    def tr(self, string):
        return QCoreApplication.translate("RemoveEmptyAndUpdateAlgorithm", string)

    def createInstance(self):
        return RemoveEmptyAndUpdateAlgorithm()
