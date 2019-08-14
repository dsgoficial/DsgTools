# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-08-x
        git sha              : $Format:%H$
        copyright            : (C) 2018 by  Jossan Costa - Surveying Technician @ Brazilian Army
        email                : jossan.costa@eb.mil.br
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
                       QgsProject,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFile)

class RuleStatisticsAlgorithm(QgsProcessingAlgorithm):
    INPUTLAYERS = 'INPUTLAYERS'
    RULEFILE = 'RULEFILE'
    RULEDATA = 'RULEDATA'
    OUTPUT = 'RESULT'

    def __init__(self):
        super(RuleStatisticsAlgorithm, self).__init__()

    def initAlgorithm(self, config=None):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUTLAYERS,
                'Camadas de entrada :'
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.RULEFILE,
                description = 'Arquivo ".json" com regras :',
                defaultValue = '.json'
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.RULEDATA,
                description =  'Regras no formato "json" :',
                multiLine = True,
                defaultValue = '{}'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layers_list = self.parameterAsLayerList(parameters, self.INPUTLAYERS, context)
        input_data = self.load_rules_from_parameters(parameters)
        for i, rules in enumerate(input_data):
            log  = self.get_statistic_rules(layers_list, rules)
            self.print_log(i, log, feedback)
        if not input_data:
            self.print_log('Carregue um arquivos com as Regras ou insira as Regras!', feedback)
            return {}
        return { self.OUTPUT : log}

    def print_log(self, number, text, feedback):
        feedback.pushInfo("{0}{1}LOG START - {2}{1}{0}\n\n".format('*'*10, ' '*3, number+1))
        feedback.pushInfo(text)
        feedback.pushInfo("{0}{1}LOG END - {2}{1}{0}\n\n".format('*'*10, ' '*3, number+1))
    
    def load_rules_from_parameters(self, parameters):
        rules_input = []
        rules_path = parameters[self.RULEFILE]
        rules_text = parameters[self.RULEDATA]
        if rules_path and rules_path != '.json':
            with open(rules_path, 'r') as f:
                rules_input.append(
                    json.load(f)
                )
        if rules_text and rules_text != '{}':
            rules_input.append(
                json.loads(rules_text)
            )
        return rules_input

    def get_statistic_rules(self, layers, rules_data): 
        rules_layers = self.get_rules_by_layers(layers, rules_data)
        self.check_rules_on_layers(rules_layers, layers)
        return self.format_output_result(rules_layers)

    def get_rules_by_layers(self, layers, rules_data):
        rules_layers = {}
        layers_name = [ l.name() for l in layers ]
        for i in rules_data:
            layer_name = rules_data[i]['camada']
            if layer_name in layers_name:
                rule_name_type = rules_data[i]['tipo_estilo']
                if not( rule_name_type in rules_layers ):
                    rules_layers[rule_name_type] = {}
                if not(layer_name in rules_layers[rule_name_type]):
                    rules_layers[rule_name_type][layer_name] = {
                        'all_rules' : [],
                        'failed' : 0
                    }
                rules_layers[rule_name_type][layer_name]['all_rules'].append(
                    rules_data[i]['regra']
                )
        return rules_layers
    
    def check_rules_on_layers(self, rules_layers, layers):
        for rule_name_type in rules_layers:
            for lyr in layers:
                layer_name = lyr.name()
                if layer_name in rules_layers[rule_name_type]:
                    rules = rules_layers[rule_name_type][layer_name]['all_rules']
                    for rule in rules:
                        lyr.selectByExpression(rule)
                        count = lyr.selectedFeatureCount()
                        lyr.removeSelection()
                        if count != 0:
                            rules_layers[rule_name_type][layer_name]['failed']+=1

    def format_output_result(self, rules_layers):
        html=""
        for rule_name_type in sorted(rules_layers):
            row = "[REGRAS] : {0}\n\n".format(rule_name_type)
            html += row
            layers_failed = []
            for layer_name in sorted(rules_layers[rule_name_type]):
                    failed = rules_layers[rule_name_type][layer_name]['failed']
                    layers_failed.append(layer_name) if failed != 0 else ''
            rows = ""
            if len(layers_failed) != 0:
                for layer_name in layers_failed:
                    rows += "{0}\n\n".format(layer_name)
            else:
                rows = "As camadas passaram em todas as regras.\n\n"
            html += rows
        return html
        
    def name(self):
        """
        Here is where the processing itself takes place.
        """
        return 'rulestatistics'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Rule Statistics')

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
        return QCoreApplication.translate('RuleStatisticsAlgorithm', string)

    def createInstance(self):
        return RuleStatisticsAlgorithm()
