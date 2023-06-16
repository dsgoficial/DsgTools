# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-11
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import os

import processing
from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsField,
    QgsFields,
    QgsProcessing,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
)
from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.utils import iface

from .validationAlgorithm import ValidationAlgorithm


class IdentifyCountourStreamIntersectionAlgorithm(ValidationAlgorithm):

    INPUT_STREAM = "INPUT_STREAM"
    INPUT_CONTOUR_LINES = "INPUT_CONTOUR_LINES"
    POINT_FLAGS = "POINT_FLAGS"
    LINE_FLAGS = "LINE_FLAGS"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "INPUT_STREAM",
                self.tr("Drainage layer"),
                types=[QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "INPUT_COUNTOUR_LINES",
                self.tr("Contour levels layer"),
                types=[QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.POINT_FLAGS, self.tr("Point Flags"))
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.LINE_FLAGS, self.tr("Line Flags"))
        )

    def processAlgorithm(self, parameters, context, feedback):

        streamLayerInput = self.parameterAsVectorLayer(
            parameters, "INPUT_STREAM", context
        )

        outputLinesSet, outputPointsSet = set(), set()
        countourLayer = self.parameterAsVectorLayer(
            parameters, "INPUT_COUNTOUR_LINES", context
        )

        (point_flag_sink, point_flag_sink_id) = self.parameterAsSink(
            parameters,
            self.POINT_FLAGS,
            context,
            streamLayerInput.fields(),
            QgsWkbTypes.Point,
            streamLayerInput.sourceCrs(),
        )

        (line_flag_sink, line_flag_sink_id) = self.parameterAsSink(
            parameters,
            self.LINE_FLAGS,
            context,
            streamLayerInput.fields(),
            QgsWkbTypes.LineString,
            streamLayerInput.sourceCrs(),
        )

        feedback.setProgressText(self.tr("Verifying inconsistency"))

        multiStepFeedback = QgsProcessingMultiStepFeedback(7, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Building intermediary structures"))

        auxStreamLayerInput = self.runAddCount(
            streamLayerInput, feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(1)
        self.runCreateSpatialIndex(auxStreamLayerInput, feedback=multiStepFeedback)

        multiStepFeedback.setCurrentStep(2)
        auxCountourLayer = self.runAddCount(countourLayer, feedback=multiStepFeedback)
        multiStepFeedback.setCurrentStep(3)
        self.runCreateSpatialIndex(auxCountourLayer, feedback=multiStepFeedback)
        multiStepFeedback.setCurrentStep(4)
        idDict = {feat["AUTO"]: feat for feat in auxCountourLayer.getFeatures()}

        multiStepFeedback.setCurrentStep(5)
        multiStepFeedback.pushInfo(self.tr("Doing spatial join"))
        spatialJoinOutput = self.runSpatialJoin(
            auxStreamLayerInput, auxCountourLayer, feedback=multiStepFeedback
        )

        multiStepFeedback.setCurrentStep(6)
        multiStepFeedback.pushInfo(self.tr("Finding flags"))

        self.findProblems(
            multiStepFeedback,
            outputPointsSet,
            outputLinesSet,
            spatialJoinOutput,
            idDict,
        )

        if outputPointsSet != set():
            self.outLayer(
                parameters, context, outputPointsSet, streamLayerInput, QgsWkbTypes.Point, point_flag_sink, 
            )
        if outputLinesSet != set():
            self.outLayer(
                parameters, context, outputLinesSet, streamLayerInput, QgsWkbTypes.LineString, line_flag_sink,
            )
        return {
            self.POINT_FLAGS: point_flag_sink_id,
            self.LINE_FLAGS: line_flag_sink_id,
        }

    def runSpatialJoin(self, streamLayerInput, countourLayer, feedback):
        output = processing.run(
            "native:joinattributesbylocation",
            {
                "INPUT": streamLayerInput,
                "JOIN": countourLayer,
                "PREDICATE": [0],
                "JOIN_FIELDS": [],
                "METHOD": 0,
                "DISCARD_NONMATCHING": True,
                "PREFIX": "",
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
            feedback=feedback,
        )
        return output["OUTPUT"]

    def runAddCount(self, inputLyr, feedback):
        output = processing.run(
            "native:addautoincrementalfield",
            {
                "INPUT": inputLyr,
                "FIELD_NAME": "AUTO",
                "START": 0,
                "GROUP_FIELDS": [],
                "SORT_EXPRESSION": "",
                "SORT_ASCENDING": False,
                "SORT_NULLS_FIRST": False,
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
            feedback=feedback,
        )
        return output["OUTPUT"]

    def runCreateSpatialIndex(self, inputLyr, feedback):
        processing.run(
            "native:createspatialindex", {"INPUT": inputLyr}, feedback=feedback
        )

    def findProblems(self, feedback, outputPointsSet, outputLinesSet, inputLyr, idDict):
        total = 100.0 / inputLyr.featureCount() if inputLyr.featureCount() else 0

        def buildOutputs(riverFeat, feedback):
            if feedback.isCanceled():
                return
            riverGeom = riverFeat.geometry()
            if riverFeat["AUTO_2"] not in idDict:
                return
            countourGeom = idDict[riverFeat["AUTO_2"]].geometry()
            intersection = countourGeom.intersection(riverGeom)
            if intersection.isEmpty() or intersection.wkbType() == QgsWkbTypes.Point:
                return
            if intersection.wkbType() == QgsWkbTypes.MultiPoint:
                outputPointsSet.add(intersection)
            if intersection.wkbType() in [QgsWkbTypes.LineString, QgsWkbTypes.MultiLineString]:
                outputLinesSet.add(intersection)

        buildOutputsLambda = lambda x: buildOutputs(x, feedback)

        pool = concurrent.futures.ThreadPoolExecutor(os.cpu_count())
        futures = set()
        current_idx = 0

        for feat in inputLyr.getFeatures():
            if feedback is not None and feedback.isCanceled():
                break
            futures.add(pool.submit(buildOutputsLambda, feat))

        for x in concurrent.futures.as_completed(futures):
            if feedback is not None and feedback.isCanceled():
                break
            feedback.setProgress(current_idx * total)
            current_idx += 1

    def outLayer(self, parameters, context, geometry, streamLayer, geomtype, sink):
        newFields = QgsFields()
        newFields.append(QgsField("id", QVariant.Int))

        for idcounter, geom in enumerate(geometry):
            newFeat = QgsFeature()
            newFeat.setGeometry(geom)
            newFeat.setFields(newFields)
            newFeat["id"] = idcounter
            sink.addFeature(newFeat, QgsFeatureSink.FastInsert)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifycountourstreamintersection"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(
            "Identifies intersections between contour lines and drainage lines"
        )

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Identification Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Identification Processes)"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifyCountourStreamIntersectionAlgorithm", string
        )

    def createInstance(self):
        return IdentifyCountourStreamIntersectionAlgorithm()
