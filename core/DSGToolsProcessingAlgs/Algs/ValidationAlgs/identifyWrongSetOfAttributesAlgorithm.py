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

from PyQt5.QtCore import QCoreApplication
import json
from qgis.core import (QgsProcessing,
                       QgsProcessingException,
                       QgsFeatureSink,
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

class IdentifyWrongSetOfAttributesAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    RULEFILE = 'RULEFILE'
    RULEDATA = 'RULEDATA'
    SELECTED = 'SELECTED'
    FLAGS = 'FLAGS'

    

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
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
                self.FLAGS,
                self.tr('{0} Flags').format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUT, context)
        if inputLyrList is None or inputLyrList == []:
            raise QgsProcessingException(self.invalidSourceError(
                parameters, self.INPUT))
        rulePath = self.parameterAsFile(parameters, self.RULEFILE, context)
        inputData = self.loadRulesData(rulePath)

        for ruleName in inputData:
            for lyr in inputLyrList:
                loadedLyrName = lyr.name()
                if loadedLyrName in inputData[ruleName]:
                    #print(loadedLyrName+",", list(ruleData.keys())[0])
                    rules = inputData[ruleName][loadedLyrName]['allRules']
                    #print(rules)
                    for rule in rules:
                        sel = lyr.selectByExpression(rule)
                        self.flagFeature(sel.geometry(), inputData[ruleName])
                        count = lyr.selectedFeatureCount()
                        #print(count)
                        lyr.removeSelection()
                        if count != 0:
                            failed = inputData[ruleName][loadedLyrName]['failed']
                            failed+=1
        return {self.FLAGS: self.flag_id}
        

    def loadRulesData(self, path):
        with open(path, 'r') as jsonFile:
            ruleDict = json.load(jsonFile)
        return ruleDict
     
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
