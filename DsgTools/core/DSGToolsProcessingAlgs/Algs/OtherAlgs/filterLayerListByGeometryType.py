# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-12-26
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
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingOutputMultipleLayers,
    QgsProcessingParameterMultipleLayers,
    QgsWkbTypes,
)


class FilterLayerListByGeometryType(QgsProcessingAlgorithm):
    INPUT_LAYERS = "INPUT_LAYERS"
    POINT_OUTPUT = "POINT_OUTPUT"
    LINE_OUTPUT = "LINE_OUTPUT"
    POLYGON_OUTPUT = "POLYGON_OUTPUT"

    def __init__(self):
        super(FilterLayerListByGeometryType, self).__init__()

    def initAlgorithm(self, config=None):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr("Input Layers"),
                QgsProcessing.TypeVectorAnyGeometry,
            )
        )
        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.POINT_OUTPUT, self.tr("Point layers")
            )
        )
        self.addOutput(
            QgsProcessingOutputMultipleLayers(self.LINE_OUTPUT, self.tr("Line layers"))
        )
        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.POLYGON_OUTPUT, self.tr("Polygon layers")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUT_LAYERS, context)
        listSize = len(inputLyrList)
        stepSize = 100 / listSize if listSize else 0
        geometryDict = {
            QgsWkbTypes.PointGeometry: [],
            QgsWkbTypes.LineGeometry: [],
            QgsWkbTypes.PolygonGeometry: [],
        }
        for current, lyr in enumerate(inputLyrList):
            if feedback.isCanceled():
                break
            geometryDict[lyr.geometryType()].append(lyr.id())
            feedback.setProgress(current * stepSize)
        return {
            self.POINT_OUTPUT: geometryDict[QgsWkbTypes.PointGeometry],
            self.LINE_OUTPUT: geometryDict[QgsWkbTypes.LineGeometry],
            self.POLYGON_OUTPUT: geometryDict[QgsWkbTypes.PolygonGeometry],
        }

    def name(self):
        """
        Here is where the processing itself takes place.
        """
        return "filterlayerlistbygeometrytype"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Filter layer list by geometry type")

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
        return QCoreApplication.translate("FilterLayerListByGeometryType", string)

    def createInstance(self):
        return FilterLayerListByGeometryType()
