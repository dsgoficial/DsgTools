# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-04-15
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import math
import random

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsExpression,
    QgsExpressionContext,
    QgsExpressionContextUtils,
    QgsFeature,
    QgsFeatureSink,
    QgsGeometry,
    QgsPointXY,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterDistance,
    QgsProcessingParameterExpression,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsRectangle,
    QgsSpatialIndex,
)

from ...algRunner import AlgRunner


class BuildingGeneralizationAlgorithm(QgsProcessingAlgorithm):
    """
    Algorithm for generalizing building point features with axis-aligned
    square symbols using iterative displacement and visibility resolution.
    """

    INPUT_BUILDINGS = "INPUT_BUILDINGS"
    INPUT_ROADS = "INPUT_ROADS"
    INPUT_WATER = "INPUT_WATER"
    INPUT_MOLDURA = "INPUT_MOLDURA"
    VISIBILITY_FIELD = "VISIBILITY_FIELD"
    SYMBOL_SIZE = "SYMBOL_SIZE"
    MIN_GAP = "MIN_GAP"
    ROAD_SYMBOL_WIDTH = "ROAD_SYMBOL_WIDTH"
    MAX_DISPLACEMENT = "MAX_DISPLACEMENT"
    MAX_ITERATIONS = "MAX_ITERATIONS"
    GENERIC_EXPRESSION = "GENERIC_EXPRESSION"
    FLAGS = "FLAGS"

    # Force system constants
    NEIGHBOR_REPULSION_FACTOR = 0.5
    FORBIDDEN_REPULSION_STRENGTH = 1.5
    ORIGIN_ATTRACTION_STRENGTH = 0.1
    INITIAL_DAMPING = 0.8
    CONVERGENCE_FRACTION = 0.01

    def name(self):
        return "buildinggeneralizationalgorithm"

    def displayName(self):
        return self.tr("Building Generalization")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate(
            "BuildingGeneralizationAlgorithm", string
        )

    def createInstance(self):
        return BuildingGeneralizationAlgorithm()

    def shortHelpString(self):
        return self.tr(
            "Generalizes building point features with axis-aligned square symbols.\n\n"
            "Resolves spatial conflicts (building-building, building-road, "
            "building-water border) by displacement and, when impossible, by "
            "hiding generic buildings (setting visibility field to 2).\n\n"
            "Non-generic buildings with unresolvable conflicts are output to "
            "a FLAGS layer for manual review.\n\n"
            "Parameters:\n"
            "- Building layer: edited in-place (geometry displaced, visibility updated)\n"
            "- Road layer: line layer for road symbol buffers\n"
            "- Water body layer (optional): polygon layer (only border used)\n"
            "- Moldura layer (optional): only buildings inside are processed\n"
            "- Visibility field: existing field (value 2 = not visible)\n"
            "- Symbol size: side length of building square symbol\n"
            "- Minimum gap: minimum spacing between symbols\n"
            "- Road symbol width: width of road symbol at target scale\n"
            "- Maximum displacement: max distance a building can be moved\n"
            "- Generic expression: identifies low-priority buildings for hiding"
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_BUILDINGS,
                self.tr("Building layer (edited in-place)"),
                [QgsProcessing.TypeVectorPoint],
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_ROADS,
                self.tr("Road layer"),
                [QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_WATER,
                self.tr("Water body layer (optional)"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_MOLDURA,
                self.tr("Moldura layer (optional)"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.VISIBILITY_FIELD,
                self.tr("Visibility field (value 2 = not visible)"),
                None,
                self.INPUT_BUILDINGS,
                QgsProcessingParameterField.Any,
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.SYMBOL_SIZE,
                self.tr("Symbol size (square side length)"),
                defaultValue=10.0,
                parentParameterName=self.INPUT_BUILDINGS,
                minValue=0.01,
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.MIN_GAP,
                self.tr("Minimum gap between symbols"),
                defaultValue=2.0,
                parentParameterName=self.INPUT_BUILDINGS,
                minValue=0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.ROAD_SYMBOL_WIDTH,
                self.tr("Road symbol width"),
                defaultValue=8.0,
                parentParameterName=self.INPUT_BUILDINGS,
                minValue=0.01,
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.MAX_DISPLACEMENT,
                self.tr("Maximum displacement"),
                defaultValue=50.0,
                parentParameterName=self.INPUT_BUILDINGS,
                minValue=0.01,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MAX_ITERATIONS,
                self.tr("Maximum iterations"),
                QgsProcessingParameterNumber.Integer,
                defaultValue=50,
                minValue=1,
                maxValue=1000,
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.GENERIC_EXPRESSION,
                self.tr("Expression for generic (low-priority) buildings"),
                defaultValue='"tipo" in (0, 9999)',
                parentLayerParameterName=self.INPUT_BUILDINGS,
                optional=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr("Non-generic buildings with unresolvable conflicts (flags)"),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        buildingLayer = self.parameterAsVectorLayer(
            parameters, self.INPUT_BUILDINGS, context
        )
        roadLayer = self.parameterAsVectorLayer(
            parameters, self.INPUT_ROADS, context
        )
        waterLayer = self.parameterAsVectorLayer(
            parameters, self.INPUT_WATER, context
        )
        molduraLayer = self.parameterAsVectorLayer(
            parameters, self.INPUT_MOLDURA, context
        )
        visibilityField = self.parameterAsString(
            parameters, self.VISIBILITY_FIELD, context
        )
        symbolSize = self.parameterAsDouble(parameters, self.SYMBOL_SIZE, context)
        gap = self.parameterAsDouble(parameters, self.MIN_GAP, context)
        roadWidth = self.parameterAsDouble(
            parameters, self.ROAD_SYMBOL_WIDTH, context
        )
        maxDisplacement = self.parameterAsDouble(
            parameters, self.MAX_DISPLACEMENT, context
        )
        maxIterations = self.parameterAsInt(parameters, self.MAX_ITERATIONS, context)
        genericExpression = self.parameterAsExpression(
            parameters, self.GENERIC_EXPRESSION, context
        )

        visFieldIdx = buildingLayer.fields().indexOf(visibilityField)
        if visFieldIdx < 0:
            raise QgsProcessingException(
                self.tr(
                    f'Visibility field "{visibilityField}" not found in building layer.'
                )
            )

        (flagSink, flagDestId) = self.parameterAsSink(
            parameters,
            self.FLAGS,
            context,
            buildingLayer.fields(),
            buildingLayer.wkbType(),
            buildingLayer.sourceCrs(),
        )

        multiFeedback = QgsProcessingMultiStepFeedback(6, feedback)
        algRunner = AlgRunner()
        halfSize = (symbolSize + gap) / 2.0

        # Phase 1: Data preparation
        multiFeedback.setCurrentStep(0)
        multiFeedback.pushInfo(self.tr("Phase 1: Data preparation"))
        if multiFeedback.isCanceled():
            return {self.FLAGS: flagDestId}
        prepData = self.prepareData(
            buildingLayer, roadLayer, waterLayer, molduraLayer,
            symbolSize, gap, roadWidth, maxDisplacement,
            visibilityField, genericExpression,
            context, multiFeedback, algRunner,
        )
        buildings = prepData["buildings"]
        forbiddenGeom = prepData["forbiddenGeom"]
        blocks = prepData["blocks"]

        if not buildings:
            multiFeedback.pushInfo(self.tr("No buildings to process."))
            return {self.FLAGS: flagDestId}

        # Phase 2: Conflict detection
        multiFeedback.setCurrentStep(1)
        multiFeedback.pushInfo(self.tr("Phase 2: Conflict detection"))
        if multiFeedback.isCanceled():
            return {self.FLAGS: flagDestId}
        spatialIndex = self.rebuildSpatialIndex(buildings, halfSize)
        conflicts = self.detectConflicts(
            buildings, halfSize, forbiddenGeom, spatialIndex
        )
        initialConflictCount = sum(1 for s in conflicts.values() if s)
        multiFeedback.pushInfo(
            self.tr(f"Detected {initialConflictCount} buildings with conflicts")
        )

        # Phase 3: Iterative displacement
        multiFeedback.setCurrentStep(2)
        multiFeedback.pushInfo(self.tr("Phase 3: Iterative displacement"))
        if multiFeedback.isCanceled():
            return {self.FLAGS: flagDestId}
        self.iterativeDisplacement(
            buildings, conflicts, forbiddenGeom, blocks,
            halfSize, maxDisplacement, maxIterations,
            multiFeedback,
        )

        # Phase 4: No-space detection
        multiFeedback.setCurrentStep(3)
        multiFeedback.pushInfo(self.tr("Phase 4: No-space detection"))
        if multiFeedback.isCanceled():
            return {self.FLAGS: flagDestId}
        self.detectNoSpace(
            buildings, conflicts, forbiddenGeom, blocks,
            halfSize, maxDisplacement, multiFeedback,
        )

        # Phase 5: Visibility resolution
        multiFeedback.setCurrentStep(4)
        multiFeedback.pushInfo(self.tr("Phase 5: Visibility resolution"))
        if multiFeedback.isCanceled():
            return {self.FLAGS: flagDestId}
        idsToHide, idsToFlag = self.resolveVisibility(
            buildings, conflicts, halfSize, multiFeedback
        )
        multiFeedback.pushInfo(
            self.tr(
                f"Hiding {len(idsToHide)} generic buildings, "
                f"flagging {len(idsToFlag)} non-generic buildings"
            )
        )

        # Phase 6: Apply results
        multiFeedback.setCurrentStep(5)
        multiFeedback.pushInfo(self.tr("Phase 6: Applying results"))
        if multiFeedback.isCanceled():
            return {self.FLAGS: flagDestId}
        self.applyResults(
            buildingLayer, buildings, idsToHide, idsToFlag,
            visFieldIdx, flagSink, multiFeedback,
        )

        # Stats
        hideSet = set(idsToHide)
        displacedCount = sum(
            1 for i, b in enumerate(buildings)
            if b["curPoint"] != b["origPoint"] and i not in hideSet
        )
        multiFeedback.pushInfo(
            self.tr(
                f"Complete: {displacedCount} displaced, "
                f"{len(idsToHide)} hidden, {len(idsToFlag)} flagged"
            )
        )

        return {self.FLAGS: flagDestId}

    def prepareData(
        self, buildingLayer, roadLayer, waterLayer, molduraLayer,
        symbolSize, gap, roadWidth, maxDisplacement,
        visibilityField, genericExpression,
        context, feedback, algRunner,
    ):
        # Determine which original feat IDs are inside moldura
        insideMolduraIds = None
        molduraGeom = QgsGeometry()
        if molduraLayer is not None:
            geomList = [
                f.geometry() for f in molduraLayer.getFeatures()
                if not f.geometry().isNull() and not f.geometry().isEmpty()
            ]
            molduraGeom = QgsGeometry.unaryUnion(geomList) if geomList else QgsGeometry()
            if molduraGeom.isNull() or molduraGeom.isEmpty():
                feedback.pushInfo(
                    self.tr("Moldura layer has no valid geometries. No buildings to process.")
                )
                return {"buildings": [], "forbiddenGeom": QgsGeometry(), "blocks": []}
            molduraEngine = QgsGeometry.createGeometryEngine(
                molduraGeom.constGet()
            )
            molduraEngine.prepareGeometry()
            insideMolduraIds = set()
            for feat in buildingLayer.getFeatures():
                geom = feat.geometry()
                if not geom.isNull() and not geom.isEmpty():
                    if molduraEngine.contains(geom.constGet()):
                        insideMolduraIds.add(feat.id())

        # Prepare expression to identify generic buildings
        expr = QgsExpression(genericExpression)
        if expr.hasParserError():
            raise QgsProcessingException(
                self.tr(f"Invalid generic expression: {expr.parserErrorString()}")
            )
        expressionContext = QgsExpressionContext()
        expressionContext.appendScopes(
            QgsExpressionContextUtils.globalProjectLayerScopes(buildingLayer)
        )

        # Build building records directly from original layer
        buildings = []
        visFieldIdx = buildingLayer.fields().indexOf(visibilityField)

        for feat in buildingLayer.getFeatures():
            geom = feat.geometry()
            if geom.isNull() or geom.isEmpty():
                continue
            if insideMolduraIds is not None and feat.id() not in insideMolduraIds:
                continue
            visValue = feat.attribute(visFieldIdx)
            if visValue == 2:
                continue

            point = geom.asPoint()
            qgsPoint = QgsPointXY(point.x(), point.y())
            expressionContext.setFeature(feat)
            isGeneric = bool(expr.evaluate(expressionContext))

            buildings.append({
                "featId": feat.id(),
                "origPoint": qgsPoint,
                "curPoint": QgsPointXY(qgsPoint.x(), qgsPoint.y()),
                "isGeneric": isGeneric,
                "blockIdx": None,
                "conflictsWithForbidden": False,
                "noSpace": False,
            })

        feedback.pushInfo(
            self.tr(f"Loaded {len(buildings)} buildings to process")
        )

        # Build forbidden zone from road buffers + water borders
        roadBufferDist = roadWidth / 2.0 + gap / 2.0
        roadBuffers = algRunner.runBuffer(
            roadLayer, roadBufferDist, context,
            dissolve=True, feedback=feedback,
        )

        forbiddenLayers = [roadBuffers]

        if waterLayer is not None:
            waterBoundaries = algRunner.runBoundary(
                waterLayer, context, feedback=feedback
            )
            waterBorderBuffers = algRunner.runBuffer(
                waterBoundaries, gap / 2.0, context,
                dissolve=True, feedback=feedback,
            )
            forbiddenLayers.append(waterBorderBuffers)

        if len(forbiddenLayers) > 1:
            mergedForbidden = algRunner.runMergeVectorLayers(
                forbiddenLayers, context, feedback=feedback
            )
            dissolvedForbidden = algRunner.runDissolve(
                mergedForbidden, context, feedback=feedback
            )
        else:
            dissolvedForbidden = algRunner.runDissolve(
                forbiddenLayers[0], context, feedback=feedback
            )

        forbiddenGeomList = [
            f.geometry() for f in dissolvedForbidden.getFeatures()
            if not f.geometry().isNull() and not f.geometry().isEmpty()
        ]
        forbiddenGeom = (
            QgsGeometry.unaryUnion(forbiddenGeomList)
            if forbiddenGeomList else QgsGeometry()
        )

        feedback.pushInfo(
            self.tr("Built forbidden zone from road/water buffers")
        )

        # Build blocks (complement of forbidden zone within extent)
        if molduraLayer is not None and insideMolduraIds is not None:
            # Reuse moldura geometry built in step 1
            extentGeom = molduraGeom
        else:
            # Use buildings bbox expanded by maxDisplacement
            extent = buildingLayer.sourceExtent()
            extent = extent.buffered(maxDisplacement + symbolSize)
            extentGeom = QgsGeometry.fromRect(extent)

        blocks = []
        if not forbiddenGeom.isNull() and not forbiddenGeom.isEmpty():
            blockGeom = extentGeom.difference(forbiddenGeom)
            if not blockGeom.isNull() and not blockGeom.isEmpty():
                # Split multipart into individual blocks
                for part in blockGeom.asGeometryCollection():
                    if not part.isNull() and not part.isEmpty() and part.area() > 0:
                        blocks.append(part)

        feedback.pushInfo(self.tr(f"Created {len(blocks)} blocks"))

        # Assign buildings to blocks
        if blocks:
            blockIndex = QgsSpatialIndex()
            for i, block in enumerate(blocks):
                feat = QgsFeature()
                feat.setId(i)
                feat.setGeometry(block)
                blockIndex.addFeature(feat)

            for building in buildings:
                pt = building["origPoint"]
                ptGeom = QgsGeometry.fromPointXY(pt)
                candidateIds = blockIndex.intersects(ptGeom.boundingBox())
                for cId in candidateIds:
                    if blocks[cId].contains(ptGeom):
                        building["blockIdx"] = cId
                        break

        return {
            "buildings": buildings,
            "forbiddenGeom": forbiddenGeom,
            "blocks": blocks,
        }

    def rebuildSpatialIndex(self, buildings, halfSize):
        spatialIndex = QgsSpatialIndex()
        for i, building in enumerate(buildings):
            pt = building["curPoint"]
            feat = QgsFeature()
            feat.setId(i)
            feat.setGeometry(
                QgsGeometry.fromRect(
                    QgsRectangle(
                        pt.x() - halfSize, pt.y() - halfSize,
                        pt.x() + halfSize, pt.y() + halfSize,
                    )
                )
            )
            spatialIndex.addFeature(feat)
        return spatialIndex

    def detectConflicts(self, buildings, halfSize, forbiddenGeom, spatialIndex,
                        forbiddenEngine=None):
        fullSize = halfSize * 2.0
        conflicts = {i: set() for i in range(len(buildings))}

        if forbiddenEngine is None and not forbiddenGeom.isNull() and not forbiddenGeom.isEmpty():
            forbiddenEngine = QgsGeometry.createGeometryEngine(
                forbiddenGeom.constGet()
            )
            forbiddenEngine.prepareGeometry()

        for i, building in enumerate(buildings):
            pt = building["curPoint"]
            searchRect = QgsRectangle(
                pt.x() - fullSize, pt.y() - fullSize,
                pt.x() + fullSize, pt.y() + fullSize,
            )
            candidateIds = spatialIndex.intersects(searchRect)

            for j in candidateIds:
                if j <= i:
                    continue
                otherPt = buildings[j]["curPoint"]
                dx = abs(pt.x() - otherPt.x())
                dy = abs(pt.y() - otherPt.y())
                if dx < fullSize and dy < fullSize:
                    conflicts[i].add(j)
                    conflicts[j].add(i)

            # Check forbidden zone
            if forbiddenEngine is not None:
                aabb = QgsGeometry.fromRect(
                    QgsRectangle(
                        pt.x() - halfSize, pt.y() - halfSize,
                        pt.x() + halfSize, pt.y() + halfSize,
                    )
                )
                building["conflictsWithForbidden"] = forbiddenEngine.intersects(
                    aabb.constGet()
                )
            else:
                building["conflictsWithForbidden"] = False

        return conflicts

    def iterativeDisplacement(
        self, buildings, conflicts, forbiddenGeom, blocks,
        halfSize, maxDisplacement, maxIterations, feedback,
    ):
        fullSize = halfSize * 2.0
        nBuildings = len(buildings)
        if nBuildings == 0:
            return

        forbiddenEngine = None
        if not forbiddenGeom.isNull() and not forbiddenGeom.isEmpty():
            forbiddenEngine = QgsGeometry.createGeometryEngine(
                forbiddenGeom.constGet()
            )
            forbiddenEngine.prepareGeometry()

        convergenceThreshold = fullSize * self.CONVERGENCE_FRACTION

        for iteration in range(maxIterations):
            if feedback.isCanceled():
                break

            damping = self.INITIAL_DAMPING * (1.0 - iteration / maxIterations)
            maxMovement = 0.0

            # Calculate forces for all buildings first, then apply
            forces = []
            for i in range(nBuildings):
                fx, fy = 0.0, 0.0
                myConflicts = conflicts.get(i, set())
                hasForbidden = buildings[i]["conflictsWithForbidden"]

                if not myConflicts and not hasForbidden:
                    forces.append((0.0, 0.0))
                    continue

                pt = buildings[i]["curPoint"]

                # Repulsion from neighbor buildings
                for j in myConflicts:
                    otherPt = buildings[j]["curPoint"]
                    dx = pt.x() - otherPt.x()
                    dy = pt.y() - otherPt.y()
                    overlapX = fullSize - abs(dx)
                    overlapY = fullSize - abs(dy)
                    if overlapX <= 0 or overlapY <= 0:
                        continue
                    # Push along axis of minimum penetration (each building absorbs half)
                    if overlapX < overlapY:
                        pushDir = 1.0 if dx >= 0 else -1.0
                        fx += pushDir * overlapX * self.NEIGHBOR_REPULSION_FACTOR
                    else:
                        pushDir = 1.0 if dy >= 0 else -1.0
                        fy += pushDir * overlapY * self.NEIGHBOR_REPULSION_FACTOR

                # Repulsion from forbidden zone
                if hasForbidden and forbiddenEngine is not None:
                    ptGeom = QgsGeometry.fromPointXY(pt)
                    nearestPt = forbiddenGeom.nearestPoint(ptGeom)
                    if not nearestPt.isNull() and not nearestPt.isEmpty():
                        nearPt = nearestPt.asPoint()
                        dx = pt.x() - nearPt.x()
                        dy = pt.y() - nearPt.y()
                        dist = math.sqrt(dx * dx + dy * dy)
                        if dist < halfSize and dist > 0.0001:
                            pushMag = (halfSize - dist) * self.FORBIDDEN_REPULSION_STRENGTH
                            fx += (dx / dist) * pushMag
                            fy += (dy / dist) * pushMag
                        elif dist <= 0.0001:
                            fx += random.uniform(-1, 1) * halfSize * self.NEIGHBOR_REPULSION_FACTOR
                            fy += random.uniform(-1, 1) * halfSize * self.NEIGHBOR_REPULSION_FACTOR

                origPt = buildings[i]["origPoint"]
                dx = origPt.x() - pt.x()
                dy = origPt.y() - pt.y()
                fx += dx * self.ORIGIN_ATTRACTION_STRENGTH
                fy += dy * self.ORIGIN_ATTRACTION_STRENGTH

                fx *= damping
                fy *= damping

                forces.append((fx, fy))

            # Apply forces
            for i in range(nBuildings):
                fx, fy = forces[i]
                if fx == 0.0 and fy == 0.0:
                    continue

                building = buildings[i]
                pt = building["curPoint"]
                newX = pt.x() + fx
                newY = pt.y() + fy

                # Clamp to max displacement from original
                origPt = building["origPoint"]
                dx = newX - origPt.x()
                dy = newY - origPt.y()
                dist = math.sqrt(dx * dx + dy * dy)
                if dist > maxDisplacement:
                    scale = maxDisplacement / dist
                    newX = origPt.x() + dx * scale
                    newY = origPt.y() + dy * scale

                # Block containment check
                blockIdx = building["blockIdx"]
                if blockIdx is not None and blockIdx < len(blocks):
                    newPtGeom = QgsGeometry.fromPointXY(QgsPointXY(newX, newY))
                    if not blocks[blockIdx].contains(newPtGeom):
                        # Try to stay inside: project onto block boundary
                        nearest = blocks[blockIdx].nearestPoint(newPtGeom)
                        if not nearest.isNull() and not nearest.isEmpty():
                            nPt = nearest.asPoint()
                            # Move slightly inside from boundary
                            cx = blocks[blockIdx].centroid().asPoint().x()
                            cy = blocks[blockIdx].centroid().asPoint().y()
                            dx2 = cx - nPt.x()
                            dy2 = cy - nPt.y()
                            d2 = math.sqrt(dx2 * dx2 + dy2 * dy2)
                            if d2 > 0.0001:
                                nudge = min(fullSize * 0.01, d2)
                                newX = nPt.x() + (dx2 / d2) * nudge
                                newY = nPt.y() + (dy2 / d2) * nudge
                            else:
                                newX = nPt.x()
                                newY = nPt.y()
                        else:
                            # Can't find nearest point, keep old position
                            continue

                movement = math.sqrt(
                    (newX - pt.x()) ** 2 + (newY - pt.y()) ** 2
                )
                maxMovement = max(maxMovement, movement)
                building["curPoint"] = QgsPointXY(newX, newY)

            spatialIndex = self.rebuildSpatialIndex(buildings, halfSize)
            conflicts.clear()
            newConflicts = self.detectConflicts(
                buildings, halfSize, forbiddenGeom, spatialIndex,
                forbiddenEngine=forbiddenEngine,
            )
            conflicts.update(newConflicts)

            currentConflictCount = sum(1 for s in conflicts.values() if s)

            if iteration % 10 == 0:
                feedback.pushInfo(
                    self.tr(
                        f"  Iteration {iteration}: {currentConflictCount} conflicts, "
                        f"max movement: {maxMovement:.6f}"
                    )
                )

            # Check convergence
            if currentConflictCount == 0:
                feedback.pushInfo(
                    self.tr(f"  All conflicts resolved at iteration {iteration}")
                )
                break
            if maxMovement < convergenceThreshold and iteration > 5:
                feedback.pushInfo(
                    self.tr(
                        f"  Converged at iteration {iteration} "
                        f"(max movement: {maxMovement:.6f})"
                    )
                )
                break

        finalConflicts = sum(1 for s in conflicts.values() if s)
        feedback.pushInfo(
            self.tr(f"Displacement complete: {finalConflicts} buildings still in conflict")
        )

    def detectNoSpace(
        self, buildings, conflicts, forbiddenGeom, blocks,
        halfSize, maxDisplacement, feedback,
    ):
        fullSize = halfSize * 2.0
        forbiddenEngine = None
        if not forbiddenGeom.isNull() and not forbiddenGeom.isEmpty():
            forbiddenEngine = QgsGeometry.createGeometryEngine(
                forbiddenGeom.constGet()
            )
            forbiddenEngine.prepareGeometry()

        # Collect buildings still in conflict
        conflictedIndices = [
            i for i in range(len(buildings))
            if conflicts.get(i) or buildings[i]["conflictsWithForbidden"]
        ]

        if not conflictedIndices:
            return

        feedback.pushInfo(
            self.tr(
                f"Testing {len(conflictedIndices)} buildings for available space"
            )
        )

        spatialIndex = self.rebuildSpatialIndex(buildings, halfSize)

        # Prepare block geometry engines for fast containment checks
        blockEngines = {}
        for idx in conflictedIndices:
            bIdx = buildings[idx]["blockIdx"]
            if bIdx is not None and bIdx < len(blocks) and bIdx not in blockEngines:
                engine = QgsGeometry.createGeometryEngine(blocks[bIdx].constGet())
                engine.prepareGeometry()
                blockEngines[bIdx] = engine

        gridStep = max(fullSize * 0.5, 0.001)
        maxDispSq = maxDisplacement * maxDisplacement
        resolved = 0

        for idx in conflictedIndices:
            if feedback.isCanceled():
                break

            building = buildings[idx]
            origPt = building["origPoint"]
            blockIdx = building["blockIdx"]
            blockEngine = blockEngines.get(blockIdx)

            found = False
            stepsX = int(maxDisplacement / gridStep) + 1

            for gx in range(-stepsX, stepsX + 1):
                if found:
                    break
                for gy in range(-stepsX, stepsX + 1):
                    candX = origPt.x() + gx * gridStep
                    candY = origPt.y() + gy * gridStep

                    dx = gx * gridStep
                    dy = gy * gridStep
                    if dx * dx + dy * dy > maxDispSq:
                        continue

                    # Block containment via prepared engine
                    if blockEngine is not None:
                        candGeom = QgsGeometry.fromPointXY(QgsPointXY(candX, candY))
                        if not blockEngine.contains(candGeom.constGet()):
                            continue

                    # Forbidden zone check
                    if forbiddenEngine is not None:
                        aabb = QgsGeometry.fromRect(
                            QgsRectangle(
                                candX - halfSize, candY - halfSize,
                                candX + halfSize, candY + halfSize,
                            )
                        )
                        if forbiddenEngine.intersects(aabb.constGet()):
                            continue

                    # Building-building conflict check
                    searchRect = QgsRectangle(
                        candX - fullSize, candY - fullSize,
                        candX + fullSize, candY + fullSize,
                    )
                    candidateIds = spatialIndex.intersects(searchRect)
                    hasConflict = False
                    for j in candidateIds:
                        if j == idx:
                            continue
                        otherPt = buildings[j]["curPoint"]
                        if (abs(candX - otherPt.x()) < fullSize
                                and abs(candY - otherPt.y()) < fullSize):
                            hasConflict = True
                            break

                    if not hasConflict:
                        oldCurPt = building["curPoint"]
                        building["curPoint"] = QgsPointXY(candX, candY)
                        oldConflicts = conflicts.get(idx, set()).copy()
                        conflicts[idx] = set()
                        for j in oldConflicts:
                            conflicts[j].discard(idx)
                        building["conflictsWithForbidden"] = False
                        # Incremental spatial index update using old curPoint
                        oldFeat = QgsFeature()
                        oldFeat.setId(idx)
                        oldFeat.setGeometry(QgsGeometry.fromRect(QgsRectangle(
                            oldCurPt.x() - halfSize, oldCurPt.y() - halfSize,
                            oldCurPt.x() + halfSize, oldCurPt.y() + halfSize,
                        )))
                        spatialIndex.deleteFeature(oldFeat)
                        newFeat = QgsFeature()
                        newFeat.setId(idx)
                        newFeat.setGeometry(QgsGeometry.fromRect(QgsRectangle(
                            candX - halfSize, candY - halfSize,
                            candX + halfSize, candY + halfSize,
                        )))
                        spatialIndex.addFeature(newFeat)
                        found = True
                        resolved += 1
                        break

            if not found:
                building["noSpace"] = True

        noSpaceCount = sum(1 for b in buildings if b["noSpace"])
        feedback.pushInfo(
            self.tr(
                f"No-space detection: {resolved} resolved, "
                f"{noSpaceCount} without valid position"
            )
        )

    def resolveVisibility(self, buildings, conflicts, halfSize, feedback):
        # Collect buildings that still have conflicts or noSpace
        problematic = []
        for i, building in enumerate(buildings):
            hasConflict = bool(conflicts.get(i))
            if hasConflict or building["noSpace"] or building["conflictsWithForbidden"]:
                problematic.append(i)

        if not problematic:
            return [], []

        # Sort: generics first, then by number of conflicts (desc)
        problematic.sort(
            key=lambda i: (
                0 if buildings[i]["isGeneric"] else 1,
                -len(conflicts.get(i, set())),
            )
        )

        idsToHide = []  # generic buildings to set visibility=2
        idsToFlag = []  # non-generic buildings for FLAGS sink

        hiddenSet = set()

        for i in problematic:
            if i in hiddenSet:
                continue

            # Check if this building still conflicts with any non-hidden building
            activeConflicts = [
                j for j in conflicts.get(i, set()) if j not in hiddenSet
            ]
            stillConflictsWithForbidden = buildings[i]["conflictsWithForbidden"]

            if not activeConflicts and not stillConflictsWithForbidden and not buildings[i]["noSpace"]:
                continue

            if buildings[i]["isGeneric"]:
                idsToHide.append(i)
                hiddenSet.add(i)
            else:
                idsToFlag.append(i)
                hiddenSet.add(i)

            # Update neighbors' conflict lists
            for j in list(conflicts.get(i, set())):
                conflicts[j].discard(i)

        return idsToHide, idsToFlag

    def applyResults(
        self, buildingLayer, buildings, idsToHide, idsToFlag,
        visFieldIdx, flagSink, feedback,
    ):
        # Write flagged features to FLAGS sink (re-read from layer)
        flagFeatIds = {buildings[idx]["featId"] for idx in idsToFlag}
        if flagFeatIds:
            for feat in buildingLayer.getFeatures():
                if feat.id() in flagFeatIds:
                    flagSink.addFeature(QgsFeature(feat), QgsFeatureSink.FastInsert)

        # Collect in-place edits
        displacements = {}
        hideIds = [buildings[idx]["featId"] for idx in idsToHide]
        hideIdxSet = set(idsToHide)

        for i, building in enumerate(buildings):
            if i in hideIdxSet:
                continue
            if building["curPoint"] != building["origPoint"]:
                displacements[building["featId"]] = QgsGeometry.fromPointXY(
                    building["curPoint"]
                )

        # Apply in-place edits
        if not displacements and not hideIds:
            feedback.pushInfo(self.tr("No changes to apply."))
            return

        buildingLayer.startEditing()
        buildingLayer.beginEditCommand("Building Generalization")

        for featId, newGeom in displacements.items():
            buildingLayer.changeGeometry(featId, newGeom, skipDefaultValue=True)

        for featId in hideIds:
            buildingLayer.changeAttributeValue(featId, visFieldIdx, 2)

        buildingLayer.endEditCommand()

        feedback.pushInfo(
            self.tr(
                f"Applied {len(displacements)} geometry changes "
                f"and {len(hideIds)} visibility changes in-place"
            )
        )
