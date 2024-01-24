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
from qgis.core import (
    QgsVectorLayer,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingMultiStepFeedback,
    QgsFeature,
    QgsSpatialIndex,
    QgsGeometry,
)
from typing import Dict, Optional, Set, Tuple
from . import graphHandler
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


@dataclass
class TerrainModel:
    contourLyr: QgsVectorLayer
    contourElevationFieldName: str
    geographicBoundsLyr: QgsVectorLayer
    depressionFieldName: str = field(default=None)
    depressionExpression: str = field(default=None)
    context: QgsProcessingContext = field(default=None)
    feedback: QgsProcessingFeedback = field(default=None)
    spotElevationLyr: QgsVectorLayer = field(default=None)
    spotElevationFieldName: str = field(default=None)

    def __post_init__(self):
        if any(i is None for i in [self.spotElevationLyr, self.spotElevationFieldName]):
            raise ValueError(
                "Both spot elevation layer and spot elevation field name must be provided if any one of them is provided."
            )
        if any(
            i is None for i in [self.depressionFieldName, self.depressionExpression]
        ):
            raise ValueError(
                "Both spot depression field name and depression expression must be provided if any one of them is provided."
            )
        self.algRunner = AlgRunner()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(3, self.feedback)
            if self.feedback is None
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
            networkLayer=self.contourCacheLyr,
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
            QgsProcessingMultiStepFeedback(3, feedback) if feedback is None else None
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
                self.geographicBoundsLyr, self.context, feedback=multiStepFeedback
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
                behavior=[self.algRunner.AlignNodesInsertExtraVerticesWhereRequired],
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

    def buildTerrainSlices(self, feedback: QgsProcessingFeedback) -> set:
        polygonBandSet = set()
        nPolygons = self.terrainPolygonLayer.featureCount()
        if nPolygons == 0:
            return polygonBandSet
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
            polygonBandSet.add(
                TerrainSlice(
                    polygonid=polygonFeat["polygonid"],
                    contourElevationFieldName=self.contourElevationFieldName,
                    outershellFeat=outershellFeat,
                    holesFeatSet=holesFeatSet,
                    contoursOnSlice=contoursOnSlice,
                )
            )
        return polygonBandSet

    def validate(self):
        invalidDict = dict()
        for polygonBand in self.terrainSliceSet:
            invalidOutputDict = polygonBand.validate(self.depressionSet)
            if invalidDict == dict():
                continue
            invalidDict.update(invalidOutputDict)
        return invalidDict


@dataclass(frozen=True)
class TerrainSlice:
    polygonid: int
    contourElevationFieldName: str
    outershellFeat: QgsFeature
    holesFeatSet: Set[QgsFeature]
    contoursOnSlice: Set[QgsFeature]

    def __post_init__(self):
        self.contourDict = dict()
        self.spatialIndex = QgsSpatialIndex()
        for feat in self.contoursOnSlice:
            self.contourDict[feat.id()] = feat
            self.spatialIndex.addFeature(feat)
        self.outershellDict = self.groupByPolygon(self.outershellFeat)
        self.holeListOfDicts = self.buildDictGroupedByPolygons(self.holesFeatSet)

    def buildDictGroupedByPolygons(self, polygons: Set[QgsFeature]):
        return [self.groupByPolygon(polygon) for polygon in polygons]

    def groupByPolygon(self, polygonFeat: QgsFeature) -> Dict[int, Set[int]]:
        geom = polygonFeat.geometry()
        polygonBoundary = QgsGeometry(geom.constGet().boundary())
        bbox = geom.boundingBox()
        heightDictOfSets = defaultdict(lambda: defaultdict(int))
        for id in self.spatialIndex.intersects(bbox):
            contourFeat = self.contourDict[id]
            if not contourFeat.geometry().intersects(polygonBoundary):
                continue
            heightDictOfSets[contourFeat[self.contourElevationFieldName]].add(id)
        return heightDictOfSets

    def validate(self, depressionIdSet):
        return dict()
