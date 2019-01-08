# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-01-04
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
                               (C) 2015 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
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
from DsgTools.core.GeometricTools.featureHandler import FeatureHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.Factories.ThreadFactory.threadFactory import ThreadFactory
from ...algRunner import AlgRunner
import processing, os, requests
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
                       QgsProcessingParameterFolderDestination,
                       QgsProcessingParameterExpression,
                       QgsProcessingException,
                       QgsProcessingParameterString,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterType,
                       QgsProcessingParameterMatrix,
                       QgsProcessingParameterFile,
                       QgsCoordinateReferenceSystem,
                       QgsProject,
                       QgsFields,
                       QgsProcessingParameterCrs,
                       QgsCoordinateTransform,
                       QgsVectorLayer)

class RaiseFlagsAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    FLAG_FIELD = 'FLAG_FIELD'
    TABLE_SCHEMA = 'TABLE_SCHEMA'
    TABLE_NAME = 'TABLE_NAME'
    OUTPUT_FLAG_TEXT_FIELD = 'OUTPUT_FLAG_TEXT_FIELD'
    GEOMETRY_COLUMN = 'GEOMETRY_COLUMN'
    CRS = 'CRS'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.FLAG_FIELD,
                self.tr('Flag text field'),
                parentLayerParameterName=self.INPUT
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.TABLE_SCHEMA,
                self.tr('Table schema')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.TABLE_NAME,
                self.tr('Table name')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.GEOMETRY_COLUMN,
                self.tr('Geometry column')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.OUTPUT_FLAG_TEXT_FIELD,
                self.tr('Flag text field')
            )
        )
        self.addParameter(
            QgsProcessingParameterCrs(
                self.CRS,
                self.tr('CRS')
            )
        )
        

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        featureHandler = FeatureHandler()
        layerHandler = LayerHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        inputAttr = self.parameterAsFields(parameters, self.FLAG_FIELD, context)
        inputAttr = inputAttr[0]
        tableSchema = self.parameterAsString(parameters, self.TABLE_SCHEMA, context)
        if tableSchema is None or tableSchema == '':
            raise QgsProcessingException(self.tr('Invalid table schema'))
        
        tableName = self.parameterAsString(parameters, self.TABLE_NAME, context)
        if tableName is None or tableName == '':
            raise QgsProcessingException(self.tr('Invalid table name'))

        geometryColumn = self.parameterAsString(parameters, self.GEOMETRY_COLUMN, context)
        if geometryColumn is None or geometryColumn == '':
            raise QgsProcessingException(self.tr('Invalid geometry column'))
        
        flagTextAttr = self.parameterAsString(parameters, self.OUTPUT_FLAG_TEXT_FIELD, context)
        if flagTextAttr is None or flagTextAttr == '':
            raise QgsProcessingException(self.tr('Invalid flag attribute column'))

        crs = self.parameterAsCrs(parameters, self.CRS, context)
        if crs is None or not crs.isValid():
            raise QgsProcessingException(self.tr('Invalid CRS.'))
        
        outputLyr = self.getOutputFromInput(inputLyr, tableSchema, tableName, geometryColumn)
        if not outputLyr.isValid():
            raise QgsProcessingException(self.tr('Invalid output layer.'))
        coordinateTransformer = QgsCoordinateTransform(
            QgsCoordinateReferenceSystem(crs.geographicCrsAuthId()),
            crs,
            QgsProject.instance()
            )
        parameterDict = layerHandler.getDestinationParameters(outputLyr)
        outputLyr.startEditing()
        outputLyr.beginEditCommand('Adding flag features')
        count = inputLyr.featureCount()
        progress_count = 100 / count if count else 0
        for current, feat in enumerate(inputLyr.getFeatures()):
            if feedback.isCanceled():
                break
            for newFeat in featureHandler.handleConvertedFeature(feat, outputLyr, parameterDict=parameterDict, coordinateTransformer=coordinateTransformer):
                newFeat[flagTextAttr] = feat[inputAttr]
                outputLyr.addFeature(newFeat)
            feedback.setProgress(current * progress_count)
        outputLyr.endEditCommand()
        outputLyr.commitChanges()
        return {}
    
    def getOutputFromInput(self, inputLyr, tableSchema, tableName, geometryColumn):
        lyrUri = inputLyr.dataProvider().dataSourceUri()
        uri = QgsDataSourceUri(lyrUri)
        uri.setDataSource(tableSchema, tableName, geometryColumn)
        outputLyr = QgsVectorLayer(uri.uri(), tableName, 'postgres')
        return outputLyr

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'raiseflags'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Raise Flags')

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
        return RaiseFlagsAlgorithm()