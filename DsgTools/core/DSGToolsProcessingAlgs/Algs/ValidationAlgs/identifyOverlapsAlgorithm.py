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
from PyQt5.QtCore import QCoreApplication
import os
import processing
import concurrent.futures
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
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
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterVectorLayer,
    QgsProcessingUtils,
    QgsProject,
    QgsWkbTypes,
    QgsProcessingFeatureSourceDefinition,
)

from .validationAlgorithm import ValidationAlgorithm
from ..Help.algorithmHelpCreator import HTMLHelpCreator as help


class IdentifyOverlapsAlgorithm(ValidationAlgorithm):
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
                [
                    QgsProcessing.TypeVectorLine,
                    QgsProcessing.TypeVectorPolygon,
                ],
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
        geometryHandler = GeometryHandler()
        layerHandler = LayerHandler()
        algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        self.prepareFlagSink(parameters, inputLyr, inputLyr.wkbType(), context)
        # Compute the number of steps to display within the progress bar and
        # get features from source
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(self.tr("Building aux structure..."))
        joinLyr, idDict = self.prepareAuxStructure(
            context, multiStepFeedback, algRunner, inputLyr, onlySelected
        )
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.setProgressText(self.tr("Finding overlaps..."))
        geometrySet = self.findOverlaps(joinLyr, idDict, feedback)
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.setProgressText(self.tr("Raising flags..."))
        total = len(geometrySet)
        for current, geom in enumerate(geometrySet):
            if multiStepFeedback.isCanceled():
                break
            self.flagFeature(
                geom, self.tr("Overlap on layer {0}").format(inputLyr.name())
            )
            multiStepFeedback.setProgress(current * total)

        return {self.FLAGS: self.flag_id}

    def prepareAuxStructure(self, context, feedback, algRunner, inputLyr, onlySelected):
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(
            self.tr("Building aux structure: creating incremental field layer...")
        )
        incrementedLyr = algRunner.runAddAutoIncrementalField(
            inputLyr=inputLyr
            if not onlySelected
            else QgsProcessingFeatureSourceDefinition(inputLyr.id(), True),
            context=context,
            feedback=multiStepFeedback,
            start=0,
            sortAscending=False,
            sortNullsFirst=False,
        )
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.setProgressText(
            self.tr("Building aux structure: spatial index...")
        )
        algRunner.runCreateSpatialIndex(
            inputLyr=incrementedLyr, context=context, feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.setProgressText(
            self.tr("Building aux structure: feature dict...")
        )
        idDict = {feat["featid"]: feat for feat in incrementedLyr.getFeatures()}
        multiStepFeedback.setCurrentStep(3)
        multiStepFeedback.setProgressText(
            self.tr("Building aux structure: Running spatial join...")
        )
        joinLyr = algRunner.runJoinAttributesByLocation(
            inputLyr=incrementedLyr,
            joinLyr=incrementedLyr,
            context=context,
            feedback=multiStepFeedback,
        )

        return joinLyr, idDict

    def findOverlaps(self, inputLyr, idDict, feedback=None):
        total = 100.0 / inputLyr.featureCount() if inputLyr.featureCount() else 0
        geomType = inputLyr.geometryType()
        if not total:
            return set()

        def _processFeature(feat, feedback):
            outputSet = set()
            if (
                (feedback is not None and feedback.isCanceled())
                or feat["featid_2"] not in idDict
                or feat["featid_2"] <= feat["featid"]
            ):
                return outputSet
            geom1 = feat.geometry()
            geom2 = idDict[feat["featid_2"]].geometry()
            if not geom1.intersects(geom2):
                return outputSet
            intersects = geom1.intersection(geom2)
            return (
                outputSet.union(
                    set(intersects.asGeometryCollection())
                    if intersects.isMultipart()
                    else {intersects}
                )
                if intersects.type() == geomType
                else outputSet
            )

        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(
            self.tr("Finding overlaps: submitting to thread...")
        )
        processLambda = lambda x: _processFeature(x, multiStepFeedback)
        pool = concurrent.futures.ThreadPoolExecutor(os.cpu_count())
        futures = set()
        outputSet = set()
        for current, feat in enumerate(inputLyr.getFeatures()):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            futures.add(pool.submit(processLambda, feat))

        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.setProgressText(
            self.tr("Finding overlaps: processing thread outputs...")
        )
        outputSet = set()
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            outputSet = outputSet.union(future.result())
            # outputSet = outputSet.union(processLambda(feat))
            multiStepFeedback.setProgress(current * total)
        return outputSet

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyoverlaps"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Overlaps")

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
        return QCoreApplication.translate("IdentifyOverlapsAlgorithm", string)

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    def helpUrl(self):
        return help().helpUrl(self.name())

    def createInstance(self):
        return IdentifyOverlapsAlgorithm()
