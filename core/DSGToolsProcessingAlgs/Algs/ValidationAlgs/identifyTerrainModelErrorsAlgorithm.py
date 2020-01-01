# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-13
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import processing
from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsGeometry, QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer, QgsProcessingUtils,
                       QgsSpatialIndex, QgsVectorLayerUtils, QgsWkbTypes)

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.GeometricTools.spatialRelationsHandler import \
    SpatialRelationsHandler

from .validationAlgorithm import ValidationAlgorithm


class IdentifyTerrainModelErrorsAlgorithm(ValidationAlgorithm):
    INPUT = 'INPUT'
    SELECTED = 'SELECTED'
    CONTOUR_INTERVAL = 'CONTOUR_INTERVAL'
    GEOGRAPHIC_BOUNDS = 'GEOGRAPHIC_BOUNDS'
    CONTOUR_ATTR = 'CONTOUR_ATTR'
    POINT_FLAGS = 'POINT_FLAGS'
    LINE_FLAGS = 'LINE_FLAGS'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorLine]
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
                self.CONTOUR_ATTR,
                self.tr('Contour value field'),
                None,
                'INPUT',
                QgsProcessingParameterField.Any
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.CONTOUR_INTERVAL,
                self.tr('Threshold'),
                minValue=0,
                defaultValue=10
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDS,
                self.tr('Geographic bounds layer'),
                [QgsProcessing.TypeVectorPolygon],
                optional=False
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POINT_FLAGS,
                self.tr('{0} Point Flags').format(self.displayName())
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.LINE_FLAGS,
                self.tr('{0} Line Flags').format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        spatialRealtionsHandler = SpatialRelationsHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        heightFieldName = self.parameterAsFields(
            parameters, self.CONTOUR_ATTR, context)[0]
        threshold = self.parameterAsDouble(
            parameters, self.CONTOUR_INTERVAL, context)
        geoBoundsLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDS, context)
        point_flagSink, point_flag_id = self.prepareAndReturnFlagSink(
            parameters, inputLyr, QgsWkbTypes.Point, context, self.POINT_FLAGS
        )
        line_flagSink, line_flag_id = self.prepareAndReturnFlagSink(
            parameters, inputLyr, QgsWkbTypes.LineString, context, self.LINE_FLAGS
        )

        invalidDict = spatialRealtionsHandler.validateTerrainModel(
            contourLyr=inputLyr,
            onlySelected=onlySelected,
            heightFieldName=heightFieldName,
            threshold=threshold,
            geoBoundsLyr=geoBoundsLyr,
            feedback=feedback
        )

        for flagGeom, text in invalidDict.items():
            geom = QgsGeometry()
            geom.fromWkb(flagGeom)
            flagSink = line_flagSink if geom.type() == QgsWkbTypes.LineGeometry else point_flagSink
            self.flagFeature(geom, text, fromWkb=False, sink=flagSink)

        return {self.POINT_FLAGS : point_flag_id, self.LINE_FLAGS : line_flag_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifyterrainmodelerrorsalgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Terrain Model Errors Algorithm')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Quality Assurance Tools (Identification Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Quality Assurance Tools (Identification Processes)'

    def tr(self, string):
        return QCoreApplication.translate('IdentifyTerrainModelErrorsAlgorithm', string)

    def createInstance(self):
        return IdentifyTerrainModelErrorsAlgorithm()
