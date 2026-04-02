# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-01-18
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import json
import uuid

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner

from qgis.PyQt.QtCore import QCoreApplication

from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsProcessing,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingException,
    QgsGeometry,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterString,
    QgsSpatialIndex,
    QgsDistanceArea,
    QgsCoordinateReferenceSystem,
)


class ReclassifyAdjacentPolygonsAlgorithm(ValidationAlgorithm):
    INPUT_VEGETATION = "INPUT_VEGETATION"
    INPUT_WATER = "INPUT_WATER"
    INPUT_BUILT_UP = "INPUT_BUILT_UP"
    INPUT_FRAME = "INPUT_FRAME"
    LABEL_FIELD = "LABEL_FIELD"
    WATER_CLASS_VALUE = "WATER_CLASS_VALUE"
    BUILT_UP_CLASS_VALUE = "BUILT_UP_CLASS_VALUE"
    MIN_AREA = "MIN_AREA"
    GENERALIZATION_RULES = "GENERALIZATION_RULES"

    DEFAULT_RULES = json.dumps(
        {
            "non_growing_classes": [1, 2],
            "class_groups": {
                "Vegetacao Cultivada": [107, 142, 150, 194, 196, 197],
                "Mangue": [201],
                "Brejo ou pantano": [301],
                "Restinga": [401],
                "Campinarana": [501],
                "Floresta": [601, 602],
                "Cerrado/Cerradao": [701],
                "Caatinga": [801],
                "Campo": [901],
                "Terreno Exposto": [1000, 1001, 1002, 1003, 1004],
                "Reflorestamento": [1296],
            },
            "size_thresholds": {"1": 10000},
        },
        indent=2,
        ensure_ascii=False,
    )

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_VEGETATION,
                self.tr("Vegetation Layer"),
                [QgsProcessing.TypeVectorPolygon],
                defaultValue="cobter_vegetacao_a",
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_WATER,
                self.tr("Water Body Layer"),
                [QgsProcessing.TypeVectorPolygon],
                defaultValue="cobter_massa_dagua_a",
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_BUILT_UP,
                self.tr("Built-up Area Layer"),
                [QgsProcessing.TypeVectorPolygon],
                defaultValue="cobter_area_edificada_a",
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_FRAME,
                self.tr("Map Frame"),
                [QgsProcessing.TypeVectorPolygon],
                defaultValue="aux_moldura_a",
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.LABEL_FIELD,
                self.tr("Class label field on vegetation layer"),
                "tipo",
                self.INPUT_VEGETATION,
                QgsProcessingParameterField.Any,
                allowMultiple=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.WATER_CLASS_VALUE,
                self.tr("Class value for water bodies"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=1,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.BUILT_UP_CLASS_VALUE,
                self.tr("Class value for built-up areas"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=2,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_AREA,
                self.tr("Default minimum area (m2)"),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=62500,
                minValue=0,
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.GENERALIZATION_RULES,
                self.tr(
                    "Generalization Rules (JSON). "
                    "non_growing_classes: class values that should not grow. "
                    "class_groups: groups of related classes for dissolution "
                    "priority. "
                    "size_thresholds: per-class minimum area overrides in m2."
                ),
                multiLine=True,
                defaultValue=self.DEFAULT_RULES,
                optional=True,
            )
        )

    def shortHelpString(self):
        return self.tr(
            "Reclassifies small polygons in a land cover dataset to the class "
            "of the adjacent neighbor with the longest shared boundary.\n\n"
            "Receives three layers (vegetation, water, built-up) and a map "
            "frame. Merges them, then iteratively dissolves small polygons "
            "respecting class group priority and non-growing constraints. "
            "Edits all three layers in-place.\n\n"
            "Polygons touching the map frame boundary are never reclassified "
            "(they may extend beyond the map sheet).\n\n"
            "Dissolution priority (highest to lowest):\n"
            "  1. Same class, longest shared boundary\n"
            "  2. Same group, longest shared boundary\n"
            "  3. Any non-restricted class, longest shared boundary\n"
            "  4. Non-growing class (last resort, e.g. island in a lake)\n\n"
            "Default rules are pre-configured for Brazilian land cover "
            "(cobter) with vegetation groups, water (1) and built-up (2) "
            "as non-growing classes."
        )

    def processAlgorithm(self, parameters, context, feedback):
        try:
            import networkx as nx
        except ImportError:
            raise QgsProcessingException(
                self.tr(
                    "This algorithm requires the Python networkx library. "
                    "Please install this library and try again."
                )
            )
        self.algRunner = AlgRunner()
        vegLyr = self.parameterAsVectorLayer(
            parameters, self.INPUT_VEGETATION, context
        )
        waterLyr = self.parameterAsVectorLayer(
            parameters, self.INPUT_WATER, context
        )
        builtUpLyr = self.parameterAsVectorLayer(
            parameters, self.INPUT_BUILT_UP, context
        )
        frameLyr = self.parameterAsVectorLayer(
            parameters, self.INPUT_FRAME, context
        )
        classFieldName = self.parameterAsStrings(
            parameters, self.LABEL_FIELD, context
        )[0]
        waterValue = self.parameterAsInt(
            parameters, self.WATER_CLASS_VALUE, context
        )
        builtUpValue = self.parameterAsInt(
            parameters, self.BUILT_UP_CLASS_VALUE, context
        )
        defaultMinArea = self.parameterAsDouble(
            parameters, self.MIN_AREA, context
        )
        rulesJson = self.parameterAsString(
            parameters, self.GENERALIZATION_RULES, context
        )

        nonGrowingClasses, classToGroup, sizeThresholds = (
            self.parseGeneralizationRules(rulesJson, defaultMinArea, feedback)
        )
        thresholdPhases = self.groupThresholds(sizeThresholds)
        nPhases = len(thresholdPhases)

        # Steps: prep(1) + merge(1) + frame(1) + dissolve+m2s(2)
        #   + per-phase(4) + write-back(1)
        nSteps = 5 + nPhases * 4 + 1
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0

        # Prepare water and built-up layers: ensure they have the class field
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Preparing layers"))
        waterReady = self._ensureClassField(
            waterLyr, classFieldName, waterValue, context, multiStepFeedback,
        )
        builtUpReady = self._ensureClassField(
            builtUpLyr, classFieldName, builtUpValue, context, multiStepFeedback,
        )
        # Collect actual non-growing class values from the layers
        waterClasses = {
            feat[classFieldName]
            for feat in waterReady.getFeatures()
            if feat[classFieldName] is not None
        }
        builtUpClasses = {
            feat[classFieldName]
            for feat in builtUpReady.getFeatures()
            if feat[classFieldName] is not None
        }
        nonGrowingClasses.update(waterClasses)
        nonGrowingClasses.update(builtUpClasses)
        feedback.pushInfo(
            self.tr("Non-growing classes (including all water/built-up subtypes): %s")
            % str(nonGrowingClasses)
        )
        currentStep += 1

        # Merge all 3 layers
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Merging layers"))
        mergedLyr = self.algRunner.runMergeVectorLayers(
            inputList=[vegLyr, waterReady, builtUpReady],
            context=context,
            feedback=multiStepFeedback,
            crs=vegLyr.sourceCrs(),
            is_child_algorithm=True,
        )
        currentStep += 1

        # Compute frame boundary for edge detection
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Computing frame boundary")
        )
        # Dissolve frame first to merge adjacent tiles, then extract
        # outer boundary (avoids marking internal tile edges as frame border)
        dissolvedFrame = self.algRunner.runDissolve(
            inputLyr=frameLyr,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        frameBoundaryLyr = self.algRunner.runBoundary(
            inputLayer=dissolvedFrame,
            context=context,
            feedback=multiStepFeedback,
        )
        geomList = [
            feat.geometry()
            for feat in frameBoundaryLyr.getFeatures()
            if not feat.geometry().isEmpty()
        ]
        frameBoundaryGeom = (
            QgsGeometry.unaryUnion(geomList) if geomList else None
        )
        currentStep += 1

        # Initial dissolve + multipart to singlepart
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Initial dissolve by class field")
        )
        cacheLyr = self.algRunner.runDissolve(
            inputLyr=mergedLyr,
            context=context,
            feedback=multiStepFeedback,
            field=[classFieldName],
            is_child_algorithm=True,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Converting multipart to singlepart")
        )
        cacheLyr = self.algRunner.runMultipartToSingleParts(
            inputLayer=cacheLyr, context=context, feedback=multiStepFeedback,
        )
        currentStep += 1

        # Configure geodetic area calculator (handles geographic CRS like 4674)
        distArea = QgsDistanceArea()
        distArea.setSourceCrs(
            cacheLyr.sourceCrs(), context.transformContext()
        )
        distArea.setEllipsoid(cacheLyr.sourceCrs().ellipsoidAcronym())

        if nPhases > 1:
            multiStepFeedback.pushInfo(
                self.tr("Processing in %d phases") % nPhases
            )

        # Multi-phase reclassification
        for phaseIdx, (threshold, dnList) in enumerate(thresholdPhases):
            if multiStepFeedback.isCanceled():
                break
            if dnList == ["default"]:
                multiStepFeedback.pushInfo(
                    self.tr("Phase %d/%d: threshold=%d m2, all other classes")
                    % (phaseIdx + 1, nPhases, threshold)
                )
            else:
                multiStepFeedback.pushInfo(
                    self.tr("Phase %d/%d: threshold=%d m2, classes %s")
                    % (phaseIdx + 1, nPhases, threshold, str(dnList))
                )

            specificDNs = {
                dn for dn, _ in sizeThresholds.items() if dn != "default"
            }

            # Build graph
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(
                self.tr("Building adjacency graph")
            )
            G, featDict, idSet, featidToFid, areaCache = (
                self.buildAuxStructures(
                    nx=nx,
                    inputLyr=cacheLyr,
                    classFieldName=classFieldName,
                    threshold=threshold,
                    dnList=dnList,
                    specificDNs=specificDNs,
                    frameBoundaryGeom=frameBoundaryGeom,
                    distArea=distArea,
                    context=context,
                    feedback=multiStepFeedback,
                )
            )
            currentStep += 1

            # Reclassify
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Reclassifying"))
            anchorIdsSet = set(featDict.keys()).difference(idSet)
            updateDict = self.reclassifyPolygons(
                G=G,
                featDict=featDict,
                anchorIdsSet=anchorIdsSet,
                candidateIdSet=idSet,
                classFieldName=classFieldName,
                nonGrowingClasses=nonGrowingClasses,
                classToGroup=classToGroup,
                areaCache=areaCache,
                feedback=multiStepFeedback,
            )
            currentStep += 1

            # Apply updates + dissolve
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(
                self.tr("Applying updates and dissolving")
            )
            if updateDict:
                fieldIdx = cacheLyr.dataProvider().fields().indexFromName(
                    classFieldName
                )
                cacheLyr.startEditing()
                cacheLyr.beginEditCommand(
                    "Reclassify phase %d" % (phaseIdx + 1)
                )
                dp = cacheLyr.dataProvider()
                for featid, classValue in updateDict.items():
                    if multiStepFeedback.isCanceled():
                        break
                    providerFid = featidToFid.get(featid)
                    if providerFid is None:
                        continue
                    dp.changeAttributeValues(
                        {providerFid: {fieldIdx: classValue}}
                    )
                cacheLyr.endEditCommand()
                multiStepFeedback.pushInfo(
                    self.tr("  Updated %d features.") % len(updateDict)
                )
            currentStep += 1

            multiStepFeedback.setCurrentStep(currentStep)
            if updateDict:
                cacheLyr = self.algRunner.runDissolve(
                    inputLyr=cacheLyr,
                    context=context,
                    feedback=multiStepFeedback,
                    field=[classFieldName],
                    is_child_algorithm=True,
                )
                cacheLyr = self.algRunner.runMultipartToSingleParts(
                    inputLayer=cacheLyr,
                    context=context,
                    feedback=multiStepFeedback,
                )
            currentStep += 1

        # Write back to original layers
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Writing results back to original layers")
        )
        self.writeBackToLayers(
            cacheLyr=cacheLyr,
            classFieldName=classFieldName,
            vegLyr=vegLyr,
            waterLyr=waterLyr,
            builtUpLyr=builtUpLyr,
            waterClasses=waterClasses,
            builtUpClasses=builtUpClasses,
            feedback=multiStepFeedback,
        )

        return {}

    def _ensureClassField(
        self, layer, classFieldName, defaultValue, context, feedback,
    ):
        """If the layer already has classFieldName, return it as-is.
        Otherwise create the field with a fixed default value."""
        if layer.fields().indexFromName(classFieldName) >= 0:
            feedback.pushInfo(
                self.tr("  Layer '%s' already has field '%s', using existing values.")
                % (layer.name(), classFieldName)
            )
            return layer
        feedback.pushInfo(
            self.tr("  Layer '%s' has no field '%s', creating with value %s.")
            % (layer.name(), classFieldName, str(defaultValue))
        )
        return self.algRunner.runCreateFieldWithExpression(
            inputLyr=layer,
            expression=str(defaultValue),
            fieldType=1,
            fieldName=classFieldName,
            feedback=feedback,
            context=context,
        )

    def writeBackToLayers(
        self, cacheLyr, classFieldName, vegLyr, waterLyr, builtUpLyr,
        waterClasses, builtUpClasses, feedback,
    ):
        """Splits the processed cache layer by class value and writes back
        to each original layer. Preserves original attributes by matching
        result polygons to originals via centroid spatial lookup."""
        # Split result features by target layer
        waterFeats = []
        builtUpFeats = []
        vegFeats = []

        for feat in cacheLyr.getFeatures():
            if feedback.isCanceled():
                return
            classVal = feat[classFieldName]
            try:
                classVal = int(classVal) if classVal is not None else None
            except (ValueError, TypeError):
                pass

            if classVal in waterClasses:
                waterFeats.append(feat)
            elif classVal in builtUpClasses:
                builtUpFeats.append(feat)
            else:
                vegFeats.append(feat)

        for lyr, feats, label in [
            (waterLyr, waterFeats, "water"),
            (builtUpLyr, builtUpFeats, "built-up"),
            (vegLyr, vegFeats, "vegetation"),
        ]:
            if feedback.isCanceled():
                return
            self._writeBackToSingleLayer(
                lyr, feats, classFieldName, label, feedback,
            )

    def _writeBackToSingleLayer(
        self, lyr, resultFeats, classFieldName, label, feedback,
    ):
        """Write result features back to a single layer, preserving
        original attributes where possible by matching via centroid."""
        # Build spatial index of original features for attribute lookup
        origIndex = QgsSpatialIndex()
        origDict = {}
        for feat in lyr.getFeatures():
            origIndex.addFeature(feat)
            origDict[feat.id()] = feat

        classFieldIdx = lyr.fields().indexFromName(classFieldName)

        lyr.startEditing()
        lyr.beginEditCommand("Reclassify adjacent polygons - %s" % label)

        # Delete all existing features
        allIds = list(origDict.keys())
        if allIds:
            lyr.deleteFeatures(allIds)

        # Identify primary key / UUID fields that need unique values
        pkIdxSet = set()
        for i in range(lyr.fields().count()):
            field = lyr.fields().at(i)
            name = field.name().lower()
            # "id" fields that are text (UUID) need regeneration
            if name == "id" and field.type() in (10,):  # QVariant.String
                pkIdxSet.add(i)

        # Add result features, copying attributes from best-matching original
        newFeats = []
        for srcFeat in resultFeats:
            if feedback.isCanceled():
                break
            newFeat = QgsFeature(lyr.fields())
            newFeat.setGeometry(srcFeat.geometry())

            # Find original feature whose centroid is closest
            centroid = srcFeat.geometry().centroid()
            if not centroid.isEmpty():
                nearest = origIndex.nearestNeighbor(
                    centroid.asPoint(), 1
                )
                if nearest:
                    origFeat = origDict[nearest[0]]
                    for i in range(lyr.fields().count()):
                        newFeat.setAttribute(i, origFeat.attribute(i))

            # Override class field with the result value
            if classFieldIdx >= 0:
                newFeat.setAttribute(classFieldIdx, srcFeat[classFieldName])
            # Regenerate UUID primary keys to avoid duplicates
            for pkIdx in pkIdxSet:
                newFeat.setAttribute(pkIdx, str(uuid.uuid4()))
            newFeats.append(newFeat)

        if newFeats:
            lyr.addFeatures(newFeats, QgsFeatureSink.FastInsert)

        lyr.endEditCommand()
        feedback.pushInfo(
            self.tr("  %s: %d features written.") % (label, len(newFeats))
        )

    def parseGeneralizationRules(self, rulesJson, defaultMinArea, feedback):
        nonGrowingClasses = set()
        classToGroup = {}
        sizeThresholds = {"default": defaultMinArea}

        if not rulesJson or not rulesJson.strip():
            return nonGrowingClasses, classToGroup, sizeThresholds

        try:
            rules = json.loads(rulesJson)
        except json.JSONDecodeError as e:
            raise QgsProcessingException(
                self.tr("Invalid JSON in Generalization Rules: %s") % str(e)
            )

        if "non_growing_classes" in rules:
            for val in rules["non_growing_classes"]:
                try:
                    nonGrowingClasses.add(int(val))
                except (ValueError, TypeError):
                    nonGrowingClasses.add(val)
            if nonGrowingClasses:
                feedback.pushInfo(
                    self.tr("Non-growing classes: %s")
                    % str(nonGrowingClasses)
                )

        if "class_groups" in rules:
            for groupName, members in rules["class_groups"].items():
                for m in members:
                    try:
                        classToGroup[int(m)] = groupName
                    except (ValueError, TypeError):
                        classToGroup[m] = groupName
            if classToGroup:
                feedback.pushInfo(
                    self.tr("Loaded %d class-to-group mappings.")
                    % len(classToGroup)
                )

        if "size_thresholds" in rules:
            for key, value in rules["size_thresholds"].items():
                try:
                    sizeThresholds[int(key)] = float(value)
                except (ValueError, TypeError):
                    feedback.pushWarning(
                        self.tr("Skipping invalid size threshold: %s -> %s")
                        % (key, value)
                    )
            feedback.pushInfo(
                self.tr("Size thresholds: %s") % str(sizeThresholds)
            )

        return nonGrowingClasses, classToGroup, sizeThresholds

    def groupThresholds(self, sizeThresholds):
        groups = defaultdict(list)
        for dn, threshold in sizeThresholds.items():
            groups[threshold].append(dn)
        return sorted(groups.items(), key=lambda x: x[0])

    def buildAuxStructures(
        self, nx, inputLyr, classFieldName, threshold, dnList,
        specificDNs, frameBoundaryGeom, distArea, context, feedback,
    ):
        G = nx.Graph()
        featDict = dict()
        idSet = set()
        featidToFid = dict()
        areaCache = dict()
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)

        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(
            self.tr("Building spatial index")
        )
        spatialIdx = QgsSpatialIndex()
        allFeatDict = dict()
        nFeats = inputLyr.featureCount()
        if nFeats == 0:
            return G, featDict, idSet, featidToFid, areaCache
        stepSize = 100 / nFeats
        isDefaultPhase = dnList == ["default"]

        for current, feat in enumerate(inputLyr.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            fid = feat.id()
            allFeatDict[fid] = feat
            featidToFid[fid] = fid
            spatialIdx.addFeature(feat)

            classVal = feat[classFieldName]
            try:
                classVal = int(classVal) if classVal is not None else None
            except (ValueError, TypeError):
                pass
            area = distArea.measureArea(feat.geometry())

            isCandidate = False
            if isDefaultPhase:
                if classVal not in specificDNs and area < threshold:
                    isCandidate = True
            else:
                if classVal in dnList and area < threshold:
                    isCandidate = True

            # Exclude candidates touching frame boundary
            if isCandidate and frameBoundaryGeom is not None:
                if feat.geometry().intersects(frameBoundaryGeom):
                    isCandidate = False

            if isCandidate:
                idSet.add(fid)
                featDict[fid] = feat
                areaCache[fid] = area

            multiStepFeedback.setProgress(current * stepSize)

        nCandidates = len(idSet)
        if nCandidates == 0:
            return G, featDict, idSet, featidToFid, areaCache

        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.setProgressText(
            self.tr("Computing shared boundaries (%d candidates)")
            % nCandidates
        )
        stepSize = 100 / nCandidates

        boundaryCache = dict()
        for current, candidateId in enumerate(idSet):
            if multiStepFeedback.isCanceled():
                break
            candidateFeat = allFeatDict[candidateId]
            candidateGeom = candidateFeat.geometry()
            candidateBbox = candidateGeom.boundingBox()
            if candidateId not in boundaryCache:
                boundaryCache[candidateId] = QgsGeometry(
                    candidateGeom.constGet().boundary()
                )
            candidateBoundary = boundaryCache[candidateId]

            for neighborFid in spatialIdx.intersects(candidateBbox):
                if neighborFid == candidateId:
                    continue
                if G.has_edge(candidateId, neighborFid):
                    continue

                neighborFeat = allFeatDict[neighborFid]
                neighborGeom = neighborFeat.geometry()

                if not candidateGeom.intersects(neighborGeom):
                    continue

                if neighborFid not in boundaryCache:
                    boundaryCache[neighborFid] = QgsGeometry(
                        neighborGeom.constGet().boundary()
                    )
                sharedGeom = candidateBoundary.intersection(
                    boundaryCache[neighborFid]
                )
                if sharedGeom.isEmpty() or sharedGeom.isNull():
                    continue
                sharedLength = sharedGeom.length()
                if sharedLength <= 0:
                    continue

                if neighborFid not in featDict:
                    featDict[neighborFid] = neighborFeat
                G.add_edge(candidateId, neighborFid, length=sharedLength)

            multiStepFeedback.setProgress(current * stepSize)

        multiStepFeedback.pushInfo(
            self.tr("  Graph: %d nodes, %d edges, %d candidates.")
            % (G.number_of_nodes(), G.number_of_edges(), nCandidates)
        )
        return G, featDict, idSet, featidToFid, areaCache

    def reclassifyPolygons(
        self, G, featDict, anchorIdsSet, candidateIdSet,
        classFieldName, nonGrowingClasses, classToGroup,
        areaCache, feedback,
    ):
        updateDict = dict()
        nIds = len(candidateIdSet)
        if nIds == 0:
            return updateDict
        stepSize = 100 / nIds
        processedFeats = 0
        visitedSet = set()

        def getClassVal(featId):
            val = featDict[featId][classFieldName]
            try:
                return int(val) if val is not None else val
            except (ValueError, TypeError):
                return val

        def chooseId(nodeId, neighborIds):
            candidateClass = getClassVal(nodeId)
            candidateGroup = classToGroup.get(candidateClass)

            tiers = [[], [], [], []]
            for nid in neighborIds:
                nClass = getClassVal(nid)
                length = G[nodeId][nid]["length"]
                if nClass == candidateClass:
                    tiers[0].append((nid, length))
                elif (
                    candidateGroup is not None
                    and classToGroup.get(nClass) == candidateGroup
                ):
                    tiers[1].append((nid, length))
                elif nClass not in nonGrowingClasses:
                    tiers[2].append((nid, length))
                else:
                    tiers[3].append((nid, length))

            for tier in tiers:
                if tier:
                    return max(tier, key=lambda x: x[1])[0]
            return None

        # Phase 1: degree-1 candidates whose only neighbor is an anchor
        for nodeId in set(
            n for n in G.nodes if G.degree(n) == 1
        ) - anchorIdsSet:
            if feedback.isCanceled():
                return updateDict
            neighborId = next(iter(G.neighbors(nodeId)))
            if neighborId not in anchorIdsSet:
                continue
            # Use chooseId even for degree-1 to respect tier priority
            chosenId = chooseId(nodeId, {neighborId})
            if chosenId is None:
                continue
            newClass = getClassVal(chosenId)
            featDict[nodeId][classFieldName] = newClass
            updateDict[nodeId] = newClass
            visitedSet.add(nodeId)
            processedFeats += 1
            feedback.setProgress(processedFeats * stepSize)

        # Phase 2: iterative BFS expansion from anchors
        originalAnchorIdSet = anchorIdsSet
        allAnchorsSet = set(anchorIdsSet)
        currentWave = set(anchorIdsSet)
        while True:
            newAnchors = set()
            for anchorId in currentWave:
                if feedback.isCanceled():
                    return updateDict
                neighbors = set(G.neighbors(anchorId)) - originalAnchorIdSet
                for nodeId in sorted(
                    neighbors - visitedSet - allAnchorsSet,
                    key=lambda x: areaCache.get(x, 0),
                ):
                    if feedback.isCanceled():
                        return updateDict
                    neighborAnchors = set(G.neighbors(nodeId)).intersection(
                        allAnchorsSet
                    )
                    if not neighborAnchors:
                        continue
                    chosenId = chooseId(nodeId, neighborAnchors)
                    if chosenId is None:
                        continue
                    newClass = getClassVal(chosenId)
                    visitedSet.add(nodeId)
                    processedFeats += 1
                    featDict[nodeId][classFieldName] = newClass
                    updateDict[nodeId] = newClass
                    newAnchors.add(nodeId)
                    feedback.setProgress(processedFeats * stepSize)
            allAnchorsSet.update(newAnchors)
            currentWave = newAnchors
            if not currentWave:
                break

        unvisited = candidateIdSet - visitedSet
        if unvisited:
            feedback.pushInfo(
                self.tr(
                    "  %d candidates not reclassified "
                    "(no reachable anchor neighbors)."
                )
                % len(unvisited)
            )
        return updateDict

    def name(self):
        return "reclassifyadjacentpolygonsalgorithm"

    def displayName(self):
        return self.tr("Reclassify Adjacent Polygons")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"

    def shortDescription(self):
        return self.tr(
            "Reclassifies small polygons in a land cover dataset to the "
            "class of the adjacent neighbor with the longest shared boundary."
        )

    def tr(self, string):
        return QCoreApplication.translate(
            "ReclassifyAdjacentPolygonsAlgorithm", string
        )

    def createInstance(self):
        return ReclassifyAdjacentPolygonsAlgorithm()
