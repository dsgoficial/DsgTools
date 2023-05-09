# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-12-07
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

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsDataSourceUri,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterDistance,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class IdentifyUnsharedVertexOnIntersectionsAlgorithm(ValidationAlgorithm):
    FLAGS = "FLAGS"
    INPUT_POINTS = "INPUT_POINTS"
    INPUT_LINES = "INPUT_LINES"
    INPUT_POLYGONS = "INPUT_POLYGONS"
    SELECTED = "SELECTED"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_POINTS,
                self.tr("Point Layers"),
                QgsProcessing.TypeVectorPoint,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LINES,
                self.tr("Linestring Layers"),
                QgsProcessing.TypeVectorLine,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_POLYGONS,
                self.tr("Polygon Layers"),
                QgsProcessing.TypeVectorPolygon,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        inputPointLyrList = self.parameterAsLayerList(
            parameters, self.INPUT_POINTS, context
        )
        inputLineLyrList = self.parameterAsLayerList(
            parameters, self.INPUT_LINES, context
        )
        inputPolygonLyrList = self.parameterAsLayerList(
            parameters, self.INPUT_POLYGONS, context
        )
        if inputPointLyrList + inputLineLyrList + inputPolygonLyrList == []:
            raise QgsProcessingException(self.tr("Select at least one layer"))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        self.prepareFlagSink(
            parameters,
            (inputPointLyrList + inputLineLyrList + inputPolygonLyrList)[0],
            QgsWkbTypes.Point,
            context,
        )
        # Compute the number of steps to display within the progress bar and
        # get features from source
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        usharedIntersectionSet = layerHandler.getUnsharedVertexOnIntersections(
            inputPointLyrList,
            inputLineLyrList,
            inputPolygonLyrList,
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(1)
        self.raiseFeaturesFlags(usharedIntersectionSet, multiStepFeedback)

        return {self.FLAGS: self.flag_id}

    def raiseFeaturesFlags(self, usharedIntersectionSet, feedback):
        size = 100 / len(usharedIntersectionSet) if usharedIntersectionSet else 0
        flagText = self.tr("Unshared vertex between the intersections of input layers.")
        for current, geomWkb in enumerate(usharedIntersectionSet):
            if feedback.isCanceled():
                break
            self.flagFeature(geomWkb, flagText, fromWkb=True)
            feedback.setProgress(size * current)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyunsharedvertexonintersectionsalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Unshared Vertex on Intersections")

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
        return "DSGTools: Quality Assurance Tools (Identification Processes)"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifyUnsharedVertexOnIntersectionsAlgorithm", string
        )

    def createInstance(self):
        return IdentifyUnsharedVertexOnIntersectionsAlgorithm()
