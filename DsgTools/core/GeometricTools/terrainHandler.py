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
import itertools
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtCore import QByteArray
from qgis.core import (
    QgsVectorLayer,
    QgsExpression,
    QgsGeometry,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingMultiStepFeedback,
    QgsFeature,
    QgsFeatureRequest,
)
from typing import Dict, Optional, Set, Tuple
from . import graphHandler
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


@dataclass()
class TerrainSlice:
    """
    Represents a terrain slice with its properties and provides validation functions.

    Attributes:
        polygonid (int): Identifier of the polygon.
        polygonFeat (QgsFeature): Feature object for the polygon.
        contourElevationFieldName (str): Name of the elevation field in contour lines.
        threshold (int): The elevation threshold for the model.
        contoursOnSlice (Set[QgsFeature]): Set of contour features in this slice.
        contourIdField (str): Field name for contour IDs.
    """

    polygonid: int
    polygonFeat: QgsFeature
    contourElevationFieldName: str
    threshold: int
    contoursOnSlice: Set[QgsFeature]
    contourIdField: str

    def __post_init__(self):
        """
        Initializes the minimum and maximum elevation features on the slice.
        """
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
        """
        Validates if the terrain slice has consistent elevation values within the threshold.

        Returns:
            Dict[QByteArray, str]: Dictionary with any errors found, keyed by geometry.
        """
        flagDict = dict()
        if self.maxHeightFeatOnSlice is None or self.minHeighFeatOnSlice is None:
            return flagDict
        if (
            self.maxHeightFeatOnSlice[self.contourElevationFieldName]
            - self.minHeighFeatOnSlice[self.contourElevationFieldName]
            > self.threshold
        ):
            geom = self.polygonFeat.geometry()
            geomWkb = geom.asWkb()
            flagDict.update(
                {
                    geomWkb: self.tr(
                        "Contour band with missing contour value between {0} and {1}"
                    ).format(self.minHeighFeatOnSlice[self.contourElevationFieldName], self.maxHeightFeatOnSlice[self.contourElevationFieldName])
                }
            )
        return flagDict

    def getMinMaxHeight(self) -> Tuple[float, float]:
        """
        Retrieves the minimum and maximum heights in the terrain slice.

        Returns:
            Tuple[float, float]: Minimum and maximum elevation values.
        """
        return (
            self.minHeighFeatOnSlice[self.contourElevationFieldName],
            self.maxHeightFeatOnSlice[self.contourElevationFieldName],
        )

    def tr(self, string: str) -> str:
        """
        Translates the given string for localization.

        Args:
            string (str): The string to translate.

        Returns:
            str: Translated string.
        """
        return QCoreApplication.translate("TerrainSlice", string)


