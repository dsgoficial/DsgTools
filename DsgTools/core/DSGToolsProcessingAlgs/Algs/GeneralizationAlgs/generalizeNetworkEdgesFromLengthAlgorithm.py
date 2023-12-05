# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-11-27
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

import concurrent.futures

from itertools import chain
import os
from typing import Dict, List, Optional, Set
from PyQt5.QtCore import QCoreApplication
from DsgTools.core.GeometricTools import graphHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.PyQt.QtCore import QByteArray
from qgis.core import (
    Qgis,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterEnum,
    QgsProcessingParameterVectorLayer,
    QgsFeedback,
    QgsProcessingContext,
    QgsVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterBoolean,
)

from ...algRunner import AlgRunner
from ..ValidationAlgs.validationAlgorithm import ValidationAlgorithm


class GeneralizeNetworkEdgesWithLengthAlgorithm(ValidationAlgorithm):
    NETWORK_LAYER = "NETWORK_LAYER"
    MIN_LENGTH = "MIN_LENGTH"
    GEOGRAPHIC_BOUNDS_LAYER = "GEOGRAPHIC_BOUNDS_LAYER"
    GROUP_BY_SPATIAL_PARTITION = "GROUP_BY_SPATIAL_PARTITION"
    POINT_CONSTRAINT_LAYER_LIST = "POINT_CONSTRAINT_LAYER_LIST"
    LINE_CONSTRAINT_LAYER_LIST = "LINE_CONSTRAINT_LAYER_LIST"
    POLYGON_CONSTRAINT_LAYER_LIST = "POLYGON_CONSTRAINT_LAYER_LIST"
    METHOD = "METHOD"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.NETWORK_LAYER,
                self.tr("Network layer"),
                [QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_LENGTH,
                self.tr("Minimum size"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.001,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.POINT_CONSTRAINT_LAYER_LIST,
                self.tr("Point constraint Layers"),
                QgsProcessing.TypeVectorPoint,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.LINE_CONSTRAINT_LAYER_LIST,
                self.tr("Line constraint Layers"),
                QgsProcessing.TypeVectorLine,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.POLYGON_CONSTRAINT_LAYER_LIST,
                self.tr("Polygon constraint Layers"),
                QgsProcessing.TypeVectorPolygon,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDS_LAYER,
                self.tr("Reference layer"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.GROUP_BY_SPATIAL_PARTITION,
                self.tr("Run algothimn grouping by spatial partition"),
            )
        )
        self.selectionIdDict = {
            1: Qgis.SelectBehavior.SetSelection,
            2: Qgis.SelectBehavior.AddToSelection,
            3: Qgis.SelectBehavior.IntersectSelection,
            4: Qgis.SelectBehavior.RemoveFromSelection,
        }
        self.method = [
            self.tr("Remove features from input layer"),
            self.tr("Modify current selection by creating new selection"),
            self.tr("Modify current selection by adding to current selection"),
            self.tr("Modify current selection by selecting within current selection"),
            self.tr("Modify current selection by removing from current selection"),
        ]

        self.addParameter(
            QgsProcessingParameterEnum(
                self.METHOD, self.tr("Method"), options=self.method, defaultValue=0
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        try:
            import networkx as nx
        except ImportError:
            raise QgsProcessingException(
                self.tr(
                    "This algorithm requires the Python networkx library. Please install this library and try again."
                )
            )
        # get the network handler
        self.algRunner = AlgRunner()
        self.layerHandler = LayerHandler()
        networkLayer = self.parameterAsLayer(parameters, self.NETWORK_LAYER, context)
        threshold = self.parameterAsDouble(parameters, self.MIN_LENGTH, context)
        geographicBoundsLayer = self.parameterAsLayer(
            parameters, self.GEOGRAPHIC_BOUNDS_LAYER, context
        )
        pointLayerList = self.parameterAsLayerList(
            parameters, self.POINT_CONSTRAINT_LAYER_LIST, context
        )
        lineLayerList = self.parameterAsLayerList(
            parameters, self.LINE_CONSTRAINT_LAYER_LIST, context
        )
        polygonLayerList = self.parameterAsLayerList(
            parameters, self.POLYGON_CONSTRAINT_LAYER_LIST, context
        )
        groupBySpatialPartition = self.parameterAsBool(
            parameters, self.GROUP_BY_SPATIAL_PARTITION, context
        )
        method = self.parameterAsEnum(parameters, self.METHOD, context)
        
        nSteps = 5 if groupBySpatialPartition else 2
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Building aux structures"))
        localCache, nodesLayer = graphHandler.buildAuxLayersPriorGraphBuilding(
            networkLayer=networkLayer,
            context=context,
            geographicBoundsLayer=geographicBoundsLayer,
            feedback=multiStepFeedback,
        )
        if not groupBySpatialPartition or (geographicBoundsLayer is not None and geographicBoundsLayer.featureCount() <= 1):
            idsToRemove = self.findIdsToRemove(nx, localCache, nodesLayer, threshold, geographicBoundsLayer, pointLayerList, lineLayerList, polygonLayerList, context, multiStepFeedback)
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            self.manageSelectedIdsUsingInputMethod(networkLayer, method, idsToRemove)
            return {}
        def compute(localGeographicBoundsLayer):
            localContext = QgsProcessingContext()
            if multiStepFeedback.isCanceled():
                return set()
            localNetworkCacheLyr = self.extractFeaturesRelatedToLayer(localCache, localGeographicBoundsLayer)
            if multiStepFeedback.isCanceled():
                return set()
            localNodesLyr = self.extractFeaturesRelatedToLayer(nodesLayer, localNetworkCacheLyr)
            if multiStepFeedback.isCanceled():
                return set()
            localPointFeatList = list(map(lambda x: self.extractFeaturesRelatedToLayer(x, localGeographicBoundsLayer), pointLayerList)) if len(pointLayerList) > 0 else []
            if multiStepFeedback.isCanceled():
                return set()
            localLineFeatList = list(map(lambda x: self.extractFeaturesRelatedToLayer(x, localGeographicBoundsLayer), lineLayerList)) if len(lineLayerList) > 0 else []
            if multiStepFeedback.isCanceled():
                return set()
            localPolygonFeatList = list(map(lambda x: self.extractFeaturesRelatedToLayer(x, localGeographicBoundsLayer), polygonLayerList)) if len(polygonLayerList) > 0 else []
            return self.findIdsToRemove(
                nx,
                localNetworkCacheLyr,
                localNodesLyr,
                threshold,
                localGeographicBoundsLayer,
                localPointFeatList,
                localLineFeatList,
                localPolygonFeatList,
                localContext,
                None
            )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Splitting geographic bounds"))
        geographicBoundaryLayerList = self.layerHandler.createMemoryLayerForEachFeature(
            layer=geographicBoundsLayer, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        nRegions = len(geographicBoundaryLayerList)
        if nRegions == 0:
            return {}
        stepSize = 100 / nRegions
        futures = set()
        idsToRemove = set()
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        multiStepFeedback.setProgressText(
            self.tr("Submitting tasks to thread...")
        )
        for current, localGeographicBoundsLayer in enumerate(
            geographicBoundaryLayerList, start=0
        ):
            if multiStepFeedback.isCanceled():
                pool.shutdown(cancel_futures=True)
                break
            futures.add(pool.submit(compute, localGeographicBoundsLayer))
            multiStepFeedback.setProgress(current * stepSize)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Evaluating results..."))
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                pool.shutdown(cancel_futures=True)
                break
            idsToRemove |= future.result()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.manageSelectedIdsUsingInputMethod(networkLayer, method, idsToRemove)
        return {}

    def manageSelectedIdsUsingInputMethod(self, networkLayer, method, idsToRemove):
        if method != 0:
            networkLayer.selectByIds(list(idsToRemove), self.selectionIdDict[method])
            return {}
        networkLayer.startEditing()
        networkLayer.beginEditCommand(self.tr("Deleting features"))
        networkLayer.deleteFeatures(list(idsToRemove))
        networkLayer.endEditCommand()
        return {}

    def findIdsToRemove(self, nx, localCache, nodesLayer, threshold, geographicBoundsLayer, pointLayerList, lineLayerList, polygonLayerList, context, feedback=None):
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback) if feedback is not None else None
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Building graph aux structures"))
        (
            nodeDict,
            nodeIdDict,
            edgeDict,
            hashDict,
            networkBidirectionalGraph,
            nodeLayerIdDict,
        ) = graphHandler.buildAuxStructures(
            nx,
            nodesLayer=nodesLayer,
            edgesLayer=localCache,
            feedback=multiStepFeedback,
            useWkt=False,
            computeNodeLayerIdDict=True,
            addEdgeLength=True,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Getting constraint points"))
        constraintSet = self.getConstraintSet(
            nodeDict=nodeDict,
            nodesLayer=nodesLayer,
            nodeLayerIdDict=nodeLayerIdDict,
            geographicBoundsLayer=geographicBoundsLayer,
            pointLayerList=pointLayerList,
            lineLayerList=lineLayerList,
            polygonLayerList=polygonLayerList,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Applying algorithm heurisic"))
        G_out = graphHandler.generalize_edges_according_to_degrees(
            G=networkBidirectionalGraph,
            constraintSet=constraintSet,
            threshold=threshold,
            feedback=multiStepFeedback
        )
        idsToRemove = set(networkBidirectionalGraph[a][b]["featid"] for a, b in networkBidirectionalGraph.edges) - set(G_out[a][b]["featid"] for a, b in G_out.edges)
        return idsToRemove
    
    def getConstraintSet(
        self,
        nodeDict: Dict[QByteArray, int],
        nodesLayer: QgsVectorLayer,
        nodeLayerIdDict: Dict[int, Dict[int, QByteArray]],
        geographicBoundsLayer: QgsVectorLayer,
        pointLayerList = List[QgsVectorLayer],
        lineLayerList = List[QgsVectorLayer],
        polygonLayerList = List[QgsVectorLayer],
        context: Optional[QgsProcessingContext] = None,
        feedback: Optional[QgsFeedback] = None,
    ) -> Set[int]:
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback) if feedback is not None else None
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        (fixedInNodeSet, fixedOutNodeSet) = graphHandler.getInAndOutNodesOnGeographicBounds(
            nodeDict=nodeDict,
            nodesLayer=nodesLayer,
            geographicBoundsLayer=geographicBoundsLayer,
            context=context,
            feedback=feedback,
        ) if geographicBoundsLayer is not None else (set(), set())
        currentStep += 1 

        constraintPointSet = fixedInNodeSet | fixedOutNodeSet

        computeLambda = lambda x: graphHandler.find_constraint_points(
            nodesLayer=nodesLayer,
            constraintLayer=x,
            nodeDict=nodeDict,
            nodeLayerIdDict=nodeLayerIdDict,
            useBuffer=False,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        constraintPointSetFromLambda = set(i for i in chain.from_iterable(map(computeLambda, pointLayerList + lineLayerList + polygonLayerList)))
        constraintPointSet |= constraintPointSetFromLambda
        return constraintPointSet
    
    def extractFeaturesRelatedToLayer(
        self, inputLyr, referenceLyr, context=None, feedback=None
    ):
        context = QgsProcessingContext() if context is None else context
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
        extractedLyr = self.algRunner.runExtractByLocation(
            inputLyr=inputLyr,
            intersectLyr=referenceLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=extractedLyr, context=context, feedback=multiStepFeedback, is_child_algorithm=True
        )
        return extractedLyr

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "generalizenetworkedgeswithlengthalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Generalize Network Edges With Length Algorithm")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Generalization Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate(
            "GeneralizeNetworkEdgesWithLengthAlgorithm", string
        )

    def createInstance(self):
        return GeneralizeNetworkEdgesWithLengthAlgorithm()
