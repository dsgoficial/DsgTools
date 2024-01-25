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
        self.maxHeight = max(self.outershellDict.keys())

    def buildDictGroupedByPolygons(self, polygonFeatSet: Set[QgsFeature]):
        return {
            polygonFeat.geometry().asWkb(): self.groupByPolygon(polygonFeat)
            for polygonFeat in polygonFeatSet
        }

    def groupByPolygon(self, polygonFeat: QgsFeature) -> Dict[int, Set[int]]:
        geom = polygonFeat.geometry()
        polygonBoundary = QgsGeometry(geom.constGet().boundary())
        bbox = geom.boundingBox()
        heightDictOfSets = defaultdict(set)
        for id in self.spatialIndex.intersects(bbox):
            contourFeat = self.contourDict[id]
            if not contourFeat.geometry().intersects(polygonBoundary):
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
                    holeGeom = QgsGeometry()
                    holeGeom.fromWkb(holeWkb)
                    shortestLine = self.outershellFeat.geometry().shortestLine(holeGeom)
                    missingContourFlagDict.update(
                        {
                            shortestLine.asWkb(): self.tr(
                                f"Missing contour between contour lines of values {outershellHeight} and {holeHeight}"
                            )
                        }
                    )
                    continue
                # from now on, there is no missing contour and holeHeight <= outershellHeight, this is only right if the contours are depression
                if holeHeight == self.maxHeight:
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
                    shortestLine = self.outershellFeat.geometry().shortestLine(
                        invalidDepressionContourGeom
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
        context: Optional[QgsProcessingContext] = None,
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

    def tr(self, string):
        return QCoreApplication.translate("TerrainSlice", string)


@dataclass
class TerrainModel:
    contourLyr: QgsVectorLayer
    contourElevationFieldName: str
    geographicBoundsLyr: QgsVectorLayer
    threshold: int
    depressionFieldName: str = field(default=None)
    depressionExpression: str = field(default=None)
    context: QgsProcessingContext = field(default=None)
    feedback: QgsProcessingFeedback = field(default=None)
    spotElevationLyr: QgsVectorLayer = field(default=None)
    spotElevationFieldName: str = field(default=None)

    def __post_init__(self):
        if (
            self.spotElevationLyr is None and self.spotElevationFieldName is not None
        ) or (
            self.spotElevationLyr is not None and self.spotElevationFieldName is None
        ):
            raise ValueError(
                "Both spot elevation layer and spot elevation field name must be provided if any one of them is provided."
            )
        if (
            self.depressionFieldName is None and self.depressionExpression is not None
        ) or (
            self.depressionFieldName is not None and self.depressionExpression is None
        ):
            raise ValueError(
                "Both spot depression field name and depression expression must be provided if any one of them is provided."
            )
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
        self.terrainSliceSet = self.buildTerrainSlices(multiStepFeedback)

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.depressionSet = (
            set()
            if self.depressionFieldName is None
            else set(
                f["contourid"]
                for f in self.contourCacheLyr.getFeatures(self.depressionExpression)
            )
        )

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
            QgsProcessingMultiStepFeedback(6, self.feedback)
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
        return polygonLyr

    def buildTerrainSlices(self, feedback: QgsProcessingFeedback) -> List[TerrainSlice]:
        polygonBandList = list()
        nPolygons = self.terrainPolygonLayer.featureCount()
        if nPolygons == 0:
            return polygonBandList
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
            polygonBandList.append(
                TerrainSlice(
                    polygonid=polygonFeat["polygonid"],
                    contourElevationFieldName=self.contourElevationFieldName,
                    threshold=self.threshold,
                    outershellFeat=outershellFeat,
                    holesFeatSet=holesFeatSet,
                    contoursOnSlice=contoursOnSlice,
                    contourIdField="contourid",
                )
            )
        return polygonBandList

    def validate(self):
        invalidDict = dict()
        for polygonBand in self.terrainSliceSet:
            invalidOutputDict = polygonBand.validate(self.depressionSet)
            if invalidOutputDict == dict():
                continue
            invalidDict.update(invalidOutputDict)
        return invalidDict
