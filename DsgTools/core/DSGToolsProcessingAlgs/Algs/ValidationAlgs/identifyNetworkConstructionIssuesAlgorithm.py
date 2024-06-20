# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-07-19
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

import itertools
import concurrent.futures
import os
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from .validationAlgorithm import ValidationAlgorithm
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterNumber,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingMultiStepFeedback,
    QgsFeatureRequest,
    QgsGeometry,
    QgsPoint,
)
from ..Help.algorithmHelpCreator import HTMLHelpCreator as help


class IdentifyNetworkConstructionIssuesAlgorithm(ValidationAlgorithm):
    INPUT_LINES = "INPUT_LINES"
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
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LINES,
                self.tr("Input lines"),
                QgsProcessing.TypeVectorLine,
                optional=False,
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
        lineLyrList = self.parameterAsLayerList(parameters, self.INPUT_LINES, context)
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
        refLyr = lineLyrList[0] if len(lineLyrList) > 0 else None
        self.prepareFlagSink(parameters, refLyr, QgsWkbTypes.Point, context)
        if refLyr is None:
            return {"FLAGS": self.flag_id}
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Building unified lines layer..."))
        mergedLines = self.getInputLineLayers(
            context, algRunner, lineLyrList, onlySelected, multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(1)
        outputLyr = algRunner.runIdentifyDangles(
            inputLayer=mergedLines,
            searchRadius=searchRadius,
            lineFilter=lineFilterLyrList,
            polygonFilter=polygonFilterLyrList,
            ignoreDanglesOnUnsegmentedLines=ignoreDanglesOnUnsegmentedLines,
            inputIsBoundaryLayer=inputIsBoundaryLayer,
            geographicBoundsLyr=geographicBoundsLyr,
            feedback=multiStepFeedback,
            context=context,
        )
        multiStepFeedback.setCurrentStep(2)
        if outputLyr.featureCount() > 0:
            self.flagSink.addFeatures(
                outputLyr.getFeatures(), QgsFeatureSink.FastInsert
            )
        multiStepFeedback.setCurrentStep(3)
        self.getUnsegmentedErrors(
            mergedLines,
            lineFilter=lineFilterLyrList,
            polygonFilter=polygonFilterLyrList,
            flagSet=set(i.geometry().asWkb() for i in outputLyr.getFeatures()),
            algRunner=algRunner,
            context=context,
            feedback=multiStepFeedback,
        )
        return {"FLAGS": self.flag_id}

    def getInputLineLayers(
        self, context, algRunner, lineLyrList, onlySelected, feedback
    ):
        nSteps = 2 if not onlySelected else 2 + len(lyrList)
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)

        def getLineLayer(currentStep, lineLyr):
            multiStepFeedback.setCurrentStep(currentStep)
            return (
                lineLyr
                if not onlySelected
                else algRunner.runSaveSelectedFeatures(
                    lineLyr, context, feedback=multiStepFeedback
                )
            )

        lyrList = [
            getLineLayer(currentStep, lineLyr)
            for currentStep, lineLyr in enumerate(lineLyrList)
        ]
        multiStepFeedback.setCurrentStep(nSteps - 1)
        mergedLines = algRunner.runMergeVectorLayers(
            inputList=lyrList, feedback=multiStepFeedback, context=context
        )
        return mergedLines

    def getUnsegmentedErrors(
        self,
        mergedLines,
        lineFilter,
        polygonFilter,
        flagSet,
        algRunner,
        context,
        feedback,
    ):
        # build spatial index on mergedLines
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        multiStepFeedback.setCurrentStep(0)
        algRunner.runCreateSpatialIndex(
            mergedLines,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        multiStepFeedback.setCurrentStep(1)
        # run intersect
        # merge and build spatial index on line filters and polygon filters
        filterLayer = self.getFilterLayers(
            lineFilter, polygonFilter, algRunner, multiStepFeedback, context
        )
        multiStepFeedback.setCurrentStep(2)
        nFeats = mergedLines.featureCount()
        if nFeats == 0:
            return
        stepSize = 100 / nFeats
        errorSet = set()

        def evaluate(feat):
            outputSet = set()
            if multiStepFeedback.isCanceled():
                return outputSet
            geom = feat.geometry()
            bbox = geom.boundingBox()
            engine = QgsGeometry.createGeometryEngine(geom.constGet())
            engine.prepareGeometry()
            request = QgsFeatureRequest().setFilterRect(bbox)
            # inner search
            iterable = (
                itertools.chain.from_iterable(
                    [mergedLines.getFeatures(request), filterLayer.getFeatures(request)]
                )
                if filterLayer is not None
                else mergedLines.getFeatures(request)
            )
            for candidateFeat in iterable:
                if multiStepFeedback.isCanceled():
                    return outputSet
                candidateGeom = candidateFeat.geometry()
                candidateConstGetGeom = candidateGeom.constGet()
                if not engine.intersects(candidateConstGetGeom):
                    continue
                if geom.equals(candidateGeom):  # same geom
                    continue
                intersection = engine.intersection(candidateConstGetGeom)
                intersectionPoints = (
                    [intersection]
                    if isinstance(intersection, QgsPoint)
                    else intersection.vertices()
                )
                for i in intersectionPoints:
                    wkb = i.asWkb()
                    if (
                        not engine.touches(i)
                        and wkb not in flagSet
                        and wkb not in outputSet
                    ):
                        outputSet.add(wkb)
            return outputSet

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        futures = set()
        for current, feat in enumerate(mergedLines.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            # put this into a thread after it is working
            futures.add(pool.submit(evaluate, feat))
            multiStepFeedback.setProgress(current * stepSize)
        concurrent.futures.wait(
            futures, timeout=None, return_when=concurrent.futures.ALL_COMPLETED
        )
        multiStepFeedback.setCurrentStep(3)
        stepSize = 100 / len(futures)
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                break
            outputSet = future.result()
            errorSet = errorSet.union(outputSet)
            multiStepFeedback.setProgress(current * stepSize)
        flagLambda = lambda x: self.flagFeature(
            x, self.tr("Line from input not split on intersection."), fromWkb=True
        )
        list(map(flagLambda, errorSet))

    def getFilterLayers(self, lineFilter, polygonFilter, algRunner, feedback, context):
        nSteps = len(polygonFilter) + 2
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)

        def makeBoundary(currentStep, layer):
            multiStepFeedback.setCurrentStep(currentStep)
            return algRunner.runBoundary(
                layer, feedback=multiStepFeedback, context=context
            )

        lineFilterList = lineFilter + [
            makeBoundary(currentStep, layer)
            for currentStep, layer in enumerate(polygonFilter)
        ]
        currentStep = len(polygonFilter) + 1
        multiStepFeedback.setCurrentStep(currentStep)
        mergedFilters = (
            algRunner.runMergeVectorLayers(
                lineFilterList, context=context, feedback=multiStepFeedback
            )
            if lineFilterList != []
            else None
        )
        if mergedFilters is None:
            return None
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            mergedFilters,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        return mergedFilters

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifynetworkconstructionissues"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Network's Geometry Construction Issues")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Network Processes")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Network Processes"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifyNetworkConstructionIssuesAlgorithm", string
        )

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    def helpUrl(self):
        return help().helpUrl(self.name())

    def createInstance(self):
        return IdentifyNetworkConstructionIssuesAlgorithm()
