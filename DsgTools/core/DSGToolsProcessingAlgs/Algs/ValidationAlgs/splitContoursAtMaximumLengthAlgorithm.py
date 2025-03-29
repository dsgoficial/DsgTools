# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-28
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
    QgsProcessingParameterDistance,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingFeatureSourceDefinition,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class SplitContoursAtMaximumLengthAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    MAX_LENGTH = "MAX_LENGTH"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input contour layer"),
                defaultValue="elemnat_curva_nivel_l",
                types=[QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        param = QgsProcessingParameterDistance(
            self.MAX_LENGTH,
            self.tr("Maximum length"),
            minValue=0,
            parentParameterName=self.INPUT,
            defaultValue=0.05,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 8}})
        self.addParameter(param)

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()

        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        if inputLyr.featureCount() == 0 or (
            onlySelected is True and inputLyr.selectedFeatureCount() == 0
        ):
            feedback.pushWarning(self.tr("Empty input"))
            return {}
        maxLength = self.parameterAsDouble(parameters, self.MAX_LENGTH, context)
        self.splitLinesAtMaximumLength(
            context,
            feedback,
            layerHandler,
            algRunner,
            inputLyr,
            onlySelected,
            maxLength,
        )
        return {}

    def splitLinesAtMaximumLength(
        self,
        context,
        feedback,
        layerHandler,
        algRunner,
        inputLyr,
        onlySelected,
        maxLength,
    ):
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Populating temp layer..."))
        auxLyr = layerHandler.createAndPopulateUnifiedVectorLayer(
            [inputLyr],
            geomType=inputLyr.wkbType(),
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr("Running split lines..."))
        outputLines = algRunner.runDSGToolsSplitLinesAtMaximumLengthAlgorithm(
            auxLyr,
            maxLength=maxLength,
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr("Updating original layer..."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [inputLyr],
            outputLines,
            feedback=multiStepFeedback,
            onlySelected=onlySelected,
        )

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "splitcontoursatmaximumlengthalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Split Contours at Maximum Length Algorithm")

    def group(self):
        return self.tr("QA Tools: Terrain Processes")

    def groupId(self):
        return "DSGTools - QA Tools: Terrain Processes"

    def tr(self, string):
        return QCoreApplication.translate(
            "SplitContoursAtMaximumLengthAlgorithm", string
        )

    def createInstance(self):
        return SplitContoursAtMaximumLengthAlgorithm()
