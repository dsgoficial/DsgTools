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
from qgis.core import (
    QgsProject,
    QgsFeature,
    QgsWkbTypes,
    QgsFeatureSink,
    QgsProcessingException,
    QgsProcessingParameterType,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterFeatureSink,
)

from DsgTools.core.GeometricTools.spatialRelationsHandler import (
    SpatialRule,
    SpatialRelationsHandler,
)
from DsgTools.core.GeometricTools.featureHandler import FeatureHandler
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from ..Help.algorithmHelpCreator import HTMLHelpCreator as help


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
            self.RULES_SET, description=self.tr("Spatial rules set")
        )
        spatialRulesSetter.setMetadata(
            {
                "widget_wrapper": "DsgTools.gui.ProcessingUI.enforceSpatialRuleWrapper.EnforceSpatialRuleWrapper"
            }
        )
        self.addParameter(spatialRulesSetter)

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.POINT_FLAGS, self.tr("Point flags"))
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.LINE_FLAGS, self.tr("Linestring flags")
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POLYGON_FLAGS, self.tr("Polygon flags")
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
        return "enforcespatialrules"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Enforce spatial rules")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Object Proximity and Relationships")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Object Proximity and Relationships"

    def tr(self, string):
        return QCoreApplication.translate("EnforceSpatialRulesAlgorithm", string)

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    def helpUrl(self):
        return help().helpUrl(self.name())

    def createInstance(self):
        return EnforceSpatialRulesAlgorithm()

    def setFlags(self, flagDict, ptLayer, lLayer, polLayer):
        """
        Saves each flag to its layer, accordingly to its geometry primitive.
        :param flags: (dict) a map from offended feature ID to offenders
                      feature set.
        :return: (tuple-of-QgsVectorLayer) filled flag layers.
        """
        fh = FeatureHandler()
        gh = GeometryHandler()
        fields = self.getFlagFields()
        layerMap = {
            QgsWkbTypes.PointGeometry: ptLayer,
            QgsWkbTypes.LineGeometry: lLayer,
            QgsWkbTypes.PolygonGeometry: polLayer,
        }
        for ruleName, flags in flagDict.items():
            flagText = self.tr('Rule "{name}" broken: {{text}}').format(name=ruleName)
            for flagList in flags.values():
                for flag in flagList:
                    geom = flag["geom"]
                    for g in gh.multiToSinglePart(geom):
                        newFeature = QgsFeature(fields)
                        newFeature["reason"] = flagText.format(text=flag["text"])
                        newFeature.setGeometry(g)
                        layerMap[g.type()].addFeature(
                            newFeature, QgsFeatureSink.FastInsert
                        )
        return (ptLayer, lLayer, polLayer)

    def validateRuleSet(self, ruleList):
        """
        Verifies whether there is at least one valid/applicable rule on the
        input list of rules.
        :param ruleList: (list-of-SpatialRule) rules to be checked.
        :return: (bool) rules validity status
        """
        return any((r.isValid(checkLoaded=True) for r in ruleList))

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        rules = self.parameterAsSpatialRulesSet(parameters, self.RULES_SET, context)
        # GUI was crashing when the SpatialRule was passed...
        rules = [SpatialRule(**r, checkLoadedLayer=False) for r in rules]
        rules = list(filter(lambda x: x.isValid(checkLoaded=True) is True, rules))
        if not rules:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.RULES_SET)
            )
        flagFields = self.getFlagFields()
        crs = QgsProject.instance().crs()
        pointFlags, ptId = self.parameterAsSink(
            parameters, self.POINT_FLAGS, context, flagFields, QgsWkbTypes.Point, crs
        )
        if not pointFlags:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.POINT_FLAGS)
            )
        lineFlags, lId = self.parameterAsSink(
            parameters,
            self.LINE_FLAGS,
            context,
            flagFields,
            QgsWkbTypes.LineString,
            crs,
        )
        if not lineFlags:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.LINE_FLAGS)
            )
        polygonFlags, polId = self.parameterAsSink(
            parameters,
            self.POLYGON_FLAGS,
            context,
            flagFields,
            QgsWkbTypes.Polygon,
            crs,
        )
        if not polygonFlags:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.POLYGON_FLAGS)
            )
        # marked as 5 steps because I *arbitrarily* set the rule enforcing
        # steps to be 4:1 to the flag layers creation
        flagsDict = SpatialRelationsHandler().enforceRules(rules, context, feedback)
        self.setFlags(flagsDict, pointFlags, lineFlags, polygonFlags)
        return {self.POINT_FLAGS: ptId, self.LINE_FLAGS: lId, self.POLYGON_FLAGS: polId}


class ParameterSpatialRulesSetType(QgsProcessingParameterType):
    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterSpatialRulesSet(name)

    def metadata(self):
        return {
            "widget_wrapper": "DsgTools.gui.ProcessingUI.enforceSpatialRuleWrapper.EnforceSpatialRuleWrapper"
        }

    def name(self):
        return QCoreApplication.translate("Processing", "Spatial Rules Set")

    def id(self):
        return "spatial_rules_set_type"

    def description(self):
        return QCoreApplication.translate(
            "Processing", "Set of spatial rules. Used on Spatial Rules Checker."
        )


class ParameterSpatialRulesSet(QgsProcessingParameterDefinition):
    def __init__(self, name, description=""):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterSpatialRulesSet(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return "spatial_rules_set"

    def checkValueIsAcceptable(self, value, context=None):
        return value is not None

    def valueAsPythonString(self, value, context):
        return str(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()
