# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-12-18
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from qgis.PyQt.QtCore import QSettings
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterNumber,
)

from DsgTools.core.DSGToolsProcessingAlgs.Algs.EnvironmentSetterAlgs.dsgtoolsBaseSetParametersAlgorithm import \
    DsgToolsBaseSetParametersAlgorithm


class SetFreeHandToolParametersAlgorithm(DsgToolsBaseSetParametersAlgorithm):
    FREE_HAND_TOLERANCE = "FREE_HAND_TOLERANCE"
    FREE_HAND_SMOOTH_ITERATIONS = "FREE_HAND_SMOOTH_ITERATIONS"
    FREE_HAND_SMOOTH_OFFSET = "FREE_HAND_SMOOTH_OFFSET"
    ALG_ITERATIONS = "ALG_ITERATIONS"
    UNDO_POINTS = "UNDO_POINTS"
    FREE_HAND_FINAL_SIMPLIFY_TOLERANCE = "FREE_HAND_FINAL_SIMPLIFY_TOLERANCE"

    QSETTINGS_DICT = {
        "FREE_HAND_TOLERANCE": "freeHandTolerance",
        "FREE_HAND_SMOOTH_ITERATIONS": "freeHandSmoothIterations",
        "FREE_HAND_SMOOTH_OFFSET": "freeHandSmoothOffset",
        "ALG_ITERATIONS": "algIterations",
        "UNDO_POINTS": "undoPoints",
        "FREE_HAND_FINAL_SIMPLIFY_TOLERANCE": "freeHandFinalSimplifyTolerance",
    }

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterNumber(
                self.FREE_HAND_TOLERANCE,
                self.tr("Free hand tolerance"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=2,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.FREE_HAND_SMOOTH_ITERATIONS,
                self.tr("Free hand smooth iterations"),
                minValue=0,
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=3,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.FREE_HAND_SMOOTH_OFFSET,
                self.tr("Free hand smooth offset"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.25,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ALG_ITERATIONS,
                self.tr("Free hand algorithm iterations"),
                minValue=0,
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=2,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.UNDO_POINTS,
                self.tr("Number of points removed on undo action"),
                minValue=0,
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=50,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.FREE_HAND_FINAL_SIMPLIFY_TOLERANCE,
                self.tr("Free hand tolerance"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=1,
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
        return "setfreehandtoolparametersalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Set Free Hand Tool Parameters")

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
        return QCoreApplication.translate("SetFreeHandToolParametersAlgorithm", string)

    def createInstance(self):
        return SetFreeHandToolParametersAlgorithm()
