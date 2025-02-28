# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-02-27
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
    QgsProcessingParameterDistance,
    QgsProcessingParameterEnum,
    QgsProcessingFeatureSourceDefinition,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterField,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class SnapFeaturesInsideLayerWithGroupByAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    ATTRIBUTE = "ATTRIBUTE"
    TOLERANCE = "TOLERANCE"

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

        self.addParameter(
            QgsProcessingParameterField(
                self.ATTRIBUTE,
                self.tr("Field to group by"),
                None,
                "INPUT",
                QgsProcessingParameterField.Any,
                allowMultiple=False,
                optional=False,
            )
        )
        param = QgsProcessingParameterDistance(
            self.TOLERANCE,
            self.tr("Search Radius"),
            parentParameterName=self.INPUT,
            defaultValue=1e-6,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 8}})
        self.addParameter(param)
        

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        algRunner = AlgRunner()
        layerHandler = LayerHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        tol = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        attributeName = self.parameterAsFields(
            parameters, self.ATTRIBUTE, context
        )[0]
        currentStep = 0
        uniqueValues = inputLyr.uniqueValues(inputLyr.dataProvider().fieldNameIndex(attributeName))
        multiStepFeedback = QgsProcessingMultiStepFeedback(3 + 3*len(uniqueValues), feedback)
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating aux structure..."))
        
        cacheLyr = algRunner.runCreateFieldWithExpression(
            inputLyr=inputLyr if not onlySelected
            else QgsProcessingFeatureSourceDefinition(inputLyr.id(), True),
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        if cacheLyr.featureCount() == 0:
            return {}
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        cacheLyr = algRunner.runCreateFieldWithExpression(
            inputLyr=cacheLyr,
            expression=f"'{inputLyr.name()}'",
            fieldName="layer",
            fieldType=2,
            context=context,
            feedback=multiStepFeedback,
        )
        snappedDict = dict()
        currentStep += 1
        for value in uniqueValues:
            multiStepFeedback.setCurrentStep(currentStep)
            currentLayer = algRunner.runFilterExpression(
                cacheLyr,
                expression=f''' "{attributeName}" = {value}''',
                context=context,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            algRunner.runCreateSpatialIndex(currentLayer, context=context, feedback=multiStepFeedback, is_child_algorithm=True)
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            snappedDict[value] = algRunner.runSnapGeometriesToLayer(
                inputLayer=currentLayer,
                referenceLayer=currentLayer,
                behavior=algRunner.SnapToAnchorNodes,
                tol=tol,
                context=context,
                feedback=multiStepFeedback,
            )
            snappedDict[value].setName(inputLyr.name())
            currentStep += 1
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        mergedLyr = algRunner.runMergeVectorLayers(
            inputList=list(snappedDict.values()),
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        snapped = algRunner.runDropFields(
            inputLayer=mergedLyr,
            fieldList=["path"],
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        if multiStepFeedback.isCanceled():
            return {}

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Updating original layer..."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [inputLyr], snapped, feedback=multiStepFeedback, onlySelected=onlySelected
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
        return "snapfeaturesinsidelayerwithgroupbyalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Snap Features Inside Layer With Group By Algorithm")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Snap Processes")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Snap Processes"

    def tr(self, string):
        return QCoreApplication.translate("SnapFeaturesInsideLayerWithGroupByAlgorithm", string)

    def createInstance(self):
        return SnapFeaturesInsideLayerWithGroupByAlgorithm()
