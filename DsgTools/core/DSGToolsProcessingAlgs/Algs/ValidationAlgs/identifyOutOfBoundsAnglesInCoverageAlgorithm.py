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
from collections import defaultdict
import math
from itertools import chain, combinations

import concurrent.futures
import os
import processing
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsGeometry,
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
            "tool": [0],
            "threshold": "-1",
            "-b": False,
            "-c": False,
            "output": output,
            "error": error,
            "GRASS_REGION_PARAMETER": None,
            "GRASS_SNAP_TOLERANCE_PARAMETER": 1e-10,
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
            6, feedback
        )
        currentStep = 0
        #merge all layers into one
        multiStepFeedback.setProgressText(self.tr('Building unified layer'))
        multiStepFeedback.setCurrentStep(currentStep)
        mergedLayers = algRunner.runMergeVectorLayers(
            inputList=inputLyrList, context=context, feedback=multiStepFeedback
        )
        currentStep += 1

        
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr('Exploding lines'))
        splitSegments = algRunner.runExplodeLines(
            inputLyr=mergedLayers, context=context, feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr('Building spatial index'))
        algRunner.runCreateSpatialIndex(
            inputLyr=splitSegments,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        

        #split segments with clean
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr('Splitting lines'))
        cleanedLyr = algRunner.runSplitLinesWithLines(
            inputLyr=splitSegments,
            linesLyr=splitSegments,
            context=context,
            feedback=multiStepFeedback
        )
        
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr('Building node angle dict'))
        nodeAngleDict = self.buildNodeAngleDict(cleanedLyr, feedback=multiStepFeedback)

        
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr('Evaluating flags'))
        self.computeSmallAnglesInCoverage(
            nodeAngleDict, tol, feedback=multiStepFeedback
        )

        return {self.FLAGS: self.flag_id}
    
    def buildNodeAngleDict(self, splitSegments, feedback=None):
        nodeAngleDict = defaultdict(set)
        # nodeAngleDict = dict()
        nFeats = splitSegments.featureCount()
        if nFeats == 0:
            return nodeAngleDict
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(self.tr('Building node angle dict: building dict'))
        multiStepFeedback.pushInfo(self.tr(f'Iterating over {nFeats} segments...'))
        for current, feat in enumerate(splitSegments.getFeatures()):
            if feedback is not None and feedback.isCanceled():
                break
            geom = feat.geometry()
            if geom.isNull():
                continue
            p1, p2 =  geom.asPolyline() if not geom.isMultipart() else geom.asMultiPolyline()[0]
            geom1 = QgsGeometry.fromPointXY(p1)
            wkb1 = geom1.asWkb()
            geom2 = QgsGeometry.fromPointXY(p2)
            wkb2 = geom2.asWkb()
            nodeAngleDict[wkb1].add(wkb2)
            nodeAngleDict[wkb2].add(wkb1)
            if feedback is not None:
                multiStepFeedback.setProgress(current * 100 / nFeats)
            
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.setProgressText(self.tr('Building node angle dict: identifying nodes to pop'))
        keysToPop = set()
        nNodes = len(nodeAngleDict)
        for current, (point, pointSet) in enumerate(nodeAngleDict.items()):
            if feedback is not None and feedback.isCanceled():
                break
            if len(pointSet) < 2:
                keysToPop.add(point)
            if feedback is not None:
                multiStepFeedback.setProgress(current * 100 / nNodes)
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.setProgressText(self.tr('Building node angle dict: removing single nodes'))
        nItems = len(keysToPop)
        for current, point in enumerate(keysToPop):
            if feedback is not None and feedback.isCanceled():
                break
            nodeAngleDict.pop(point)
            if feedback is not None:
                multiStepFeedback.setProgress(current * 100 / nItems)
        return nodeAngleDict

    def computeSmallAnglesInCoverage(
        self, nodeAngleDict, tol, feedback=None
    ):
        flagWkbSet = set()
        nIntersections = len(nodeAngleDict)
        if nIntersections == 0:
            return flagWkbSet
        total = 100 / nIntersections
        for current, (wkb2, pointSet) in enumerate(nodeAngleDict.items()):
            if feedback is not None and feedback.isCanceled():
                break
            if wkb2 in flagWkbSet:
                continue
            p2 = self.getPointXYFromWkb(wkb2)
            for wkb1, wkb3 in combinations(pointSet, 2):
                p1 = self.getPointXYFromWkb(wkb1)
                p3 = self.getPointXYFromWkb(wkb3)
                angle = QgsGeometryUtils.angleBetweenThreePoints(
                    p1.x(), p1.y(), p2.x(), p2.y(), p3.x(), p3.y()
                )
                vertexAngle = abs(math.degrees(angle))
                # vertexAngle = vertexAngle if vertexAngle < 180 else 360 - vertexAngle
                if vertexAngle < tol:
                    flagWkbSet.add(wkb2)
                    break
            if feedback is not None:
                feedback.setProgress(current * total)
        flagLambda = lambda x: self.flagFeature(
            x, flagText=self.tr("Small angle in coverage"), fromWkb=True
        )
        list(map(flagLambda, flagWkbSet))

    def getPointXYFromWkb(self, wkb):
        geom = QgsGeometry()
        geom.fromWkb(wkb)
        return geom.asPoint()

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