@dataclass
class TerrainModel:
    """
    Represents a terrain model composed of multiple terrain slices and processing algorithms.

    Attributes:
        contourLyr (QgsVectorLayer): Layer containing contour lines.
        contourElevationFieldName (str): Field name for contour elevations.
        geographicBoundsLyr (QgsVectorLayer): Layer defining the geographic bounds.
        threshold (int): Elevation threshold for contour line consistency.
        depressionExpression (str): Expression for identifying depressions in contours.
        spotElevationLyr (QgsVectorLayer): Layer containing spot elevations.
        spotElevationFieldName (str): Field name for spot elevations.
        feedback (QgsProcessingFeedback): Feedback object for processing steps.
    """

    contourLyr: QgsVectorLayer
    contourElevationFieldName: str
    geographicBoundsLyr: QgsVectorLayer
    threshold: int
    depressionExpression: str = field(default=None)
    spotElevationLyr: QgsVectorLayer = field(default=None)
    spotElevationFieldName: str = field(default=None)
    feedback: QgsProcessingFeedback = field(default=None)

    def __post_init__(self):
        """
        Initializes the minimum and maximum elevation features on the slice.
        """
        try:
            import networkx as nx
        except ImportError:
            raise ImportError(
                self.tr("This algorithm requires the Python networkx library. Please install this library and try again.")
            )
        self.nx = nx
        self.context = QgsProcessingContext()
        self.algRunner = AlgRunner()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(10, self.feedback)
            if self.feedback is not None
            else None
        )
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Creating contours cache"))
            multiStepFeedback.setCurrentStep(currentStep)

        # A curva de nível chega da preparação com os anéis segmentados em arcos
        # abertos, então a validação precisa recompô-los: o topo de morro e o fundo
        # de depressão são reconhecidos por is_closed, e sem o anel fechado não há
        # topo nenhum a validar. Dissolver pelos atributos que importam e depois
        # unir as partes reconstrói o anel; o contourid vem em seguida, para
        # identificar a curva já inteira.
        mergedContourLyr = self.algRunner.runMergeLines(
            inputLyr=self.algRunner.runDissolve(
                inputLyr=self.contourLyr,
                context=self.context,
                field=sorted(self.getFieldsToPreserveOnMerge()),
                separateDisjoint=True,
                feedback=multiStepFeedback,
            ),
            context=self.context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Merging lines"))
            multiStepFeedback.setCurrentStep(currentStep)

        self.contourCacheLyr: QgsVectorLayer = (
            self.algRunner.runCreateFieldWithExpression(
                inputLyr=self.algRunner.runMultipartToSingleParts(
                    inputLayer=mergedContourLyr,
                    context=self.context,
                    feedback=multiStepFeedback,
                ),
                expression="$id",
                fieldName="contourid",
                fieldType=1,
                context=self.context,
                feedback=multiStepFeedback,
            )
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(
                self.tr("Creating spatial index on merged lines")
            )
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
        singlePartClippedContourCacheLyr: QgsVectorLayer = (
            self.algRunner.runMultipartToSingleParts(
                inputLayer=auxClippedContourCacheLyr,
                context=self.context,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Finding closed lines"))
            multiStepFeedback.setCurrentStep(currentStep)
        self.clippedContourCacheLyr: QgsVectorLayer = (
            self.algRunner.runCreateFieldWithExpression(
                inputLyr=singlePartClippedContourCacheLyr,
                expression="is_closed($geometry)",
                fieldName="is_closed",
                fieldType=1,
                context=self.context,
                feedback=multiStepFeedback,
            )
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(
                self.tr("Creating spatial index on clipped lines")
            )
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
        self.geoBoundsLineLyr: QgsVectorLayer = self.buildBoundaryLines(
            context=self.context, feedback=multiStepFeedback
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Extracting middle vertices"))
            multiStepFeedback.setCurrentStep(currentStep)
        self.contourMiddlePointsLyr: QgsVectorLayer = (
            self.algRunner.runDSGToolsExtractMiddleVertexOnLine(
                inputLayer=self.clippedContourCacheLyr,
                context=self.context,
                feedback=multiStepFeedback,
            )
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(
                self.tr("Creating spatial index for middle vertices")
            )
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=self.contourMiddlePointsLyr,
            context=self.context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

    def getFieldsToPreserveOnMerge(self) -> Set[str]:
        """
        Returns the fields that must take part on the merge grouping key.

        Merging lines that differ on a field keeps the value of an arbitrary
        one of them, so every field the validation reads afterwards has to be
        part of the key. Besides the elevation, that means the fields the
        depression expression refers to.

        Returns:
            Set[str]: field names that must not be blacklisted on the merge.
        """
        fieldsToPreserve = {self.contourElevationFieldName}
        if self.depressionExpression is None:
            return fieldsToPreserve
        expression = QgsExpression(self.depressionExpression)
        if expression.hasParserError():
            return fieldsToPreserve
        return fieldsToPreserve | {
            column
            for column in expression.referencedColumns()
            if column != QgsFeatureRequest.ALL_ATTRIBUTES
        }

    def buildAuxStructures(
        self,
        context: Optional[QgsProcessingContext] = None,
        feedback: Optional[QgsProcessingFeedback] = None,
    ):
        """
        Builds auxiliary data structures required for terrain processing.

        Args:
            context (Optional[QgsProcessingContext]): Processing context.
            feedback (Optional[QgsProcessingFeedback]): Feedback object.
        """
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(3, feedback)
            if feedback is not None
            else None
        )
        context = QgsProcessingContext() if context is None else context
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.terrainPolygonLayer = self.buildTerrainPolygonLayerFromContours(
            context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Building terrain slices"))
            multiStepFeedback.setCurrentStep(currentStep)
        self.terrainSlicesDict = self.buildTerrainSlices(feedback=multiStepFeedback)

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        self.depressionIdSet = (
            set()
            if self.depressionExpression is None
            else set(
                f["contourid"]
                for f in self.contourCacheLyr.getFeatures(self.depressionExpression)
            )
        )
        self.contourFeatCache = {
            f["contourid"]: f for f in self.contourCacheLyr.getFeatures()
        }
        self.ringGeomCache = dict()
        self.terrainGraph = self.nx.Graph()

    def tr(self, string: str) -> str:
        """
        Initializes the minimum and maximum elevation features on the slice.
        """
        return QCoreApplication.translate("TerrainModel", string)

    def buildTerrainPolygonLayerFromContours(
        self,
        context: Optional[QgsProcessingContext] = None,
        feedback: Optional[QgsProcessingFeedback] = None,
    ) -> QgsVectorLayer:
        """
        Builds a polygon layer from the contours in the terrain model.

        Args:
            context (Optional[QgsProcessingContext]): Processing context.
            feedback (Optional[QgsProcessingFeedback]): Feedback object.

        Returns:
            QgsVectorLayer: Layer containing polygons built from contours.
        """
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
        """
        Creates boundary lines from the geographic bounds of the terrain model.

        Args:
            context (Optional[QgsProcessingContext]): Processing context.
            feedback (Optional[QgsProcessingFeedback]): Feedback object.

        Returns:
            QgsVectorLayer: Layer containing boundary lines.
        """
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
        """
        Constructs terrain slices by dividing polygons based on contours.

        Args:
            context (Optional[QgsProcessingContext]): Processing context.
            feedback (Optional[QgsProcessingFeedback]): Feedback object.

        Returns:
            Dict[int, TerrainSlice]: Dictionary of TerrainSlice objects keyed by polygon ID.
        """
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
        self.contoursMiddlePointsJoinnedByPolygonBand = (
            self.algRunner.runJoinAttributesByLocation(
                inputLyr=self.contourMiddlePointsLyr,
                joinLyr=self.terrainPolygonLayer,
                context=context,
                feedback=multiStepFeedback,
                predicateList=[self.algRunner.Intersects],
                method=0,
                discardNonMatching=True,
                is_child_algorithm=False,
            )
        )

        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
            multiStepFeedback.pushInfo(
                self.tr("Joinning polygon band by middle points.")
            )

        self.polygonBandJoinnedByContoursMiddlePoints = (
            self.algRunner.runJoinAttributesByLocation(
                inputLyr=self.terrainPolygonLayer,
                joinLyr=self.contourMiddlePointsLyr,
                context=context,
                feedback=multiStepFeedback,
                predicateList=[self.algRunner.Intersects],
                method=0,
                discardNonMatching=True,
                is_child_algorithm=False,
            )
        )
        stepSize = 100 / nPolygons
        for current, polygonFeat in enumerate(
            self.terrainPolygonLayer.getFeatures(), start=0
        ):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            request = QgsFeatureRequest()
            request.setFilterExpression(
                f""" "polygonid" = {polygonFeat["polygonid"]}"""
            )
            contoursOnSlice = set(
                f
                for f in self.contoursMiddlePointsJoinnedByPolygonBand.getFeatures(
                    request
                )
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
        """
        Finds contour lines that do not meet the threshold elevation criteria.

        Args:
            context (Optional[QgsProcessingContext]): Processing context.
            feedback (Optional[QgsProcessingFeedback]): Feedback object.

        Returns:
            Dict[QByteArray, str]: Dictionary of errors, keyed by geometry, indicating contours out of threshold.
        """
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
        """
        Validates the entire terrain model for inconsistencies in contours, bands, and spot elevations.

        Args:
            context (Optional[QgsProcessingContext]): Processing context.
            feedback (Optional[QgsProcessingFeedback]): Feedback object.

        Returns:
            Dict[QByteArray, str]: Dictionary with invalid geometries and their messages.
        """
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
        self.buildAuxStructures(context=context, feedback=multiStepFeedback)
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
        invalidDict.update(
            self.validateSpotElevation(context=context, feedback=multiStepFeedback)
        )
        return invalidDict

    def validateContourLines(
        self,
        context: Optional[QgsProcessingContext] = None,
        feedback: Optional[QgsProcessingFeedback] = None,
    ) -> Dict[QByteArray, str]:
        """
        Validates contour lines for dangles, intersections, and threshold compliance.

        Args:
            context (Optional[QgsProcessingContext]): Processing context.
            feedback (Optional[QgsProcessingFeedback]): Feedback object.

        Returns:
            Dict[QByteArray, str]: Dictionary with any errors found in contour lines, keyed by geometry.
        """
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

    def buildTerrainGraph(
        self, feedback: Optional[QgsProcessingFeedback] = None
    ) -> Dict[QByteArray, str]:
        """
        Builds a graph representation of terrain relationships.

        Args:
            feedback (Optional[QgsProcessingFeedback]): Feedback object.

        Returns:
            nx.Graph: Graph representation of terrain with nodes and edges.
        """
        G = self.nx.Graph()
        auxDict = defaultdict(set)
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
        featCount = self.contoursMiddlePointsJoinnedByPolygonBand.featureCount()
        if featCount == 0:
            return G
        stepSize = 100 / featCount
        for current, feat in enumerate(
            self.contoursMiddlePointsJoinnedByPolygonBand.getFeatures()
        ):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                return G
            geom = feat.geometry()
            geomKey = geom.asWkb()
            auxDict[geomKey].add(feat)
            if multiStepFeedback is not None:
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
            if len(polygonSet) != 2:
                continue
            p1, p2 = polygonSet
            G.add_edge(
                p1["polygonid"],
                p2["polygonid"],
                **{
                    "contourid": p1["contourid"],
                    "is_closed": p1["is_closed"],
                    "height": p1[self.contourElevationFieldName],
                },
            )
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)
        return G

    def validateTerrainWithGraph(
        self, feedback: Optional[QgsProcessingFeedback] = None
    ) -> Dict[QByteArray, str]:
        """
        Validates terrain bands using graph traversal for connectivity checks.

        Args:
            feedback (Optional[QgsProcessingFeedback]): Feedback object.

        Returns:
            Dict[QByteArray, str]: Dictionary of validation errors, keyed by geometry.
        """
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        sortedHilltops = self.getHilltops(multiStepFeedback)
        firstOrderNodesThatAreNotHilltops = [
            i
            for i in self.terrainGraph.nodes
            if self.terrainGraph.degree(i) == 1 and i not in sortedHilltops
        ]
        visitedSet = set()
        flagDict = dict()
        for node in itertools.chain(sortedHilltops, firstOrderNodesThatAreNotHilltops):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            visitedSet.add(node)
            edgeData = self.terrainGraph.get_edge_data(
                node, list(self.terrainGraph.neighbors(node))[0]
            )
            currentHeight = edgeData["height"]
            edgeContourId = edgeData["contourid"]
            heightRange = (
                (currentHeight + self.threshold, currentHeight)
                if edgeContourId not in self.depressionIdSet
                else (currentHeight, currentHeight - self.threshold)
            )
            self.nx.set_node_attributes(
                self.terrainGraph, {node: heightRange}, name="heightRange"
            )
            for node in graphHandler.fetch_connected_nodes(
                self.terrainGraph, node, max_degree=2
            ):
                visitedSet.add(node)
                if self.terrainGraph.degree(node) == 1:
                    continue
                n_a, n_b = list(self.terrainGraph.neighbors(node))
                h1 = self.terrainGraph.get_edge_data(node, n_a)["height"]
                h2 = self.terrainGraph.get_edge_data(node, n_b)["height"]
                if abs(h1 - h2) > self.threshold:
                    self.flag_terrain_band(flagDict, node)
                heightRange = (max(h1, h2), min(h1, h2))
                self.nx.set_node_attributes(
                    self.terrainGraph, {node: heightRange}, name="heightRange"
                )
        if len(flagDict) > 0:
            return flagDict
        degreeToStop = -1
        cyclesUnchanged = 0
        while set(self.terrainGraph.nodes) - visitedSet != set():
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            currentVisitedSet = set(visitedSet)
            for node in sorted(
                set(self.terrainGraph.nodes) - visitedSet,
                key=lambda x: self.terrainGraph.degree(x),
            ):
                if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                    break
                if node in visitedSet:
                    continue
                if degreeToStop > 0 and self.terrainGraph.degree(node) > degreeToStop:
                    break
                # grau maior ou igual a 3 daqui para frente
                connectedNodesRanges = set(
                    filter(
                        lambda x: x is not None,
                        (
                            self.terrainGraph.nodes[i].get("heightRange", None)
                            for i in self.terrainGraph.neighbors(node)
                        ),
                    )
                )
                nConnectedNodeRanges = len(list(connectedNodesRanges))
                if nConnectedNodeRanges > 1:
                    self.flag_terrain_band(flagDict, node)
                    degreeToStop = self.terrainGraph.degree(node)
                    visitedSet.add(node)
                    continue

                elif (
                    nConnectedNodeRanges == 1
                    and self.terrainGraph.nodes[node].get("heightRange", None) is None
                ):
                    previousHeightRange = list(connectedNodesRanges)[0]
                    currentHeightRange = (
                        min(previousHeightRange),
                        min(previousHeightRange) - self.threshold,
                    )
                    self.nx.set_node_attributes(
                        self.terrainGraph,
                        {node: currentHeightRange},
                        name="heightRange",
                    )
                else:
                    continue

                visitedSet.add(node)

            if visitedSet - currentVisitedSet == set():
                cyclesUnchanged += 1
            if cyclesUnchanged > 10:
                break
        return flagDict

    def getHilltops(self, feedback: Optional[QgsProcessingFeedback] = None):
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
        self.terrainGraph = self.buildTerrainGraph(feedback=multiStepFeedback)
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
        hilltops = (
            i
            for i in self.terrainGraph.nodes
            if self.terrainGraph.degree(i) == 1
            and self.terrainGraph.get_edge_data(
                i, list(self.terrainGraph.neighbors(i))[0]
            )["is_closed"]
            == True
        )
        sortedHilltops = list(
            sorted(
                hilltops,
                key=lambda x: self.terrainGraph.get_edge_data(
                    x, list(self.terrainGraph.neighbors(x))[0]
                )["height"],
                reverse=True,
            )
        )

        return sortedHilltops

    def getRingGeometry(self, contourid: int) -> Optional[QgsGeometry]:
        """
        Returns the polygon enclosed by a closed contour, or None when the
        contour does not enclose one.

        Args:
            contourid (int): the contour id.

        Returns:
            Optional[QgsGeometry]: the enclosed polygon.
        """
        if contourid in self.ringGeomCache:
            return self.ringGeomCache[contourid]
        contourFeat = self.contourFeatCache.get(contourid)
        ringGeom = (
            None
            if contourFeat is None
            else QgsGeometry.polygonize([contourFeat.geometry()])
        )
        if ringGeom is not None and ringGeom.isEmpty():
            ringGeom = None
        self.ringGeomCache[contourid] = ringGeom
        return ringGeom

    def getInnerBand(self, nodeA: int, nodeB: int, contourid: int) -> Optional[int]:
        """
        Returns which of the two bands separated by a closed contour lies inside
        its ring.

        Telling the two sides apart is what allows the terrain direction to be
        read: the region outside the outermost closed contour of a hill looks
        exactly like a cap from the graph alone.

        Args:
            nodeA (int): polygonid of one of the bands.
            nodeB (int): polygonid of the other band.
            contourid (int): id of the closed contour between them.

        Returns:
            Optional[int]: polygonid of the inner band, or None if undetermined.
        """
        ringGeom = self.getRingGeometry(contourid)
        if ringGeom is None:
            return None
        for candidate in (nodeA, nodeB):
            terrainSlice = self.terrainSlicesDict.get(candidate)
            if terrainSlice is None:
                continue
            bandPoint = terrainSlice.polygonFeat.geometry().pointOnSurface()
            if ringGeom.contains(bandPoint):
                return candidate
        return None

    def getClosedCapContourId(self, bandId: int) -> Optional[int]:
        """
        Returns the id of the closed contour that delimits bandId when bandId is
        the innermost band of a hilltop or of a depression, and None otherwise.

        Args:
            bandId (int): the polygonid of the band.

        Returns:
            Optional[int]: contourid of the delimiting contour, or None.
        """
        if bandId not in self.terrainGraph or self.terrainGraph.degree(bandId) != 1:
            return None
        neighbor = list(self.terrainGraph.neighbors(bandId))[0]
        edgeData = self.terrainGraph.get_edge_data(bandId, neighbor)
        if not edgeData.get("is_closed"):
            return None
        contourid = edgeData["contourid"]
        if self.getInnerBand(bandId, neighbor, contourid) != bandId:
            return None
        return contourid

    def getContourHeightsAroundBand(self, bandId: int, exclude: int) -> list:
        """
        Returns the heights of the contours bounding a band, skipping the one
        shared with the excluded band.

        Args:
            bandId (int): the polygonid of the band.
            exclude (int): polygonid of the neighbour to skip.

        Returns:
            list: heights of the remaining bounding contours.
        """
        return [
            self.terrainGraph.get_edge_data(bandId, neighbor)["height"]
            for neighbor in self.terrainGraph.neighbors(bandId)
            if neighbor != exclude
        ]

    def isDepressionContour(self, nodeA: int, nodeB: int) -> Optional[bool]:
        """
        Tells whether the closed contour between two bands is a depression
        contour, i.e. whether the terrain descends as one moves inside its ring.

        The reading is taken from the band inside the ring: if every other
        contour bounding it is lower, the terrain descends inwards and the
        contour delimits a depression; if every one of them is higher, it
        ascends and the contour delimits a hilltop. The innermost band has no
        other contour, so the surrounding band is read instead, the other way
        around. Anything else (mixed or equal heights) is undetermined.

        Args:
            nodeA (int): polygonid of one of the bands.
            nodeB (int): polygonid of the other band.

        Returns:
            Optional[bool]: True for a depression contour, False for a hilltop
                            one, None when the terrain direction is undetermined.
        """
        edgeData = self.terrainGraph.get_edge_data(nodeA, nodeB)
        if edgeData is None or not edgeData.get("is_closed"):
            return None
        height = edgeData["height"]
        innerBand = self.getInnerBand(nodeA, nodeB, edgeData["contourid"])
        if innerBand is None:
            return None
        outerBand = nodeB if innerBand == nodeA else nodeA
        innerHeights = self.getContourHeightsAroundBand(innerBand, exclude=outerBand)
        if innerHeights:
            if all(h < height for h in innerHeights):
                return True
            if all(h > height for h in innerHeights):
                return False
            return None
        outerHeights = self.getContourHeightsAroundBand(outerBand, exclude=innerBand)
        if not outerHeights:
            return None
        if all(h < height for h in outerHeights):
            return False
        if all(h > height for h in outerHeights):
            return True
        return None

    def validateDepressionAttribution(
        self, feedback: Optional[QgsProcessingFeedback] = None
    ) -> Dict[QByteArray, str]:
        """
        Checks the depression attribute of every closed contour whose terrain
        direction can be determined, which covers the contours nested inside a
        hilltop or a depression and not only the innermost one.

        Args:
            feedback (Optional[QgsProcessingFeedback]): Feedback object.

        Returns:
            Dict[QByteArray, str]: Dictionary of errors, keyed by geometry.
        """
        flagDict = dict()
        for nodeA, nodeB in list(self.terrainGraph.edges):
            if feedback is not None and feedback.isCanceled():
                break
            isDepression = self.isDepressionContour(nodeA, nodeB)
            if isDepression is None:
                continue
            edgeData = self.terrainGraph.get_edge_data(nodeA, nodeB)
            contourid = edgeData["contourid"]
            isMarkedAsDepression = contourid in self.depressionIdSet
            if isDepression == isMarkedAsDepression:
                continue
            height = edgeData["height"]
            flagMessage = (
                self.tr(
                    f"Contour with height {height} is not marked as depression but terrain model indicates it is a depression."
                )
                if isDepression
                else self.tr(
                    f"Contour with height {height} is marked as depression but terrain model indicates it is a normal hilltop (peak)."
                )
            )
            contourFeat = self.contourFeatCache.get(contourid)
            if contourFeat is not None:
                flagDict[contourFeat.geometry().asWkb()] = flagMessage
        return flagDict

    def flag_terrain_band(self, flagDict, node):
        """
        Flags terrain bands that are out of the threshold range.

        Args:
            flagDict (dict): Dictionary for storing validation errors.
            node: Node in the terrain graph to be flagged.
        """
        polygonFeat = self.terrainSlicesDict[node].polygonFeat
        geom = polygonFeat.geometry()
        geomKey = geom.asWkb()
        flagDict[geomKey] = self.tr("Terrain band contours out of threshold.")

    def validateTerrainBands(
        self, feedback: Optional[QgsProcessingFeedback] = None
    ) -> Dict[QByteArray, str]:
        """
        Validates terrain bands for elevation consistency.

        Args:
            feedback (Optional[QgsProcessingFeedback]): Feedback object.

        Returns:
            Dict[QByteArray, str]: Dictionary of errors, keyed by geometry.
        """
        invalidDict = dict()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(3, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Validating terrain bands"))
            multiStepFeedback.setCurrentStep(0)

        for slice in self.terrainSlicesDict.values():
            output = slice.validate()
            if output == dict():
                continue
            invalidDict.update(output)
        if invalidDict != dict():
            return invalidDict
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(
                self.tr("Building terrain graph and validating built terrain with it")
            )
            multiStepFeedback.setCurrentStep(1)
        invalidDict = self.validateTerrainWithGraph(feedback=multiStepFeedback)
        if invalidDict != dict():
            return invalidDict
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(
                self.tr("Validating depression attribution on hilltops")
            )
            multiStepFeedback.setCurrentStep(2)
        invalidDict.update(
            self.validateDepressionAttribution(feedback=multiStepFeedback)
        )
        return invalidDict

    def getSpotElevationFlagText(
        self, bandId: int, pointHeight: float, h_min: float, h_max: float
    ) -> Optional[str]:
        """
        Returns the reason why a spot elevation is inconsistent with the band it
        falls into, or None when it is acceptable.

        On a regular band the valid range is the one delimited by the bounding
        contours. On the innermost band of a hilltop or of a depression both
        bounding heights are the same and the range is open ended, so the
        direction comes from the depression attribution: a peak runs from the
        contour up, a depression runs from the contour down.

        Args:
            bandId (int): the polygonid of the band the point falls into.
            pointHeight (float): the spot elevation height.
            h_min (float): lowest contour bounding the band.
            h_max (float): highest contour bounding the band.

        Returns:
            Optional[str]: flag message, or None if the spot elevation is valid.
        """
        if h_min != h_max:
            if h_min <= pointHeight <= h_max:
                return None
            return self.tr(
                f"Elevation point with height {pointHeight} out of threshold. This value should be between {h_min} and {h_max}"
            )
        capContourId = self.getClosedCapContourId(bandId)
        if capContourId is None:
            # Not a cap: the band is bounded by distinct contours that happen to
            # share a height (a saddle, for instance), which says nothing about
            # which way the terrain runs. Only the permissive range is checked.
            if h_max + self.threshold >= pointHeight >= h_min - self.threshold:
                return None
            return self.tr(
                f"Elevation point with height {pointHeight} out of threshold. This value should be between {h_min - self.threshold} and {h_max + self.threshold}"
            )
        if capContourId in self.depressionIdSet:
            if h_min - self.threshold <= pointHeight <= h_min:
                return None
            return self.tr(
                f"Elevation point with height {pointHeight} out of threshold. This value is on a valley/depression and should be between {h_min - self.threshold} and {h_min}"
            )
        if h_max <= pointHeight <= h_max + self.threshold:
            return None
        return self.tr(
            f"Elevation point with height {pointHeight} out of threshold. This value is on a hilltop and should be between {h_max} and {h_max + self.threshold}"
        )

    def validateSpotElevation(
        self,
        context: Optional[QgsProcessingContext],
        feedback: Optional[QgsProcessingFeedback] = None,
    ) -> Dict[QByteArray, str]:
        """
        Validates spot elevations for consistency with contour lines and elevation bands.

        Args:
            context (Optional[QgsProcessingContext]): Processing context.
            feedback (Optional[QgsProcessingFeedback]): Feedback object.

        Returns:
            Dict[QByteArray, str]: Dictionary with invalid spot elevation features.
        """
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(3, feedback)
            if feedback is not None
            else None
        )
        currentStep = 0
        context = QgsProcessingContext() if context is None else context
        invalidDict = dict()
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        if (
            self.spotElevationLyr is not None
            and self.spotElevationLyr.featureCount() == 0
        ):
            return invalidDict
        spotElevationsThatIntersectContours = self.algRunner.runExtractByLocation(
            inputLyr=self.spotElevationLyr,
            intersectLyr=self.contourLyr,
            context=context,
            predicate=[self.algRunner.Intersects],
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
            multiStepFeedback.pushInfo(
                self.tr("Checking spot elevations with contour interval multiples")
            )
        interval = int(self.threshold)
        if interval > 0:
            filterExpr = (
                f'"{self.spotElevationFieldName}" IS NOT NULL AND '
                f'"{self.spotElevationFieldName}" % {interval} = 0'
            )
            request = QgsFeatureRequest().setFilterExpression(filterExpr)
            for feat in self.spotElevationLyr.getFeatures(request):
                if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                    break
                pointHeight = feat[self.spotElevationFieldName]
                pointGeom = feat.geometry()
                invalidDict[pointGeom.asWkb()] = self.tr(
                    f"Spot elevation with height {pointHeight} is a multiple of the contour interval ({interval}). "
                    f"Spot elevations should not have the same value as contour lines."
                )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        joinnedSpotElevation = self.algRunner.runJoinAttributesByLocation(
            inputLyr=self.spotElevationLyr,
            joinLyr=self.terrainPolygonLayer,
            context=context,
        )
        nFeats = joinnedSpotElevation.featureCount()
        if nFeats == 0:
            return invalidDict
        stepSize = 100 / nFeats

        for current, feat in enumerate(joinnedSpotElevation.getFeatures()):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            bandId = feat["polygonid"]
            pointHeight = feat[self.spotElevationFieldName]
            if bandId not in self.terrainSlicesDict:
                continue
            h_min, h_max = self.terrainSlicesDict[bandId].getMinMaxHeight()
            if h_min is None or h_max is None or pointHeight is None:
                continue
            flagText = self.getSpotElevationFlagText(bandId, pointHeight, h_min, h_max)
            if flagText is None:
                continue
            pointGeom = feat.geometry()
            invalidDict[pointGeom.asWkb()] = flagText
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)
        return invalidDict
