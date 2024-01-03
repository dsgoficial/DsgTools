# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-10-26
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
from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsField,
    QgsFields,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsWkbTypes,
    QgsProcessingParameterCrs,
    QgsRectangle,
)
from qgis.PyQt.Qt import QVariant

from ...algRunner import AlgRunner


class CreateGridFromCoordinatesAlgorithm(QgsProcessingAlgorithm):
    X_MIN = "X_MIN"
    Y_MIN = "Y_MIN"
    X_MAX = "X_MAX"
    Y_MAX = "Y_MAX"
    CRS = "CRS"
    N_TILES_X = "N_TILES_X"
    N_TILES_Y = "N_TILES_Y"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """

        self.addParameter(
            QgsProcessingParameterNumber(
                self.X_MIN,
                self.tr("Min x coordinates"),
                defaultValue=0.005,
                type=QgsProcessingParameterNumber.Double,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.Y_MIN,
                self.tr("Min y coordinates"),
                defaultValue=0.005,
                type=QgsProcessingParameterNumber.Double,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.X_MAX,
                self.tr("Max x coordinates"),
                defaultValue=0.005,
                type=QgsProcessingParameterNumber.Double,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.Y_MAX,
                self.tr("Max y coordinates"),
                defaultValue=0.005,
                type=QgsProcessingParameterNumber.Double,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.N_TILES_X,
                self.tr("Number of subdivisions on x"),
                defaultValue=2,
                minValue=0,
                type=QgsProcessingParameterNumber.Integer,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.N_TILES_Y,
                self.tr("Number of subdivisions on y"),
                defaultValue=2,
                minValue=1,
                type=QgsProcessingParameterNumber.Integer,
            )
        )

        self.addParameter(QgsProcessingParameterCrs(self.CRS, self.tr("CRS")))

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Grid"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        algRunner = AlgRunner()

        xMin = self.parameterAsDouble(parameters, self.X_MIN, context)
        yMin = self.parameterAsDouble(parameters, self.Y_MIN, context)
        xMax = self.parameterAsDouble(parameters, self.X_MAX, context)
        yMax = self.parameterAsDouble(parameters, self.Y_MAX, context)

        nTilesX = self.parameterAsDouble(parameters, self.N_TILES_X, context)
        nTilesY = self.parameterAsDouble(parameters, self.N_TILES_Y, context)

        crs = self.parameterAsCrs(parameters, self.CRS, context)
        if crs is None or not crs.isValid():
            raise QgsProcessingException(self.tr("Invalid CRS."))

        (output_sink, output_sink_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            QgsFields(),
            QgsWkbTypes.Polygon,
            crs,
        )
        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        multiStepFeedback.setCurrentStep(0)
        xGridSize = abs(xMax - xMin) / nTilesX
        yGridSize = abs(yMax - yMin) / nTilesY
        grid = algRunner.runCreateGrid(
            extent=QgsRectangle(xMin, yMin, xMax, yMax, normalize=False),
            crs=crs,
            hSpacing=xGridSize,
            vSpacing=yGridSize,
            feedback=multiStepFeedback,
            context=context,
        )
        list(
            map(
                lambda x: output_sink.addFeature(x, QgsFeatureSink.FastInsert),
                grid.getFeatures(),
            )
        )

        return {"OUTPUT": output_sink_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "creategridfromcoordinatesalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Create Grid From Coordinates")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Grid Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Grid Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("CreateGridFromCoordinatesAlgorithm", string)

    def createInstance(self):
        return CreateGridFromCoordinatesAlgorithm()
