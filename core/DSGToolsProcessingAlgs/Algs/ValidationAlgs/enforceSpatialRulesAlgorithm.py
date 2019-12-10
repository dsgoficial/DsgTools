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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessingContext,
                       QgsProcessingException,
                       QgsProcessingParameterType,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterFeatureSink)

from DsgTools.core.GeometricTools.spatialRelationsHandler import SpatialRelationsHandler
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import ValidationAlgorithm

class EnforceSpatialRulesAlgorithm(ValidationAlgorithm):
    RULES_SET = "RULES_SET"
    POINT_FLAGS = "POINT_FLAGS"
    LINE_FLAGS = "LINE_FLAGS"
    POLYGON_FLAGS = "POLYGON_FLAGS"

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

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POINT_FLAGS,
                self.tr('{0} flags (points)').format(self.displayName())
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.LINE_FLAGS,
                self.tr('{0} flags (lines)').format(self.displayName())
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POLYGON_FLAGS,
                self.tr('{0} flags (polygons)').format(self.displayName())
            )
        )

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

    def setFlags(self, rule, flags, ctx, feedback):
        """
        :param rule: (dict) a map to checked rule's attributes.
        :param flags: (dict) a map from offended feature ID to offenders
                      feature set.
        :param ctx: (QgsProcessingContext) context in which processing was run.
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking
                         component.
        :return: (?)
        """
        text = self.tr(
            "Rule {name} offended: feature {{fidA}} ({layerA}) {predicate} "
            "{{count}} feature(s) from {layerB}"
        ).format(**rule)

    def validateRules(self, ruleDict):
        """
        Verifies whether given rule set is valid/applicable.
        :param ruleDict: (dict) rules to be checked.
        :return: (bool) rules validity status
        """
        # TODO
        return True

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        rules = self.parameterAsSpatialRulesSet(
            parameters, self.RULES_SET, context
        )
        if not rules or self.validateRuleSet(rules):
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.RULES_SET)
            )
        pointFlags = self.parameterAsLayer(parameters, self.POINT_FLAGS, context)
        if not pointFlags:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.POINT_FLAGS)
            )
        lineFlags = self.parameterAsLayer(parameters, self.LINE_FLAGS, context)
        if not lineFlags:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.LINE_FLAGS)
            )
        polygonFlags = self.parameterAsLayer(parameters, self.POLYGON_FLAGS, context)
        if not polygonFlags:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.POLYGON_FLAGS)
            )
        flagsDict = SpatialRelationsHandler().enforceRules(
            rules, context, feedback
        )
        # set flags to their layers accordingly to its geometry
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
