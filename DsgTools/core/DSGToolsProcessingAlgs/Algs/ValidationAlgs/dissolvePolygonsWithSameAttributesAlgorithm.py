# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-10
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
    QgsProcessingMultiStepFeedback,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingParameterDistance,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class DissolvePolygonsWithSameAttributesAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    MIN_AREA = "MIN_AREA"
    ATTRIBUTE_BLACK_LIST = "ATTRIBUTE_BLACK_LIST"
    IGNORE_VIRTUAL_FIELDS = "IGNORE_VIRTUAL_FIELDS"
    IGNORE_PK_FIELDS = "IGNORE_PK_FIELDS"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT, self.tr("Input layer"), [QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        param = QgsProcessingParameterDistance(
            self.MIN_AREA,
            self.tr("Max dissolve area"),
            parentParameterName=self.INPUT,
            minValue=0,
            optional=True,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param)
        self.addParameter(
            QgsProcessingParameterField(
                self.ATTRIBUTE_BLACK_LIST,
                self.tr("Fields to ignore"),
                None,
                "INPUT",
                QgsProcessingParameterField.Any,
                allowMultiple=True,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_VIRTUAL_FIELDS,
                self.tr("Ignore virtual fields"),
                defaultValue=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_PK_FIELDS,
                self.tr("Ignore primary key fields"),
                defaultValue=True,
            )
        )
        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT, self.tr("Original layer with dissolved polygons")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        tol = self.parameterAsDouble(parameters, self.MIN_AREA, context)
        attributeBlackList = self.parameterAsFields(
            parameters, self.ATTRIBUTE_BLACK_LIST, context
        )
        ignoreVirtual = self.parameterAsBool(
            parameters, self.IGNORE_VIRTUAL_FIELDS, context
        )
        ignorePK = self.parameterAsBool(parameters, self.IGNORE_PK_FIELDS, context)

        tol = -1 if tol is None else tol
        nSteps = 4 if tol > 0 else 3
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Populating temp layer...\n"))
        unifiedLyr = layerHandler.createAndPopulateUnifiedVectorLayer(
            [inputLyr],
            geomType=QgsWkbTypes.MultiPolygon,
            attributeBlackList=attributeBlackList,
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
            attributeTupple=False if tol == -1 else True,
        )
        currentStep += 1

        if tol > 0:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Adding size constraint field...\n"))
            unifiedLyr = layerHandler.addDissolveField(
                unifiedLyr, tol, feedback=multiStepFeedback
            )
            currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Running dissolve...\n"))
        dissolvedLyr = algRunner.runDissolve(
            unifiedLyr, context, feedback=multiStepFeedback, field=["tupple"]
        )
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [inputLyr],
            dissolvedLyr,
            feedback=multiStepFeedback,
            onlySelected=onlySelected,
        )

        return {self.OUTPUT: inputLyr}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "dissolvepolygonswithsameattributes"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Dissolve Polygons With Same Attribute Set")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Polygon Handling")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Polygon Handling"

    def tr(self, string):
        return QCoreApplication.translate(
            "DissolvePolygonsWithSameAttributesAlgorithm", string
        )

    def createInstance(self):
        return DissolvePolygonsWithSameAttributesAlgorithm()
