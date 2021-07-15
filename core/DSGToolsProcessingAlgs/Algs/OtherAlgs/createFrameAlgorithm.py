# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-12-18
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
from DsgTools.core.GeometricTools.featureHandler import FeatureHandler
from DsgTools.core.Utils.FrameTools.map_index import UtmGrid
from ...algRunner import AlgRunner
import processing, os, requests
from time import sleep
from qgis.PyQt.Qt import QVariant
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
                       QgsProcessingException,
                       QgsProcessingParameterString,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterType,
                       QgsProcessingParameterCrs,
                       QgsCoordinateTransform,
                       QgsProject,
                       QgsCoordinateReferenceSystem,
                       QgsField,
                       QgsFields)

class CreateFrameAlgorithm(QgsProcessingAlgorithm):
    START_SCALE = 'START_SCALE'
    STOP_SCALE = 'STOP_SCALE'
    INDEX_TYPE = 'INDEX_TYPE'
    INDEX = 'INDEX'
    CRS = 'CRS'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.setValidCharacters()
        self.scales = ['1000k',
                      '500k',
                      '250k',
                      '100k',
                      '50k',
                      '25k',
                      '10k',
                      '5k',
                      '2k',
                      '1k']
        self.addParameter(
            QgsProcessingParameterEnum(
                self.START_SCALE,
                self.tr('Base scale'),
                options=self.scales,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.STOP_SCALE,
                self.tr('Desired scale'),
                options=self.scales,
                defaultValue=0
            )
        )
        self.indexTypes = [
            'MI/MIR',
            'INOM'
        ]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INDEX_TYPE,
                self.tr('Index type'),
                options=self.indexTypes,
                defaultValue=0
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.INDEX,
                self.tr('Index')
            )
        )
        self.addParameter(
            QgsProcessingParameterCrs(
                self.CRS,
                self.tr('CRS')
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Created Frames')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        featureHandler = FeatureHandler()
        startScaleIdx = self.parameterAsEnum(parameters, self.START_SCALE, context)
        stopScaleIdx = self.parameterAsEnum(parameters, self.STOP_SCALE, context)
        stopScale = self.scales[stopScaleIdx]
        stopScale = int(stopScale.replace('k', ''))
        if startScaleIdx > stopScaleIdx:
            raise QgsProcessingException(self.tr('The desired scale denominator must not be bigger than the base scale denominator.'))
        indexTypeIdx = self.parameterAsEnum(parameters, self.INDEX_TYPE, context)
        inputIndex = self.parameterAsString(parameters, self.INDEX, context)
        if startScaleIdx in [0,1] and indexTypeIdx == 0:
            raise QgsProcessingException(self.tr('{index} is only valid for scales 250k and below.').format(index=self.indexTypes[indexTypeIdx]))
        if inputIndex is None or inputIndex == '':
            raise QgsProcessingException(self.tr('Invalid {index}').format(index=self.indexTypes[indexTypeIdx]))
        index = self.getIndex(inputIndex, indexTypeIdx, startScaleIdx)
        if index is None or not self.validateIndex(index):
            raise QgsProcessingException(self.tr('Invalid {index} format.').format(index=self.indexTypes[indexTypeIdx]))
        crs = self.parameterAsCrs(parameters, self.CRS, context)
        if crs is None or not crs.isValid():
            raise QgsProcessingException(self.tr('Invalid CRS.'))
        fields = QgsFields()
        fields.append(QgsField('inom', QVariant.String))
        fields.append(QgsField('mi', QVariant.String))
        (output_sink, output_sink_id) = self.parameterAsSink(parameters, self.OUTPUT,
                context, fields, QgsWkbTypes.Polygon, crs)
        featureList = []
        coordinateTransformer = QgsCoordinateTransform(
            QgsCoordinateReferenceSystem(crs.geographicCrsAuthId()),
            crs,
            QgsProject.instance()
            )
        featureHandler.getSystematicGridFeatures(featureList, index, stopScale, coordinateTransformer, fields, feedback=feedback)
        for feat in featureList:
            output_sink.addFeature(feat, QgsFeatureSink.FastInsert)

        return {'OUTPUT':output_sink_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'gridzonegenerator'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Generate Systematic Grid')

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
        return QCoreApplication.translate('CreateFrameAlgorithm', string)

    def createInstance(self):
        return CreateFrameAlgorithm()
    
    def getIndex(self, inputIndex, indexType, scaleType):
        """
        Returns map_index
        """
        if indexType == 0:
            if scaleType == 2:
                return UtmGrid().getINomenFromMIR(inputIndex)
            else:
                return UtmGrid().getINomenFromMI(inputIndex)
        return inputIndex
    
    def setValidCharacters(self):
        """
        Method to define the valid characters
        """
        self.chars = []

        chars = 'NS'
        self.chars.append(chars)
        chars = 'ABCDEFGHIJKLMNOPQRSTUVZ'
        self.chars.append(chars)
        chars = ['01','02','03','04','05','06','07','08','09','10',
                   '11','12','13','14','15','16','17','18','19','20',
                   '21','22','23','24','25','26','27','28','29','30',
                   '31','32','33','34','35','36','37','38','39','40',
                   '41','42','43','44','45','46','47','48','49','50',
                   '51','52','53','54','55','56','57','58','59','60']
        self.chars.append(chars)
        chars = 'VXYZ'
        self.chars.append(chars)
        chars = 'ABCD'
        self.chars.append(chars)
        chars = ['I','II','III','IV','V','VI']
        self.chars.append(chars)
        chars = '1234'
        self.chars.append(chars)
        chars = ['NO','NE','SO','SE']
        self.chars.append(chars)
        chars = 'ABCDEF'
        self.chars.append(chars)
        chars = ['I','II','III','IV']
        self.chars.append(chars)
        chars = '123456'
        self.chars.append(chars)
        chars = 'ABCD'
        self.chars.append(chars)
    
    def validateIndex(self, index):
        """
        Parses the index to see if it is valid
        """
        for i, word in enumerate(index.split('-')):
            if len(word) == 0:
                return False
            if i == 0:
                if word[0] not in self.chars[0]:
                    return False
                if word[1] not in self.chars[1]:
                    return False
            elif i == 1:
                if word not in self.chars[2]:
                    return False
            elif i == 2:
                if word not in self.chars[3]:
                    return False
            elif i == 3:
                if word not in self.chars[4]:
                    return False
            elif i == 4:
                if word not in self.chars[5]:
                    return False
            elif i == 5:
                if word not in self.chars[6]:
                    return False
            elif i == 6:
                if word not in self.chars[7]:
                    return False
            elif i == 7:
                if word not in self.chars[8]:
                    return False
            elif i == 8:
                if word not in self.chars[9]:
                    return False
            elif i == 9:
                if word not in self.chars[10]:
                    return False
            elif i == 10:
                if word not in self.chars[11]:
                    return False
        return True


# class ParameterFMEManagerType(QgsProcessingParameterType):

#     def __init__(self):
#         super().__init__()

#     def create(self, name):
#         return ParameterFMEManager(name)

#     def metadata(self):
#         return {'widget_wrapper': 'DsgTools.gui.ProcessingUI.fmeManagerWrapper.FMEManagerWrapper'}

#     def name(self):
#         return QCoreApplication.translate('Processing', 'FME Manager Parameters')

#     def id(self):
#         return 'fme_manager'

#     def description(self):
#         return QCoreApplication.translate('Processing', 'FME Manager parameters. Used on Run Remote FME Workspace')

# class ParameterFMEManager(QgsProcessingParameterDefinition):

#     def __init__(self, name, description=''):
#         super().__init__(name, description)

#     def clone(self):
#         copy = ParameterFMEManager(self.name(), self.description())
#         return copy

#     def type(self):
#         return self.typeName()

#     @staticmethod
#     def typeName():
#         return 'fme_manager'

#     def checkValueIsAcceptable(self, value, context=None):
#         return True

#     def valueAsPythonString(self, value, context):
#         return str(value)

#     def asScriptCode(self):
#         raise NotImplementedError()

#     @classmethod
#     def fromScriptCode(cls, name, description, isOptional, definition):
#         raise NotImplementedError()