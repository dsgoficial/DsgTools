# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-10
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
from .validationAlgorithm import ValidationAlgorithm
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
                       QgsProcessingParameterField)

class DissolvePolygonsWithSameAttributesAlgorithm(ValidationAlgorithm):
    INPUT = 'INPUT'
    SELECTED = 'SELECTED'
    MIN_AREA = 'MIN_AREA'
    ATTRIBUTE_BLACK_LIST = 'ATTRIBUTE_BLACK_LIST'
    IGNORE_VIRTUAL_FIELDS = 'IGNORE_VIRTUAL_FIELDS'
    IGNORE_PK_FIELDS = 'IGNORE_PK_FIELDS'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorLine ]
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
                'INPUT', 
                QgsProcessingParameterField.Any,
                allowMultiple=True,
                optional = True
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

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        attributeBlackList = self.parameterAsFields(parameters, self.ATTRIBUTE_BLACK_LIST, context)
        ignoreVirtual = self.parameterAsBool(parameters, self.IGNORE_VIRTUAL_FIELDS, context)
        ignorePK = self.parameterAsBool(parameters, self.IGNORE_PK_FIELDS, context)

        layerHandler.dissolvePolygonsWithSameAttributes(inputLyr, feedback = feedback, onlySelected=onlySelected, ignoreVirtualFields = ignoreVirtual, attributeBlackList = attributeBlackList, excludePrimaryKeys=ignorePK)

        return {self.INPUT: inputLyr}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'dissolvepolygonswithsameattributes'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Dissolve polygons with same attribute set')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Validation Tools (Manipulation Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Validation Tools (Manipulation Processes)'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DissolvePolygonsWithSameAttributesAlgorithm()