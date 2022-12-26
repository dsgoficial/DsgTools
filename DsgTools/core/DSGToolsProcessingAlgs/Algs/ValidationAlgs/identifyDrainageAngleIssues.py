# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-09-05
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Mateus Sereno - Cartographic Engineer @ Brazilian Army
        email                : mateus.sereno@ime.eb.br
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
import concurrent.futures
import os

from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsFeature,
    QgsFeatureRequest,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsGeometryUtils,
    QgsPoint,
    QgsPointXY,
    QgsProcessing,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProject,
    QgsWkbTypes,
    QgsProcessingMultiStepFeedback,
)

from .validationAlgorithm import ValidationAlgorithm
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler


class IdentifyDrainageAngleIssues(ValidationAlgorithm):
    FLAGS = "FLAGS"
    INPUT = "INPUT"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Input"),
                [
                    QgsProcessing.TypeVectorLine,
                ],
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        lines = self.parameterAsVectorLayer(parameters, "INPUT", context)
        self.prepareFlagSink(parameters, lines, QgsWkbTypes.Point, context)

        # Dictionary that stores azimuths entering and exiting the point
        pointInAndOutDictionary = {}

        # Iterate over lines setting the dictionary content:
        lineCount = lines.featureCount()
        if lineCount == 0:
            return {self.FLAGS: self.flag_id}
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(self.tr("Evaluating line structure..."))
        stepSize = 100 / lineCount

        for current, line in enumerate(lines.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            geom = list(line.geometry().vertices())
            if len(geom) == 0:
                continue
            first_vertex = geom[0]
            second_vertex = geom[1]
            semilast_vertex = geom[-2]
            last_vertex = geom[-1]

            outgoing_azimuth = GeometryHandler.calcAzimuth(first_vertex, second_vertex)
            incoming_azimuth = GeometryHandler.calcAzimuth(semilast_vertex, last_vertex)

            if first_vertex.asWkt() not in pointInAndOutDictionary:
                pointInAndOutDictionary[first_vertex.asWkt()] = {
                    "incoming": [],
                    "outgoing": [],
                }

            if last_vertex.asWkt() not in pointInAndOutDictionary:
                pointInAndOutDictionary[last_vertex.asWkt()] = {
                    "incoming": [],
                    "outgoing": [],
                }

            pointInAndOutDictionary[first_vertex.asWkt()]["outgoing"].append(
                outgoing_azimuth
            )
            pointInAndOutDictionary[last_vertex.asWkt()]["incoming"].append(
                incoming_azimuth
            )
            multiStepFeedback.setProgress(current * stepSize)

        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.setProgressText(self.tr("Raising flags..."))
        stepSize = 100 / len(pointInAndOutDictionary)
        # Iterate over dictionary:
        for current, (pointStr, inAndOutLists) in enumerate(
            pointInAndOutDictionary.items()
        ):
            if multiStepFeedback.isCanceled():
                break
            errorMsg = self.errorWhenCheckingInAndOut(inAndOutLists)
            if errorMsg != "":
                self.flagFeature(
                    flagGeom=QgsGeometry.fromWkt(pointStr), flagText=self.tr(errorMsg)
                )
            multiStepFeedback.setProgress(current * stepSize)

        return {self.FLAGS: self.flag_id}

    def errorWhenCheckingInAndOut(self, inAndOutLists):
        azimuths_in = inAndOutLists["incoming"]
        azimuths_out = inAndOutLists["outgoing"]

        for azi_in in azimuths_in:
            for azi_out in azimuths_out:
                directionChange = self.deltaBetweenAzimuths(azi_in, azi_out)
                if directionChange > 90:
                    return "There is an unexpected sharp turn here."

        return ""

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifydrainageangleissues"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Drainage Angle Issues")

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
        return self.tr("DSGTools: Quality Assurance Tools (Identification Processes)")

    def tr(self, string):
        return QCoreApplication.translate("IdentifyDrainageAngleIssues", string)

    def createInstance(self):
        return IdentifyDrainageAngleIssues()

    @staticmethod
    def deltaBetweenAzimuths(az1: float, az2: float) -> float:
        delta_1 = az1 - az2
        delta_2 = az2 - az1

        if delta_1 < 0:
            delta_1 += 360
        if delta_2 < 0:
            delta_2 += 360

        return min(delta_1, delta_2)
