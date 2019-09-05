# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-09-03
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
                       QgsConditionalStyle)

from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.ruleStatisticsAlgorithm import \
    RuleStatisticsAlgorithm
from operator import itemgetter
from collections import defaultdict


class AssignFormFormatRulesToLayersAlgorithm(RuleStatisticsAlgorithm):
    CLEAN_BEFORE_ASSIGN = 'CLEAN_BEFORE_ASSIGN'

    def initAlgorithm(self, config=None):
        super(AssignFormFormatRulesToLayersAlgorithm, self).initAlgorithm(config=config)
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
            self.INPUTLAYERS,
            context
        )
        if not inputLyrList:
            return {}
        input_data = self.load_rules_from_parameters(parameters)
        cleanBefore = self.parameterAsBool(
            parameters,
            self.CLEAN_BEFORE_ASSIGN,
            context
            )
        if cleanBefore:
            self.cleanRules(inputLyrList)
        listSize = len(inputLyrList)
        stepSize = 100/listSize if listSize else 0
        ruleDict = self.buildRuleDict(input_data)

        for current, lyr in enumerate(inputLyrList):
            if feedback.isCanceled():
                break
            for field in lyr.fields():
                if feedback.isCanceled():
                    break
                self.addRuleToLayer(lyr, field, ruleDict)
            feedback.setProgress(current * stepSize)

        return {}

    def buildRuleDict(self, input_data):
        input_data = input_data[0] if isinstance(input_data, list) else input_data
        sortedRuleList = sorted(
            input_data.values(),
            key=itemgetter('camada', 'atributo', 'ordem'),
            reverse=False
        )
        ruleDict = defaultdict(
            lambda: defaultdict(list)
        )
        for data in sortedRuleList:
            ruleDict[data['camada']][data['atributo']].append(data)
        return ruleDict

    def addRuleToLayer(self, lyr, field, ruleDict):
        data = ruleDict[lyr.name()][field.name()]
        if not data:
            return
        fieldStyleList = [self.createConditionalStyle(i) for i in data if i['tipo_regra'] == 'Atributo']
        rowStyleList = [self.createConditionalStyle(i) for i in data if i['tipo_regra'] != 'Atributo']
        if fieldStyleList:
            lyr.conditionalStyles().setFieldStyles(
                field.name(),
                fieldStyleList
            )
        elif rowStyleList:
            lyr.conditionalStyles().setRowStyes(rowStyleList)

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
        return conditionalStyle

    def cleanRules(self, inputLayerList):
        for lyr in inputLayerList:
            for field in lyr.fields():
                lyr.conditionalStyles().setFieldStyles(field.name(), [])

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'assignformformatrulestolayersalgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Assign Form Format Rules to Layers')

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
        return QCoreApplication.translate('AssignFormFormatRulesToLayersAlgorithm', string)

    def createInstance(self):
        return AssignFormFormatRulesToLayersAlgorithm()
