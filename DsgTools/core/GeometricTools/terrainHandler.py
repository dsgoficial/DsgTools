# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-01-19
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations, product
import os
from PyQt5.QtCore import QCoreApplication
from qgis.PyQt.QtCore import QByteArray
from qgis.core import (
    QgsVectorLayer,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingMultiStepFeedback,
    QgsFeature,
    QgsSpatialIndex,
    QgsGeometry,
    QgsProject,
    QgsProcessingUtils,
    QgsFeatureRequest,
)
from typing import Dict, List, Optional, Set, Tuple, Union
from . import graphHandler
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


@dataclass()
class TerrainSlice:
    polygonid: int
    polygonFeat: QgsFeature
    contourElevationFieldName: str
    threshold: int
    contoursOnSlice: Set[QgsFeature]
    contourIdField: str

    def __post_init__(self):
        self.maxHeightFeatOnSlice: QgsFeature = max(
            self.contoursOnSlice,
            key=lambda x: x[self.contourElevationFieldName],
            default=None,
        )
        self.minHeighFeatOnSlice: QgsFeature = min(
            self.contoursOnSlice,
            key=lambda x: x[self.contourElevationFieldName],
            default=None,
        )

    def validate(self) -> Dict[QByteArray, str]:
        flagDict = dict()
        if self.maxHeightFeatOnSlice is None or self.minHeighFeatOnSlice is None:
            return flagDict
        if self.maxHeightFeatOnSlice[self.contourElevationFieldName] - self.minHeighFeatOnSlice[self.contourElevationFieldName] > self.threshold:
            geom = self.polygonFeat.geometry()
            geomWkb = geom.asWkb()
            flagDict.update(
                {
                    geomWkb: self.tr(f"Contour band with missing contour value between {self.minHeighFeatOnSlice[self.contourElevationFieldName]} and {self.maxHeightFeatOnSlice[self.contourElevationFieldName]}")
                }
            )
        return flagDict

    def getMinMaxHeight(self) -> Tuple[float, float]:
        return self.minHeighFeatOnSlice[self.contourElevationFieldName], self.maxHeightFeatOnSlice[self.contourElevationFieldName]

    def tr(self, string: str) -> str:
        return QCoreApplication.translate("TerrainSlice", string)


