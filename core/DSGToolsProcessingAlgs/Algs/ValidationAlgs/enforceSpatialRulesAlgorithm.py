# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-11-14
        git sha              : $Format:%H$
        copyright            : (C) 2019 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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

import os
from time import sleep

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProject,
                       QgsVectorLayer,
                       QgsProcessingContext,
                       QgsProcessingException,
                       QgsProcessingParameterType,
                       QgsProcessingParameterDefinition)

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import ValidationAlgorithm

class EnforceSpatialRulesAlgorithm(ValidationAlgorithm):
    RULES_SET = 'RULES_SET'
    # a map to canvas layers, reset every time alg is asked to be run: make
    # reusage of layers available for each cycle, reducing re-reading time 
    __layers = dict()

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        spatialRulesSetter = ParameterSpatialRulesSet(
            self.RULES_SET,
            description=self.tr('Spatial Rules Set')
        )
        spatialRulesSetter.setMetadata({
            'widget_wrapper' : 'DsgTools.gui.ProcessingUI.enforceSpatialRuleWrapper.EnforceSpatialRuleWrapper'
        })
        self.addParameter(spatialRulesSetter)

    def parameterAsSpatialRulesSet(self, parameters, name, context):
        return parameters[name]

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'enforcespatialrules'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Enforce Spatial Rules')

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
        return QCoreApplication.translate('EnforceSpatialRulesAlgorithm', string)

    def createInstance(self):
        return EnforceSpatialRulesAlgorithm()

    def setupLayer(self, layername, expression, context=None, feedback=None):
        """
        Reads layer from canvas and applies the filtering expression.
        :param layername: (str) layer to be setup.
        :param expression: (str) filtering expression to be applied to the
                           target layer.
        :param context: (QgsProcessingContext) environment context in which 
                        layer is retrieved and setup.
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking
                         component.
        :return: (QgsVectorLayer) vector layer ready to be 
        """
        
        if layername not in self.__layers:
            # by default, it is assumed layer names are unique on canvas
            vl = QgsProject.instance().mapLayersByName(layername)
            if not vl:
                raise QgsProcessingException(
                    self.tr("Layer {l} was not found!").format(l=layername)
                )
            # layer caching happens here
            self.__layers[layername] = vl[0]
        vl = self.__layers[layername]
        if expression:
            vl = AlgRunner().runFilterExpression(
                vl,
                expression,
                context or QgsProcessingContext(),
                outputLyr='memory:',
                feedback=feedback
            )
        return vl

    def verifyTopologicalRelation(self, predicate, layerA, layerB, cardinality):
        """
        
        """
        pass

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        rules = self.parameterAsSpatialRulesSet(
            parameters, self.RULES_SET, context
        )
        for rule in rules:
            name = rule["name"]
            out = self.verifyTopologicalRelation(
                rule["predicate"],
                self.setupLayer(rule["layer_a"], rule["filter_a"]),
                self.setupLayer(rule["layer_b"], rule["filter_b"]),
                rule["cardinality"] 
            )
        # dont forget to clear cached layers
        del self.__layers
        self.__layers = dict()
        return {}

class ParameterSpatialRulesSetType(QgsProcessingParameterType):

    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterSpatialRulesSet(name)

    def metadata(self):
        return {'widget_wrapper': 'DsgTools.gui.ProcessingUI.enforceSpatialRuleWrapper.EnforceSpatialRuleWrapper'}

    def name(self):
        return QCoreApplication.translate('Processing', 'Spatial Rules Set')

    def id(self):
        return 'spatial_rules_set_type'

    def description(self):
        return QCoreApplication.translate('Processing', 'Set of spatial rules. Used on Spatial Rules Checker.')

class ParameterSpatialRulesSet(QgsProcessingParameterDefinition):

    def __init__(self, name, description=''):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterSpatialRulesSet(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return 'spatial_rules_set'

    def checkValueIsAcceptable(self, value, context=None):
        return True

    def valueAsPythonString(self, value, context):
        return str(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()
