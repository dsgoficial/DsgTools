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


class AssignAliasesToLayersAlgorithm(RuleStatisticsAlgorithm):

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
        listSize = len(inputLyrList)
        stepSize = 100/listSize if listSize else 0
        aliasDict = self.buildAliasDict(input_data)

        for current, lyr in enumerate(inputLyrList):
            if feedback.isCanceled():
                break
            layerName = lyr.name()
            for idx, field in enumerate(lyr.fields()):
                if feedback.isCanceled() or layerName not in aliasDict:
                    break
                fieldName = field.name()
                if fieldName in aliasDict[layerName]['attributeAlias']:
                    lyr.setFieldAlias(
                        idx,
                        aliasDict[layerName]['attributeAlias'][fieldName]
                    )
            if layerName in aliasDict:
                lyr.setLayerName(aliasDict[layerName]['layerAlias'])
            feedback.setProgress(current * stepSize)

        return {}

    def buildAliasDict(self, input_data):
        """
        atividade.camadas é um array de dict que tem os atributos "nome", "alias", "atributos".
        "atributos" é um array de dict com atributos "nome" e "alias"
        """
        input_data = input_data[0] if isinstance(input_data, list) else input_data
        aliasDict = dict()
        for data in input_data:
            attributeAliasDict = defaultdict(lambda: defaultdict(list))
            attributeAliasDict['layerAlias'] = data['alias']
            attributeAliasDict['attributeAlias'] = {i['nome']:i['alias'] for i in data['atributos']}
            aliasDict[data['nome']] = attributeAliasDict
        return aliasDict

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'AssignAliasesToLayersAlgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Assign Aliases to Layers')

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
        return QCoreApplication.translate('AssignAliasesToLayersAlgorithm', string)

    def createInstance(self):
        return AssignAliasesToLayersAlgorithm()
