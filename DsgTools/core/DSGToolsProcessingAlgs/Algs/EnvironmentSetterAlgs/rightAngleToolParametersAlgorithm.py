# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-07-27
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
from PyQt5.QtCore import QCoreApplication
from qgis.core import QgsProcessingParameterNumber

from DsgTools.core.DSGToolsProcessingAlgs.Algs.EnvironmentSetterAlgs.dsgtoolsBaseSetParametersAlgorithm import \
    DsgToolsBaseSetParametersAlgorithm


class RightAngleToolParametersAlgorithm(DsgToolsBaseSetParametersAlgorithm):
    MIN_SEGMENT_DISTANCE = "MIN_SEGMENT_DISTANCE"
    RIGHT_ANGLE_DECIMALS = "RIGHT_ANGLE_DECIMALS"

    QSETTINGS_DICT = {
        "MIN_SEGMENT_DISTANCE": "minSegmentDistance",
        "RIGHT_ANGLE_DECIMALS": "rightAngleDecimals",
    }

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_SEGMENT_DISTANCE,
                self.tr("Minimum Segment Distance"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=2,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.RIGHT_ANGLE_DECIMALS,
                self.tr("Number of decimal points"),
                minValue=0,
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=3,
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
        return "rightangletoolparametersalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Right Angle Tool Parameters")

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
        return "DSGTools: Environment Setters"

    def tr(self, string):
        return QCoreApplication.translate("RightAngleToolParametersAlgorithm", string)

    def createInstance(self):
        return RightAngleToolParametersAlgorithm()
