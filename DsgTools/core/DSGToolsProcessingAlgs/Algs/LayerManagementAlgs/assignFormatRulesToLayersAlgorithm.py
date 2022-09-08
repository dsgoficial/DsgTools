# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-06-23
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import json
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QColor
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
                       QgsProcessingParameterString,
                       QgsConditionalStyle,
                       QgsExpression)

from operator import itemgetter
from collections import defaultdict
import fnmatch

class AssignFormatRulesToLayersAlgorithm(QgsProcessingAlgorithm):
    INPUT_LAYERS = 'INPUT_LAYERS'
    FILE = 'FILE'
    TEXT = 'TEXT'
    CLEAN_BEFORE_ASSIGN = 'CLEAN_BEFORE_ASSIGN'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr("Input layers")
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.TEXT,
                description =  self.tr('Input json text'),
                multiLine = True,
                defaultValue = '{}',
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.FILE,
                description = self.tr('JSON File with rules'),
                behavior=QgsProcessingParameterFile.File,
                fileFilter='JSON (*.json)',
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.CLEAN_BEFORE_ASSIGN,
                self.tr('Clean before assign format rules')
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
        inputLyrList = [lyr for lyr in inputLyrList if lyr.dataProvider().name() == 'postgres']
        if not inputLyrList:
            return {}
        
        inputData = self.loadRulesFromFile(parameters, context)
        cleanBefore = self.parameterAsBool(
            parameters,
            self.CLEAN_BEFORE_ASSIGN,
            context
            )
        if cleanBefore:
            self.cleanRules(inputLyrList)
            self.cleanExpressionField(inputLyrList)
        listSize = len(inputLyrList)
        stepSize = 100/listSize if listSize else 0
        inputLyrNamesWithSchemaList = [
            f"{lyr.dataProvider().uri().schema()}.{lyr.dataProvider().uri().table()}" for lyr in inputLyrList
        ]
        self.ruleDict = self.buildRuleDict(inputData, inputLyrNamesWithSchemaList)

        for current, lyr in enumerate(inputLyrList):
            if feedback.isCanceled():
                break
            self.addRuleToLayer(lyr, feedback=feedback)
            self.createRuleVirtualField(lyr)
            feedback.setProgress(current * stepSize)
        return {}


    def loadRulesFromFile(self, parameters, context):
        inputText = json.loads(
            self.parameterAsString(
                parameters,
                self.TEXT,
                context
            )
        )
        if inputText != {}:
            return inputText
        inputFile = self.parameterAsFile(
            parameters,
            self.FILE,
            context,
        )
        
        with open(inputFile, 'r') as f:
            rulesData = json.load(f)
        return rulesData

    def buildRuleDict(self, inputData, inputLyrNamesWithSchemaList):
        ruleDict = defaultdict(lambda: defaultdict(list))
        styleDict = {
            style["tipo_estilo"]: {
                "corRgb": list(map(int, style["cor_rgb"].split(","))),
                "rank": idx
            } for idx, style in enumerate(inputData["grupo_estilo"])
        }
        for rule in inputData["regras"]:
            lyrSet = self.getLayerNames(rule["camadas"], inputLyrNamesWithSchemaList)
            ruleItem = rule.copy()
            ruleItem.update(styleDict[rule["tipo_estilo"]])
            for lyr in lyrSet:
                ruleDict[lyr][rule["atributo"]].append(ruleItem)
            for lyr in ruleDict:
                for attribute in ruleDict[lyr]:
                    ruleDict[lyr][attribute] = sorted(
                        ruleDict[lyr][attribute],
                        key=itemgetter('rank'),
                        reverse=False
                    ) #reverses the list so that it is already in the right order
        return ruleDict
    
    def getLayerNames(self, filterList, nameList):
        outputSet = set()
        wildCardFilterList = [filterItem for filterItem in filterList if "*" in filterItem]
        for wildCardFilter in wildCardFilterList:
            outputSet = outputSet.union(set(fnmatch.filter(nameList, wildCardFilter)))
        outputSet = outputSet.union(set(name for name in nameList if name in filterList))
        return outputSet


    def addRuleToLayer(self, lyr, feedback=None):
        key = f"{lyr.dataProvider().uri().schema()}.{lyr.dataProvider().uri().table()}"
        for field in lyr.fields():
            if feedback is not None and feedback.isCanceled():
                break
            if key not in self.ruleDict or \
                field.name() not in self.ruleDict[key]:
                continue
            fieldStyleList = [
                self.createConditionalStyle(i) for i in self.ruleDict[key][field.name()]
            ]
            lyr.conditionalStyles().setFieldStyles(
                field.name(),
                fieldStyleList
            )

    def createConditionalStyle(self, data):
        """
        data: {
            'descricao' : 'descricao da regra',
            'regra' : 'regra condicional',
            'corRgb' : 'cor da regra'
        }
        Returns a QgsConditionalStyle
        """
        conditionalStyle = QgsConditionalStyle()
        conditionalStyle.setName(data['descricao'])
        conditionalStyle.setRule(data['regra'])
        conditionalStyle.setBackgroundColor(
            QColor(
                data['corRgb'][0],
                data['corRgb'][1],
                data['corRgb'][2]
            ) 
        )
        if not conditionalStyle.isValid():
            raise Exception(f"Invalid conditional style: \n{data['descricao']}\n{data['regra']}")
        return conditionalStyle
    
    def createRuleVirtualField(self, lyr):
        expressionString = """CASE\n"""
        key = f"{lyr.dataProvider().uri().schema()}.{lyr.dataProvider().uri().table()}"
        fieldNameList = [field.name() for field in lyr.fields()]
        ruleList = []
        for fieldName, dataList in self.ruleDict[key].items():
            if fieldName not in fieldNameList:
                continue
            ruleList += dataList
        sortedRuleList = sorted(
            ruleList,
            key=itemgetter('rank', 'atributo'),
            reverse=False
        )
        for data in sortedRuleList:
            fieldName = data['atributo']
            expressionString += """WHEN {condition} THEN '{result}'\n""".format(
                condition=data['regra'],
                result=data['descricao']
            )
            if not self.expressionHasParseError(expressionString):
                raise Exception(f"Error while trying to apply rule:\n {data}\ncurrent field: {fieldName}\ncurrent layer name: {key}")
        expressionString += """ELSE ''\nEND"""
        if expressionString == "CASE\nELSE ''\nEND": ## did not apply any rule
            return
        expression = QgsExpression(expressionString)
        if expression.hasParserError():
            raise Exception(
                f"Invalid expression: \n{expressionString}"
            )
        lyr.addExpressionField(
            expressionString,
            QgsField(
                'attribute_error_description',
                QVariant.String
            )
        )
    
    def expressionHasParseError(self, expressionString):
        expr = expressionString if """ELSE ''\nEND""" in expressionString else expressionString + """ELSE ''\nEND"""
        expression = QgsExpression(expr)
        return expression.isValid()

    def cleanRules(self, inputLayerList):
        for lyr in inputLayerList:
            for field in lyr.fields():
                lyr.conditionalStyles().setFieldStyles(field.name(), [])
    
    def cleanExpressionField(self, inputLayerList):
        for lyr in inputLayerList:
            errorDescriptionIndex = -1
            for idx, field in enumerate(lyr.fields()):
                if field.name() == 'attribute_error_description':
                    errorDescriptionIndex = idx
                    break
            if errorDescriptionIndex != -1:
                lyr.removeExpressionField(errorDescriptionIndex)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'assignformatrulestolayersalgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Assign Format Rules to Layers')

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
        return QCoreApplication.translate('AssignFormatRulesToLayersAlgorithm', string)

    def createInstance(self):
        return AssignFormatRulesToLayersAlgorithm()
