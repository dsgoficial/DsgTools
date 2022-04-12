# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import (QCoreApplication, QVariant)
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSink,
                       QgsCoordinateReferenceSystem,
                       QgsProcessingParameterMultipleLayers,
                       QgsFeatureRequest,
                       QgsFeature,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterVectorLayer,
                       QgsField,
                       QgsFields,
                       QgsWkbTypes
                       )
from qgis import processing
from qgis.utils import iface
import csv
import concurrent.futures
import os

class UnicodeFilterAlgorithm(QgsProcessingAlgorithm): 

    INPUT_LAYERS = 'INPUT_LAYER_LIST'
    OUTPUT1 = 'OUTPUT1'
    OUTPUT2 = 'OUTPUT2'
    OUTPUT3 = 'OUTPUT3'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                'INPUT_LAYER_LIST',
                self.tr('Selecionar camadas'),
                QgsProcessing.TypeVectorAnyGeometry
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT1,
                self.tr('Flag - unicode não permitido (ponto)')
            )
        ) 
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT2,
                self.tr('Flag - unicode não permitido (linha)')
            )
        ) 
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT3,
                self.tr('Flag - unicode não permitido (área)')
            )
        ) 

    def processAlgorithm(self, parameters, context, feedback):      
        feedback.setProgressText('Verificando unicodes...')
        layerList = self.parameterAsLayerList(parameters,'INPUT_LAYER_LIST', context)
        whitelist = self.getWhitelist(self.getCsvFilePath())
        listSize = len(layerList)
        progressStep = 100/listSize if listSize else 0
        step = 0
        flags = {}

        def checkUnicode(layer):
            featuresNotApproved = []
            for feature in layer.getFeatures():
                for attribute in feature.attributes():
                    for char in attribute:
                        if hex(ord(char))[2:].lower().rjust(4, '0') in whitelist:
                            continue
                        featuresNotApproved.append(feature)
                        break
                    else:
                        continue
                    break
                else:
                    continue
                break
            flags[layer.geometryType()] += featuresNotApproved

        pool = concurrent.futures.ThreadPoolExecutor(os.cpu_count()-1)
        futures = set()
        for step, layer in enumerate(layerList):
            if not(layer.geometryType() in flags):
                flags[layer.geometryType()] = []
            futures.add(pool.submit(checkUnicode, layer))
        concurrent.futures.wait(futures, timeout=None, return_when=concurrent.futures.ALL_COMPLETED)
        
        output = {self.OUTPUT1: '', self.OUTPUT2: '', self.OUTPUT3: ''}
        for geometryType in flags:
            features = flags[geometryType]
            if len(features) == 0:
                continue
            if geometryType == QgsWkbTypes.PointGeometry:
                out = self.OUTPUT1 
                wkbType = QgsWkbTypes.MultiPoint
            elif geometryType == QgsWkbTypes.LineGeometry:
                out = self.OUTPUT2
                wkbType = QgsWkbTypes.MultiLineString
            elif geometryType == QgsWkbTypes.PolygonGeometry:
                out = self.OUTPUT3
                wkbType = QgsWkbTypes.MultiPolygon
            flagLayer = self.outLayer(parameters, context, out, features, wkbType)
            output[out] = flagLayer
            
        return output
  
    def outLayer(self, parameters, context, output, features, geomType):
        CRSstr = iface.mapCanvas().mapSettings().destinationCrs().authid()
        CRS = QgsCoordinateReferenceSystem(CRSstr)
        newField = QgsFields()
        newField.append(QgsField('id', QVariant.Int))
        #newField.append(QgsField('nome_da_camada', QVariant.String))
        (sink, newLayer) = self.parameterAsSink(
            parameters,
            output,
            context,
            newField,
            geomType,
            CRS
        )
        for idx, feature in enumerate(features):
            onlyfeature = feature[0]
            newFeat = QgsFeature()
            newFeat.setGeometry(feature.geometry())
            newFeat.setFields(newField)
            newFeat['id'] = idx
            sink.addFeature(newFeat, QgsFeatureSink.FastInsert)
        return newLayer

    def getWhitelist(self, csvFilePath):
        whitelist = []
        with open(csvFilePath, newline = '') as csvFile:
            table = csv.reader(csvFile, delimiter = ',', quotechar='"')
            for row in table:
                whitelist.append(row[0].lower())
        return whitelist

    def getCsvFilePath(self):
        return os.path.join(
            os.path.abspath(os.path.join(
                os.path.dirname(__file__)
            )),
            'data',
            'unicode-whitelist.csv'
        )
                
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return UnicodeFilterAlgorithm()

    def name(self):
        return 'unicodefilter'

    def displayName(self):
        return self.tr('Identifica Feições que contém unicode não permitido')

    def group(self):
        return self.tr('Other Algorithms')

    def groupId(self):
        return 'DSGTools: Other Algorithms'

    def shortHelpString(self):
        return self.tr("O algoritmo identifica se existe algum atributo com um unicode que não está na whitelist")
    
