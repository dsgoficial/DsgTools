# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-11-07
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
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterVectorLayer, QgsWkbTypes, QgsFields)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class UnbuildPolygonsAlgorithm(ValidationAlgorithm):
    INPUT_POLYGONS = 'INPUT_POLYGONS'
    SELECTED = 'SELECTED'
    CONSTRAINT_LINE_LAYERS = 'CONSTRAINT_LINE_LAYERS'
    CONSTRAINT_POLYGON_LAYERS = 'CONSTRAINT_POLYGON_LAYERS'
    GEOGRAPHIC_BOUNDARY = 'GEOGRAPHIC_BOUNDARY'
    OUTPUT_CENTER_POINTS = 'OUTPUT_CENTER_POINTS'
    OUTPUT_BOUNDARIES = 'OUTPUT_BOUNDARIES'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_POLYGONS,
                self.tr('Polygon Layers'),
                QgsProcessing.TypeVectorPolygon
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.CONSTRAINT_LINE_LAYERS,
                self.tr('Line Constraint Layers'),
                QgsProcessing.TypeVectorLine,
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.CONSTRAINT_POLYGON_LAYERS,
                self.tr('Polygon Constraint Layers'),
                QgsProcessing.TypeVectorPolygon,
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr('Geographic Boundary'),
                [QgsProcessing.TypeVectorPolygon],
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_CENTER_POINTS,
                self.tr('Output Center Points')
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_BOUNDARIES,
                self.tr('Output Boundaries')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()
        inputPolygonLyrList = self.parameterAsLayerList(
            parameters,
            self.INPUT_POLYGONS,
            context
        )
        constraintLineLyrList = self.parameterAsLayerList(
            parameters,
            self.CONSTRAINT_LINE_LAYERS,
            context
        )
        constraintPolygonLyrList = self.parameterAsLayerList(
            parameters,
            self.CONSTRAINT_POLYGON_LAYERS,
            context
        )
        if set(constraintPolygonLyrList).intersection(set(inputPolygonLyrList)):
            raise QgsProcessingException(
                self.tr('Input polygon layers must not be in constraint polygon list.')
            )
        onlySelected = self.parameterAsBool(
            parameters,
            self.SELECTED,
            context
        )
        boundaryLyr = self.parameterAsLayer(
            parameters,
            self.GEOGRAPHIC_BOUNDARY,
            context
        )
        # Compute the number of steps to display within the progress bar and
        # get features from source
        # alg steps:
        # 1- Build single polygon layer
        # 2- Compute center points
        # 3- Compute boundaries
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(
            self.tr('Building single polygon layer')
        )
        singlePolygonLayer = layerHandler.getMergedLayer(
            inputPolygonLyrList,
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
            context=context,
            algRunner=algRunner
        )
        multiStepFeedback.setCurrentStep(1)
        (
            output_center_point_sink,
            output_center_point_sink_id
        ) = self.parameterAsSink(
            parameters,
            self.OUTPUT_CENTER_POINTS,
            context,
            singlePolygonLayer.fields(),
            QgsWkbTypes.Point,
            singlePolygonLayer.sourceCrs()
        )
        (
            output_boundaries_sink,
            output_boundaries_sink_id
        ) = self.parameterAsSink(
            parameters,
            self.OUTPUT_BOUNDARIES,
            context,
            QgsFields(),
            QgsWkbTypes.LineString,
            singlePolygonLayer.sourceCrs()
        )
        layerHandler.getCentroidsAndBoundariesFromPolygons(
            singlePolygonLayer,
            output_center_point_sink,
            output_boundaries_sink,
            constraintLineLyrList=constraintLineLyrList,
            constraintPolygonLyrList=constraintPolygonLyrList,
            context=context,
            feedback=multiStepFeedback,
            algRunner=algRunner
        )

        return {
            self.OUTPUT_CENTER_POINTS : output_center_point_sink_id,
            self.OUTPUT_BOUNDARIES : output_boundaries_sink_id
        }

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'unbuildpolygonsalgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Unbuild Polygons')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Quality Assurance Tools (Manipulation Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Quality Assurance Tools (Manipulation Processes)'

    def tr(self, string):
        return QCoreApplication.translate('UnbuildPolygonsAlgorithm', string)

    def createInstance(self):
        return UnbuildPolygonsAlgorithm()
