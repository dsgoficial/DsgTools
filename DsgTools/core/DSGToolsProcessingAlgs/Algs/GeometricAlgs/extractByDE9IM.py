# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-04-28
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import itertools
import json
import os

import concurrent.futures

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.featureHandler import FeatureHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler

from qgis.PyQt.Qt import QVariant
from PyQt5.QtCore import QCoreApplication, QRegExp, QCoreApplication
from qgis.PyQt.QtGui import QRegExpValidator

from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterField,
    QgsProcessingException,
    QgsProcessingParameterDistance,
    QgsProcessingMultiStepFeedback,
    QgsProcessingFeatureSourceDefinition,
    QgsGeometry,
    QgsProcessingParameterString,
    QgsProcessingParameterNumber,
    QgsProcessingParameterExpression,
    QgsFeatureRequest,
    QgsProcessingContext,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsSpatialIndex,
)


class ValidationString(QgsProcessingParameterString):
    """
    Auxiliary class for pre validation on measurer's names.
    """

    # __init__ not necessary

    def __init__(self, name, description=""):
        super().__init__(name, description)

    def checkValueIsAcceptable(self, value, context=None):
        regex = QRegExp("[FfTt012\*]{9}")
        acceptable = QRegExpValidator.Acceptable
        return (
            isinstance(value, str)
            and QRegExpValidator(regex).validate(value, 9)[0] == acceptable
        )


class ExtractByDE9IMAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    INTERSECT = "INTERSECT"
    DE9IM = "DE9IM"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Select features from"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INTERSECT,
                self.tr("By comparing features from"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )

        param = ValidationString(self.DE9IM, description=self.tr("DE9IM"))
        self.addParameter(param)

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Output"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.layerHandler = LayerHandler()
        self.algRunner = AlgRunner()
        source = self.parameterAsSource(parameters, self.INPUT, context)
        layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        intersectSource = self.parameterAsSource(parameters, self.INTERSECT, context)
        de9im = self.parameterAsString(parameters, self.DE9IM, context)

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            source.fields(),
            source.wkbType(),
            source.sourceCrs(),
        )

        nFeats = intersectSource.featureCount()
        if nFeats == 0:
            return {self.OUTPUT: dest_id}
        if de9im == "FF1FF0102":
            return self.algRunner.runExtractByLocation(
                inputLyr=parameters[self.INPUT],
                intersectLyr=parameters[self.INTERSECT],
                context=context,
                feedback=feedback,
                predicate=[2],
                method=0,
                is_child_algorithm=False,
            )
        nSteps = 2
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        selectedLyr = self.algRunner.runExtractByLocation(
            inputLyr=parameters[self.INPUT],
            intersectLyr=parameters[self.INTERSECT],
            context=context,
            feedback=multiStepFeedback,
            predicate=[2] if de9im == "FF1FF0102" else [0],
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        nFeats = selectedLyr.featureCount()
        if nFeats == 0:
            return {self.OUTPUT: dest_id}
        stepSize = 100 / nFeats

        def compute(feat):
            returnSet = set()
            geom = feat.geometry()
            bbox = geom.boundingBox()
            engine = QgsGeometry.createGeometryEngine(geom.constGet())
            engine.prepareGeometry()
            for f in selectedLyr.getFeatures(bbox):
                if multiStepFeedback.isCanceled():
                    return {}
                intersectGeom = f.geometry()
                if intersectGeom.isEmpty() or intersectGeom.isNull():
                    continue
                if engine.relatePattern(intersectGeom.constGet(), de9im):
                    returnSet.add(f)
            return returnSet

        for current, feat in enumerate(intersectSource.getFeatures()):
            if multiStepFeedback.isCanceled():
                return {}
            outputSet = compute(feat)
            sink.addFeatures(list(outputSet))
            multiStepFeedback.setProgress(current * stepSize)

        return {self.OUTPUT: dest_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "extractbyde9im"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Extract features by DE9IM")

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
        return "DSGTools: Geometric Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("ExtractByDE9IMAlgorithm", string)

    def createInstance(self):
        return ExtractByDE9IMAlgorithm()
