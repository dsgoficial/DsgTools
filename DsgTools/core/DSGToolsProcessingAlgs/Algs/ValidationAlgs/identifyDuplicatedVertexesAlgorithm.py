# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-06-23
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from collections import defaultdict
from dataclasses import dataclass
from PyQt5.QtCore import QCoreApplication

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsDataSourceUri,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterDistance,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingFeatureSourceDefinition,
    QgsFeatureRequest,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm
from ..Help.algorithmHelpCreator import HTMLHelpCreator as help


class IdentifyDuplicatedVertexesAlgorithm(ValidationAlgorithm):
    FLAGS = "FLAGS"
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
                [QgsProcessing.TypeVectorLine, QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
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
        algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.Point, context)

        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(self.tr("Building aux structure..."))
        usedInput = (
            inputLyr
            if not onlySelected
            else QgsProcessingFeatureSourceDefinition(inputLyr.id(), True)
        )
        incrementedLayer = algRunner.runAddAutoIncrementalField(
            usedInput, context, feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.setProgressText(self.tr("Extracting vertexes..."))
        vertexLayer = algRunner.runExtractVertices(
            inputLyr=incrementedLayer, context=context, feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.setProgressText(self.tr("Building search structure..."))
        pointDict = self.buildPointDict(vertexLayer, feedback=multiStepFeedback)
        multiStepFeedback.setCurrentStep(3)
        multiStepFeedback.setProgressText(self.tr("Searching duplicated vertexes..."))
        flagDict = self.getDuplicatedVertexes(pointDict, feedback=multiStepFeedback)
        multiStepFeedback.setCurrentStep(4)
        multiStepFeedback.setProgressText(self.tr("Raising flags (if any)..."))
        self.raiseFlags(flagDict, feedback=multiStepFeedback)

        return {self.FLAGS: self.flag_id}

    def buildPointDict(self, inputLyr, feedback=None):
        featCount = inputLyr.featureCount()
        if featCount == 0:
            return {}
        total = 100 / featCount
        pointDict = defaultdict(lambda: defaultdict(list))
        for current, feat in enumerate(inputLyr.getFeatures()):
            if feedback is not None and feedback.isCanceled():
                break
            geom = feat.geometry()
            pointDict[feat["featid"]][geom.asWkb()].append(geom)
            if feedback is not None:
                feedback.setProgress(current * total)
        return pointDict

    def getDuplicatedVertexes(self, pointDict, feedback=None):
        flagSet = set()
        for vertexDict in pointDict.values():
            for vertex, geomList in vertexDict.items():
                if len(geomList) > 1:
                    flagSet.add(vertex)
        return flagSet

    def raiseFlags(self, flagSet, feedback=None):
        nFlags = len(flagSet)
        if nFlags == 0:
            return
        size = 100 / nFlags
        for current, flagGeom in enumerate(flagSet):
            if feedback is not None and feedback.isCanceled():
                break
            self.flagFeature(
                flagGeom=flagGeom,
                fromWkb=True,
                flagText=f"Duplicated vertex.",
            )
            if feedback is not None:
                feedback.setProgress(current * size)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyduplicatedvertexesalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Duplicated Vertexes")

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
        return QCoreApplication.translate("IdentifyDuplicatedVertexesAlgorithm", string)

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    def helpUrl(self):
        return  help().helpUrl(self.name())

    def createInstance(self):
        return IdentifyDuplicatedVertexesAlgorithm()
