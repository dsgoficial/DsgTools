# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-05-01
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Jossan
        email                :
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
from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSink,
    QgsFeature,
    QgsProcessingParameterFeatureSource,
    QgsGeometry,
    QgsLineString,
    QgsProcessingMultiStepFeedback,
    QgsWkbTypes,
    QgsFields,
    QgsField,
    QgsMultiLineString,
)

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class Line2Multiline(QgsProcessingAlgorithm):

    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT, self.tr("Select line layer"), [QgsProcessing.TypeVectorLine]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Output"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        self.algRunner = AlgRunner()
        lines = self.parameterAsSource(parameters, self.INPUT, context)

        fields = QgsFields()
        fields.append(QgsField("length", QVariant.String))
        (sink_l, sinkId_l) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.MultiLineString,
            lines.sourceCrs(),
        )
        multiStepFeedback = QgsProcessingMultiStepFeedback(6, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)

        lines = self.algRunner.runAddAutoIncrementalField(
            inputLyr=parameters[self.INPUT],
            context=context,
            feedback=multiStepFeedback,
            fieldName="AUTO",
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=lines,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        spatialJoinOutput = self.algRunner.runJoinAttributesByLocation(
            inputLyr=lines,
            joinLyr=lines,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        self.populateAuxStructure(lines, feedback=multiStepFeedback)
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        self.buildMatchingFeaturesDict(spatialJoinOutput, feedback=multiStepFeedback)
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        self.processFeatures(fields, sink_l, feedback=multiStepFeedback)

        return {self.OUTPUT: sinkId_l}

    def processFeatures(self, fields, sink_l, feedback):
        nFeats = len(self.ids_in_stack)
        if nFeats == 0:
            return
        stepSize = 100 / nFeats
        current = 0
        while len(self.ids_in_stack) > 0:
            if feedback.isCanceled():
                break
            currentid = self.ids_in_stack.pop()
            current = nFeats - len(self.ids_in_stack)

            mls_array = self.aggregate(currentid, feedback=feedback)

            mls = QgsMultiLineString()
            for el in mls_array:
                mls.addGeometry(QgsLineString(list(el.vertices())))
            self.addSink(QgsGeometry(mls), sink_l, fields)
            feedback.setProgress(current * stepSize)

    def buildMatchingFeaturesDict(self, spatialJoinOutput, feedback):
        self.matching_features = defaultdict(list)
        nFeats = spatialJoinOutput.featureCount()
        if nFeats == 0:
            return
        stepSize = 100 / nFeats
        for current, feat in enumerate(spatialJoinOutput.getFeatures()):
            if feedback.isCanceled():
                break
            if feat["AUTO"] == feat["AUTO_2"]:
                continue
            self.matching_features[feat["AUTO"]].append(feat["AUTO_2"])
            feedback.setProgress(current * stepSize)

    def populateAuxStructure(self, lines, feedback):
        self.id_to_feature = {}
        self.ids_in_stack = set()
        nFeats = lines.featureCount()
        if nFeats == 0:
            return
        stepSize = 100 / nFeats
        for current, currentFeature in enumerate(lines.getFeatures()):
            if feedback.isCanceled():
                break
            self.id_to_feature[currentFeature["AUTO"]] = currentFeature
            self.ids_in_stack.add(currentFeature["AUTO"])
            feedback.setCurrentStep(current * stepSize)

    def aggregate(self, featureId, feedback):
        stack = [featureId]
        mls_array = []

        while stack:
            current_id = stack.pop()
            currentfeature = self.id_to_feature[current_id]
            currentgeom = currentfeature.geometry()
            mls_array.append(currentgeom)

            if feedback.isCanceled():
                return mls_array

            matching_features_ids = set(
                el for el in self.matching_features[current_id] if el in self.ids_in_stack
            )

            self.ids_in_stack = self.ids_in_stack - matching_features_ids

            stack.extend(matching_features_ids)

        return mls_array

    def addSink(self, geom, sink, fields):
        newFeat = QgsFeature(fields)
        newFeat.setGeometry(geom)
        newFeat["length"] = geom.length()
        sink.addFeature(newFeat, QgsFeatureSink.FastInsert)

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return Line2Multiline()

    def name(self):
        return "line2multiline"

    def displayName(self):
        return self.tr("Convert Line to Multiline")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Geometric Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Geometric Algorithms"

    def shortHelpString(self):
        return self.tr("O algoritmo converte linhas que se tocam para multilinha")
