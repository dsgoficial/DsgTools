# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-27
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
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from ...algRunner import AlgRunner
import processing
from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsFeature,
                       QgsDataSourceUri,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsWkbTypes,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingUtils,
                       QgsSpatialIndex,
                       QgsGeometry,
                       QgsProcessingParameterField,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterExpression,
                       QgsProcessingException)

class ConvertLayer2LayerAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    INPUT_FILTER_EXPRESSION = 'INPUT_FILTER_EXPRESSION'
    FILTER_LAYER = 'FILTER_LAYER'
    FL_FILTER_EXPRESSION = 'FL_FILTER_EXPRESSION'
    BEHAVIOR = 'BEHAVIOR'
    OUTPUT = 'OUTPUT'
    CONVERSION_MAP = 'CONVERSION_MAP'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.INPUT_FILTER_EXPRESSION,
                description = self.tr('Input layer expression'),
                parentLayerParameterName = self.INPUT,
                optional = True
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.FILTER_LAYER,
                self.tr('Filter layer'),
                [QgsProcessing.TypeVectorPolygon],
                optional = True
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.FL_FILTER_EXPRESSION,
                description = self.tr('Filter layer expression'),
                parentLayerParameterName = self.FILTER_LAYER,
                optional = True
            )
        )
        self.modes = [self.tr('Only features from input that intersect features from filter layer'),
                      self.tr('Clip features from input with features from filter layer and take inside features'),
                      self.tr('Clip features from input with features from filter layer and take outside features')
                      ]

        self.addParameter(
            QgsProcessingParameterEnum(
                self.BEHAVIOR,
                self.tr('Behavior'),
                options=self.modes,
                optional = True
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.CONVERSION_MAP,
                description = self.tr('JSON Map'),
                extension = '.json',
                optional = True
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.OUTPUT,
                self.tr('Output layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        outputLyr = self.parameterAsVectorLayer(parameters, self.OUTPUT, context)
        if outputLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.OUTPUT))
        if inputLyr == outputLyr:
            raise QgsProcessingException(self.tr('Input must be different from output!'))
        inputExpression = self.parameterAsExpression(parameters, self.INPUT_FILTER_EXPRESSION, context)
        filterLyr = self.parameterAsVectorLayer(parameters, self.FILTER_LAYER, context)
        


        

        return {self.INPUT: inputLyr}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'convertlayer2layer'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Convert layer to layer')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Other Algorithms')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Other Algorithms'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ConvertLayer2LayerAlgorithm()