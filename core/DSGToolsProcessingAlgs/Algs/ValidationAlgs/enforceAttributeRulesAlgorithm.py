# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2020-07-27
        git sha              : $Format:%H$
        copyright            : (C) 2020 by  Francisco Alves Camello Neto -
                                    Surveying Technician @ Brazilian Army
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

import processing
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QColor, QFont
from qgis.core import (QgsFeature,
                       QgsFeatureRequest,
                       QgsProject,
                       QgsWkbTypes,
                       QgsConditionalStyle,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingException,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterType,
                       QgsProcessingParameterDefinition)
from qgis.PyQt.QtWidgets import (QMessageBox)

from .validationAlgorithm import ValidationAlgorithm



class EnforceAttributeRulesAlgorithm(QgsProcessingAlgorithm):
    """
    Algorithm for applying user-defined attribute rules to
    verify the filling of database attributes.
    """

    RULES_SET = "RULES_SET"
    SELECTED = "SELECTED"
    POINT_FLAGS = "POINT_FLAGS"
    LINE_FLAGS = "LINE_FLAGS"
    POLYGON_FLAGS = "POLYGON_FLAGS"

    def __init__(self):
        """
        Constructor.
        """
        super().__init__()
        self.valAlg = ValidationAlgorithm()
        self.flagFields = self.valAlg.getFlagFields()
        self.font = QFont()
        self.font.setBold(True)
        self.conditionalStyle = QgsConditionalStyle()

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        attributeRulesSetter = ParameterAttributeRulesSet(
            self.RULES_SET,
            description=self.tr("Attribute Rules Set")
        )
        attributeRulesSetter.setMetadata({
            "widget_wrapper": "DsgTools.gui.ProcessingUI.enforceAttributeRulesWrapper.EnforceAttributeRulesWrapper"
        })
        self.addParameter(attributeRulesSetter)

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr("Process only selected features")
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POINT_FLAGS,
                self.tr("Point flags")
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.LINE_FLAGS,
                self.tr("Linestring flags")
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POLYGON_FLAGS,
                self.tr("Polygon flags")
            )
        )

    def parameterAsAttributeRulesSet(self, parameters, name, context):
        """
        Adds data from wrapper to algorithm parameters.
        :param parameters: (QgsProcessingParameter) a set of algorithm
            parameters;
        :param name: (json) JSON formatted attribute rules;
        :param context: (QgsProcessingContext) context in which
            processing was run;
        :return: (dict) parameters dictionary.
        """
        return parameters[name]

    def validateRuleSet(self, attrRulesMap):
        """
        Verifies whether given rule set is valid/applicable.
        :param ruleDict: (dict) rules to be checked;
        :return: (bool) rules validity status.
            0: valueMap["description"],
            1: valueMap["layerField"],
            2: valueMap["expression"],
            3: valueMap["errorType"],
            4: valueMap["color"]
        """
        return True

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        :param parameters: (QgsProcessingParameter) a set of algorithm
            parameters.
        :param context: (QgsProcessingContext) context in which
            processing was run.
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking
                         component.
        :return: (dict) filled flag layers.
        """

        rules = self.parameterAsAttributeRulesSet(
            parameters, self.RULES_SET, context
        )
        
        if not rules or not self.validateRuleSet(rules):
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.RULES_SET)
            )

        if self.validateRuleSet(rules):

            onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)

            crs = QgsProject.instance().crs()
            pointFlags, ptId = self.parameterAsSink(
                parameters, self.POINT_FLAGS, context,
                self.flagFields, QgsWkbTypes.Point, crs)

            if not pointFlags:
                raise QgsProcessingException(
                    self.invalidSourceError(parameters, self.POINT_FLAGS))

            lineFlags, lId = self.parameterAsSink(
                parameters, self.LINE_FLAGS, context,
                self.flagFields, QgsWkbTypes.LineString, crs)

            if not lineFlags:
                raise QgsProcessingException(
                    self.invalidSourceError(parameters, self.LINE_FLAGS))

            polygonFlags, polId = self.parameterAsSink(
                parameters, self.POLYGON_FLAGS, context,
                self.flagFields, QgsWkbTypes.Polygon, crs)

            if not polygonFlags:
                raise QgsProcessingException(
                    self.invalidSourceError(parameters, self.POLYGON_FLAGS))

            failedFeatures = self.applyAttrRules(rules, onlySelected)

            self.flagsFromFailedList(failedFeatures,
                                    pointFlags,
                                    lineFlags,
                                    polygonFlags,
                                    feedback)
            return {
                self.POINT_FLAGS: ptId,
                self.LINE_FLAGS: lId,
                self.POLYGON_FLAGS: polId}

    def applyAttrRules(self, attrRulesMap, onlySelected):
        """
        Filters a layer or a set of selected features as from conditional rules,
        and the result is added to a list in a dictionary.
        :param attrRulesMap: (dict) dictionary with conditional rules;
        :param onlySelected: (boolean) indicates whether the attribute rules
            should be applied exclusively on selected features of each
            verified layer;
        :return: (dict) modified attrRulesMap with filtered features.
        """
        proj = QgsProject.instance()

        for ruleOrder, ruleParam in attrRulesMap.items():
            if onlySelected:
                lyr = proj.mapLayersByName(ruleParam["layerField"][0])[0]
                request = QgsFeatureRequest().setFilterExpression(
                    ruleParam["expression"])
                selectedFeatures = lyr.getSelectedFeatures(request)
                ruleParam["features"] = [feature for feature in selectedFeatures]
            else:
                ruleParam["features"] = [
                    feature for feature in proj.mapLayersByName(
                        ruleParam["layerField"][0])[0].getFeatures(ruleParam["expression"])]
            self.applyConditionalStyle(proj.mapLayersByName(
                ruleParam["layerField"][0])[0], ruleParam)
        return attrRulesMap

    def flagsFromFailedList(self, attrRulesMap, ptLayer, lLayer, polLayer, feedback):
        """
        Creates new features from a failed conditional rules dictionary.
        :param attrRulesMap: (dict) dictionary with conditional rules;
        :param ptLayer: (QgsVectorLayer) output point vector layer;
        :param lLayer: (QgsVectorLayer) output line vector layer;
        :param polLayer: (QgsVectorLayer) output polygon vector layer;
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking
                         component;
        :return: (tuple-of-QgsVectorLayer) filled flag layers.
        """
        layerMap = {
            QgsWkbTypes.PointGeometry: ptLayer,
            QgsWkbTypes.LineGeometry: lLayer,
            QgsWkbTypes.PolygonGeometry: polLayer
        }

        for ruleParam in attrRulesMap.values():
            flagText = "{name}".format(name=ruleParam["description"])
            for flag in ruleParam["features"]:
                geom = flag.geometry()
                newFeature = QgsFeature(self.flagFields)
                newFeature["reason"] = flagText
                newFeature.setGeometry(geom)
                layerMap[geom.type()].addFeature(
                    newFeature, QgsFeatureSink.FastInsert
                )
        self.logResult(attrRulesMap, feedback)
        return (ptLayer, lLayer, polLayer)

    def applyConditionalStyle(self, lyr, values):
        """
        Applies a conditional style for each wrong attribute
        in the attribute table.
        :param lyr: (QgsVectorLayer) vector layer;
        :param values: (dict) dictionary with conditional rules.
        """
        self.conditionalStyle.setRule(values["expression"])
        self.conditionalStyle.setFont(self.font)
        self.conditionalStyle.setTextColor(QColor(255, 255, 255))

        for field in lyr.fields():
            if field.name() in values["layerField"]:
                if isinstance(values["color"], (list, tuple)):
                    self.conditionalStyle.setBackgroundColor(
                        QColor(
                            values["color"][0],
                            values["color"][1],
                            values["color"][2]))
                else:
                    self.conditionalStyle.setBackgroundColor(
                        QColor(values["color"]))

                lyr.conditionalStyles().setFieldStyles(
                    field.name(), [self.conditionalStyle])

    def logResult(self, attrRulesMap, feedback):
        """
        Creates a statistics text log from each layer and your
        respectively wrong attribute.
        :param attrRulesMap: (dict) dictionary with conditional rules;
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking
                         component.
        """
        feedback.pushInfo("{0} {1} {0}\n".format(
            "===" * 5, self.tr("LOG START")))

        for ruleParam in attrRulesMap.values():
            if len(ruleParam["features"]) > 0:
                row = self.tr("[RULE]") + ": {0} - {1}\n{2}: {3} {4}\n".format(
                    ruleParam["layerField"][1],
                    ruleParam["errorType"],
                    ruleParam["layerField"][0],
                    len(ruleParam["features"]),
                    self.tr("features") if len(ruleParam["features"]) > 1 else self.tr("feature"))
                feedback.pushInfo(row)
            else:
                pass

        feedback.pushInfo("{0} {1} {0}\n".format(
            "===" * 5, self.tr("LOG END")))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "enforceattributerulesalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Enforce Attribute Rules")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Identification Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Identification Processes)"

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate("EnforceAttributeRulesAlgorithm", string)

    def createInstance(self):
        """
        Must return a new copy of your algorithm.
        """
        return EnforceAttributeRulesAlgorithm()


class ParameterAttributeRulesSetType(QgsProcessingParameterType):

    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterAttributeRulesSet(name)

    def metadata(self):
        return {"widget_wrapper": "DsgTools.gui.ProcessingUI.validationAttributeRulesWrapper.ValidationAttributeRulesWrapper"}

    def name(self):
        return QCoreApplication.translate("Processing", self.tr("Attribute Rules Set"))

    def id(self):
        return "attribute_rules_set_type"

    def description(self):
        return QCoreApplication.translate("Processing", self.tr("Set of attribute rules. Used on Attribute Rules Checker."))


class ParameterAttributeRulesSet(QgsProcessingParameterDefinition):

    def __init__(self, name, description=""):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterAttributeRulesSet(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return "attribute_rules_set"

    def checkValueIsAcceptable(self, value, context=None):
        return True

    def valueAsPythonString(self, value, context):
        return str(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()
