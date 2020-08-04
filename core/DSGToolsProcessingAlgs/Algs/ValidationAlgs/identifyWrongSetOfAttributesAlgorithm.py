# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2020-07-27
        git sha              : $Format:%H$
        copyright            : (C) 2020 by  Francisco Alves Camello Neto - Surveying Technician @ Brazilian Army
        email                : camello.francisco@eb.mil.br
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

from qgis.PyQt.QtCore import QCoreApplication, QVariant
import json
from qgis.core import (QgsProcessing,
                       QgsProcessingException,
                       QgsFeatureSink,
                       QgsField,
                       QgsFields,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsFeature,
                       QgsDataSourceUri,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterString,
                       QgsWkbTypes,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterMultipleLayers,
                       QgsWkbTypes,
                       QgsProcessingUtils,
                       QgsJsonUtils,
                       QgsProject,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFile)

from .validationAlgorithm import ValidationAlgorithm
from ....GeometricTools.layerHandler import LayerHandler
from ....GeometricTools.geometryHandler import GeometryHandler

class IdentifyWrongSetOfAttributesAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    RULEFILE = 'RULEFILE'
    RULEDATA = 'RULEDATA'
    SELECTED = 'SELECTED'
    POINT_FLAGS = 'POINT_FLAGS'
    LINE_FLAGS = 'LINE_FLAGS'
    POLYGON_FLAGS = 'POLYGON_FLAGS'


    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.valAlg = ValidationAlgorithm()

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT,
                self.tr('Input layers:'),
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.RULEFILE,
                self.tr('JSON rules file:'),
                defaultValue = '.json'
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.RULEDATA,
                description =  self.tr('JSON formatted rules:'),
                multiLine = True,
                defaultValue = '{}'
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POINT_FLAGS,
                self.tr('Point Flags')
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.LINE_FLAGS,
                self.tr('Linestring Flags')
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POLYGON_FLAGS,
                self.tr('Polygon Flags')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUT, context)
        #inputLyrList = layerHandler.getFeatureList(self.INPUT)
        if inputLyrList is None or inputLyrList == []:
            raise QgsProcessingException(self.invalidSourceError(
                parameters, self.INPUT))
        
        flagFields = self.valAlg.getFlagFields()
        crs = QgsProject.instance().crs()
        pointFlags, ptId = self.parameterAsSink(
                parameters, self.POINT_FLAGS, context,
                flagFields, QgsWkbTypes.Point, crs
        )
        if not pointFlags:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.POINT_FLAGS)
            )
        lineFlags, lId = self.parameterAsSink(
                parameters, self.LINE_FLAGS, context,
                flagFields, QgsWkbTypes.LineString, crs
        )
        if not lineFlags:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.LINE_FLAGS)
            )
        polygonFlags, polId = self.parameterAsSink(
                parameters, self.POLYGON_FLAGS, context,
                flagFields, QgsWkbTypes.Polygon, crs
        )
        if not polygonFlags:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.POLYGON_FLAGS)
            )
        
        rulePath = self.parameterAsFile(parameters, self.RULEFILE, context)
        inputData = self.loadRulesData(rulePath)
        failedFeatures = self.checkedFeatures(inputData, inputLyrList)
        flags = self.flagsFromFailedList(failedFeatures, pointFlags, lineFlags,
            polygonFlags, context, feedback
        )
        return {
            self.POINT_FLAGS: ptId,
            self.LINE_FLAGS: lId,
            self.POLYGON_FLAGS: polId
        }

    def loadRulesData(self, path):
        with open(path, 'r') as jsonFile:
            ruleDict = json.load(jsonFile)
        return ruleDict

    def checkedFeatures(self, rules, layerList):
        
        failedDict = {}
        for ruleName in rules:
            failedList = []
            for lyr in layerList:
                loadedLyrName = lyr.name()
                if loadedLyrName in rules[ruleName]:
                    allRules = rules[ruleName][loadedLyrName]['allRules']
                    for rule in allRules:
                        lyr.selectByExpression(rule)
                        failedList+=[feat for feat in lyr.selectedFeatures()]
                        lyr.removeSelection()
            failedDict[ruleName] = failedList
            
                      
        return failedDict

    def flagsFromFailedList(self, featureDict, ptLayer, lLayer, polLayer, ctx, feedback):
        fields = QgsFields()
        fields.append(QgsField('reason',QVariant.String))
        layerMap = {
            QgsWkbTypes.PointGeometry: ptLayer,
            QgsWkbTypes.LineGeometry: lLayer,
            QgsWkbTypes.PolygonGeometry: polLayer
        }
        
        for ruleName, flagList in featureDict.items():
            flagText = self.tr('Rule "{name}" broken: {{text}}').format(
                name = ruleName
            )  
            for flag in flagList:
                geom = flag.geometry()
                flag.setFields(fields)
                #for g in GeometryHandler.multiToSinglePart(geom):
                newFeature = QgsFeature(fields)
                newFeature["reason"] = flagText
                newFeature.setGeometry(geom)
                layerMap[geom.type()].addFeature(
                    newFeature, QgsFeatureSink.FastInsert
                )
                print("texto")
            
        return (ptLayer, lLayer, polLayer)
     
    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifywrongsetofattributesalgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Wrong Sets of Attributes')

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
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('IdentifyWrongSetOfAttributesAlgorithm', string)

    def createInstance(self):
        """
        Must return a new copy of your algorithm.
        """
        return IdentifyWrongSetOfAttributesAlgorithm()
