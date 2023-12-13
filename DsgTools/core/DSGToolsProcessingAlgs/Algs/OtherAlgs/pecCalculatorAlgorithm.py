# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-05-31
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
                                           Emerson Xavier - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
                               emerson.xavier@eb.mil.br
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
import functools
from ...algRunner import AlgRunner
import processing
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsFeature,
    QgsDataSourceUri,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingUtils,
    QgsSpatialIndex,
    QgsGeometry,
    QgsProcessingParameterField,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFile,
    QgsProcessingParameterExpression,
    QgsProcessingException,
    QgsFeatureRequest,
    QgsRectangle,
)


class PecCalculatorAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    REFERENCE = "REFERENCE"
    TOLERANCE = "TOLERANCE"
    # OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT, self.tr("Input layer"), [QgsProcessing.TypeVectorPoint]
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.REFERENCE,
                self.tr("Reference layer"),
                [QgsProcessing.TypeVectorPoint],
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE,
                self.tr("Max distance"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=2,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        referenceLyr = self.parameterAsVectorLayer(parameters, self.REFERENCE, context)
        tol = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        distanceDict = dict()
        featList = [i for i in inputLyr.getFeatures()]
        step = 100 / len(featList) if featList else 0
        for current, feat in enumerate(featList):
            if feedback.isCanceled():
                break
            if not feat.geometry().isGeosValid():
                continue
            id = feat.id()
            geom = feat.geometry().asGeometryCollection()[0].asPoint()
            x = geom.x()
            y = geom.y()
            bbox = QgsRectangle(x - tol, y - tol, x + tol, y + tol)
            request = QgsFeatureRequest()
            request.setFilterRect(bbox)
            minDistance = 0
            candidateId = None
            for candidateFeat in referenceLyr.getFeatures(request):
                dist = feat.geometry().distance(candidateFeat.geometry())
                if candidateId is None:
                    minDistance = dist
                    candidateId = candidateFeat.id()
                    continue
                elif dist < minDistance:
                    minDistance = dist
                    candidateId = candidateFeat.id()
            if candidateId is not None:
                distanceDict[id] = {
                    "minDistance": minDistance,
                    "candidateId": candidateId,
                }
            feedback.setProgress(current * step)

        distanceList = [i["minDistance"] for i in distanceDict.values()]
        n = len(distanceList)
        distanceSquared = [i["minDistance"] ** 2 for i in distanceDict.values()]
        rms = math.sqrt(sum(distanceSquared) / n)
        percFunc = functools.partial(self.percentile, frequency=0.9)
        perc = percFunc(distanceList)
        mean = sum(distanceList) / n
        feedback.pushInfo("MEAN: {mean}".format(mean=mean))
        feedback.pushInfo("RMS: {rms}".format(rms=rms))
        feedback.pushInfo("PERC: {perc}".format(perc=perc))

        return {}

    def percentile(self, N, frequency, key=lambda x: x):
        """
        Find the percentile of a list of values.

        @parameter N - is a list of values. Note N MUST BE already sorted.
        @parameter percent - a float value from 0.0 to 1.0.
        @parameter key - optional key function to compute value from each element of N.

        @return - the percentile of the values
        """
        if not N:
            return None
        sortedN = sorted(N)
        if len(sortedN) < 1:
            return 0 if not sortedN else 1
        if frequency <= 0:
            return sortedN[0]
        elif frequency >= 1:
            return sortedN[-1]
        position = frequency * (len(sortedN) - 1)

        bottom = math.floor(position)
        top = math.ceil(position)
        if top == bottom:
            return sortedN[top]
        return sortedN[bottom] * (1.0 + bottom - position) + sortedN[top] * (
            1.0 + position - top
        )

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "peccalculator"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Compute RMS and Percentile 90 of Layer")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Data Quality")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider.
        """
        return "DSGTools - Data Quality"

    def tr(self, string):
        return QCoreApplication.translate("PecCalculatorAlgorithm", string)

    def createInstance(self):
        return PecCalculatorAlgorithm()
