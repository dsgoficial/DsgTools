# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-08-24
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Mateus Sereno, Arthur Santos - Cartographic Engineers @ Brazilian Army
        email                : mateus.sereno@ime.eb.br - arthur.santos@ime.eb.br
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
from qgis.PyQt.Qt import QVariant
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
                       QgsProcessingException,
                       QgsProcessingParameterString,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterType,
                       QgsProcessingParameterCrs,
                       QgsCoordinateTransform,
                       QgsProject,
                       QgsCoordinateReferenceSystem,
                       QgsField,
                       QgsFields,
                       QgsProcessingOutputMultipleLayers,
                       QgsVectorLayer,
                       QgsProcessingParameterString)

class LockAttributeEditingAlgorithm(QgsProcessingAlgorithm):
    INPUT_LAYERS = 'INPUT_LAYERS'
    COLUMN_NAMES = 'COLUMN_NAMES'
    OUTPUT = 'OUTPUT'
    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr('Input Layers'),
                QgsProcessing.TypeVectorAnyGeometry
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.COLUMN_NAMES,
                description =  self.tr('Attributes to lock (separated by comma)'),
                multiLine = False,
                defaultValue = ''
            )
        )

        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.OUTPUT,
                self.tr('Original layers with locked attributes edit')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputLyrList = self.parameterAsLayerList(
            parameters,
            self.INPUT_LAYERS,
            context
        )
        inputColumnNames = self.parameterAsString(
            parameters,
            self.COLUMN_NAMES,
            context
        )

        listSize = len(inputLyrList)
        stepSize = 100/listSize if listSize else 0

        self.COLUMNS_TO_LOCK = list(map(str.strip, inputColumnNames.upper().split(',')))
        
        for current, lyr in enumerate(inputLyrList):
            if feedback.isCanceled():
                break
            self.tryLockAttributeEditing(lyr)
            feedback.setProgress(current * stepSize)

        return {self.OUTPUT: [lyr.id() for lyr in inputLyrList]}

    def tryLockAttributeEditing(self, layer : QgsVectorLayer):
        layerFields = layer.fields()
        layerFieldNames = list(map(str.upper, layerFields.names()))
        for columnToLockName in self.COLUMNS_TO_LOCK:
            try:
                idxOnLayer = layerFieldNames.index(columnToLockName)
            except ValueError:
                # In case the column is not present on the layer:
                continue
            formConfig = layer.editFormConfig()
            formConfig.setReadOnly(idxOnLayer, True)
            layer.setEditFormConfig(formConfig)
        
        return layer

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'lockattributeediting'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Lock Attribute Editing')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Layer Management Algorithms')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Layer Management Algorithms'

    def tr(self, string):
        return QCoreApplication.translate('LockAttributeEditingAlgorithm', string)

    def createInstance(self):
        return LockAttributeEditingAlgorithm()