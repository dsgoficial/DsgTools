# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-13
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
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from .validationAlgorithm import ValidationAlgorithm
import processing
from PyQt5.QtCore import QCoreApplication
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
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingUtils,
    QgsSpatialIndex,
    QgsGeometry,
    QgsProcessingMultiStepFeedback,
    QgsProcessingException,
)


class IdentifyAndFixInvalidGeometriesAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    IGNORE_CLOSED = "IGNORE_CLOSED"
    TYPE = "TYPE"
    FLAGS = "FLAGS"
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
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_CLOSED,
                self.tr(
                    "Ignore flags on start point or end points of closed linestrings"
                ),
                defaultValue=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.TYPE, self.tr("Fix input geometries"), defaultValue=False
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )
        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT,
                self.tr("Original layer (has fixed geometries if fix mode is chosen)"),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        ignoreClosed = self.parameterAsBool(parameters, self.IGNORE_CLOSED, context)
        fixInput = self.parameterAsBool(parameters, self.TYPE, context)
        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.Point, context)

        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Identifying invalid geometries"))
        flagDict = layerHandler.identifyAndFixInvalidGeometries(
            inputLyr=inputLyr,
            ignoreClosed=ignoreClosed,
            fixInput=fixInput,
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setProgressText(self.tr("Raising Flags"))
        multiStepFeedback.setCurrentStep(currentStep)
        itemSize = len(flagDict)
        progressSize = 100 / itemSize if itemSize else 0
        for current, (key, outDict) in enumerate(flagDict.items()):
            if multiStepFeedback.isCanceled():
                break
            self.flagFeature(flagGeom=outDict["geom"], flagText=outDict["reason"])
            multiStepFeedback.setProgress(current * progressSize)

        return {self.FLAGS: self.flag_id, self.OUTPUT: inputLyr}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyandfixinvalidgeometries"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify And Fix Invalid Geometries")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Identification Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Identification Processes)"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifyAndFixInvalidGeometriesAlgorithm", string
        )

    def createInstance(self):
        return IdentifyAndFixInvalidGeometriesAlgorithm()
