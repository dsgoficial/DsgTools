# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-03-29
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

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSink,
    QgsFeature,
    QgsField,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSource,
)
from DsgTools.core.GeometricTools import graphHandler


class StreamOrder(QgsProcessingAlgorithm):

    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Input network"),
                [QgsProcessing.TypeVectorLine],
                optional=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Output"))
        )

    def processAlgorithm(self, parameters, context, feedback):

        try:
            import networkx as nx
        except ImportError:
            raise QgsProcessingException(
                self.tr(
                    "This algorithm requires the Python networkx library. Please install this library and try again."
                )
            )
        algRunner = AlgRunner()
        networkLayer = self.parameterAsSource(parameters, self.INPUT, context)
        fields = networkLayer.fields()
        fields.append(QgsField("stream_order", QVariant.Int))
        (sink, sink_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            networkLayer.wkbType(),
            networkLayer.sourceCrs(),
        )
        multiStepFeedback = QgsProcessingMultiStepFeedback(6, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        localCache = algRunner.runCreateFieldWithExpression(
            inputLyr=parameters[self.INPUT],
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            inputLyr=localCache, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        nodesLayer = algRunner.runExtractSpecificVertices(
            inputLyr=localCache,
            vertices="0,-1",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        (
            nodeDict,
            nodeIdDict,
            edgeDict,
            hashDict,
            networkBidirectionalGraph,
        ) = graphHandler.buildAuxStructures(
            nx,
            nodesLayer=nodesLayer,
            edgesLayer=localCache,
            feedback=multiStepFeedback,
            directed=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        G_copy = graphHandler.evaluateStreamOrder(
            networkBidirectionalGraph, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        if len(G_copy.edges) == 0:
            return {self.OUTPUT: sink_id}
        stepSize = 100 / len(G_copy.edges)
        for current, (n0, n1) in enumerate(G_copy.edges):
            if multiStepFeedback.isCanceled():
                break
            newFeat = QgsFeature(fields)
            oldFeat = edgeDict[G_copy[n0][n1]["featid"]]
            newFeat.setGeometry(oldFeat.geometry())
            for idx, attrValue in enumerate(oldFeat.attributes()):
                newFeat.setAttribute(idx, attrValue)
            newFeat["stream_order"] = G_copy[n0][n1]["stream_order"]

            sink.addFeature(newFeat)
            multiStepFeedback.setProgress(current * stepSize)
        return {self.OUTPUT: sink_id}

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return StreamOrder()

    def name(self):
        return "streamorder"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Stream Order")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Network Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Network Processes)"

    def shortHelpString(self):
        return self.tr(
            "O algoritmo orderna ou direciona fluxo, como linhas de drenagem "
        )
