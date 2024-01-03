# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-06
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
    QgsProcessingParameterVectorLayer,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class SnapToGridAndUpdateAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    TOLERANCE = "TOLERANCE"
    OUTPUT = "OUTPUT"

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
        param = QgsProcessingParameterDistance(
            self.TOLERANCE,
            self.tr("Tolerance"),
            parentParameterName=self.INPUT,
            minValue=0,
            defaultValue=1e-10,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 12}})
        self.addParameter(param)
        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT, self.tr("Original layer with features snapped to grid")
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
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        tol = self.parameterAsDouble(parameters, self.TOLERANCE, context)

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
        multiStepFeedback.pushInfo(
            self.tr(
                "Snapping geometries from layer {input} to grid with size {tol}..."
            ).format(input=inputLyr.name(), tol=tol)
        )
        snappedLayer = algRunner.runSnapToGrid(
            auxLyr, tol, context, feedback=multiStepFeedback
        )

        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr("Updating original layer..."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [inputLyr],
            snappedLayer,
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
        return "snaptogridandupdate"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Snap to grid and update")

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
        return QCoreApplication.translate("SnapToGridAndUpdateAlgorithm", string)

    def createInstance(self):
        return SnapToGridAndUpdateAlgorithm()