@dataclass
class TerrainModel:
    contourLyr: QgsVectorLayer
    contourElevationFieldName: str
    geographicBoundsLyr: QgsVectorLayer
    threshold: int
    depressionExpression: str = field(default=None)
    spotElevationLyr: QgsVectorLayer = field(default=None)
    spotElevationFieldName: str = field(default=None)
    feedback: QgsProcessingFeedback = field(default=None)

    def __post_init__(self):
        try:
            import networkx as nx
        except ImportError:
            raise self.tr(
                "This algorithm requires the Python networkx library. Please install this library and try again."
            )
        self.nx = nx
        self.context = QgsProcessingContext()
        self.algRunner = AlgRunner()
        multiStepFeedback = QgsProcessingMultiStepFeedback(10, self.feedback) if self.feedback is not None else None
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Creating contours cache"))
            multiStepFeedback.setCurrentStep(currentStep)

        self.contourCacheLyr: QgsVectorLayer = self.algRunner.runCreateFieldWithExpression(
            inputLyr=self.contourLyr,
            expression="$id",
            fieldName="contourid",
            fieldType=1,
            context=self.context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Merging lines"))
            multiStepFeedback.setCurrentStep(currentStep)

        self.algRunner.runDSGToolsMergeLines(
            inputLayer=self.contourCacheLyr,
            context=self.context,
            attributeBlackList=[
                f.name() for f in self.contourCacheLyr.fields() \
                    if f.name() not in [self.contourElevationFieldName]
            ],
            allowClosed=True,
            feedback=multiStepFeedback,
        )
        self.contourCacheLyr.commitChanges()
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Creating spatial index on merged lines"))
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=self.contourCacheLyr,
            context=self.context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Clipping to geographic bounds"))
            multiStepFeedback.setCurrentStep(currentStep)
        auxClippedContourCacheLyr: QgsVectorLayer = self.algRunner.runClip(
            inputLayer=self.contourCacheLyr,
            overlayLayer=self.geographicBoundsLyr,
            context=self.context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Clipping to geographic bounds"))
            multiStepFeedback.setCurrentStep(currentStep)
        singlePartClippedContourCacheLyr: QgsVectorLayer = self.algRunner.runMultipartToSingleParts(
            inputLayer=auxClippedContourCacheLyr,
            context=self.context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Finding closed lines"))
            multiStepFeedback.setCurrentStep(currentStep)
        self.clippedContourCacheLyr: QgsVectorLayer = self.algRunner.runCreateFieldWithExpression(
            inputLyr=singlePartClippedContourCacheLyr,
            expression="is_closed($geometry)",
            fieldName="is_closed",
            fieldType=1,
            context=self.context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Creating spatial index on clipped lines"))
            multiStepFeedback.setCurrentStep(currentStep)

        self.algRunner.runCreateSpatialIndex(
            inputLyr=self.clippedContourCacheLyr,
            context=self.context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Computing boundary lines"))
            multiStepFeedback.setCurrentStep(currentStep)
        self.geoBoundsLineLyr: QgsVectorLayer = self.buildBoundaryLines(context=self.context, feedback=multiStepFeedback)
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Extracting middle vertices"))
            multiStepFeedback.setCurrentStep(currentStep)
        self.contourMiddlePointsLyr: QgsVectorLayer = self.algRunner.runDSGToolsExtractMiddleVertexOnLine(
            inputLayer=self.clippedContourCacheLyr,
            context=self.context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Creating spatial index for middle vertices"))
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=self.contourMiddlePointsLyr,
            context=self.context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

    def buildAuxStructures(
        self,
        context: Optional[QgsProcessingContext] = None,
        feedback: Optional[QgsProcessingFeedback] = None,
    ):
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(3, feedback)
            if feedback is not None
            else None
        )
        context = QgsProcessingContext() if context is None else context
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.terrainPolygonLayer = self.buildTerrainPolygonLayerFromContours(context=context, feedback=multiStepFeedback)
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Building terrain slices"))
            multiStepFeedback.setCurrentStep(currentStep)
        self.terrainSlicesDict = self.buildTerrainSlices(feedback=multiStepFeedback)

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.depressionSet = (
            set()
            if self.depressionExpression is None
            else set(
                f["contourid"]
                for f in self.contourCacheLyr.getFeatures(self.depressionExpression)
            )
        )

    def tr(self, string: str) -> str:
        return QCoreApplication.translate("TerrainModel", string)

    def buildTerrainPolygonLayerFromContours(
        self,
        context: Optional[QgsProcessingContext] = None,
        feedback: Optional[QgsProcessingFeedback] = None,
    ) -> QgsVectorLayer:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(4, feedback)
            if feedback is not None
            else None
        )
        context = QgsProcessingContext() if context is None else context
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        if self.geoBoundsLineLyr is not None:
            buffered = self.algRunner.runBuffer(
                inputLayer=self.geographicBoundsLyr,
                distance=1e-6,
                context=context,
                feedback=None,
                endCapStyle=1,
                is_child_algorithm=True,
            )
            clipped = self.algRunner.runClip(
                inputLayer=self.contourCacheLyr,
                overlayLayer=buffered,
                context=context,
                feedback=None,
                is_child_algorithm=True,
            )
            lineLyrList = [clipped, self.geoBoundsLineLyr]
        else:
            lineLyrList = [self.contourCacheLyr]
        linesLyr = self.algRunner.runMergeVectorLayers(
            lineLyrList, context, feedback=multiStepFeedback
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        polygonLyr = self.algRunner.runPolygonize(
            linesLyr, context, feedback=multiStepFeedback
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        polygonLyr = self.algRunner.runCreateFieldWithExpression(
            inputLyr=polygonLyr,
            expression="$id",
            fieldName="polygonid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=polygonLyr,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        return polygonLyr

    def buildBoundaryLines(
        self,
        context: Optional[QgsProcessingContext] = None,
        feedback: Optional[QgsProcessingFeedback] = None,
    ) -> QgsVectorLayer:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(3, feedback)
            if feedback is not None
            else None
        )
        context = QgsProcessingContext() if context is None else context
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        boundsLineLyr = (
            self.algRunner.runPolygonsToLines(
                self.geographicBoundsLyr, context, feedback=multiStepFeedback
            )
            if self.geographicBoundsLyr is not None
            else None
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        boundsLineLyr = (
            self.algRunner.runExplodeLines(
                boundsLineLyr, context, feedback=multiStepFeedback
            )
            if self.geographicBoundsLyr is not None
            else None
        )

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)

        boundsLineLyr = (
            self.algRunner.runSnapGeometriesToLayer(
                inputLayer=boundsLineLyr,
                referenceLayer=self.contourCacheLyr,
                tol=1e-6 if self.contourCacheLyr.crs().isGeographic() else 1e-4,
                context=context,
                behavior=self.algRunner.AlignNodesInsertExtraVerticesWhereRequired,
                feedback=multiStepFeedback,
                is_child_algorithm=False,
            )
            if self.geographicBoundsLyr is not None
            else None
        )

        return boundsLineLyr

    def buildTerrainSlices(
        self,
        context: Optional[QgsProcessingContext] = None,
        feedback: Optional[QgsProcessingFeedback] = None,
    ) -> Dict[int, TerrainSlice]:
        polygonBandDict = dict()
        nPolygons = self.terrainPolygonLayer.featureCount()
        if nPolygons == 0:
            return polygonBandDict
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(3, feedback)
            if feedback is not None
            else None
        )
        context = QgsProcessingContext() if context is None else context
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
            multiStepFeedback.pushInfo(
                self.tr("Joinning contours middle points by polygon band.")
            )
        self.contoursMiddlePointsJoinnedByPolygonBand = self.algRunner.runJoinAttributesByLocation(
            inputLyr=self.contourMiddlePointsLyr,
            joinLyr=self.terrainPolygonLayer,
            context=context,
            feedback=multiStepFeedback,
            predicateList=[self.algRunner.Intersect],
            method=0,
            discardNonMatching=True,
            is_child_algorithm=False,
        )

        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
            multiStepFeedback.pushInfo(
                self.tr("Joinning polygon band by middle points.")
            )

        self.polygonBandJoinnedByContoursMiddlePoints = self.algRunner.runJoinAttributesByLocation(
            inputLyr=self.terrainPolygonLayer,
            joinLyr=self.contourMiddlePointsLyr,
            context=context,
            feedback=multiStepFeedback,
            predicateList=[self.algRunner.Intersect],
            method=0,
            discardNonMatching=True,
            is_child_algorithm=False,
        )
        stepSize = 100/nPolygons
        for current, polygonFeat in enumerate(
            self.terrainPolygonLayer.getFeatures(), start=0
        ):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            request = QgsFeatureRequest()
            request.setFilterExpression(f""" "polygonid" = {polygonFeat["polygonid"]}""")
            contoursOnSlice = set(
                f for f in self.contoursMiddlePointsJoinnedByPolygonBand.getFeatures(request)
            )
            if contoursOnSlice == set():
                continue
            polygonBandDict[polygonFeat["polygonid"]] = TerrainSlice(
                polygonid=polygonFeat["polygonid"],
                polygonFeat=polygonFeat,
                contourElevationFieldName=self.contourElevationFieldName,
                threshold=self.threshold,
                contoursOnSlice=contoursOnSlice,
                contourIdField="contourid",
            )
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)
        return polygonBandDict

    def findContourOutOfThreshold(
        self,
        context: Optional[QgsProcessingContext] = None,
        feedback: Optional[QgsProcessingFeedback] = None,
    ) -> Dict[QByteArray, str]:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(1, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
        contourOutOfThreshold = self.algRunner.runFilterExpression(
            inputLyr=self.contourCacheLyr,
            expression=f""" "{self.contourElevationFieldName}" % {self.threshold} != 0 """,
            context=context,
            feedback=multiStepFeedback,
        )
        if contourOutOfThreshold.featureCount() == 0:
            return dict()
        return {
            feat.geometry().asWkb(): self.tr("Contour out of threshold.")
            for feat in contourOutOfThreshold.getFeatures()
        }

    def validate(
        self,
        context: Optional[QgsProcessingContext] = None,
        feedback: Optional[QgsProcessingFeedback] = None,
    ) -> Dict[QByteArray, str]:
        invalidDict = dict()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(4, feedback)
            if feedback is not None
            else None
        )
        context = QgsProcessingContext() if context is None else context
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Validating contour lines"))
        invalidDict.update(
            self.validateContourLines(context=context, feedback=multiStepFeedback)
        )
        if len(invalidDict) > 0:
            return invalidDict
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Building terrain aux structures"))
        self.buildAuxStructures(feedback=multiStepFeedback)
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Validating terrain bands"))
        invalidDict.update(self.validateTerrainBands(feedback=multiStepFeedback))
        if len(invalidDict) > 0 or self.spotElevationLyr is None:
            return invalidDict
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Validating spot elevation"))
        invalidDict.update(self.validateSpotElevation(feedback=multiStepFeedback))
        return invalidDict

    def validateContourLines(
        self,
        context: Optional[QgsProcessingContext] = None,
        feedback: Optional[QgsProcessingFeedback] = None,
    ) -> Dict[QByteArray, str]:
        invalidDict = dict()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(8, feedback)
            if feedback is not None
            else None
        )
        context = QgsProcessingContext() if context is None else context
        currentStep = 0

        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        invalidDict.update(
            self.findContourOutOfThreshold(context=context, feedback=multiStepFeedback)
        )
        if len(invalidDict) > 0:
            return invalidDict
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        dangleCandidates = self.algRunner.runIdentifyDangles(
            inputLayer=self.contourCacheLyr,
            searchRadius=1e-4,
            context=context,
            ignoreDanglesOnUnsegmentedLines=False,
            inputIsBoundaryLayer=True,
            geographicBoundsLyr=self.geographicBoundsLyr,
            feedback=multiStepFeedback,
        )
        if dangleCandidates.featureCount() > 0:
            invalidDict.update(
                {
                    feat.geometry().asWkb(): self.tr("Dangle on Contour line.")
                    for feat in dangleCandidates.getFeatures()
                }
            )
            if len(invalidDict) > 0:
                return invalidDict
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        splitCurves = self.algRunner.runSplitLinesByLength(
            inputLayer=self.contourCacheLyr,
            length=1e-2 if self.contourCacheLyr.crs().isGeographic() else 1e3,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            splitCurves, context, multiStepFeedback, is_child_algorithm=True
        )

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)

        pointIntersectionLyr = self.algRunner.runLineIntersections(
            inputLyr=splitCurves,
            intersectLyr=splitCurves,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            pointIntersectionLyr, context, multiStepFeedback, is_child_algorithm=True
        )

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)

        pointCountLyr = self.algRunner.runJoinByLocationSummary(
            inputLyr=pointIntersectionLyr,
            joinLyr=pointIntersectionLyr,
            predicateList=[0],
            summaries=[0],
            joinFields=[self.contourElevationFieldName],
            context=context,
            feedback=multiStepFeedback,
        )
        for feat in pointCountLyr.getFeatures():
            if feat[f"{self.contourElevationFieldName}_count"] < 2:
                continue
            if feat[f"{self.contourElevationFieldName}_count"] == 2:
                if (
                    feat[self.contourElevationFieldName]
                    != feat[f"{self.contourElevationFieldName}_2"]
                ):
                    invalidDict[feat.geometry().asWkb()] = self.tr(
                        f"""Invalid contour lines intersection: lines with height {feat[self.contourElevationFieldName]} and {feat[f"{self.contourElevationFieldName}_2"]} touch each other."""
                    )
                continue
            invalidDict[feat.geometry().asWkb()] = self.tr(
                "Invalid contour lines intersection: more than two contour lines intersect."
            )
        return invalidDict
    
    def buildTerrainGraph(self, feedback: Optional[QgsProcessingFeedback] = None) -> Dict[QByteArray, str]:
        G = self.nx.Graph()
        auxDict = defaultdict(set)
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback) if feedback is not None else None
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
        featCount = self.contoursMiddlePointsJoinnedByPolygonBand.featureCount()
        if featCount == 0:
            return G
        stepSize = 100 / featCount
        for current, feat in enumerate(self.contoursMiddlePointsJoinnedByPolygonBand.getFeatures()):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                return G
            geom = feat.geometry()
            geomKey = geom.asWkb()
            auxDict[geomKey].add(feat)
            multiStepFeedback.setProgress(current * stepSize)
        
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
        dictSize = len(auxDict)
        if dictSize == 0:
            return G
        stepSize = 100 / dictSize
        for polygonSet in auxDict.values():
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                return G
            if len(polygonSet) < 1:
                continue
            p1, p2 = polygonSet
            G.add_edge(
                p1["polygonid"],
                p2["polygonid"],
                {
                    "contourid": p1["contourid"],
                    "is_closed": p1["is_closed"],
                    "height": p1[self.contourElevationFieldName],
                }
            )
            multiStepFeedback.setProgress(current * stepSize)
        return G
    
    def validateTerrainWithGraph(self, depressionIdSet, feedback: Optional[QgsProcessingFeedback] = None) -> Dict[QByteArray, str]:
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback) if feedback is not None else None
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
        self.terrainGraph = self.buildTerrainGraph(feedback=multiStepFeedback)
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
        hilltops = (
            i for i in self.terrainGraph.nodes \
                if self.terrainGraph.degree(i) == 1 \
                and self.terrainGraph.get_edge_data(i, list(self.terrainGraph.neighbors(i)[0]))["is_closed"] == True
        )
        sortedHilltops = sorted(hilltops, key=lambda x: self.terrainGraph.get_edge_data(x, list(self.terrainGraph.neighbors(x)[0]))["height"], reverse=True)
        visitedSet = set()
        flagDict = dict()
        for hilltop in sortedHilltops:
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            visitedSet.add(visitedSet)
            currentHeight = list(self.terrainGraph.neighbors(hilltop)[0])["height"]
            heightRange = (currentHeight, currentHeight + self.threshold) if hilltop not in depressionIdSet else (currentHeight - self.threshold, currentHeight)
            self.nx.set_node_attributes(self.terrainGraph, {hilltop: heightRange}, name="heightRange")
            for node in graphHandler.fetch_connected_nodes(self.terrainGraph, hilltop, max_degree=2):
                if self.terrainGraph.degree(node) == 1:
                    continue
                n_a, n_b = list(self.terrainGraph.neighbors(node))
                h1 = self.terrainGraph.get_edge_data(node, n_a)["height"]
                h2 = self.terrainGraph.get_edge_data(node, n_b)["height"]
                if abs(h1-h2) > self.threshold:
                    polygonFeat = self.terrainSlicesDict[node].polygonFeat
                    geom = polygonFeat.geometry()
                    geomKey = geom.asWkb()
                    flagDict[geomKey] = self.tr("")
        

    def validateTerrainBands(
        self, feedback: Optional[QgsProcessingFeedback] = None
    ) -> Dict[QByteArray, str]:
        invalidDict = dict()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Validating terrain bands"))
            multiStepFeedback.setCurrentStep(0)
        
        # TODO find bands with missing contour
        for slice in self.terrainSlicesDict.values():
            output = slice.validate()
            if output == dict():
                continue
            invalidDict.update(output)
        if invalidDict != dict():
            return invalidDict
        # TODO search on graph starting on hilltops
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Building terrain graph"))
            multiStepFeedback.setCurrentStep(1)
        G = self.buildTerrainGraph(feedback=multiStepFeedback)


        
        # TODO output flags
        return invalidDict

    def validateSpotElevation(
        self,
        context: Optional[QgsProcessingContext],
        feedback: Optional[QgsProcessingFeedback] = None,
    ) -> Dict[QByteArray, str]:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        currentStep = 0
        context = QgsProcessingContext() if context is not None else context
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        spotElevationsThatIntersectContours = self.algRunner.runExtractByLocation(
            inputLyr=self.spotElevationLyr,
            intersectLyr=self.contourLyr,
            context=context,
            predicate=[self.algRunner.Intersect],
        )
        if spotElevationsThatIntersectContours.featureCount() > 0:
            flagDict = dict()
            for feat in spotElevationsThatIntersectContours.getFeatures():
                geom = feat.geometry()
                flagDict[geom.asWkb()] = self.tr(
                    f"Spot elevation with height {feat[self.spotElevationFieldName]} (featid={feat.id()}) intersects contour line."
                )
            return flagDict
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        joinnedSpotElevation = self.algRunner.runJoinAttributesByLocation(
            inputLyr=self.spotElevationLyr,
            joinLyr=self.terrainPolygonLayer,
            context=context,
        )
        nFeats = joinnedSpotElevation.featureCount()
        stepSize = 100 / nFeats
        invalidDict = dict()
        for current, feat in enumerate(joinnedSpotElevation.getFeatures()):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            bandId = joinnedSpotElevation["polygonid"]
            pointHeight = joinnedSpotElevation[self.spotElevationFieldName]
            h_min, h_max = self.terrainSlicesDict[bandId].getMinMaxHeight()
            if h_min is None or h_max is None:
                continue
            if pointHeight == h_min or pointHeight == h_max:
                continue
            if h_min == h_max:
                if pointHeight > h_max + self.threshold:
                    flagText = self.tr(
                        f"Elevation point with height {pointHeight} out of threshold. This value is on a hilltop and should be between {h_max} and {h_max+self.threshold}"
                    )
                elif pointHeight < h_min - self.threshold:
                    flagText = self.tr(
                        f"Elevation point with height {pointHeight} out of threshold. This value is on a valley/depression and should be between {h_min} and {h_min-self.threshold}"
                    )
                else:
                    continue
            elif pointHeight < h_min or pointHeight > h_max:
                flagText = self.tr(
                    f"Elevation point with height {pointHeight} out of threshold. This value should be between {self.h_min} and {self.h_max}"
                )
            else:
                continue
            pointGeom = feat.geometry()
            invalidDict[pointGeom.asWkb()] = flagText
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)
        return invalidDict
