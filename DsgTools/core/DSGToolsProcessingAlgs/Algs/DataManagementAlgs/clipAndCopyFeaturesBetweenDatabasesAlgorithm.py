# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-08-01
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

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsWkbTypes,
    QgsVectorLayerUtils,
    QgsProcessingException,
    QgsProcessingParameterProviderConnection,
    QgsProcessingAlgorithm,
    QgsProcessingParameterGeometry,
)


class ClipAndCopyFeaturesBetweenDatabasesAlgorithm(QgsProcessingAlgorithm):
    ORIGIN_DATABASE = "DESTINATION_LAYER"
    DESTINATION_DATABASE = "DESTINATION_DATABASE"
    WKT_POLYGON = "LAYER_WITH_FEATURES_TO_APPEND"

    def flags(self):
        return (
            super().flags()
            | QgsProcessingAlgorithm.FlagNotAvailableInStandaloneTool
            | QgsProcessingAlgorithm.FlagRequiresProject
        )

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        origin_db_param = QgsProcessingParameterProviderConnection(
            self.ORIGIN_DATABASE,
            self.tr("Origin Database (connection name)"),
            "postgres",
        )
        self.addParameter(origin_db_param)

        destination_db_param = QgsProcessingParameterProviderConnection(
            self.DESTINATION_DATABASE,
            self.tr("Destination Database (connection name)"),
            "postgres",
        )
        self.addParameter(destination_db_param)
        self.addParameter(
            QgsProcessingParameterGeometry(
                self.WKT_POLYGON,
                self.tr("WKT Geographic Bounds"),
                geometryTypes=[QgsWkbTypes.PolygonGeometry],
                allowMultipart=True,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        geom = self.parameterAsGeometry(parameters, self.WKT_POLYGON)
        feedback.pushInfo(geom)
        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "clipandcopyfeaturesbetweendatabasesalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Append Features to Layer")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Data Management Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Data Management Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("AppendFeaturesToLayerAlgorithm", string)

    def createInstance(self):
        return ClipAndCopyFeaturesBetweenDatabasesAlgorithm()
