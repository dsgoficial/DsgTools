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
import concurrent.futures
import os
from collections import defaultdict
from typing import DefaultDict, Dict, Tuple, Union

import processing
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsFeatureRequest,
    QgsGeometry,
    QgsPointXY,
    QgsProcessing,
    QgsProcessingFeatureSourceDefinition,
    QgsProcessingFeedback,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsSpatialIndex,
    QgsVectorLayer,
    QgsWkbTypes,
)

from .validationAlgorithm import ValidationAlgorithm
from ..Help.algorithmHelpCreator import HTMLHelpCreator as help


class IdentifyDanglesAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    TOLERANCE = "TOLERANCE"
    LINEFILTERLAYERS = "LINEFILTERLAYERS"
    POLYGONFILTERLAYERS = "POLYGONFILTERLAYERS"
    IGNORE_DANGLES_ON_UNSEGMENTED_LINES = "IGNORE_DANGLES_ON_UNSEGMENTED_LINES"
    INPUT_IS_BOUDARY_LAYER = "INPUT_IS_BOUDARY_LAYER"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT, self.tr("Input layer"), [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.INPUT_IS_BOUDARY_LAYER,
                self.tr(
                    "Input is a boundary layer (every line must be connected "
                    "to an element of either the input layer or the filters)"
                ),
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE,
                self.tr("Search radius"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.0001,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.LINEFILTERLAYERS,
                self.tr("Linestring Filter Layers"),
                QgsProcessing.TypeVectorLine,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.POLYGONFILTERLAYERS,
                self.tr("Polygon Filter Layers"),
                QgsProcessing.TypeVectorPolygon,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_DANGLES_ON_UNSEGMENTED_LINES,
                self.tr("Ignore dangle on unsegmented lines"),
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr(
                    "Geographic Boundary (this layer only filters the output dangles)"
                ),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
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
        self.layerHandler = LayerHandler()
        algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.Point, context)
        if inputLyr is None:
            return {self.FLAGS: self.flag_id}
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        searchRadius = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        lineFilterLyrList = self.parameterAsLayerList(
            parameters, self.LINEFILTERLAYERS, context
        )
        polygonFilterLyrList = self.parameterAsLayerList(
            parameters, self.POLYGONFILTERLAYERS, context
        )
        ignoreDanglesOnUnsegmentedLines = self.parameterAsBool(
            parameters, self.IGNORE_DANGLES_ON_UNSEGMENTED_LINES, context
        )
        inputIsBoundaryLayer = self.parameterAsBool(
            parameters, self.INPUT_IS_BOUDARY_LAYER, context
        )
        geographicBoundsLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )
        # cacheInput = self.parameterAsBool(parameters, self.CACHE_INPUT, context)

        # Compute the number of steps to display within the progress bar and
        # get features from source
        feedbackTotal = 3
        feedbackTotal += 1 if lineFilterLyrList or polygonFilterLyrList else 0
        feedbackTotal += 1 if not inputIsBoundaryLayer else 0
        # feedbackTotal += 2 if cacheInput else 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(feedbackTotal, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Building local cache..."))
        inputLyr = algRunner.runAddAutoIncrementalField(
            inputLyr=inputLyr
            if not onlySelected
            else QgsProcessingFeatureSourceDefinition(inputLyr.id(), True),
            context=context,
            feedback=multiStepFeedback,
            fieldName="AUTO",
        )
        onlySelected = False
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            inputLyr=inputLyr, context=context, feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Building search structure..."))
        endVerticesDict = self.buildInitialAndEndPointDict(
            inputLyr,
            algRunner,
            context=context,
            geographicBoundsLyr=geographicBoundsLyr,
            feedback=multiStepFeedback,
        )

        # search for dangles candidates
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Looking for dangle candidates..."))
        pointSet = self.searchDanglesOnPointDict(endVerticesDict, multiStepFeedback)
        # build filter layer
        filterLayer = self.buildFilterLayer(
            lineFilterLyrList,
            polygonFilterLyrList,
            context,
            multiStepFeedback,
            onlySelected=onlySelected,
        )
        # filter pointList with filterLayer
        dangleSet = set()
        relatedDict = dict()

        if filterLayer:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(
                self.tr("Filtering dangles candidates with filter layer features...")
            )
            danglesWithFilterLayersSet, relatedDict = self.getDanglesWithFilterLayers(
                pointSet,
                filterLayer,
                searchRadius,
                multiStepFeedback,
            )
            dangleSet = dangleSet.union(danglesWithFilterLayersSet)
            pointSet = pointSet.difference(dangleSet)
        # filter with own layer
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(
            self.tr("Filtering dangles candidates with input layer features...")
        )
        danglesOnInputLayerSet = self.getDanglesOnInputLayerFeatures(
            pointSet=pointSet,
            inputLyr=inputLyr,
            ignoreDanglesOnUnsegmentedLines=ignoreDanglesOnUnsegmentedLines,
            inputIsBoundaryLayer=inputIsBoundaryLayer,
            relatedDict=relatedDict,
            searchRadius=searchRadius,
            feedback=multiStepFeedback,
        )
        dangleSet = dangleSet.union(danglesOnInputLayerSet)
        # build flag list with filtered points
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Raising flags..."))
        if dangleSet:
            # currentValue = feedback.progress()
            currentTotal = 100 / len(dangleSet)
            for current, point in enumerate(dangleSet):
                if multiStepFeedback.isCanceled():
                    break
                self.flagFeature(
                    QgsGeometry.fromPointXY(point),
                    self.tr("Dangle on {0}").format(inputLyr.name()),
                )
                multiStepFeedback.setProgress(current * currentTotal)
        # feedback.setProgress(100)
        return {self.FLAGS: self.flag_id}

    def buildInitialAndEndPointDict(
        self, lyr, algRunner, context, feedback, geographicBoundsLyr=None
    ):
        pointDict = defaultdict(set)
        nSteps = 5 if geographicBoundsLyr is not None else 3
        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        multiStepFeedback.setCurrentStep(currentStep)
        # this process of extracting the boundary is intentionally without the feedback
        # to avoid the excessive amount of error messages that are generated due to closed lines.
        boundaryLyr = algRunner.runBoundary(inputLayer=lyr, context=context)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        boundaryLyr = algRunner.runMultipartToSingleParts(
            inputLayer=boundaryLyr, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        if geographicBoundsLyr is not None:
            algRunner.runCreateSpatialIndex(
                inputLyr=boundaryLyr, context=context, feedback=multiStepFeedback
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            boundaryLyr = algRunner.runExtractByLocation(
                inputLyr=boundaryLyr,
                intersectLyr=geographicBoundsLyr,
                context=context,
                feedback=multiStepFeedback,
            )
            currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        featCount = boundaryLyr.featureCount()
        if featCount == 0:
            return pointDict
        step = 100 / featCount
        for current, feat in enumerate(boundaryLyr.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            geom = feat.geometry()
            if geom is None or not geom.isGeosValid():
                continue
            id = feat["AUTO"]
            pointList = geom.asMultiPoint() if geom.isMultipart() else [geom.asPoint()]
            for point in pointList:
                pointDict[point].add(id)
            multiStepFeedback.setProgress(current * step)
        return pointDict

    def searchDanglesOnPointDict(
        self, endVerticesDict: Dict, feedback: QgsProcessingFeedback
    ) -> set:
        """
        Counts the number of points on each endVerticesDict's key and returns a set of QgsPoint built from key candidate.
        """
        pointSet = set()
        nVertexes = len(endVerticesDict)
        if nVertexes == 0:
            return pointSet
        localTotal = 100 / nVertexes if nVertexes else 0
        # actual search for dangles
        for current, point in enumerate(endVerticesDict):
            if feedback.isCanceled():
                break
            # this means we only have one occurrence of point, therefore it is a dangle
            if len(endVerticesDict[point]) <= 1:
                pointSet.add(point)
            feedback.setProgress(localTotal * current)
        return pointSet

    def buildFilterLayer(
        self, lineLyrList, polygonLyrList, context, feedback, onlySelected=False
    ):
        """
        Buils one layer of filter lines.
        Build unified layer is not used because we do not care for attributes here, only geometry.
        refLyr elements are also added.
        """
        if not (lineLyrList + polygonLyrList):
            return []
        lineLyrs = lineLyrList
        for polygonLyr in polygonLyrList:
            if feedback.isCanceled():
                break
            lineLyrs += [self.makeBoundaries(polygonLyr, context, feedback)]
        if not lineLyrs:
            return None
        return self.layerHandler.createAndPopulateUnifiedVectorLayer(
            lineLyrs, QgsWkbTypes.MultiLineString, onlySelected=onlySelected
        )

    def makeBoundaries(self, lyr, context, feedback):
        parameters = {"INPUT": lyr, "OUTPUT": "memory:"}
        output = processing.run("native:boundary", parameters, context=context)
        return output["OUTPUT"]

    def getDanglesOnInputLayerFeatures(
        self,
        pointSet: set,
        inputLyr: QgsVectorLayer,
        searchRadius: float,
        ignoreDanglesOnUnsegmentedLines: bool = False,
        inputIsBoundaryLayer: bool = False,
        relatedDict: dict = None,
        feedback: QgsProcessingMultiStepFeedback = None,
    ) -> set:
        inputLayerDangles = set()
        nPoints = len(pointSet)
        relatedDict = dict() if relatedDict is None else relatedDict
        if nPoints == 0:
            return inputLayerDangles
        localTotal = 100 / nPoints
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        futures = set()

        def evaluate(point) -> Union[QgsPointXY, None]:
            qgisPoint = QgsGeometry.fromPointXY(point)
            buffer = qgisPoint.buffer(searchRadius, -1)
            bufferBB = buffer.boundingBox()
            # search radius to narrow down candidates
            request = QgsFeatureRequest().setFilterRect(bufferBB)
            bufferCount, intersectCount = 0, 0
            point_relationship_lambda = (
                lambda x: qgisPoint.intersects(x) or qgisPoint.distance(x) < 1e-8
                if ignoreDanglesOnUnsegmentedLines
                else qgisPoint.touches(x)
            )
            for feat in inputLyr.getFeatures(request):
                geom = feat.geometry()
                if feedback is not None and feedback.isCanceled():
                    return None
                if geom.intersects(buffer):
                    bufferCount += 1
                    if point_relationship_lambda(geom):
                        intersectCount += 1
            if intersectCount > 1:
                return None
            if inputIsBoundaryLayer and intersectCount == 1 and bufferCount == 1:
                if relatedDict == dict():
                    return point
                if (
                    point in relatedDict
                    and relatedDict[point]["candidateCount"]
                    == relatedDict[point]["bufferCount"]
                    and relatedDict[point]["candidateCount"] > 0
                ):
                    return None
                return point
            return point if bufferCount != intersectCount else None

        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        multiStepFeedback.setCurrentStep(0)
        for current, point in enumerate(pointSet):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            futures.add(pool.submit(evaluate, point))
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * localTotal)
        multiStepFeedback.setCurrentStep(1)
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            output = future.result()
            if output is not None:
                inputLayerDangles.add(output)
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * localTotal)
        return inputLayerDangles

    def getDanglesWithFilterLayers(
        self,
        pointSet: set,
        filterLayer: QgsVectorLayer,
        searchRadius: float,
        feedback: QgsProcessingMultiStepFeedback,
        ignoreNotSplit: bool = False,
    ) -> Tuple[set, Dict[QgsPointXY, dict]]:
        """
        Builds buffer areas from each point and evaluates the intersecting lines.
        If the number of candidates that intersect the buffer is different than the
        number of intersections of the point with the neighbors, it is a dangle.

        Returns the set containing the dangles.
        """
        nPoints = len(pointSet)
        danglesWithFilterLayers = set()
        relatedDict = dict()
        if nPoints == 0:
            return danglesWithFilterLayers, relatedDict
        localTotal = 100 / nPoints
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        multiStepFeedback.setCurrentStep(0)
        spatialIdx, allFeatureDict = self.buildSpatialIndexAndIdDict(
            filterLayer, feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(1)

        def evaluate(point: QgsPointXY) -> dict:
            candidateCount, bufferCount = 0, 0
            qgisPoint = QgsGeometry.fromPointXY(point)
            # search radius to narrow down candidates
            buffer = qgisPoint.buffer(searchRadius, -1)
            bufferBB = buffer.boundingBox()
            # if there is only one feat in candidateIds, that means that it is not a dangle
            for id in spatialIdx.intersects(bufferBB):
                candidateGeom = allFeatureDict[id].geometry()
                if multiStepFeedback.isCanceled():
                    return None
                if buffer.intersects(candidateGeom):
                    bufferCount += 1
                    if qgisPoint.intersects(candidateGeom):
                        candidateCount += 1
            return point, {"candidateCount": candidateCount, "bufferCount": bufferCount}

        futures = set()
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        multiStepFeedback.setCurrentStep(2)
        for current, point in enumerate(pointSet):
            if multiStepFeedback.isCanceled():
                break
            futures.add(pool.submit(evaluate, point))
            multiStepFeedback.setProgress(localTotal * current)
        multiStepFeedback.setCurrentStep(3)
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                break
            dangle, dangleDict = future.result()
            relatedDict[dangle] = dangleDict
            if dangleDict["candidateCount"] != dangleDict["bufferCount"]:
                danglesWithFilterLayers.add(dangle)
            multiStepFeedback.setProgress(localTotal * current)

        return danglesWithFilterLayers, relatedDict

    def buildSpatialIndexAndIdDict(self, inputLyr, feedback=None):
        """
        creates a spatial index for the centroid layer
        """
        spatialIdx = QgsSpatialIndex()
        idDict = {}
        for feat in inputLyr.getFeatures():
            if feedback is not None and feedback.isCanceled():
                break
            spatialIdx.addFeature(feat)
            idDict[feat.id()] = feat
        return spatialIdx, idDict

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifydangles"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Dangles")

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
        return QCoreApplication.translate("IdentifyDanglesAlgorithm", string)

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    def helpUrl(self):
        return  help().helpUrl(self.name())

    def createInstance(self):
        return IdentifyDanglesAlgorithm()
