# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-07-27
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Matheus Alves Silva - Cartographic Engineer @ Brazilian Army
        email                : matheus.alvessilva@eb.mil.br
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
from qgis.core import QgsProcessingParameterNumber

from DsgTools.core.DSGToolsProcessingAlgs.Algs.EnvironmentSetterAlgs.dsgtoolsBaseSetParametersAlgorithm import (
    DsgToolsBaseSetParametersAlgorithm,
)


class SmoothLinesToolParametersAlgorithm(DsgToolsBaseSetParametersAlgorithm):
    NUMBER_SMOOTHING_ITERATIONS = "NUMBER_SMOOTHING_ITERATIONS"
    FRACTION_LINE_CREATE_NEW_VERTICES = "FRACTION_LINE_CREATE_NEW_VERTICES"

    QSETTINGS_DICT = {
        "NUMBER_SMOOTHING_ITERATIONS": "numberSmoothingIterations",
        "FRACTION_LINE_CREATE_NEW_VERTICES": "fractionLineCreateNewVertices",
    }

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterNumber(
                self.NUMBER_SMOOTHING_ITERATIONS,
                self.tr("Smoothing Iterations"),
                minValue=0,
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=2,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.FRACTION_LINE_CREATE_NEW_VERTICES,
                self.tr("Fraction of line to create new vertices"),
                minValue=0,
                maxValue=1,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.30,
            )
        )

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "smoothlinestoolparametersalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Smooth Lines Tool Parameters")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Environment Setters")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Environment Setters"

    def tr(self, string):
        return QCoreApplication.translate("SmoothLinesToolParametersAlgorithm", string)

    def createInstance(self):
        return SmoothLinesToolParametersAlgorithm()