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

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink, QgsFields,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterVectorLayer, QgsWkbTypes)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class BuildPolygonsFromCenterPointsAndBoundariesAlgorithm(ValidationAlgorithm):
    INPUT_CENTER_POINTS = 'INPUT_CENTER_POINTS'
    SELECTED = 'SELECTED'
    ATTRIBUTE_BLACK_LIST = 'ATTRIBUTE_BLACK_LIST'
    CONSTRAINT_LINE_LAYERS = 'CONSTRAINT_LINE_LAYERS'
    CONSTRAINT_POLYGON_LAYERS = 'CONSTRAINT_POLYGON_LAYERS'
    GEOGRAPHIC_BOUNDARY = 'GEOGRAPHIC_BOUNDARY'
    OUTPUT_POLYGONS = 'OUTPUT_POLYGONS'
    FLAGS = 'FLAGS'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_CENTER_POINTS,
                self.tr('Center Point Layer'),
                [QgsProcessing.TypeVectorPoint]
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.ATTRIBUTE_BLACK_LIST, 
                self.tr('Fields to ignore'),
                None, 
                'INPUT_CENTER_POINTS', 
                QgsProcessingParameterField.Any,
                allowMultiple=True,
                optional = True
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
                self.OUTPUT_POLYGONS,
                self.tr('Output Polygons')
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr('{0} Flags').format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()
        inputCenterPointLyr = self.parameterAsVectorLayer(
            parameters,
            self.INPUT_CENTER_POINTS,
            context
        )
        if inputCenterPointLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(
                    parameters,
                    self.INPUT_CENTER_POINTS
                )
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
        onlySelected = self.parameterAsBool(
            parameters,
            self.SELECTED,
            context
        )
        geographicBoundaryLyr = self.parameterAsLayer(
            parameters,
            self.GEOGRAPHIC_BOUNDARY,
            context
        )
        attributeBlackList = self.parameterAsFields(
            parameters,
            self.ATTRIBUTE_BLACK_LIST,
            context
        )
        (
            output_polygon_sink,
            output_polygon_sink_id
        ) = self.parameterAsSink(
            parameters,
            self.OUTPUT_POLYGONS,
            context,
            inputCenterPointLyr.fields(),
            QgsWkbTypes.Polygon,
            inputCenterPointLyr.sourceCrs()
        )
        self.prepareFlagSink(
            parameters,
            inputCenterPointLyr,
            QgsWkbTypes.Polygon,
            context
        )
        polygonFeatList, flagDict = layerHandler.getPolygonsFromCenterPointsAndBoundaries(
            inputCenterPointLyr,
            geographicBoundaryLyr=geographicBoundaryLyr,
            constraintLineLyrList=constraintLineLyrList,
            constraintPolygonLyrList=constraintPolygonLyrList,
            onlySelected=onlySelected,
            context=context,
            feedback=feedback,
            attributeBlackList=attributeBlackList, 
            algRunner=algRunner
        )
        output_polygon_sink.addFeatures(
            polygonFeatList, QgsFeatureSink.FastInsert
        )
        for flagGeom, flagText in flagDict.items():
            self.flagFeature(flagGeom, flagText, fromWkb=True)

        return {
            self.OUTPUT_POLYGONS : output_polygon_sink_id,
            self.FLAGS : self.flag_id
        }

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'buildpolygonsfromcenterpointsandboundariesalgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Build Polygons From Center Points and Boundaries')

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
        return QCoreApplication.translate('BuildPolygonsFromCenterPointsAndBoundariesAlgorithm', string)

    def createInstance(self):
        return BuildPolygonsFromCenterPointsAndBoundariesAlgorithm()
