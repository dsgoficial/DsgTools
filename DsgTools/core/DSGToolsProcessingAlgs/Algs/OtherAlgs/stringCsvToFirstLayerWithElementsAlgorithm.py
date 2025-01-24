# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-07-19
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

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterString,
    QgsProcessingUtils,
)


class StringCsvToFirstLayerWithElementsAlgorithm(QgsProcessingAlgorithm):
    INPUTLAYERS = "INPUTLAYERS"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterString(
                self.INPUTLAYERS, self.tr("Comma separated Input Layer Names")
            )
        )

        self.addOutput(
            QgsProcessingOutputVectorLayer(self.OUTPUT, self.tr("Loaded layer"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerCsv = self.parameterAsString(parameters, self.INPUTLAYERS, context)
        layerNameList = layerCsv.split(",")
        nSteps = len(layerNameList)
        if not nSteps:
            return {self.OUTPUT: None}
        progressStep = 100 / nSteps
        for idx, layerName in enumerate(layerNameList):
            if feedback.isCanceled():
                break
            lyr = QgsProcessingUtils.mapLayerFromString(layerName, context)
            if lyr is None:
                continue
            if lyr.featureCount() > 0:
                feedback.setProgress(100)
                return {"OUTPUT": lyr}
            feedback.setProgress(idx * progressStep)
        if nSteps == 1:
            lyr = QgsProcessingUtils.mapLayerFromString(layerName, context)
            return {"OUTPUT": lyr}

        return {"OUTPUT": None}  # case where no layer from input has elements

    def name(self):
        """
        Here is where the processing itself takes place.
        """
        return "stringcsvtofirstlayerwithelementsalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("String CSV to First Layer With Elements")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Model Helpers")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Model Helpers"

    def tr(self, string):
        return QCoreApplication.translate(
            "StringCsvToFirstLayerWithElementsAlgorithm", string
        )

    def createInstance(self):
        return StringCsvToFirstLayerWithElementsAlgorithm()
