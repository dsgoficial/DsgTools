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
)
from typing import Dict, List, Optional, Set, Tuple, Union
from . import graphHandler
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


@dataclass()
class TerrainSlice:
    polygonid: int
    contourElevationFieldName: str
    threshold: int
    outershellFeat: QgsFeature
    holesFeatSet: Set[QgsFeature]
    contoursOnSlice: Set[QgsFeature]
    contourLineLayer: Union[QgsVectorLayer, str]
    contourIdField: str

    def __post_init__(self):
        self.contourDict = dict()
        self.spatialIndex = QgsSpatialIndex()
        for feat in self.contoursOnSlice:
            self.contourDict[feat.id()] = feat
            self.spatialIndex.addFeature(feat)
        if isinstance(self.contourLineLayer, str):
            self.context = QgsProcessingContext()
            self.contourLineLayer: QgsVectorLayer = QgsProcessingUtils.mapLayerFromString(self.contourLineLayer, self.context)
        self.contourLineDict = {
            feat[self.contourIdField]: feat
            for feat in self.contourLineLayer.getFeatures()
        }
        self.outershellDict = self.groupByPolygon(self.outershellFeat)
        self.holesGeomToSetDict = self.buildDictGroupedByPolygons(self.holesFeatSet)
        self.maxOutershellHeight = max(self.outershellDict.keys())
        self.minOutershellHeight = min(self.outershellDict.keys())
        self.maxHeighOnSlice = max(
            self.contoursOnSlice,
            key=lambda x: x[self.contourElevationFieldName],
            default=None,
        )
        self.minHeighOnSlice = min(
            self.contoursOnSlice,
            key=lambda x: x[self.contourElevationFieldName],
            default=None,
        )

    def buildDictGroupedByPolygons(self, polygonFeatSet: Set[QgsFeature]):
        polygonDict = dict()
        for polygonFeat in polygonFeatSet:
            geom = polygonFeat.geometry()
            polygonDict[geom.asWkb()] = self.groupByPolygon(polygonFeat)
        return polygonDict

    def groupByPolygon(self, polygonFeat: QgsFeature) -> Dict[int, Set[int]]:
        geom = polygonFeat.geometry()
        geomConstGet = geom.constGet()
        bounds = geomConstGet.boundary()
        polygonBoundary = QgsGeometry(bounds)
        bbox = geom.boundingBox()
        heightDictOfSets = defaultdict(set)
        for id in self.spatialIndex.intersects(bbox):
            contourFeat = self.contourDict[id]
            contourGeom = contourFeat.geometry()
            if not contourGeom.intersects(polygonBoundary):
                continue
            heightDictOfSets[contourFeat[self.contourElevationFieldName]].add(id)
        return heightDictOfSets

    def validateOutershellContours(
        self, feedback: Optional[QgsProcessingFeedback] = None
    ) -> Dict[QByteArray, str]:
        missingContourFlagDict = dict()
        nGroups = len(self.outershellDict)
        if nGroups < 2:
            return dict()
        stepSize = 100 / nGroups
        for current, (h1, h2) in enumerate(combinations(self.outershellDict.keys(), 2)):
            if abs(h1 - h2) <= self.threshold:
                continue
            min_h12 = min(h1, h2)  # done to fix the way flags are built.
            max_h12 = max(h1, h2)
            for outershellId in self.outershellDict[h1]:
                outershellFeat = self.contourDict[outershellId]
                geom = outershellFeat.geometry()
                if feedback is not None and feedback.isCanceled():
                    break
                shortestLineGeomList = [
                    geom.shortestLine(
                        self.contourLineDict[
                            self.contourDict[featId][self.contourIdField]
                        ].geometry()
                    )
                    for featId in self.outershellDict[h2]
                    if not self.contourDict[featId].geometry().equals(geom)
                ]
                shortestLine = min(shortestLineGeomList, key=lambda x: x.length())
                missingContourFlagDict.update(
                    {
                        shortestLine.asWkb(): self.tr(
                            f"Missing contour between contour lines of values {min_h12} and {max_h12}"
                        )
                    }
                )
            if feedback is not None:
                feedback.setProgress(current * stepSize)
        return missingContourFlagDict

    def validateOutershellAndInnerShellContours(
        self,
        depressionIdSet: Set[int],
        feedback: Optional[QgsProcessingFeedback] = None,
    ) -> Dict[QByteArray, str]:
        missingContourFlagDict = dict()
        if len(self.holesGeomToSetDict) == 0:
            return missingContourFlagDict
        pairs = list(
            product(self.outershellDict.keys(), self.holesGeomToSetDict.keys())
        )
        nPairs = len(pairs)
        stepSize = 100 / nPairs
        for current, (outershellHeight, holeWkb) in enumerate(pairs):
            if feedback is not None and feedback.isCanceled():
                break
            for holeHeight, contourIdSet in self.holesGeomToSetDict[holeWkb].items():
                diff = holeHeight - outershellHeight
                if diff == self.threshold:
                    continue
                if abs(diff) > self.threshold:  # missing contour
                    shortestLineList = [
                        self.contourLineDict[self.contourDict[a][self.contourIdField]]
                        .geometry()
                        .shortestLine(
                            self.contourLineDict[
                                self.contourDict[b][self.contourIdField]
                            ].geometry()
                        )
                        for a, b in product(
                            self.outershellDict[outershellHeight], contourIdSet
                        )
                    ]
                    shortestLine = min(
                        filter(
                            lambda x: x.length() > 0 and x.isGeosValid(),
                            shortestLineList,
                        ),
                        key=lambda x: x.length(),
                    )
                    missingContourFlagDict.update(
                        {
                            shortestLine.asWkb(): self.tr(
                                f"Missing contour between contour lines of values {outershellHeight} and {holeHeight}"
                            )
                        }
                    )
                    continue
                # from now on, there is no missing contour and holeHeight <= outershellHeight, this is only right if the contours are depression
                if holeHeight == self.maxOutershellHeight:
                    continue
                for invalidDepressionId in contourIdSet:
                    if (
                        self.contourDict[invalidDepressionId][self.contourIdField]
                        in depressionIdSet
                    ):
                        continue
                    invalidDepressionContourFeat = self.contourLineDict[
                        self.contourDict[invalidDepressionId][self.contourIdField]
                    ]
                    invalidDepressionContourGeom = (
                        invalidDepressionContourFeat.geometry()
                    )
                    shortestLineList = [
                        invalidDepressionContourGeom.shortestLine(
                            self.contourLineDict[
                                self.contourDict[h][self.contourIdField]
                            ].geometry()
                        )
                        for h in self.outershellDict[outershellHeight]
                    ]
                    shortestLine = min(
                        filter(
                            lambda x: x.length() > 0 and x.isGeosValid(),
                            shortestLineList,
                        ),
                        key=lambda x: x.length(),
                    )
                    missingContourFlagDict.update(
                        {
                            shortestLine.asWkb(): self.tr(
                                f"Contour (featid={invalidDepressionContourFeat[self.contourIdField]}) with height {holeHeight} is smaller or equal than terrain slice height {outershellHeight}. This is a depression and is not set as such. Verify contour value height and depression classification."
                            )
                        }
                    )

            if feedback is not None:
                feedback.setProgress(current * stepSize)
        return missingContourFlagDict

    def validate(
        self,
        depressionIdSet: Set[int],
        feedback: Optional[QgsProcessingFeedback] = None,
    ) -> Dict[QByteArray, str]:
        flagDict = dict()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(3, feedback)
            if feedback is not None
            else None
        )
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        # validating outershell contours
        flagDict.update(self.validateOutershellContours(feedback=multiStepFeedback))
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        flagDict.update(
            self.validateOutershellAndInnerShellContours(
                depressionIdSet=depressionIdSet, feedback=multiStepFeedback
            )
        )
        return flagDict

    def getMinMaxHeight(self) -> Tuple[float, float]:
        return self.minHeighOnSlice, self.maxHeighOnSlice

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

    def __post_init__(self):
        self.context = QgsProcessingContext()
        self.algRunner = AlgRunner()
        (
            self.contourCacheLyr,
            self.nodesLayer,
        ) = graphHandler.buildAuxLayersPriorGraphBuilding(
            networkLayer=self.contourLyr,
            context=self.context,
            geographicBoundsLayer=self.geographicBoundsLyr,
            feedback=None,
            clipOnGeographicBounds=True,
            idFieldName="contourid",
        )
        self.algRunner.runCreateSpatialIndex(
            inputLyr=self.nodesLayer,
            context=self.context,
            feedback=None,
            is_child_algorithm=True,
        )
        self.geoBoundsLineLyr = self.buildBoundaryLines()

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

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Building terrain polygons"))
        self.terrainPolygonLayer = self.buildTerrainPolygonLayerFromContours()

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        (
            self.terrainPolygonsOuterShells,
            self.terrainPolygonHoles,
        ) = self.getOuterShellAndHolesFromTerrainPolygons(feedback=multiStepFeedback)

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Building terrain slices"))
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

    def getOuterShellAndHolesFromTerrainPolygons(
        self,
        context: Optional[QgsProcessingContext] = None,
        feedback: Optional[QgsProcessingFeedback] = None,
    ) -> Tuple[QgsVectorLayer, QgsVectorLayer]:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(3, feedback)
            if feedback is not None
            else None
        )
        context = QgsProcessingContext() if context is None else context
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        outershell, donuthole = self.algRunner.runDonutHoleExtractor(
            inputLyr=self.terrainPolygonLayer,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=outershell,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=donuthole,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        return outershell, donuthole

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
        lineLyrList = (
            [self.contourCacheLyr]
            if self.geoBoundsLineLyr is None
            else [self.contourCacheLyr, self.geoBoundsLineLyr]
        )
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
            QgsProcessingMultiStepFeedback(1 + nPolygons, feedback)
            if feedback is not None
            else None
        )
        context = QgsProcessingContext() if context is None else context
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
        self.contoursJoinnedByPolygonBand = self.algRunner.runJoinAttributesByLocation(
            inputLyr=self.nodesLayer,
            joinLyr=self.terrainPolygonLayer,
            context=context,
            feedback=multiStepFeedback,
            predicateList=[self.algRunner.Intersect],
            method=0,
            discardNonMatching=False,
            is_child_algorithm=True,
        )

        def buildTerrainBand(
            polygonFeat, outershellFeat, holesFeatSet, contoursOnSlice, contourLineLayer
        ):
            return polygonFeat["polygonid"], TerrainSlice(
                polygonid=polygonFeat["polygonid"],
                contourElevationFieldName=self.contourElevationFieldName,
                threshold=self.threshold,
                outershellFeat=outershellFeat,
                holesFeatSet=holesFeatSet,
                contoursOnSlice=contoursOnSlice,
                contourLineLayer=contourLineLayer,
                contourIdField="contourid",
            )

        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
            multiStepFeedback.pushInfo(
                self.tr("Submitting terrain polygons to thread to build terrain bands.")
            )
        futures = set()
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        stepSize = 100 / nPolygons
        for current, polygonFeat in enumerate(
            self.terrainPolygonLayer.getFeatures(), start=0
        ):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            contoursOnSlice = set(
                f
                for f in self.algRunner.runFilterExpression(
                    inputLyr=self.contoursJoinnedByPolygonBand,
                    expression=f""" "polygonid" = {polygonFeat["polygonid"]}""",
                    context=context,
                ).getFeatures()
            )
            if contoursOnSlice == set():
                continue
            outershellFeat = [
                f
                for f in self.algRunner.runFilterExpression(
                    inputLyr=self.terrainPolygonsOuterShells,
                    expression=f""" "polygonid" = {polygonFeat["polygonid"]}""",
                    context=context,
                ).getFeatures()
            ][0]
            holesFeatSet = set(
                f
                for f in self.algRunner.runFilterExpression(
                    inputLyr=self.terrainPolygonHoles,
                    expression=f""" "polygonid" = {polygonFeat["polygonid"]}""",
                    context=context,
                ).getFeatures()
            )
            contourLineLayer = self.algRunner.runFilterExpression(
                inputLyr=self.contourCacheLyr,
                expression=f""" "contourid" in {tuple(i["contourid"] for i in contoursOnSlice)}""".replace(
                    ",)", ")"
                ),
                context=context,
                is_child_algorithm=True,
            )
            futures.add(
                pool.submit(
                    buildTerrainBand,
                    polygonFeat,
                    outershellFeat,
                    holesFeatSet,
                    contoursOnSlice,
                    contourLineLayer,
                )
            )
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)

        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(2)
            multiStepFeedback.pushInfo(self.tr("Evaluating thread results."))
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            polygonId, terrainSlice = future.result()
            polygonBandDict[polygonId] = terrainSlice
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
            searchRadius=1e-5,
            context=context,
            ignoreDanglesOnUnsegmentedLines=False,
            geographicBoundsLyr=self.geographicBoundsLyr,
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
        futures = set()
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        func = lambda x: x.validate(self.depressionSet)
        nSlices = len(self.terrainSlicesDict)
        if nSlices == 0:
            return invalidDict
        stepSize = 100 / nSlices
        for current, polygonBand in enumerate(self.terrainSlicesDict.values()):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            futures.add(pool.submit(func, polygonBand))
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)

        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Evaluating results"))
            multiStepFeedback.setCurrentStep(1)
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            invalidOutputDict = future.result()
            if invalidOutputDict == dict():
                continue
            invalidDict.update(invalidOutputDict)
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
