# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-10-22
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

from itertools import tee, combinations
from collections import defaultdict, OrderedDict
import os

from qgis.core import (
    QgsProject,
    QgsGeometry,
    QgsExpression,
    QgsVectorLayer,
    QgsSpatialIndex,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingMultiStepFeedback,
    QgsFeatureRequest,
)
from qgis.PyQt.Qt import QObject
from qgis.PyQt.QtCore import QRegExp, QCoreApplication
from qgis.PyQt.QtGui import QRegExpValidator

from .featureHandler import FeatureHandler
from .geometryHandler import GeometryHandler
from .layerHandler import LayerHandler
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class SpatialRelationsHandler(QObject):
    __predicates = (
        QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "equals"),
        QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "is not equals"),
        QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "disjoint"),
        QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "intersects"),
        QCoreApplication.translate(
            "EnforceSpatialRulesAlgorithm", "does not intersect"
        ),
        QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "touches"),
        QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "does not touch"),
        QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "crosses"),
        QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "does not cross"),
        QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "within"),
        QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "is not within"),
        QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "overlaps"),
        QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "does not overlap"),
        QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "contains"),
        QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "does not contain"),
        QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "de9im"),
    )
    (
        EQUALS,
        NOTEQUALS,
        DISJOINT,
        INTERSECTS,
        NOTINTERSECTS,
        TOUCHES,
        NOTTOUCHES,
        CROSSES,
        NOTCROSSES,
        WITHIN,
        NOTWITHIN,
        OVERLAPS,
        NOTOVERLAPS,
        CONTAINS,
        NOTCONTAINS,
        DE9IM,
    ) = range(len(__predicates))

    def __init__(self, iface=None, parent=None):
        super(SpatialRelationsHandler, self).__init__()
        self.parent = parent
        self.iface = iface
        if iface:
            self.canvas = iface.mapCanvas()
        self.layerHandler = LayerHandler(iface)
        self.featureHandler = FeatureHandler(iface)
        self.geometryHandler = GeometryHandler(iface)
        self.algRunner = AlgRunner()

    def validateTerrainModel(
        self,
        contourLyr,
        heightFieldName,
        threshold,
        elevationPointsLyr=None,
        elevationPointHeightFieldName=None,
        onlySelected=False,
        geoBoundsLyr=None,
        context=None,
        feedback=None,
    ):
        """
        Does several validation procedures with terrain elements.
        """
        invalidDict = OrderedDict()
        nSteps = 7 if elevationPointsLyr is None else 9
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(nSteps, feedback)
            if feedback is not None
            else None
        )  # ajustar depois
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Splitting lines..."))
        splitLinesLyr = self.algRunner.runSplitLinesWithLines(
            contourLyr, contourLyr, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Building aux structure..."))
        (
            contourSpatialIdx,
            contourIdDict,
            contourNodeDict,
            heightsDict,
        ) = self.buildSpatialIndexAndIdDictRelateNodesAndAttributeGroupDict(
            inputLyr=splitLinesLyr,
            attributeName=heightFieldName,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        geoBoundsGeomEngine, geoBoundsPolygonEngine = (
            (None, None)
            if geoBoundsLyr is None
            else self.getGeoBoundsGeomEngine(
                geoBoundsLyr, context=context, feedback=multiStepFeedback
            )
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(
                self.tr("Validating contour relations...")
            )
        contourFlags = self.validateContourRelations(
            contourNodeDict,
            heightFieldName,
            geoBoundsGeomEngine=geoBoundsGeomEngine,
            geoBoundsPolygonEngine=geoBoundsPolygonEngine,
        )
        currentStep += 1

        invalidDict.update(contourFlags)
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(
                self.tr("Finding contour out of threshold...")
            )
        contourOutOfThresholdDict = self.findContourOutOfThreshold(
            heightsDict, threshold, feedback=multiStepFeedback
        )
        currentStep += 1
        invalidDict.update(contourOutOfThresholdDict)
        if len(invalidDict) > 0:
            return invalidDict
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Building contour area dict.."))
        contourAreaDict, polygonLyr = self.buildContourAreaDict(
            inputLyr=splitLinesLyr,
            geoBoundsLyr=geoBoundsLyr,
            attributeName=heightFieldName,
            contourSpatialIdx=contourSpatialIdx,
            contourIdDict=contourIdDict,
            depressionExpression=None,  # TODO
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Finding missing contours..."))
        missingContourDict = self.findMissingContours(
            contourAreaDict, threshold, context=context, feedback=multiStepFeedback
        )
        invalidDict.update(missingContourDict)
        currentStep += 1

        if elevationPointsLyr is None or len(missingContourDict) > 0:
            return invalidDict
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(
                self.tr("Finding elevation points out of threshold...")
            )
        pointErrorDict = self.findElevationPointsOutOfThreshold(
            elevationPointsLyr,
            polygonLyr,
            contourAreaDict,
            threshold,
            elevationPointHeightFieldName,
            context=context,
            feedback=multiStepFeedback,
        )
        invalidDict.update(pointErrorDict)
        return invalidDict

    def getGeoBoundsGeomEngine(self, geoBoundsLyr, context=None, feedback=None):
        """
        returns an initiated QgsGeometryEngine from the merged polygon boundary of geoBoundsLyr
        """
        if geoBoundsLyr is None:
            return None, None
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
        mergedPolygonLyr = self.algRunner.runAggregate(
            geoBoundsLyr, context=context, feedback=multiStepFeedback
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
        mergedPolygonGeom = (
            [i for i in mergedPolygonLyr.getFeatures()][0].geometry()
            if mergedPolygonLyr.featureCount() != 0
            else None
        )
        if mergedPolygonGeom is None:
            return None, None
        polygonBoundary = self.algRunner.runBoundary(
            mergedPolygonLyr, context=context, feedback=multiStepFeedback
        )
        mergedGeom = (
            [i for i in polygonBoundary.getFeatures()][0].geometry()
            if polygonBoundary.featureCount() != 0
            else None
        )
        if mergedGeom is None:
            return None, None
        polygonEngine = QgsGeometry.createGeometryEngine(mergedPolygonGeom.constGet())
        polygonEngine.prepareGeometry()
        engine = QgsGeometry.createGeometryEngine(mergedGeom.constGet())
        engine.prepareGeometry()
        return engine, polygonEngine

    def buildContourAreaDict(
        self,
        inputLyr,
        geoBoundsLyr,
        attributeName,
        contourSpatialIdx,
        contourIdDict,
        depressionExpression=None,
        context=None,
        feedback=None,
    ):
        """
        Builds a dict in the following format:
        {
            'areaSpatialIdx' : QgsSpatialIndex of the built areas,
            'areaIdDict' : {id:feat}
            'areaContourRelations' : {id : {height:[list of feats]}}
        }
        """
        contourAreaDict = {
            "areaSpatialIdx": QgsSpatialIndex(),
            "areaIdDict": {},
            "areaContourRelations": {},
        }
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
        polygonLyr = self.buildTerrainPolygonLayerFromContours(
            inputLyr=inputLyr,
            geoBoundsLyr=geoBoundsLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
        self.populateContourAreaDict(
            polygonLyr,
            geoBoundsLyr,
            attributeName,
            contourAreaDict,
            contourSpatialIdx,
            contourIdDict,
            feedback=multiStepFeedback,
        )
        return contourAreaDict, polygonLyr

    def buildTerrainPolygonLayerFromContours(
        self,
        inputLyr: QgsVectorLayer,
        geoBoundsLyr: QgsVectorLayer,
        context: QgsProcessingContext = None,
        feedback: QgsProcessingFeedback = None,
        createSpatialIndex: bool = False,
    ) -> QgsVectorLayer:
        nSteps = 3 if not createSpatialIndex else 4
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(nSteps, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
        boundsLineLyr = (
            self.algRunner.runPolygonsToLines(
                geoBoundsLyr, context, feedback=multiStepFeedback
            )
            if geoBoundsLyr is not None
            else None
        )
        lineLyrList = [inputLyr] if boundsLineLyr is None else [inputLyr, boundsLineLyr]
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
        linesLyr = self.algRunner.runMergeVectorLayers(
            lineLyrList, context, feedback=multiStepFeedback
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(2)
        polygonLyr = self.algRunner.runPolygonize(
            linesLyr, context, feedback=multiStepFeedback
        )
        if createSpatialIndex:
            self.algRunner.runCreateSpatialIndex(
                inputLyr=polygonLyr,
                context=context,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )
        return polygonLyr

    def createHilltopLayerFromPolygonLayer(
        self,
        polygonLayer: QgsVectorLayer,
        geographicBoundsLyr: QgsVectorLayer,
        context: QgsProcessingContext,
        feedback: QgsProcessingFeedback = None,
        computeOrder: bool = False,
    ) -> QgsVectorLayer:
        nSteps = 13 if not computeOrder else 16
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(nSteps, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
        outerShellLyr, _ = self.algRunner.runDonutHoleExtractor(
            polygonLayer,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=outerShellLyr,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        hilltopsLyr = self.algRunner.runExtractByLocation(
            inputLyr=polygonLayer,
            intersectLyr=outerShellLyr,
            predicate=[3],
            context=context,
            feedback=multiStepFeedback,
        )
        if not computeOrder:
            return hilltopsLyr
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        outershellWithOrder = self.algRunner.runCreateFieldWithExpression(
            inputLyr=outerShellLyr,
            expression="1",
            fieldName="order",
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=outerShellLyr,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        hilltopsWithOrder = self.algRunner.runJoinByLocationSummary(
            inputLyr=hilltopsLyr,
            joinLyr=outershellWithOrder,
            predicateList=[5],
            summaries=[0],
            joinFields=["order"],
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        hilltopsWithOrder = self.algRunner.runCreateFieldWithExpression(
            inputLyr=hilltopsWithOrder,
            expression="$id",
            fieldType=1,
            fieldName="hfid",
            feedback=multiStepFeedback,
            context=context,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=hilltopsWithOrder,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        geographicBoundsLineLyr = self.algRunner.runPolygonsToLines(
            inputLyr=geographicBoundsLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        geographicBoundsLineLyr = self.algRunner.runExplodeLines(
            geographicBoundsLineLyr, context=context, feedback=multiStepFeedback
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runAddUnsharedVertexOnSharedEdges(
            inputLinesList=[geographicBoundsLineLyr],
            inputPolygonsList=[hilltopsWithOrder],
            searchRadius=1e-5 if geographicBoundsLyr.crs().isGeographic() else 1e-2,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        intersectedLines = self.algRunner.runIntersection(
            inputLyr=geographicBoundsLineLyr,
            overlayLyr=hilltopsWithOrder,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        singleParts = self.algRunner.runMultipartToSingleParts(
            inputLayer=intersectedLines, context=context, feedback=multiStepFeedback
        )
        nFeats = singleParts.featureCount()
        if nFeats == 0:
            return hilltopsWithOrder
        groupDict = defaultdict(set)
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        stepSize = 100 / nFeats
        for current, feat in enumerate(singleParts.getFeatures()):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                return hilltopsWithOrder
            groupDict[feat["hfid"]].add(feat)
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        stepSize = 100 / len(groupDict)
        idsToIgnoreSet = set()
        for current, (featId, featSet) in enumerate(groupDict.items()):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                return hilltopsWithOrder
            if len(featSet) <= 1:
                continue
            idsToIgnoreSet.add(featId)
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        outputHilltopWithOrder = (
            self.algRunner.runFilterExpression(
                inputLyr=hilltopsWithOrder,
                context=context,
                expression=f"hfid not in {tuple(idsToIgnoreSet)}".replace(",)", ")"),
                feedback=multiStepFeedback,
            )
            if len(idsToIgnoreSet) > 0
            else hilltopsWithOrder
        )
        return outputHilltopWithOrder

    def populateContourAreaDict(
        self,
        polygonLyr,
        geoBoundsLyr,
        attributeName,
        contourAreaDict,
        contourSpatialIdx,
        contourIdDict,
        feedback=None,
    ):
        boundsGeom = (
            [i for i in geoBoundsLyr.getFeatures()][0].geometry()
            if geoBoundsLyr is not None
            else None
        )
        nPolygons = polygonLyr.featureCount()
        size = 100 / nPolygons if nPolygons else 0
        for current, feat in enumerate(polygonLyr.getFeatures()):
            if feedback is not None and feedback.isCanceled():
                break
            featId = feat.id()
            geom = feat.geometry()
            featBB = geom.boundingBox()
            contourAreaDict["areaSpatialIdx"].addFeature(feat)
            contourAreaDict["areaIdDict"][featId] = feat
            if featId not in contourAreaDict["areaContourRelations"]:
                contourAreaDict["areaContourRelations"][featId] = defaultdict(list)
            for contourId in contourSpatialIdx.intersects(featBB):
                if feedback is not None and feedback.isCanceled():
                    break
                candidateContourFeat = contourIdDict[contourId]
                if not candidateContourFeat.geometry().intersects(geom):
                    continue
                contourValue = candidateContourFeat[attributeName]
                candidateContourGeom = (
                    candidateContourFeat.geometry()
                    if boundsGeom is not None
                    and not candidateContourFeat.geometry().intersects(boundsGeom)
                    else candidateContourFeat.geometry().intersection(boundsGeom)
                )
                contourAreaDict["areaContourRelations"][featId][contourValue].append(
                    candidateContourGeom
                )
            if feedback is not None:
                feedback.setProgress(current * size)

    def findContourOutOfThreshold(self, heightsDict, threshold, feedback=None):
        contourOutOfThresholdDict = OrderedDict()
        size = 100 / len(heightsDict) if len(heightsDict) else 0
        for current, (k, valueSet) in enumerate(heightsDict.items()):
            if feedback is not None and feedback.isCanceled():
                break
            for i in valueSet:
                if feedback is not None and feedback.isCanceled():
                    break
                if k % threshold != 0:
                    contourOutOfThresholdDict[i.asWkb()] = self.tr(
                        "Contour out of threshold."
                    )
            if feedback is not None:
                feedback.setProgress(current * size)
        return contourOutOfThresholdDict

    def findMissingContours(
        self, contourAreaDict, threshold, context=None, feedback=None
    ):
        """
        Can be more efficient, the first draft will be of several for inside for.
        """
        relationCount = len(contourAreaDict["areaContourRelations"])
        size = 100 / relationCount if relationCount else 0
        missingContourFlagDict = dict()
        for current, (areaId, heightDict) in enumerate(
            contourAreaDict["areaContourRelations"].items()
        ):
            if feedback is not None and feedback.isCanceled():
                break
            if len(heightDict) < 2:
                continue
            for h1, h2 in combinations(heightDict.keys(), 2):
                if abs(h1 - h2) <= threshold:
                    continue
                min_h12 = min(h1, h2)  # done to fix the way flags are built.
                max_h12 = max(h1, h2)
                for geom in heightDict[h1]:
                    if feedback is not None and feedback.isCanceled():
                        break
                    shortestLineGeomList = [
                        geom.shortestLine(i) for i in heightDict[h2]
                    ]
                    shortestLine = min(shortestLineGeomList, key=lambda x: x.length())
                    missingContourFlagDict.update(
                        {
                            shortestLine.asWkb(): self.tr(
                                "Missing contour between contour lines of values {v1} and {v2}"
                            ).format(v1=min_h12, v2=max_h12)
                        }
                    )
            if feedback is not None:
                feedback.setProgress(current * size)
        return missingContourFlagDict

    def findElevationPointsOutOfThreshold(
        self,
        elevationPoints,
        polygonLyr,
        contourAreaDict,
        threshold,
        elevationPointHeightFieldName,
        context,
        feedback=None,
    ):
        self.algRunner.runCreateSpatialIndex(
            polygonLyr, context, feedback=feedback, is_child_algorithm=True
        )
        invalidDict = dict()
        nFeats = (
            elevationPoints.featureCount()
            if isinstance(elevationPoints, QgsVectorLayer)
            else len(elevationPoints)
        )
        iterator = (
            elevationPoints.getFeatures()
            if isinstance(elevationPoints, QgsVectorLayer)
            else elevationPoints
        )
        if nFeats == 0:
            return invalidDict
        stepSize = 100 / nFeats
        for current, pointFeat in enumerate(iterator):
            if feedback is not None and feedback.isCanceled():
                break
            pointGeom = pointFeat.geometry()
            pointBuffer = pointGeom.buffer(1e-8, -1)
            bbox = pointBuffer.boundingBox()
            pointHeight = pointFeat[elevationPointHeightFieldName]
            for areaFeat in polygonLyr.getFeatures(bbox):
                areaGeom = areaFeat.geometry()
                if not areaGeom.intersects(pointGeom):
                    continue
                areaId = areaFeat.id()
                countourList = contourAreaDict["areaContourRelations"][areaId].keys()
                if countourList == [] or countourList is None or len(countourList) == 0:
                    continue
                h_min = min(countourList, default=None)
                h_max = max(countourList, default=None)
                if h_min is None or h_max is None:
                    continue
                if pointHeight == h_min or pointHeight == h_max:
                    continue
                if h_min == h_max:
                    if pointHeight > h_max + threshold:
                        flagText = self.tr(
                            f"Elevation point with height {pointHeight} out of threshold. This value is on a hilltop and should be between {h_max} and {h_max+threshold}"
                        )
                    elif pointHeight < h_min - threshold:
                        flagText = self.tr(
                            f"Elevation point with height {pointHeight} out of threshold. This value is on a valley/depression and should be between {h_min} and {h_min-threshold}"
                        )
                    else:
                        continue
                elif pointHeight < h_min or pointHeight > h_max:
                    flagText = self.tr(
                        f"Elevation point with height {pointHeight} out of threshold. This value should be between {h_min} and {h_max}"
                    )
                else:
                    continue
                invalidDict[pointGeom.asWkb()] = flagText

            if feedback is not None:
                feedback.setProgress(current * stepSize)
        return invalidDict

    def relateDrainagesWithContours(
        self,
        drainageLyr,
        contourLyr,
        frameLinesLyr,
        heightFieldName,
        threshold,
        topologyRadius,
        feedback=None,
    ):
        """
        Checks the conformity between directed drainages and contours.
        Drainages must be propperly directed.
        :param drainageLyr: QgsVectorLayer (line) with drainage lines.
        This must have a primary key field;
        :param contourLyr: QgsVectorLayer (line) with contour lines.
        This must have a primary key field;
        :param frameLinesLyrLyr: QgsVectorLayer (line) with frame lines;
        :param heightFieldName: (str) name of the field that stores
        contour's height;
        :param threshold: (int) equidistance between contour lines;
        :param threshold: (float) topology radius;
        Process steps:
        1- Build spatial indexes;
        2- Compute intersections between drainages and contours;
        3- Relate intersections grouping by drainages: calculate the
        distance between the start point and each intersection, then
        order the points by distance. If the height of each point does
        not follow this order, flag the intersection.
        4- After relating everything,
        """
        maxSteps = 4
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(maxSteps, feedback)
            if feedback is not None
            else None
        )
        currentStep = 0
        if multiStepFeedback is not None:
            if multiStepFeedback.isCanceled():
                return []
            multiStepFeedback.setCurrentStep(currentStep)
            currentStep += 1
            multiStepFeedback.pushInfo(self.tr("Building contour structures..."))
        (
            contourSpatialIdx,
            contourIdDict,
            contourNodeDict,
            heightsDict,
        ) = self.buildSpatialIndexAndIdDictRelateNodesAndAttributeGroupDict(
            inputLyr=contourLyr,
            attributeName=heightFieldName,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            if multiStepFeedback.isCanceled():
                return []
            multiStepFeedback.setCurrentStep(currentStep)
            currentStep += 1
            multiStepFeedback.pushInfo(
                self.tr("Validating contour structures. Check 1/4...")
            )
        invalidDict = self.validateContourRelations(
            contourNodeDict, feedback=multiStepFeedback
        )
        if invalidDict:
            multiStepFeedback.setCurrentStep(maxSteps - 1)
            return invalidDict

        if multiStepFeedback is not None:
            if multiStepFeedback.isCanceled():
                return []
            multiStepFeedback.setCurrentStep(currentStep)
            currentStep += 1
            multiStepFeedback.pushInfo(self.tr("Building drainage spatial index..."))
        (
            drainageSpatialIdx,
            drainageIdDict,
            drainageNodeDict,
        ) = self.buildSpatialIndexAndIdDictAndRelateNodes(
            inputLyr=drainageLyr, feedback=multiStepFeedback
        )
        if multiStepFeedback is not None:
            if multiStepFeedback.isCanceled():
                return []
            multiStepFeedback.setCurrentStep(currentStep)
            currentStep += 1
            multiStepFeedback.pushInfo(self.tr("Relating contours with drainages..."))
        intersectionDict = self.buildIntersectionDict(
            drainageLyr,
            drainageIdDict,
            drainageSpatialIdx,
            contourIdDict,
            contourIdDict,
        )

    def buildSpatialIndexAndIdDictAndRelateNodes(
        self, inputLyr, feedback=None, featureRequest=None
    ):
        """
        creates a spatial index for the input layer
        :param inputLyr: (QgsVectorLayer) input layer;
        :param feedback: (QgsProcessingFeedback) processing feedback;
        :param featureRequest: (QgsFeatureRequest) optional feature request;
        """
        spatialIdx = QgsSpatialIndex()
        idDict = {}
        nodeDict = defaultdict(list)
        featCount = inputLyr.featureCount()
        size = 100 / featCount if featCount else 0
        iterator = (
            inputLyr.getFeatures()
            if featureRequest is None
            else inputLyr.getFeatures(featureRequest)
        )
        firstAndLastNode = lambda x: self.geometryHandler.getFirstAndLastNode(
            inputLyr, x
        )
        addFeatureAlias = lambda x: self.addFeatureToSpatialIndexAndNodeDict(
            current=x[0],
            feat=x[1],
            spatialIdx=spatialIdx,
            idDict=idDict,
            nodeDict=nodeDict,
            size=size,
            firstAndLastNode=firstAndLastNode,
            feedback=feedback,
        )
        list(map(addFeatureAlias, enumerate(iterator)))

        return spatialIdx, idDict, nodeDict

    def addFeatureToSpatialIndexAndNodeDict(
        self, current, feat, spatialIdx, idDict, nodeDict, size, feedback
    ):
        """
        Adds feature to spatial index. Used along side with a python map
        operator to improve performance.
        :param current : (int) current index
        :param feat : (QgsFeature) feature to be added on spatial index and
        on idDict
        :param spatialIdx: (QgsSpatialIndex) spatial index
        :param idDict: (dict) dictionary with format {feat.id(): feat}
        :param nodeDict: (defaultdict(list)) dictionary with format
        {node:[list of features]}
        :param size: (int) size to be used to update feedback
        :param feedback: (QgsProcessingFeedback) feedback to be used on
        processing
        """
        if feedback is not None and feedback.isCanceled():
            return
        firstNode, lastNode = self.geometryHandler.getFirstAndLastNodeFromGeom(
            feat.geometry()
        )
        nodeDict[firstNode] += [feat]
        nodeDict[lastNode] += [feat]
        self.layerHandler.addFeatureToSpatialIndex(
            current, feat, spatialIdx, idDict, size, feedback
        )

    def buildSpatialIndexAndIdDictRelateNodesAndAttributeGroupDict(
        self, inputLyr, attributeName, feedback=None, featureRequest=None
    ):
        """ """
        spatialIdx = QgsSpatialIndex()
        idDict = {}
        nodeDict = defaultdict(list)
        attributeGroupDict = {}
        featCount = inputLyr.featureCount()
        size = 100 / featCount if featCount else 0
        iterator = (
            inputLyr.getFeatures()
            if featureRequest is None
            else inputLyr.getFeatures(featureRequest)
        )
        addFeatureAlias = (
            lambda x: self.addFeatureToSpatialIndexNodeDictAndAttributeGroupDict(
                current=x[0],
                feat=x[1],
                spatialIdx=spatialIdx,
                idDict=idDict,
                nodeDict=nodeDict,
                size=size,
                attributeGroupDict=attributeGroupDict,
                attributeName=attributeName,
                feedback=feedback,
            )
        )
        list(map(addFeatureAlias, enumerate(iterator)))
        return spatialIdx, idDict, nodeDict, attributeGroupDict

    def addFeatureToSpatialIndexNodeDictAndAttributeGroupDict(
        self,
        current,
        feat,
        spatialIdx,
        idDict,
        nodeDict,
        size,
        attributeGroupDict,
        attributeName,
        feedback,
    ):
        """
        Adds feature to spatial index. Used along side with a python map operator
        to improve performance.
        :param current : (int) current index
        :param feat : (QgsFeature) feature to be added on spatial index and on idDict
        :param spatialIdx: (QgsSpatialIndex) spatial index
        :param idDict: (dict) dictionary with format {feat.id(): feat}
        :param size: (int) size to be used to update feedback
        :param firstAndLastNode: (dict) dictionary used to relate nodes of features
        :param feedback: (QgsProcessingFeedback) feedback to be used on processing
        """
        attrValue = feat[attributeName]
        if attrValue not in attributeGroupDict:
            attributeGroupDict[attrValue] = set()
        attributeGroupDict[attrValue].add(feat.geometry())
        self.addFeatureToSpatialIndexAndNodeDict(
            current, feat, spatialIdx, idDict, nodeDict, size, feedback
        )

    def validateContourRelations(
        self,
        contourNodeDict,
        heightFieldName,
        geoBoundsGeomEngine=None,
        geoBoundsPolygonEngine=None,
        feedback=None,
    ):
        """
        param: contourNodeDict: (dict) dictionary with contour nodes
        Invalid contours:
        - Contours that relates to more than 2 other contours;
        - Contours that do not relate to any other contour and is inside the geographic
        bounds;
        """
        invalidDict = dict()
        contoursNumber = len(contourNodeDict)
        step = 100 / contoursNumber if contoursNumber else 0
        for current, (node, contourList) in enumerate(contourNodeDict.items()):
            nodeGeom = QgsGeometry.fromPointXY(node)
            nodeWkb = nodeGeom.asWkb()
            if feedback is not None and feedback.isCanceled():
                break
            if (
                geoBoundsPolygonEngine is not None
                and not geoBoundsPolygonEngine.intersects(nodeGeom.constGet())
            ):
                continue
            if len(contourList) == 1 and (
                geoBoundsGeomEngine is not None
                and not (
                    geoBoundsGeomEngine.intersects(nodeGeom.constGet())
                    or geoBoundsGeomEngine.distance(nodeGeom.constGet()) < 10**-9
                )
            ):
                invalidDict[nodeWkb] = self.tr(
                    "Contour lines must be closed or intersect the geographic boundary."
                )
            if (
                len(contourList) == 2
                and contourList[0][heightFieldName] != contourList[1][heightFieldName]
            ):
                invalidDict[nodeWkb] = self.tr(
                    "Contour lines touch each other and have different height values."
                )
            if len(contourList) > 2:
                invalidDict[nodeWkb] = self.tr(
                    "Contour lines intersect each other. Contour lines must touch itself or only one other with same height value."
                )
            if feedback is not None:
                feedback.setProgress(step * current)
        return invalidDict

    def isDangle(self, point, featureDict, spatialIdx, searchRadius=10**-15):
        """
        :param point: (QgsPointXY) node tested as dangle;
        :param featureDict: (dict) dict {featid:feat};
        :param spatialIdx: (QgsSpatialIndex) spatial index
        of features from featureDict;
        :param searchRadius: (float) search radius.
        """
        qgisPoint = QgsGeometry.fromPointXY(point)
        buffer = qgisPoint.buffer(searchRadius, -1)
        bufferBB = buffer.boundingBox()
        for featid in spatialIdx.intersects(bufferBB):
            if (
                buffer.intersects(featureDict[featid].geometry())
                and qgisPoint.distance(featureDict[featid].geometry()) < 10**-9
            ):
                return True
        return False

    def buildIntersectionDict(
        self,
        drainageLyr,
        drainageIdDict,
        drainageSpatialIdx,
        contourIdDict,
        contourSpatialIdx,
        feedback=None,
    ):
        intersectionDict = dict()
        flagDict = dict()
        firstNode = lambda x: self.geometryHandler.getFirstNode(drainageLyr, x)
        lastNode = lambda x: self.geometryHandler.getLastNode(drainageLyr, x)
        addItemsToIntersectionDict = lambda x: self.addItemsToIntersectionDict(
            dictItem=x,
            contourSpatialIdx=contourSpatialIdx,
            contourIdDict=contourIdDict,
            intersectionDict=intersectionDict,
            firstNode=firstNode,
            lastNode=lastNode,
            flagDict=flagDict,
        )
        # map for, this means: for item in drainageIdDict.items() ...
        list(map(addItemsToIntersectionDict, drainageIdDict.items()))
        return intersectionDict

    def addItemsToIntersectionDict(
        self,
        dictItem,
        contourSpatialIdx,
        contourIdDict,
        intersectionDict,
        firstNode,
        lastNode,
        flagDict,
    ):
        gid, feat = dictItem
        featBB = feat.geometry().boundingBox()
        featid = feat.id()
        featGeom = feat.geometry()
        intersectionDict[featid] = {
            "start_point": firstNode(featGeom),
            "end_point": lastNode(featGeom),
            "intersection_list": [],
        }
        for candidateId in contourSpatialIdx.intersects(featBB):
            candidate = contourIdDict[candidateId]
            candidateGeom = candidate.geometry()
            if candidateGeom.intersects(featGeom):  # add intersection
                intersectionGeom = candidateGeom.intersection(featGeom)
                intersectionList += (
                    [intersectionGeom.asPoint()]
                    if not intersectionGeom.asMultiPoint()
                    else intersectionGeom.asMultiPoint()
                )
                flagFeature = True if len(intersectionList) > 1 else False
                for inter in intersectionList:
                    if flagFeature:
                        flagDict[inter] = self.tr(
                            "Contour id={c_id} intersects drainage id={d_id} in more than one point"
                        ).format(c_id=candidateId, d_id=gid)
                    newIntersection = {
                        "contour_id": candidateId,
                        "intersection_point": inter,
                    }
                    intersectionDict[featid]["intersection_list"].append(
                        newIntersection
                    )

    def validateIntersections(self, intersectionDict, heightFieldName, threshold):
        """
        1- Sort list
        2-
        """
        validatedIdsDict = dict()
        invalidatedIdsDict = dict()
        for id, values in intersectionDict.items():
            interList = values["intersection_list"]
            if len(interList) <= 1:
                continue
            # sort list by distance from start point
            interList.sort(
                key=lambda x: x["intersection_point"]
                .geometry()
                .distance(values["start_point"])
            )
            referenceElement = interList[0]
            for idx, elem in enumerate(interList[1::], start=1):
                elemen_id = elem.id()
                if int(elem[heightFieldName]) != threshold * idx + int(
                    referenceElement[heightFieldName]
                ):
                    invalidatedIdsDict[elemen_id] = elem
                else:
                    if elemen_id not in invalidatedIdsDict:
                        validatedIdsDict[elemen_id] = elem
        for id in validatedIdsDict:
            if id in invalidatedIdsDict:
                validatedIdsDict.pop(id)
        return validatedIdsDict, invalidatedIdsDict

    def validateContourPolygons(
        self,
        contourPolygonDict,
        contourPolygonIdx,
        threshold,
        heightFieldName,
        depressionValueDict=None,
    ):
        hilltopDict = self.buildHilltopDict(contourPolygonDict, contourPolygonIdx)
        invalidDict = dict()
        for hilltopGeom, hilltop in hilltopDict.items():
            localFlagList = []
            polygonList = hilltop["downhill"]
            feat = hilltop["feat"]
            if len(polygonList) < 2:
                break
            # sort polygons by area, from minimum to max
            polygonList.sort(key=lambda x: x.geometry().area())
            # pair comparison
            a, b = tee([feat] + polygonList)
            next(b, None)
            for elem1, elem2 in zip(a, b):
                if abs(elem1[heightFieldName] - elem2[heightFieldName]) != threshold:
                    elem1GeomKey = elem1.geometry().asWkb()
                    if elem1GeomKey not in invalidDict:
                        invalidDict[elem1GeomKey] = []
                    invalidDict[elem1GeomKey] += [
                        self.tr(
                            "Difference between contour with values {id1} \
                        and {id2} do not match equidistance {equidistance}.\
                        Probably one contour is \
                        missing or one of the contours have wrong value.\n"
                        ).format(
                            id1=elem1[heightFieldName],
                            id2=elem2[heightFieldName],
                            equidistance=threshold,
                        )
                    ]
        return invalidDict

    def buildHilltopDict(self, contourPolygonDict, contourPolygonIdx):
        hilltopDict = dict()
        buildDictAlias = lambda x: self.initiateHilltopDict(x, hilltopDict)
        # c loop to build contourPolygonDict
        list(map(buildDictAlias, contourPolygonDict.values()))
        # iterate over contour polygon dict and build hilltopDict
        for idx, feat in contourPolygonDict.items():
            geom = feat.geometry()
            bbox = geom.boundingBox()
            geomWkb = geom.asWkb()
            for candId in contourPolygonIdx.intersects(bbox):
                candFeat = contourPolygonDict[candId]
                candGeom = candFeat.geometry()
                if candId != idx and candGeom.within(geom):
                    hilltopDict.pop(geomWkb.asWkb())
                    break
                if (
                    candId != idx
                    and candGeom.contains(geom)
                    and candFeat not in hilltopDict[geomWkb]["donwhill"]
                ):
                    hilltopDict[geomWkb]["donwhill"].append(candFeat)
            return hilltopDict

    def initiateHilltopDict(self, feat, hilltopDict):
        hilltopDict[feat.geometry().asWkb()] = {"feat": feat, "downhill": []}

    def buildTerrainPolygons(self, featList):
        pass

    def validateContourLines(self, contourLyr, contourAttrName, refLyr, feedback=None):
        """
        1. Validate contour connectivity;
        2. Build terrain polygons by contour value;
        3. Build terrain dict;
        4. Validate contours.
        """
        pass

    def validateSpatialRelations(
        self, ruleList, createSpatialIndex=True, feedback=None
    ):
        """
        1. iterate over rule list and get all layers.
        2. build spatial index
        3. test rule
        """
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(4, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
        spatialDict = self.buildSpatialDictFromRuleList(
            ruleList, feedback=multiStepFeedback
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
        spatialRuleDict = self.buildSpatialRuleDict(
            ruleList, feedback=multiStepFeedback
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(2)
        self.buildSpatialRelationDictOnSpatialRuleDict(
            spatialDict=spatialDict,
            spatialRuleDict=spatialRuleDict,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(3)
        flagList = self.identifyInvalidRelations(
            spatialDict, spatialRuleDict, feedback=multiStepFeedback
        )
        return flagList

    def buildSpatialDictFromRuleList(self, ruleList, feedback=None):
        """
        returns {
            'key formed by layer name and filter' : {
                'spatial_index' : QgsSpatialIndex
                'feature_id_dict' : {
                    'feat_id' : 'feat'
                }
            }
        }
        """
        progressStep = 100 / len(ruleList) if ruleList else 0
        spatialDict = defaultdict(dict)
        for current, rule in enumerate(ruleList):
            if feedback is not None and feedback.isCanceled():
                break
            inputKey = "_".join(rule["input_layer"].name(), rule["input_layer_filter"])
            candidateKey = "_".join(
                rule["candidate_layer"].name(), rule["candidate_layer_filter"]
            )
            for key in [inputKey, candidateKey]:
                if key not in spatialDict:
                    (
                        spatialDict[key]["spatial_index"],
                        spatialDict[key]["feature_id_dict"],
                    ) = self.layerHandler.buildSpatialIndexAndIdDict(
                        inputLyr=rule["input_layer"],
                        featureRequest=rule["input_layer_filter"],
                    )
            if feedback is not None:
                feedback.setProgress(current * progressStep)
        return spatialDict

    def buildSpatialRuleDict(self, ruleList, feedback=None):
        """
        ruleList comes from the ui
        Rule list has the following format:
        ruleList = [
            {
                'input_layer': QgsVectorLayer,
                'input_layer_filter' : str,
                'predicate' : str,
                'candidate_layer' : QgsVectorLayer,
                'candidate_layer_filter' : str,
                'cardinality' : str,
                'feat_relation_list' : list of pairs of (featId, relatedFeatures),
                'flag_text' : str
            }
        ]

        outputs:
        { 'input_layer_input_layer_filter' : {
                        'input_layer': QgsVectorLayer,
                        'input_layer_filter' : str,
                        'rule_list' : [
                            {
                                'predicate' : str,
                                'candidate_layer' : QgsVectorLayer,
                                'candidate_layer_filter' : str,
                                'cardinality' : str,
                                'flag_text' : str,
                                'feat_relation_list' : list of pairs of (featId, relatedFeatures)
                            }
                        ]
                    }
        }
        """
        spatialRuleDict = defaultdict(
            lambda: {"input_layer": None, "input_layer_filter": "", "rule_list": []}
        )
        progressStep = 100 / len(ruleList) if ruleList else 0
        for current, rule in enumerate(ruleList):
            if feedback is not None and feedback.isCanceled():
                break
            key = "_".join(rule["input_layer"].name(), rule["input_layer_filter"])
            spatialRuleDict[key]["input_layer"] = rule["input_layer"]
            spatialRuleDict[key]["input_layer_filter"] = rule["input_layer_filter"]
            spatialRuleDict[key]["rule_list"].append(
                {k: v for k, v in rule.items() if "input" not in k}
            )
            if feedback is not None:
                feedback.setProgress(current * progressStep)
        return spatialRuleDict

    def buildSpatialRelationDictOnSpatialRuleDict(
        self, spatialDict, spatialRuleDict, feedback=None
    ):
        """
        layerFeatureDict = {
            'layer_name' = {
                featId : QgsFeature
            }
        }
        spatialIndexDict = {
            'layer_name' : QgsSpatialIndex
        }
        spatialRuleDict = { 'input_layer_input_layer_filter' : {
                                                                    'input_layer': QgsVectorLayer,
                                                                    'input_layer_filter' : str,
                                                                    'rule_list' : [
                                                                        {
                                                                            'predicate' : str,
                                                                            'candidate_layer' : QgsVectorLayer,
                                                                            'candidate_layer_filter' : str,
                                                                            'cardinality' : str,
                                                                            'flag_text' : str
                                                                        }
                                                                    ]
                                                                }
        }

        """
        totalSteps = self.countSteps(spatialRuleDict, spatialDict)
        progressStep = 100 / totalSteps if totalSteps else 0
        counter = 0
        for inputKey, inputDict in spatialRuleDict.items():
            if feedback is not None and feedback.isCanceled():
                break
            keyRuleList = [
                "_".join(i["candidate_layer"], i["candidate_layer_filter"])
                for i in inputDict["rule_list"]
            ]
            for featId, feat in spatialDict[inputKey]["feature_id_dict"]:
                if feedback is not None and feedback.isCanceled():
                    break
                for idx, rule in enumerate(inputDict["rule_list"]):
                    if feedback is not None and feedback.isCanceled():
                        break
                    rule["feat_relation_list"].append(
                        (
                            featId,
                            self.relateFeatureAccordingToPredicate(
                                feat=feat,
                                rule=rule,
                                key=keyRuleList[idx],
                                predicate=rule["predicate"],
                                spatialDict=spatialDict,
                            ),
                        )
                    )
                    counter += 1
                    if feedback is not None:
                        feedback.setProgress(counter * progressStep)

    def countSteps(self, spatialRuleDict, spatialDict):
        """
        Counts the number of steps of execution.
        """
        steps = len(spatialRuleDict)
        for k, v in spatialRuleDict.items():
            steps += len(v["rule_list"])
            steps += len(spatialDict[k]["feature_id_dict"])
        return steps

    def identifyInvalidRelations(self, spatialDict, spatialRuleDict, feedback=None):
        """
        Identifies invalid spatial relations and returns a list with flags to be raised.
        """
        totalSteps = self.countSteps(spatialRuleDict, spatialDict)
        progressStep = 100 / totalSteps if totalSteps else 0
        counter = 0
        invalidFlagList = []
        for inputKey, inputDict in spatialRuleDict:
            if feedback is not None and feedback.isCanceled():
                break
            inputLyrName = inputDict["input_layer"]
            for rule in inputDict["rule_list"]:
                if feedback is not None and feedback.isCanceled():
                    break
                candidateLyrName = inputDict["candidate_layer"]
                candidateKey = "_".join(
                    candidateLyrName, inputDict["candidate_layer_filter"]
                )
                sameLayer = True if inputKey == candidateKey else False
                lambdaCompair = self.parseCardinalityAndGetLambdaToIdentifyProblems(
                    cardinality=rule["cardinality"],
                    necessity=rule["necessity"],
                    isSameLayer=sameLayer,
                )
                for featId, relatedFeatures in rule["feat_relation_list"]:
                    if feedback is not None and feedback.isCanceled():
                        break
                    inputFeature = spatialDict[inputKey][featId]
                    if lambdaCompair(relatedFeatures):
                        if (
                            inputLyrName == candidateLyrName
                            and inputFeature in relatedFeatures
                        ):
                            relatedFeatures.pop(inputFeature)
                        invalidFlagList += self.buildSpatialFlags(
                            inputFeature=inputFeature,
                            relatedFeatures=relatedFeatures,
                            flagText=rule["flag_text"],
                        )
                    if feedback is not None:
                        feedback.setProgress(counter * progressStep)
                        counter += 1
        return invalidFlagList

    def buildSpatialFlags(
        self, inputLyrName, inputFeature, candidateLyrName, relatedFeatures, flagText
    ):
        input_id = inputFeature.id()
        inputGeom = inputFeature.geometry()
        spatialFlags = []
        for feat in relatedFeatures:
            flagGeom = inputGeom.intersection(feat.geometry().constGet())
            flagText = self.tr(
                "Feature from {input} with id {input_id} violates the following predicate with feature from {candidate} with id {candidate_id}: {predicate_text}"
            ).format(
                input=inputLyrName,
                input_id=input_id,
                candidate=candidateLyrName,
                candidate_id=feat.id(),
                predicate_text=flagText,
            )
            spatialFlags.append({"flagGeom": flagGeom, "flagText": flagText})
        return spatialFlags

    def availablePredicates(self):
        """
        Returns the name of all available predicates.
        :return: (tuple-of-str) list of available predicates.
        """
        return {i: p for i, p in enumerate(self.__predicates)}

    def getCardinalityTest(self, cardinality=None):
        """
        Parses cardinality string and gets a callable to check if the iterable
        tested (e.g. list of features) complies with the cardinality.
        :param cardinality: (str) cardinality string to be tested against.
        :return: (function) testing method to be applied to an iterable.
        """
        if cardinality is None:
            # default is "1..*"
            return lambda x: len(x) > 0
        min_card, max_card = cardinality.split("..")
        if max_card == "*":
            return lambda x: len(x) >= int(min_card)
        elif min_card == max_card:
            return lambda x: len(x) == int(min_card)
        else:
            return lambda x: len(x) >= int(min_card) and len(x) <= int(max_card)

    def testPredicate(self, predicate, engine, targetGeometries):
        """
        Applies a predicate test to a given feature from a list of features.
        :param predicate: (int) topological relation code to be tested against.
        :param engine: (QgsGeometryEngine) reference feature's QGIS structure
                       for based on geometries for faster spatial operations.
        :param targetGeometries: (dict) maps feature ids to their geometries
                                 that will be tested.
        :param cardinality: (str) cardinality string to be tested against.
        :return: (set-of-int) feature IDs for those that the geometries do
                 comply with given predicate/cardinality.
        """
        # negatives are disregarded. method simply apply the predicate comparison
        positives = set()
        negatives = set()
        methods = {
            self.EQUALS: "isEqual",
            self.DISJOINT: "disjoint",
            self.INTERSECTS: "intersects",
            self.TOUCHES: "touches",
            self.CROSSES: "crosses",
            self.WITHIN: "within",
            self.OVERLAPS: "overlaps",
            self.CONTAINS: "contains",
        }
        if predicate not in methods:
            raise NotImplementedError(
                self.tr("Invalid predicate ({0}).").format(predicate)
            )
        predicateMethod = methods[predicate]
        for test_fid, test_geom in targetGeometries.items():
            if getattr(engine, predicateMethod)(test_geom.constGet()):
                positives.add(test_fid)
        return positives

    def checkPredicate(
        self, layerA, layerB, predicate, cardinality, ctx=None, feedback=None
    ):
        """
        Checks if a duo of layers comply with a spatial predicate at a given
        cardinality.
        :param layerA: (QgsVectorLayer) reference layer.
        :param layerB: (QgsVectorLayer) layer to have its features spatially
                    compared to reference layer.
        :param predicate: (str) topological comparison method to be applied.
        :param cardinality: (str) a formatted string that informs minimum and
                            maximum occurences of a spatial predicate.
        :param ctx: (QgsProcessingContext) processing context in which algorithm
                    should be executed.
        :param feedback: (QgsFeedback) QGIS progress tracking component.
        :return: (dict) a map from offended feature IDs to the list of its
                offending features.
        """
        ctx = ctx or QgsProcessingContext()
        feedback = feedback or QgsProcessingFeedback()
        size = layerA.featureCount()
        stepSize = 100 / size if size else 0
        flags = defaultdict(list)
        predicates = self.availablePredicates()
        denials = [
            self.NOTEQUALS,
            self.NOTINTERSECTS,
            self.NOTTOUCHES,
            self.NOTCROSSES,
            self.NOTWITHIN,
            self.NOTOVERLAPS,
            self.NOTCONTAINS,
        ]
        if predicate in denials:
            # denials always follow the "affirmitives" (contains = 14
            # -> notcontains = 15), hence -1.
            # denials are ALWAYS absolute (cardinality is not applicable)
            predicate -= 1
            cardinality = "0..0"
        if predicate == self.DISJOINT:
            predicateFlagText = self.tr(
                "feature ID {{fid_a}} from {layer_a} "
                "id not {pred} to {{size}} features of"
                " {layer_b}"
            ).format(
                layer_a=layerA.name(), pred=predicates[predicate], layer_b=layerB.name()
            )
            cardinality = "0..0"
        else:
            predicateFlagText = self.tr(
                "feature ID {{fid_a}} from {layer_a} "
                "{pred} {{size}} features of "
                "{layer_b}"
            ).format(
                layer_a=layerA.name(), pred=predicates[predicate], layer_b=layerB.name()
            )
        if predicate in (self.EQUALS, self.WITHIN):
            getFlagGeometryMethod = lambda geom, _: geom
        else:
            getFlagGeometryMethod = lambda geomA, geomB: geomA.intersection(geomB)
        testingMethod = self.getCardinalityTest(cardinality)
        for step, featA in enumerate(layerA.getFeatures()):
            if feedback.isCanceled():
                break
            geomA = featA.geometry()
            engine = QgsGeometry.createGeometryEngine(geomA.constGet())
            engine.prepareGeometry()
            geometriesB = {
                f.id(): f.geometry() for f in layerB.getFeatures(geomA.boundingBox())
            }
            positives = self.testPredicate(predicate, engine, geometriesB)
            if predicate == self.DISJOINT:
                # disjoint comparison wants those that are NOT disjoint to flag
                positives = set(geometriesB.keys()) - positives
            if not testingMethod(positives):
                fidA = featA.id()
                size = len(positives)
                if not size:
                    flags[fidA].append(
                        {
                            "text": predicateFlagText.format(fid_a=fidA, size=0),
                            "geom": geomA,
                        }
                    )
                    continue
                if size > 1:
                    predicateFlagText_ = "{0} (IDs {1})".format(
                        predicateFlagText, ", ".join(map(str, positives))
                    )
                elif size == 1:
                    predicateFlagText_ = "{0} (ID {1})".format(
                        predicateFlagText, str(set(positives).pop())
                    )
                for fidB in positives:
                    flags[fidA].append(
                        {
                            "text": predicateFlagText_.format(fid_a=fidA, size=size),
                            "geom": getFlagGeometryMethod(geomA, geometriesB[fidB]),
                        }
                    )
            feedback.setProgress(stepSize * (step + 1))
        return {fid: flag for fid, flag in flags.items() if flag}

    def checkDE9IM(self, layerA, layerB, mask, cardinality, ctx=None, feedback=None):
        """
        Applies a DE-9IM mask to compare the features of between and checks
        whether the occurrence limits are respected.
        :param layerA: (QgsVectorLayer | iterator) reference layer.
        :param layerB: (QgsVectorLayer) layer to have its features spatially
                    compared to reference layer.
        :param mask: (str) a linearized DE-9IM mask to be used for the spatial
                     comparison between features of layer A and of layer B.
        :param cardinality: (str) a formatted string that informs minimum and
                            maximum occurences of a spatial predicate.
        :param ctx: (QgsProcessingContext) processing context in which algorithm
                    should be executed.
        :param feedback: (QgsFeedback) QGIS progress tracking component.
        :return: (dict) a map from offended to flag text and its geometry.
        """
        ctx = ctx or QgsProcessingContext()
        feedback = feedback or QgsProcessingFeedback()
        testingMethod = self.getCardinalityTest(cardinality)
        candidates = defaultdict(list)
        flags = defaultdict(list)
        predicateFlagText = self.tr(
            "feature ID {{fid_a}} from {layer_a} "
            "has {{size}} occurrences using the "
            "DE-9IM mask '{mask}' when compared to"
            " layer {layer_b}"
        ).format(layer_a=layerA.name(), mask=mask, layer_b=layerB.name())
        size = layerA.featureCount()
        stepSize = 100 / size if size else 0
        iteratorA = (
            layerA.getFeatures() if isinstance(layerA, QgsVectorLayer) else layerA
        )
        for step, featA in enumerate(iteratorA):
            if feedback.isCanceled():
                break
            fidA = featA.id()
            geomA = featA.geometry()
            engine = QgsGeometry.createGeometryEngine(geomA.constGet())
            for featB in layerB.getFeatures(geomA.boundingBox()):
                if engine.relatePattern(featB.geometry().constGet(), mask):
                    candidates[fidA].append(featB.id())
            if not testingMethod(candidates[fidA]):
                # if the mask has an 'invalid' count of occurrences, it is a flag!
                size = len(candidates[fidA])
                if not size:
                    flags[fidA].append(
                        {
                            "text": predicateFlagText.format(fid_a=fidA, size=0),
                            "geom": geomA,
                        }
                    )
                    continue
                if size > 1:
                    predicateFlagText_ = "{0} (IDs {1})".format(
                        predicateFlagText, ", ".join(map(str, candidates[fidA]))
                    )
                elif size == 1:
                    predicateFlagText_ = "{0} (ID {1})".format(
                        predicateFlagText.replace("occurrences", "occurrence"),
                        str(set(candidates[fidA]).pop()),
                    )
                flags[fidA].append(
                    {
                        "text": predicateFlagText_.format(fid_a=fidA, size=size),
                        "geom": geomA,
                    }
                )
            feedback.setProgress(stepSize * (step + 1))
        return flags

    def setupLayer(self, layerName, exp, ctx=None, feedback=None):
        """
        Retrieves layer from canvas and applies filtering expression. If CRS is
        different than project's, layer is reprojected.
        :param layerName: (str) layer's name on canvas.
        :param exp: (str) filtering expression to be applied to target layer.
        :param ctx: (QgsProcessingContext) processing context in which algorithm
                    should be executed.
        :param feedback: (QgsFeedback) QGIS progress tracking component.
        :return: (QgsVectorLayer) layer ready to be compared.
        """
        lh = LayerHandler()
        ctx = ctx or QgsProcessingContext()
        if exp:
            layer = lh.filterByExpression(layerName, exp, ctx, feedback)
            # filter expression is an output is from another algo
            # it is the temp output -> its name is not the same as the input
            layer.setName(layerName)
        else:
            # this will raise an error if layer is not loaded
            layer = ctx.getMapLayer(layerName)
            if not layer:
                raise Exception(self.tr("Layer not found on canvas."))
        projectCrs = QgsProject.instance().crs()
        if layer.crs() != projectCrs:
            layer = lh.reprojectLayer(layer, projectCrs)
            layer.setName(layerName)
        return layer

    def enforceRule(self, rule, ctx=None, feedback=None):
        """
        Applies a given set of spatial restrictions to a duo of layers.
        :param rule: (SpatialRule) objetc containing all properties for
                     the feature comparison.
        :param ctx: (QgsProcessingContext) processing context in which
                    algorithm should be executed.
        :param feedback: (QgsFeedback) QGIS progress tracking component.
        :return: (dict) a map from offended feature's ID to offenders feature
                 set.
        """
        lh = LayerHandler()
        ctx = ctx or QgsProcessingContext()
        feedback = feedback or QgsProcessingFeedback()
        # setup step is ignored for the enforcing rule progress tracking
        layerA = self.setupLayer(rule.layerA(), rule.filterA(), ctx, None)
        layerB = self.setupLayer(rule.layerB(), rule.filterB(), ctx, None)
        method = self.checkDE9IM if rule.useDE9IM() else self.checkPredicate
        return method(
            layerA, layerB, rule.predicate(), rule.cardinality(), ctx, feedback
        )

    def enforceRules(self, ruleList, ctx=None, feedback=None):
        """
        Applies a set of spatial rules to current active layers on canvas.
        :param ruleList: (list-of-SpatialRule) all rules that should be applied
                         to canvas.
        :param ctx: (QgsProcessingContext) processing context in which algorithm
                    should be executed.
        :param feedback: (QgsFeedback) QGIS progress tracking component.
        :return: (dict) a map of offended rules to its flags.
        """
        out = dict()
        ctx = ctx or QgsProcessingContext()
        size = len(ruleList)
        feedback = feedback or QgsProcessingFeedback()
        multiStepFeedback = QgsProcessingMultiStepFeedback(size, feedback)
        for idx, rule in enumerate(ruleList):
            ruleName = rule.ruleName()
            if multiStepFeedback.isCanceled():
                break
            multiStepFeedback.pushInfo(
                self.tr('Checking rule "{0}"... [{1}/{2}]').format(
                    ruleName, idx + 1, size
                )
            )
            if not rule.isValid():
                multiStepFeedback.pushInfo(
                    self.tr(
                        "Rule {0} is invalid and will be skipped. " "Error: {1}"
                    ).format(ruleName, rule.validate(checkLoaded=True))
                )
                continue
            flags = self.enforceRule(rule, ctx, multiStepFeedback)
            if flags:
                if ruleName in out:
                    previous = out[ruleName]
                    for fid in flags:
                        if fid in previous:
                            out[ruleName][fid] += flags[fid]
                        else:
                            out[ruleName][fid] = flags[fid]
                else:
                    out[ruleName] = flags
                multiStepFeedback.reportError(
                    self.tr('Rule "{0}" raised flags\n').format(ruleName, idx + 1, size)
                )
            else:
                multiStepFeedback.pushDebugInfo(
                    self.tr('Rule "{0}" did not raise any flags\n').format(ruleName)
                )
            multiStepFeedback.setCurrentStep(idx + 1)
        return out


class SpatialRule(QObject):
    """
    Wrapper class around a map of spatial rule attributes. This object handles
    the attributes and verifies its validity.
    """

    def __init__(
        self,
        name=None,
        layer_a=None,
        filter_a=None,
        predicate=None,
        de9im_predicate=None,
        layer_b=None,
        filter_b=None,
        cardinality=None,
        useDE9IM=False,
        checkLoadedLayer=True,
    ):
        """
        Initiates an instance of SpatialRule.
        :param name: (str) display name for the spatial rule.
        :param layer_a: (str) layer A's name as it would be on canvas.
        :param filter_a: (str) filtering expression to be applied to layer A.
        :param predicate: (int) spatial predicate to be used to compare A and
                          B's features. These predicates are available as per
                          SpatialRelationsHandler.
        :param de9im_predicate: (str) string containing a DE-9IM relationship
                                mask (linearized) to be applied between
                                features from layers A and B.
        :param layer_b: (str) layer B's name as it would be on canvas.
        :param filter_b: (str) filtering expression to be applied to layer B.
        :param cardinality: (str) text containing maximum and minimum limits of
                            predicate's events ocurrence between layer A and B.
        :param useDE9IM: (bool) whether this spatial rule should be using the
                         DE-9IM mask to spatially compare features from layer A
                         to layer B's instead of the enumerator predicate.
        :param checkLoadedLayer: (bool) whether layers A and B should be loaded
                                 on canvas to be considered valid for its value
                                 setting upon object's initialization.
        """
        # OBS.: parameters are not following the camel case rule in order to
        # make it compatible with the first map produced. this should be sorted
        # when v5 is launched and map version 0.1 is not supported!
        super(SpatialRule, self).__init__()
        self._useDE9IM = useDE9IM
        self._attr = dict()
        if name is not None:
            self.setRuleName(name)
        if layer_a is not None:
            self.setLayerA(layer_a, checkLoadedLayer)
        if filter_a is not None:
            self.setFilterA(filter_a)
        if predicate is not None:
            self.setPredicateEnum(predicate)
        if de9im_predicate is not None:
            self.setPredicateDE9IM(de9im_predicate)
        if layer_b is not None:
            self.setLayerB(layer_b, checkLoadedLayer)
        if filter_b is not None:
            self.setFilterB(filter_b)
        if cardinality is not None:
            self.setCardinality(cardinality)

    def validateRuleName(self, name):
        """
        Checks whether a given name is considered a valid display name for the
        rule.
        :param name: (str) display name for the spatial rule.
        :return: (bool) whether provided name is a valid setting.
        """
        return isinstance(name, str) and name != ""

    def ruleNameIsValid(self):
        """
        Checks whether current name is a valid spatial rule name.
        :return: (bool) whether current display name is valid.
        """
        return self.validateRuleName(self.ruleName())

    def setRuleName(self, name):
        """
        Updates current rule's display name. If provided name is invalid,
        rule's name is not updated.
        :param name: (str) proposed new display name for the rule.
        :return: (bool) whether rule's name was updated.
        """
        if not self.validateRuleName(name):
            return False
        self._attr["name"] = name
        return self.ruleName() == name

    def ruleName(self):
        """
        Gets current rule name.
        :return: (str) rule's name.
        """
        return str(self._attr.get("name", ""))

    def validateLayerName(self, layer, checkLoaded=False):
        """
        Checks whether a provided layer name is a valid setting. This method
        may take its availability on canvas into consideration, if necessary.
        :param layer: (str) layer name to be checked.
        :param checkLoaded: (bool) whether canvas availability should be
                            considered.
        :return: (bool) provided layer name's validity.
        """
        isLoaded = False
        if checkLoaded:
            for vl in QgsProject.instance().mapLayersByName(layer):
                if isinstance(vl, QgsVectorLayer):
                    isLoaded = True
                    break
        return (not (checkLoaded and not isLoaded)) and layer != ""

    def _setLayer(self, layer, key, checkLoaded=False):
        """
        Private method to route a layer's setting request to the correct dict
        key. Sets a layer to either Layer A or Layer B property.
        :param layer: (str) layer name to be set.
        :param key: (str) "a" if layer is to be set as Layer A, otherwise the
                    method populates Layer B property.
        :param checkLoaded: (bool) whether canvas availability should be
                            considered.
        :return: (bool) whether value update was successful.
        """
        if not self.validateLayerName(layer, checkLoaded):
            return False
        self._attr["layer_a" if key == "a" else "layer_b"] = layer
        return (self.layerA() if key == "a" else self.layerB()) == layer

    def layerAIsValid(self, checkLoaded=False):
        """
        Checks whether current value stored as Layer A is valid.
        :param checkLoaded: (bool) whether canvas availability should be
                            considered.
        :return: (bool) whether property stored as layer A is valid.
        """
        return self.validateLayerName(self.layerA(), checkLoaded)

    def setLayerA(self, layer, checkLoaded=False):
        """
        Updates current layer A property. If provided layer is invalid, the
        property is not updated.
        :param layer: (str) layer name to set as layer A.
        :param checkLoaded: (bool) whether canvas availability should be
                            considered.
        :return: (bool) whether property was updated.
        """
        return self._setLayer(layer, "a", checkLoaded)

    def layerA(self):
        """
        Retrieves current value registered as layer A.
        :return: (str) layer A's name.
        """
        return str(self._attr.get("layer_a", ""))

    def validateFilterExpression(self, exp):
        """
        Checks whether a filtering expression is syntactically valid.
        :param exp: (str) filtering expression to be checked.
        :return: (bool) whether filtering expression is syntactically valid.
        """
        # empty filters are allowed
        return exp == "" or QgsExpression(exp.replace("\\", "")).isValid()

    def _setFilterExpression(self, exp, key):
        """
        Private method used to route filter expression's updates to the correct
        rule property. It updates either Filter A or Filter B's value. If
        provided expression is invalid, the value is not updated.
        :param exp: (str) filtering expression to be applied.
        :param key: (str) "a" if expression is to be set as Filter A, otherwise
                    the method populates Filter B property.
        :return: (bool) whether property was updated.
        """
        if not self.validateFilterExpression(exp):
            return False
        self._attr["filter_a" if key == "a" else "filter_b"] = exp
        return (self.filterA() if key == "a" else self.filterB()) == exp

    def filterAIsValid(self):
        """
        Checks whether current filtering expression for layer A is valid.
        :return: (bool) whether filter expression for layer A is valid.
        """
        return self.validateFilterExpression(self.filterA())

    def setFilterA(self, exp):
        """
        Updates the filtering expression applied to layer A's features. If the
        provided expression is invalid, the value is not updated.
        :param exp: (str) filtering expression to be applied.
        :return: (bool) whether property was updated.
        """
        return self._setFilterExpression(exp, "a")

    def filterA(self):
        """
        Retrieves the filtering expression applied to layer A set on the
        spatial rule.
        :return: (str) filtering expression to be applied to layer A.
        """
        return str(self._attr.get("filter_a", ""))

    def setUseDE9IM(self, useDE9IM):
        """
        Updates whether the spatial rule should use DE-9IM masks to compare
        features from layer A to the ones from layer B.
        :param useDE9IM: (bool) whether spatial rule should use DE-9IM masks
                         instead of the predicate's enumerator.
        :return: (bool) whether the mask usage was updated.
        """
        if not isinstance(useDE9IM, bool):
            return False
        self._useDE9IM = useDE9IM
        return self.useDE9IM() == useDE9IM

    def useDE9IM(self):
        """
        Checks whether spatial rule should use DE-9IM masks instead of the
        predicate's enumerator.
        :return: (bool) whether the spatial rule is considering DE-9IM masks.
        """
        return self._useDE9IM

    def validatePredicate(self, pred, useDE9IM):
        """
        Checks whether a predicate value is a valid setting. This method may be
        used to either DE-9IM masks and the enumerator.
        :param pred: (int/str) either the predicate enumerator or the DE-9IM
                     mask to be checked.
        :param useDE9IM: (bool) whether provided predicate is a DE-9IM mask.
        :return: (bool) provided predicate's validity.
        """
        if useDE9IM:
            regex = QRegExp("[FfTt012\*]{9}")
            acceptable = QRegExpValidator.Acceptable
            return (
                isinstance(pred, str)
                and QRegExpValidator(regex).validate(pred, 9)[0] == acceptable
            )
        else:
            return pred in SpatialRelationsHandler().availablePredicates()

    def predicateIsValid(self):
        """
        Checks if current predicate is valid. If the rule is set to use DE-9IM
        masks, the method checks the value filled for the property
        predicateDE9IM, else it checks the enumerator property. It may return
        true in cases that "active" predicate is valid and the other isn't.
        :return: (bool) property's value validity.
        """
        return (
            self.predicateDE9IMIsValid()
            if self.useDE9IM()
            else self.predicateEnumIsValid()
        )

    def setPredicate(self, pred):
        """
        Updates current value for the predicate property. The method is a proxy
        to DE-9IM masks and the enumerator and decides which one is going to be
        updated based on masks usage property. If the provided predicate is
        invalid, the property is not updated.
        :param pred: (int/str) either the predicate enumerator or the DE-9IM
                     mask to be set.
        :return: (bool) whether the property was updated.
        """
        return (
            self.setPredicateDE9IM(pred)
            if self.useDE9IM()
            else self.setPredicateEnum(pred)
        )

    def predicate(self):
        """
        Retrieves current predicate. If the rule is set to use DE-9IM masks, it
        retrieves the predicateDE9IM and predicateEnum otherwise.
        :return: (int/bool) either the predicate enumerator or the DE-9IM mask
                 value.
        """
        useDE9IM = self.useDE9IM()
        return self.predicateDE9IM() if useDE9IM else self.predicateEnum()

    def predicateEnumIsValid(self):
        """
        Checks whether current enumerator predicate property's value is valid.
        :return: (bool) enumerator predicate property's value validity.
        """
        return self.validatePredicate(self.predicateEnum(), useDE9IM=False)

    def setPredicateEnum(self, pred):
        """
        Updates the predicate enumerator property. If provided predicate is
        invalid, the property is not updated.
        :param pred: (int) predicate to be set.
        :return: (bool) whether the property was updated.
        """
        if not self.validatePredicate(pred, useDE9IM=False):
            return False
        self._attr["predicate"] = pred
        return self.predicateEnum() == pred

    def predicateEnum(self):
        """
        Retrieves the predicate enumerator value set to the spatial rule.
        :return: (int) current predicate enumerator.
        """
        return self._attr.get("predicate", -1)

    def predicateDE9IMIsValid(self):
        """
        Checks the validity of current's DE-9IM mask.
        :return: (bool) whether DE-9IM mask is a valid input.
        """
        return self.validatePredicate(self.predicateDE9IM(), useDE9IM=True)

    def setPredicateDE9IM(self, pred):
        """
        Updates the value of the DE-9IM mask set for the spatial rule. If the
        value is invalid, the property is not updated.
        :param pred: (str) the DE-9IM mask linearized as a string to be set.
        :return: (bool) whether the property was updated.
        """
        if not self.validatePredicate(pred, useDE9IM=True):
            return False
        # geometry engine must the 'pattern'/mask as an upper case string
        pred = pred.upper()
        self._attr["de9im_predicate"] = pred
        return self.predicateDE9IM() == pred

    def predicateDE9IM(self):
        """
        Retrieves the DE-9IM mask set for the spatial rule to compare layer A's
        features to layer B's.
        :return: (str) DE-9IM mask set.
        """
        return str(self._attr.get("de9im_predicate", ""))

    def layerBIsValid(self, checkLoaded=False):
        """
        Checks whether current value stored as Layer B is valid.
        :param checkLoaded: (bool) whether canvas availability should be
                            considered.
        :return: (bool) whether property stored as layer B is valid.
        """
        return self.validateLayerName(self.layerB(), checkLoaded)

    def setLayerB(self, layer, checkLoaded=False):
        """
        Updates current layer B property. If provided layer is invalid, the
        property is not updated.
        :param layer: (str) layer name to set as layer B.
        :param checkLoaded: (bool) whether canvas availability should be
                            considered.
        :return: (bool) whether property was updated.
        """
        return self._setLayer(layer, "b", checkLoaded)

    def layerB(self):
        """
        Retrieves current value registered as layer B.
        :return: (str) layer B's name.
        """
        return str(self._attr.get("layer_b", ""))

    def filterBIsValid(self):
        """
        Checks whether current filtering expression for layer B is valid.
        :return: (bool) whether filter expression for layer B is valid.
        """
        return self.validateFilterExpression(self.filterB())

    def setFilterB(self, exp):
        """
        Updates the filtering expression applied to layer B's features. If the
        provided expression is invalid, the value is not updated.
        :param exp: (str) filtering expression to be applied.
        :return: (bool) whether property was updated.
        """
        return self._setFilterExpression(exp, "b")

    def filterB(self):
        """
        Retrieves the filtering expression applied to layer B set on the
        spatial rule.
        :return: (str) filtering expression to be applied to layer B.
        """
        return str(self._attr.get("filter_b", ""))

    def validateCardinality(self, card):
        """
        Checks the validity of a given string as a relationship cardinality
        string. The expected input format is 'MIN..MAX', with '*' as wild card.
        :param card: (str) string of cardinality to be evaluated.
        :return: (bool) provided cardinality's validity.
        """
        regex = QRegExp("[0-9\*]\.\.[0-9\*]")
        acceptable = QRegExpValidator.Acceptable
        return (
            isinstance(card, str)
            and QRegExpValidator(regex).validate(card, 9)[0] == acceptable
        )

    def cardinalityIsValid(self):
        """
        Checks whether current value of cardinality is a valid input.
        :return: (bool) cardinality's validity.
        """
        return self.validateCardinality(self.cardinality())

    def setCardinality(self, card):
        """
        Updates the cardinality to be used by the spatial rule. If the provided
        cardinality is invalid, the property is not updated.
        :param card: (str) cardinality to be set.
        :return: (bool) whether the property was updated.
        """
        if not self.validateCardinality(card):
            return False
        self._attr["cardinality"] = card
        return self.cardinality() == card

    def cardinality(self):
        """
        Retrieves the cardinality to be used by the spatial rule.
        :return: (str) cardinality's value to be used.
        """
        return str(self._attr.get("cardinality", ""))

    def validate(self, checkLoaded=False):
        """
        Checks the spatial rule's validity and informs the first invalidation
        reason, if any.
        :param checkLoaded: (bool) whether canvas availability should be
                            considered.
        :return: (str) invalidation reason.
        """
        methodMap = {
            "name": self.ruleNameIsValid,
            "layer_a": lambda: self.layerAIsValid(checkLoaded),
            "filter_a": self.filterAIsValid,
            # "predicate": self.predicateEnum,
            # "de9im_predicate": self.predicateDE9IM,
            "layer_b": lambda: self.layerBIsValid(checkLoaded),
            "filter_b": self.filterBIsValid,
            "cardinality": self.cardinalityIsValid,
        }
        valueMethodMap = {
            "name": self.ruleName,
            "layer_a": self.layerA,
            "filter_a": self.filterA,
            "layer_b": self.layerB,
            "filter_b": self.filterB,
            "cardinality": self.cardinality,
        }
        for prop, validationMethod in methodMap.items():
            if not validationMethod():
                return self.tr(
                    "'{val}' is an invalid value for property '{prop}'"
                ).format(val=valueMethodMap[prop](), prop=prop)
        if not self.predicateIsValid():
            val = self.predicate()
            if self.useDE9IM():
                return self.tr("'{0}' is not a valid DE-9IM mask").format(val)
            return self.tr("'{0}' is not a valid predicate").format(val)
        return ""

    def isValid(self, checkLoaded=False):
        """
        Checks whether the filled properties may be used as a valid spatial
        rule. This may be true even if one of the predicates is invalid, given
        that it is not selected to be used (either mask or enumerator).
        :param checkLoaded: (bool) whether canvas availability should be
                            considered.
        :return: (bool) whether spatial rule may be enforced.
        """
        return (
            self.ruleNameIsValid()
            and self.layerAIsValid(checkLoaded)
            and self.filterAIsValid()
            and self.predicateIsValid()
            and self.layerBIsValid(checkLoaded)
            and self.filterBIsValid()
            and self.cardinalityIsValid()
        )

    def asDict(self):
        """
        Displays the spatial rule as a map containing all of its properties.
        :return: (dict) map of this spatial rule instance's properties.
        """
        # self._attr is not directly returned to avoid in-place modifications
        # outside this object's scope being reflected on its SpatialRule
        # instance
        return {
            "name": self.ruleName(),
            "layer_a": self.layerA(),
            "filter_a": self.filterA(),
            "predicate": self.predicateEnum(),
            "de9im_predicate": self.predicateDE9IM(),
            "layer_b": self.layerB(),
            "filter_b": self.filterB(),
            "cardinality": self.cardinality(),
            "useDE9IM": self.useDE9IM(),
        }
