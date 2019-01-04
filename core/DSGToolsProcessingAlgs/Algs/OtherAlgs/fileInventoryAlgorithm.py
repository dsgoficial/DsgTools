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
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from ...algRunner import AlgRunner
import processing, os, requests
from osgeo import gdal, ogr
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
                       QgsProcessingParameterFile)

class FileInventoryAlgorithm(QgsProcessingAlgorithm):
    INPUT_FOLDER = 'INPUT_FOLDER'
    ONLY_GEO = 'ONLY_GEO'
    SEARCH_TYPE = 'SEARCH_TYPE'
    FILE_FORMATS = 'FILE_FORMATS'
    TYPE_LIST = 'TYPE_LIST'
    COPY_FILES = 'COPY_FILES'
    COPY_FOLDER= 'COPY_FOLDER'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        gdal.DontUseExceptions()
        ogr.DontUseExceptions()
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_FOLDER,
                self.tr('Input folder'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ONLY_GEO,
                self.tr('Search only georreferenced files'),
                defaultValue=True
            )
        )
        self.searchTypes = [
            'Search only listed formats',
            'Exclude listed formats'
        ]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.SEARCH_TYPE,
                self.tr('Search type'),
                options=self.searchTypes,
                defaultValue=0
            )
        )
        self.addParameter(
            QgsProcessingParameterMatrix(
                self.FILE_FORMATS,
                self.tr('Formats'),
                headers=[self.tr('File Formats')],
                numberRows=1,
                defaultValue=['shp','tif']
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.COPY_FILES,
                self.tr('Copy files to output'),
                defaultValue=False
            )
        )
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.COPY_FOLDER,
                self.tr('Copy files to folder'),
                optional=True,
                defaultValue=None
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Inventory layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputFolder = self.parameterAsString(parameters, self.INPUT_FOLDER, context)
        matrixItems = self.parameterAsMatrix(parameters, self.FILE_FORMATS, context)
        copyFolder = self.parameterAsString(parameters, self.COPY_FOLDER, context)
        feedback.pushInfo(inputFolder)
        feedback.pushInfo(','.join(matrixItems))
        feedback.pushInfo(copyFolder)

        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'runfileinventory'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Run File Inventory')

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
        return FileInventoryAlgorithm()