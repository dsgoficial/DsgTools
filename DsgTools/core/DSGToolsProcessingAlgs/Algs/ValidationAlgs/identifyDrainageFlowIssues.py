# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-07-28
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Sereno, Alves Silva, Samuel, Ferreira - Cartographic Engineers @ Brazilian Army
        email                : mateus.sereno@ime.eb.br - matheus.silva@ime.eb.br - samuel.melo@ime.eb.br - matheus.ferreira@ime.eb.br
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
from ..Help.algorithmHelpCreator import HTMLHelpCreator as help


class IdentifyDrainageFlowIssues(ValidationAlgorithm):
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

        # Dictionary that indicates how many lines enter and how many lines exit a given point:
        pointInAndOutDictionary = {}

        # Iterate over lines setting the dictionary counters:
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
            last_vertex = geom[-1]

            if first_vertex.asWkt() not in pointInAndOutDictionary:
                pointInAndOutDictionary[first_vertex.asWkt()] = {
                    "incoming": 0,
                    "outgoing": 0,
                }

            if last_vertex.asWkt() not in pointInAndOutDictionary:
                pointInAndOutDictionary[last_vertex.asWkt()] = {
                    "incoming": 0,
                    "outgoing": 0,
                }

            pointInAndOutDictionary[first_vertex.asWkt()]["outgoing"] += 1
            pointInAndOutDictionary[last_vertex.asWkt()]["incoming"] += 1
            multiStepFeedback.setProgress(current * stepSize)

        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.setProgressText(self.tr("Raising flags..."))
        stepSize = 100 / len(pointInAndOutDictionary)
        # Iterate over dictionary:
        for current, (pointStr, inAndOutCounters) in enumerate(
            pointInAndOutDictionary.items()
        ):
            if multiStepFeedback.isCanceled():
                break
            errorMsg = self.errorWhenCheckingInAndOut(inAndOutCounters)
            if errorMsg != "":
                self.flagFeature(
                    flagGeom=QgsGeometry.fromWkt(pointStr), flagText=self.tr(errorMsg)
                )
            multiStepFeedback.setProgress(current * stepSize)

        return {self.FLAGS: self.flag_id}

    def errorWhenCheckingInAndOut(self, inAndOutCounters):
        incoming = inAndOutCounters["incoming"]
        outgoing = inAndOutCounters["outgoing"]
        total = incoming + outgoing

        if total == 1:
            return ""
        if total >= 4:
            return "4 or more lines conected to this point."

        if incoming == 0:
            return "There are lines coming from this point, but not lines going in."

        if outgoing == 0:
            return (
                "There are lines going into this point, but not lines coming from it."
            )

        return ""

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifydrainageflowissues"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Drainage Flow Issues")

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
        return QCoreApplication.translate("IdentifyDrainageFlowIssues", string)

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    def helpUrl(self):
        return  help().helpUrl(self.name())

    def createInstance(self):
        return IdentifyDrainageFlowIssues()
