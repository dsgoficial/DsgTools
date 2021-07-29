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
from ....GeometricTools.spatialRelationsHandler import SpatialRule


class BuildPolygonsFromCenterPointsAndBoundariesAlgorithm(ValidationAlgorithm):
    INPUT_CENTER_POINTS = 'INPUT_CENTER_POINTS'
    SELECTED = 'SELECTED'
    ATTRIBUTE_BLACK_LIST = 'ATTRIBUTE_BLACK_LIST'
    IGNORE_VIRTUAL_FIELDS = 'IGNORE_VIRTUAL_FIELDS'
    IGNORE_PK_FIELDS = 'IGNORE_PK_FIELDS'
    CONSTRAINT_LINE_LAYERS = 'CONSTRAINT_LINE_LAYERS'
    CONSTRAINT_POLYGON_LAYERS = 'CONSTRAINT_POLYGON_LAYERS'
    GEOGRAPHIC_BOUNDARY = 'GEOGRAPHIC_BOUNDARY'
    OUTPUT_POLYGONS = 'OUTPUT_POLYGONS'
    FLAGS = 'FLAGS'
    DELIMITERS_FLAGS='DELIMITERS_FLAGS'

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
            QgsProcessingParameterField(
                self.ATTRIBUTE_BLACK_LIST,
                self.tr('Fields to ignore'),
                None,
                'INPUT_CENTER_POINTS',
                QgsProcessingParameterField.Any,
                allowMultiple=True,
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_VIRTUAL_FIELDS,
                self.tr('Ignore virtual fields'),
                defaultValue=True
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_PK_FIELDS,
                self.tr('Ignore primary key fields'),
                defaultValue=True
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
                self.DELIMITERS_FLAGS,
                self.tr('Delimiters Flags')
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr('{0} Polygon Flags').format(self.displayName())
            )
        )
        

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.layerHandler = LayerHandler()
        algRunner = AlgRunner()
        spatialRule = SpatialRule(name="Unused delimiters",
                                  layer_a="segmentsWithoutDuplicates",
                                  filter_a=None,
                                  predicate=None,
                                  de9im_predicate="*1*******",
                                  layer_b="builtPolygonLyr",
                                  filter_b=None,
                                  cardinality="1..*",
                                  useDE9IM=True,
                                  checkLoadedLayer=False)

        inputCenterPointLyr = self.parameterAsVectorLayer(
            parameters,
            self.INPUT_CENTER_POINTS,
            context)

        if inputCenterPointLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(
                    parameters,
                    self.INPUT_CENTER_POINTS))

        constraintLineLyrList = self.parameterAsLayerList(
            parameters,
            self.CONSTRAINT_LINE_LAYERS,
            context)

        constraintPolygonLyrList = self.parameterAsLayerList(
            parameters,
            self.CONSTRAINT_POLYGON_LAYERS,
            context)

        onlySelected = self.parameterAsBool(
            parameters,
            self.SELECTED,
            context)

        geographicBoundaryLyr = self.parameterAsLayer(
            parameters,
            self.GEOGRAPHIC_BOUNDARY,
            context)

        attributeBlackList = self.parameterAsFields(
            parameters,
            self.ATTRIBUTE_BLACK_LIST,
            context)

        ignoreVirtual = self.parameterAsBool(
            parameters, self.IGNORE_VIRTUAL_FIELDS, context)

        ignorePK = self.parameterAsBool(
            parameters, self.IGNORE_PK_FIELDS, context)

        outputFields = self.retrieveFieldsFromInputToOutputLyr(inputCenterPointLyr,
                                                               attributeBlackList, 
                                                               ignorePK, 
                                                               ignoreVirtual)
        (output_polygon_sink, output_polygon_sink_id) = self.parameterAsSink(parameters,
                                                                             self.OUTPUT_POLYGONS,
                                                                             context,
                                                                             outputFields,
                                                                             QgsWkbTypes.Polygon,
                                                                             inputCenterPointLyr.sourceCrs())
        
        unusedDelimitersFields = self.getFlagFields()
        (unused_delimiters_sink, unused_delimiters_sink_id) = self.parameterAsSink(parameters,
                                                                             self.DELIMITERS_FLAGS,
                                                                             context,
                                                                             unusedDelimitersFields,
                                                                             QgsWkbTypes.LineString,
                                                                             inputCenterPointLyr.sourceCrs())

        self.prepareFlagSink(parameters, inputCenterPointLyr,
                             QgsWkbTypes.Polygon, context)

        polygonFeatList, flagDict, delimiterFlagDict = self.layerHandler.getPolygonsFromCenterPointsAndBoundaries(
            inputCenterPointLyr,
            geographicBoundaryLyr=geographicBoundaryLyr,
            constraintLineLyrList=constraintLineLyrList,
            constraintPolygonLyrList=constraintPolygonLyrList,
            onlySelected=onlySelected,
            spatialRule=[spatialRule.asDict()],
            context=context,
            feedback=feedback,
            attributeBlackList=attributeBlackList,
            algRunner=algRunner)

        for delimiterFlagGeom, delimiterFlagText in delimiterFlagDict.items():
            self.flagFeature(delimiterFlagGeom, delimiterFlagText, fromWkb=False, sink=unused_delimiters_sink)

        output_polygon_sink.addFeatures(polygonFeatList, QgsFeatureSink.FastInsert)

        for flagGeom, flagText in flagDict.items():
            self.flagFeature(flagGeom, flagText, fromWkb=True)

        return {
            self.OUTPUT_POLYGONS: output_polygon_sink_id,
            self.FLAGS: self.flag_id,
            self.DELIMITERS_FLAGS: unused_delimiters_sink_id}
    
    def retrieveFieldsFromInputToOutputLyr(self, inputLyr, attributeBlackList, ignorePK, ignoreVirtual):
        """
        Prepare a list of fields based on the attributeBlackList to the
        algorithm outputs
        :param inputLyr: (QgsVectorLayer) Layer with Point which you want to take
            the attr
        :param attributeBlackList: (list) list of fields blacklisted
        :param ignorePK: (bool) to ignore primary key fields
        :param ignoreVirtual: (bool) to ignore virtual fields
        :return: (list) list of fields to output
        """
        if ignoreVirtual or ignorePK:
            virtualAndPrimaryKeyFields = self.layerHandler.getVirtualAndPrimaryKeyFields(inputLyr)
            attributeBlackList.extend(virtualAndPrimaryKeyFields)
            outputFields = self.layerHandler.getFieldsFromAttributeBlackList(inputLyr,
                                                                        attributeBlackList,
                                                                        ignoreVirtualFields=ignoreVirtual,
                                                                        excludePrimaryKeys=ignorePK)
            return outputFields
        else:
            outputFields = self.layerHandler.getFieldsFromAttributeBlackList(inputLyr,
                                                                        attributeBlackList,
                                                                        ignoreVirtualFields=ignoreVirtual,
                                                                        excludePrimaryKeys=ignorePK)
            return outputFields

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
