# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-06-08
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
import math
from itertools import chain, combinations

import processing
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsFeatureRequest,
    QgsGeometryUtils,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingUtils,
    QgsWkbTypes,
)

from .validationAlgorithm import ValidationAlgorithm


class IdentifyOutOfBoundsAnglesInCoverageAlgorithm(ValidationAlgorithm):
    FLAGS = "FLAGS"
    INPUTLAYERS = "INPUTLAYERS"
    SELECTED = "SELECTED"
    TOLERANCE = "TOLERANCE"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUTLAYERS, self.tr("Input layer"), QgsProcessing.TypeVectorLine
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE,
                self.tr("Minimum angle (in degrees)"),
                minValue=0,
                defaultValue=10,
                maxValue=360,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )

    def runIdentifyOutOfBoundsAngles(self, lyr, onlySelected, tol, context, feedback):
        parameters = {
            "INPUT": lyr,
            "SELECTED": onlySelected,
            "TOLERANCE": tol,
            "FLAGS": "memory:",
        }
        output = processing.run(
            "dsgtools:identifyoutofboundsangles",
            parameters,
            context=context,
            feedback=feedback,
        )
        self.flagFeaturesFromProcessOutput(output)

    def cleanCoverage(self, coverage, context, feedback=None):
        output = QgsProcessingUtils.generateTempFilename("output.shp")
        error = QgsProcessingUtils.generateTempFilename("error.shp")
        parameters = {
            "input": coverage,
            "type": [0, 1, 2, 3, 4, 5, 6],
            "tool": [0, 6],
            "threshold": "-1",
            "-b": False,
            "-c": True,
            "output": output,
            "error": error,
            "GRASS_REGION_PARAMETER": None,
            "GRASS_SNAP_TOLERANCE_PARAMETER": -1,
            "GRASS_MIN_AREA_PARAMETER": 0.0001,
            "GRASS_OUTPUT_TYPE_PARAMETER": 0,
            "GRASS_VECTOR_DSCO": "",
            "GRASS_VECTOR_LCO": "",
        }
        x = processing.run(
            "grass7:v.clean", parameters, context=context, feedback=feedback
        )
        lyr = QgsProcessingUtils.mapLayerFromString(x["output"], context)
        return lyr

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        algRunner = AlgRunner()
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUTLAYERS, context)
        if inputLyrList == []:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUTLAYERS)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        tol = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        self.prepareFlagSink(parameters, inputLyrList[0], QgsWkbTypes.Point, context)
        multiStepFeedback = QgsProcessingMultiStepFeedback(
            len(inputLyrList) + 11, feedback
        )
        currentStep = 0
        for lyr in inputLyrList:
            if feedback.isCanceled():
                break
            multiStepFeedback.setCurrentStep(currentStep)
            self.runIdentifyOutOfBoundsAngles(
                lyr, onlySelected, tol, context, feedback=multiStepFeedback
            )
            currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        mergedLayers = algRunner.runMergeVectorLayers(
            inputList=inputLyrList, context=context, feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            mergedLayers, context=context, feedback=multiStepFeedback
        )
        currentStep += 1

        intersectedLyr = algRunner.runLineIntersections(
            inputLyr=mergedLayers,
            intersectLyr=mergedLayers,
            context=context,
            feedback=multiStepFeedback,
        )
        nIntersections = intersectedLyr.featureCount()
        if nIntersections == 0:
            return {self.FLAGS: self.flag_id}
        currentStep += 1

        intersectedLyr = algRunner.runDeaggregate(
            inputLyr=intersectedLyr, context=context, feedback=multiStepFeedback
        )

        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            intersectedLyr, context=context, feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        splitSegments = algRunner.runExplodeLines(
            inputLyr=mergedLayers, context=context, feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            splitSegments, context=context, feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        joinedLyr = algRunner.runExtractByLocation(
            inputLyr=splitSegments,
            intersectLyr=intersectedLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        splitLines = algRunner.runSplitLinesWithLines(
            inputLyr=joinedLyr,
            linesLyr=joinedLyr,
            context=context,
            feedback=multiStepFeedback,
        )

        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            splitLines, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.computeSmallAnglesInCoverage(
            intersectedLyr, splitLines, nIntersections, tol, feedback=multiStepFeedback
        )

        return {self.FLAGS: self.flag_id}

    def computeSmallAnglesInCoverage(
        self, intersectedLyr, joinedLyr, nIntersections, tol, feedback=None
    ):
        flagWkbSet = set()
        total = 100 / nIntersections
        radTol = tol * math.pi / 180
        for current, pointFeat in enumerate(intersectedLyr.getFeatures()):
            if feedback is not None and feedback.isCanceled():
                break
            geom = pointFeat.geometry()
            p2 = geom.asPoint()
            geomWkb = geom.asWkb()
            if geomWkb in flagWkbSet:
                continue
            bbox = geom.boundingBox()
            request = QgsFeatureRequest().setFilterRect(bbox)
            for f1, f2 in combinations(joinedLyr.getFeatures(request), 2):
                geom1 = f1.geometry()
                geom2 = f2.geometry()
                if not geom.intersects(geom1) or not geom.intersects(geom2):
                    continue

                p1, p3 = set(
                    i
                    for i in chain.from_iterable(
                        [geom1.asPolyline(), geom2.asPolyline()]
                    )
                    if i != p2
                )
                angle = QgsGeometryUtils.angleBetweenThreePoints(
                    p1.x(), p1.y(), p2.x(), p2.y(), p3.x(), p3.y()
                )
                # angle in radians
                if angle < radTol:
                    flagWkbSet.add(geom.asWkb())
                    break
            if feedback is not None:
                feedback.setProgress(current * total)
        flagLambda = lambda x: self.flagFeature(
            x, flagText=self.tr("Small angle in coverage"), fromWkb=True
        )
        list(map(flagLambda, flagWkbSet))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyoutofboundsanglesincoverage"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Out Of Bounds Angles in Coverage")

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
            "IdentifyOutOfBoundsAnglesInCoverageAlgorithm", string
        )

    def createInstance(self):
        return IdentifyOutOfBoundsAnglesInCoverageAlgorithm()
