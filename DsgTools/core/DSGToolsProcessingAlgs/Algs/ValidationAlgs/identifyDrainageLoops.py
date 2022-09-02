# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-08-26
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import os
import concurrent.futures
from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing, QgsProcessingException,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource, QgsGeometry,
                       QgsWkbTypes, QgsPoint)

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler

from .validationAlgorithm import ValidationAlgorithm


class IdentifyDrainageLoops(ValidationAlgorithm):
    INPUT = 'INPUT'
    BUILD_CACHE = 'BUILD_CACHE'
    FLAGS = 'FLAGS'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input'),
                [
                    QgsProcessing.TypeVectorLine,
                ]
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.BUILD_CACHE,
                self.tr('Build local cache of the input layer')
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr('{0} Flags').format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        try:
            import networkx as nx
        except ImportError:
            raise QgsProcessingException(
                self.tr('This algorithm requires the Python networkx library. Please install this library and try again.')
            )
        algRunner = AlgRunner()
        geometryHandler = GeometryHandler()

        inputLyr = self.parameterAsVectorLayer(
            parameters,
            'INPUT',
            context
        )
        buildCache = self.parameterAsBool(
            parameters, self.BUILD_CACHE, context
        )
        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.LineString, context)

        # Iterate over lines setting the dictionary counters:
        nSteps = 6 if buildCache else 4
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        if buildCache:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Building input cache..."))
            inputLyr = algRunner.runAddAutoIncrementalField(
                inputLyr=inputLyr, context=context, feedback=multiStepFeedback
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            algRunner.runCreateSpatialIndex(
                inputLyr=inputLyr, context=context, feedback=multiStepFeedback
            )
            currentStep += 1
        
        multiStepFeedback.setProgressText(self.tr("Building loop area candidates..."))
        multiStepFeedback.setCurrentStep(currentStep)
        polygonLyr = algRunner.runPolygonize(
            inputLyr=inputLyr, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        
        multiStepFeedback.setCurrentStep(currentStep)
        mergedPolygons = algRunner.runDissolve(
            inputLyr=polygonLyr, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        
        multiStepFeedback.setCurrentStep(currentStep)
        polygonLoops = algRunner.runMultipartToSingleParts(
            inputLayer=mergedPolygons, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        polygonCount = polygonLoops.featureCount()
        if polygonCount == 0:
            multiStepFeedback.setProgressText(self.tr("Building loop area candidates..."))
            return {self.FLAGS: self.flag_id}

        multiStepFeedback.setCurrentStep(currentStep)
        self.searchLoops(nx, geometryHandler, inputLyr, multiStepFeedback, polygonLoops, polygonCount)

        return {self.FLAGS: self.flag_id}

    def searchLoops(self, nx, geometryHandler, inputLyr, feedback, polygonLoops, polygonCount):
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        stepSize = 100 / polygonCount
        flagFeatLambda = lambda x: self.flagFeature(
            flagGeom=x, flagText=self.tr('Loop on input drainages')
        )
        firstAndLastNode = lambda x: geometryHandler.getFirstAndLastNode(
            inputLyr, x
        )
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(self.tr('Submitting tasks to thread'))
        def evaluate(polygonFeature):
            geom = polygonFeature.geometry()
            geomEngine = QgsGeometry.createGeometryEngine(geom.constGet())
            graph = nx.DiGraph()
            for i, feat in enumerate(inputLyr.getFeatures()):
                if not geomEngine.intersects(feat.geometry().constGet()):
                    continue
                p0, pn = firstAndLastNode(feat)
                p0 = QgsGeometry.fromPointXY(p0)
                pn = QgsGeometry.fromPointXY(pn)
                if not geomEngine.intersects(p0.constGet()) or not geomEngine.intersects(pn.constGet()):
                    continue
                vertexList = list(feat.geometry().vertices())
                for v1, v2 in zip(vertexList, vertexList[1:]):
                    graph.add_edge(v1.asWkt(), v2.asWkt())
            loopSet = self.findLoopsOnEdgeSet(nx, graph, feedback=multiStepFeedback)
            return loopSet
        pool = concurrent.futures.ThreadPoolExecutor(os.cpu_count()-1)
        futures = set()
        for current, polygonFeature in enumerate(polygonLoops.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            futures.add(pool.submit(evaluate, polygonFeature))
            multiStepFeedback.setCurrentStep(current * stepSize)

        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.setProgressText(self.tr('Evaluating results'))
        
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                break
            loopSet = future.result()
            if loopSet != set():
                list(map(flagFeatLambda, loopSet))
            multiStepFeedback.setCurrentStep(current * stepSize)

    def findLoopsOnEdgeSet(self, nx, graph, feedback):
        # loops = nx.strongly_connected_components(graph)
        loops = nx.simple_cycles(graph)
        # loops = nx.kosaraju_strongly_connected_components(graph)
        loopSet = set()
        for loop in loops:
            if feedback.isCanceled():
                return loopSet
            initialNode, *nodeList = loop
            if nodeList == []:
                continue
            pointFromWkt = lambda x: QgsPoint(QgsGeometry.fromWkt(x).asPoint())
            loopGeom = QgsGeometry.fromPolyline(
                [pointFromWkt(initialNode)] + 
                list(map(pointFromWkt, nodeList)) + 
                [pointFromWkt(initialNode)]
            )
            loopSet.add(loopGeom)
        return loopSet
            
        

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifydrainageloops'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Drainage Loops')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Quality Assurance Tools (Identification Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return self.tr('DSGTools: Quality Assurance Tools (Identification Processes)')

    def tr(self, string):
        return QCoreApplication.translate('IdentifyDrainageLoops', string)

    def createInstance(self):
        return IdentifyDrainageLoops()
