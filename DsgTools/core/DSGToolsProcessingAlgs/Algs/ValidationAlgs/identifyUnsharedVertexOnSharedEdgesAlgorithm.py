# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-11-05
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


class IdentifyUnsharedVertexOnSharedEdgesAlgorithm(ValidationAlgorithm):
    FLAGS = "FLAGS"
    INPUT_LINES = "INPUT_LINES"
    INPUT_POLYGONS = "INPUT_POLYGONS"
    SELECTED = "SELECTED"
    SEARCH_RADIUS = "SEARCH_RADIUS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
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
            QgsProcessingParameterDistance(
                self.SEARCH_RADIUS, self.tr("Search Radius"), defaultValue=1.0
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
        inputLineLyrList = self.parameterAsLayerList(
            parameters, self.INPUT_LINES, context
        )
        inputPolygonLyrList = self.parameterAsLayerList(
            parameters, self.INPUT_POLYGONS, context
        )
        if inputLineLyrList + inputPolygonLyrList == []:
            raise QgsProcessingException(self.tr("Select at least one layer"))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        searchRadius = self.parameterAsDouble(parameters, self.SEARCH_RADIUS, context)
        self.prepareFlagSink(
            parameters,
            (inputLineLyrList + inputPolygonLyrList)[0],
            QgsWkbTypes.Point,
            context,
        )
        # Compute the number of steps to display within the progress bar and
        # get features from source
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        vertexNearEdgeFlagDict = layerHandler.getUnsharedVertexOnSharedEdgesDict(
            inputLineLyrList,
            inputPolygonLyrList,
            searchRadius,
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(1)
        self.raiseFeaturesFlags(vertexNearEdgeFlagDict, multiStepFeedback)

        return {self.FLAGS: self.flag_id}

    def raiseFeaturesFlags(self, geomDict, feedback):
        size = 100 / len(geomDict) if geomDict else 0
        for current, (featid, vertexDict) in enumerate(geomDict.items()):
            if feedback.isCanceled():
                break
            for vertexWkt, flagDict in vertexDict.items():
                edgeText = ", ".join([edge.asWkt() for edge in flagDict["edges"]])
                flagText = self.tr(
                    "Vertex {vertex_geom} is near edge(s) {edge_text}."
                ).format(vertex_geom=vertexWkt, edge_text=edgeText)
                flagGeom = flagDict["flagGeom"]
                self.flagFeature(flagGeom, flagText)
            feedback.setProgress(size * current)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyunsharedvertexonsharededgesalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Unshared Vertex on Shared Edges")

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
            "IdentifyUnsharedVertexOnSharedEdgesAlgorithm", string
        )

    def createInstance(self):
        return IdentifyUnsharedVertexOnSharedEdgesAlgorithm()
