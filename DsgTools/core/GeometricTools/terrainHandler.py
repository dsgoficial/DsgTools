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

from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations, product
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
)
from typing import Dict, List, Optional, Set, Tuple
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
    contourIdField: str

    def __post_init__(self):
        self.contourDict = dict()
        self.spatialIndex = QgsSpatialIndex()
        for feat in self.contoursOnSlice:
            self.contourDict[feat.id()] = feat
            self.spatialIndex.addFeature(feat)
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
                    geom.shortestLine(i)
                    for i in self.contourDict[self.outershellDict[h2]]
                    if not i.equals(geom)
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
                        self.contourDict[a]
                        .geometry()
                        .shortestLine(self.contourDict[b].geometry())
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
                    invalidDepressionContourFeat = self.contourDict[invalidDepressionId]
                    invalidDepressionContourGeom = (
                        invalidDepressionContourFeat.geometry()
                    )
                    shortestLineList = [
                        invalidDepressionContourGeom.shortestLine(
                            self.contourDict[h].geometry()
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
    context: QgsProcessingContext = field(default=None)
    feedback: QgsProcessingFeedback = field(default=None)
    spotElevationLyr: QgsVectorLayer = field(default=None)
    spotElevationFieldName: str = field(default=None)

    def __post_init__(self):
        self.algRunner = AlgRunner()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(3, self.feedback)
            if self.feedback is not None
            else None
        )
        self.context = QgsProcessingContext() if self.context is None else self.context
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        (
            self.contourCacheLyr,
            self.nodesLayer,
        ) = graphHandler.buildAuxLayersPriorGraphBuilding(
            networkLayer=self.contourLyr,
            context=self.context,
            geographicBoundsLayer=self.geographicBoundsLyr,
            feedback=multiStepFeedback,
            clipOnGeographicBounds=True,
            idFieldName="contourid",
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=self.nodesLayer,
            context=self.context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.terrainPolygonLayer = self.buildTerrainPolygonLayerFromContours()

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        (
            self.terrainPolygonsOuterShells,
            self.terrainPolygonHoles,
        ) = self.getOuterShellAndHolesFromTerrainPolygons(multiStepFeedback)

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.terrainSlicesDict = self.buildTerrainSlices(multiStepFeedback)

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
        self, feedback: QgsProcessingFeedback
    ) -> Tuple[QgsVectorLayer, QgsVectorLayer]:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(3, feedback)
            if feedback is not None
            else None
        )
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        outershell, donuthole = self.algRunner.runDonutHoleExtractor(
            inputLyr=self.terrainPolygonLayer,
            context=self.context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=outershell,
            context=self.context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=donuthole,
            context=self.context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        return outershell, donuthole

    def buildTerrainPolygonLayerFromContours(self) -> QgsVectorLayer:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(7, self.feedback)
            if self.feedback is not None
            else None
        )
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        boundsLineLyr = (
            self.algRunner.runPolygonsToLines(
                self.geographicBoundsLyr, self.context, feedback=multiStepFeedback
            )
            if self.geographicBoundsLyr is not None
            else None
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        boundsLineLyr = (
            self.algRunner.runExplodeLines(
                boundsLineLyr, self.context, feedback=multiStepFeedback
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
                tol=1e-5 if self.contourCacheLyr.crs().isGeographic() else 1e-3,
                context=self.context,
                behavior=self.algRunner.AlignNodesInsertExtraVerticesWhereRequired,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )
            if self.geographicBoundsLyr is not None
            else None
        )

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        lineLyrList = (
            [self.contourCacheLyr]
            if boundsLineLyr is None
            else [self.contourCacheLyr, boundsLineLyr]
        )
        linesLyr = self.algRunner.runMergeVectorLayers(
            lineLyrList, self.context, feedback=multiStepFeedback
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        polygonLyr = self.algRunner.runPolygonize(
            linesLyr, self.context, feedback=multiStepFeedback
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        polygonLyr = self.algRunner.runCreateFieldWithExpression(
            inputLyr=polygonLyr,
            expression="$id",
            fieldName="polygonid",
            fieldType=1,
            context=self.context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=polygonLyr,
            context=self.context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        return polygonLyr

    def buildTerrainSlices(
        self, feedback: QgsProcessingFeedback
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
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
        contoursJoinnedByPolygonBand = self.algRunner.runJoinAttributesByLocation(
            inputLyr=self.nodesLayer,
            joinLyr=self.terrainPolygonLayer,
            context=self.context,
            feedback=multiStepFeedback,
            predicateList=[self.algRunner.Intersect],
            method=0,
            discardNonMatching=False,
        )
        for currentStep, polygonFeat in enumerate(
            self.terrainPolygonLayer.getFeatures(), start=1
        ):
            if multiStepFeedback is not None:
                if multiStepFeedback.isCanceled():
                    break
                multiStepFeedback.setCurrentStep(currentStep)
            outershellFeat = [
                f
                for f in self.algRunner.runFilterExpression(
                    inputLyr=self.terrainPolygonsOuterShells,
                    expression=f""" "polygonid" = {polygonFeat["polygonid"]}""",
                    context=QgsProcessingContext(),
                ).getFeatures()
            ][0]
            holesFeatSet = set(
                f
                for f in self.algRunner.runFilterExpression(
                    inputLyr=self.terrainPolygonHoles,
                    expression=f""" "polygonid" = {polygonFeat["polygonid"]}""",
                    context=QgsProcessingContext(),
                ).getFeatures()
            )
            contoursOnSlice = set(
                f
                for f in self.algRunner.runFilterExpression(
                    inputLyr=contoursJoinnedByPolygonBand,
                    expression=f""" "polygonid" = {polygonFeat["polygonid"]}""",
                    context=QgsProcessingContext(),
                ).getFeatures()
            )
            polygonBandDict[polygonFeat["polygonid"]] = TerrainSlice(
                polygonid=polygonFeat["polygonid"],
                contourElevationFieldName=self.contourElevationFieldName,
                threshold=self.threshold,
                outershellFeat=outershellFeat,
                holesFeatSet=holesFeatSet,
                contoursOnSlice=contoursOnSlice,
                contourIdField="contourid",
            )
        return polygonBandDict

    def validate(
        self, feedback: Optional[QgsProcessingFeedback] = None
    ) -> Dict[QByteArray, str]:
        if self.spotElevationLyr is None:
            return self.validateTerrainBands(feedback)
        invalidDict = dict()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
            multiStepFeedback.pushInfo(self.tr("Validating terrain bands"))
        invalidDict.update(self.validateTerrainBands(multiStepFeedback))
        if len(invalidDict) > 0:
            return invalidDict
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
            multiStepFeedback.pushInfo(self.tr("Validating spot elevation"))
        invalidDict.update(self.validateSpotElevation(multiStepFeedback))
        return invalidDict

    def validateTerrainBands(
        self, feedback: Optional[QgsProcessingFeedback] = None
    ) -> Dict[QByteArray, str]:
        invalidDict = dict()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(len(self.terrainSlicesDict), feedback)
            if feedback is not None
            else None
        )
        for currentStep, polygonBand in enumerate(self.terrainSlicesDict.values()):
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(currentStep)
            invalidOutputDict = polygonBand.validate(
                self.depressionSet, feedback=feedback
            )
            if invalidOutputDict == dict():
                continue
            invalidDict.update(invalidOutputDict)
        return invalidDict

    def validateSpotElevation(
        self, feedback: Optional[QgsProcessingFeedback] = None
    ) -> Dict[QByteArray, str]:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        spotElevationsThatIntersectContours = self.algRunner.runExtractByLocation(
            inputLyr=self.spotElevationLyr,
            intersectLyr=self.contourLyr,
            context=self.context,
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
            context=self.context,
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
