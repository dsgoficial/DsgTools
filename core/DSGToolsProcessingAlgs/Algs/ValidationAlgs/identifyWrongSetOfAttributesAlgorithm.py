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

import json
import processing
from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.PyQt.QtGui import QColor, QFont
from qgis.core import (QgsFeature,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingException,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterString,
                       QgsProject,
                       QgsWkbTypes,
                       QgsConditionalStyle)

from .validationAlgorithm import ValidationAlgorithm


class IdentifyWrongSetOfAttributesAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    RULEFILE = 'RULEFILE'
    RULEDATA = 'RULEDATA'
    SELECTED = 'SELECTED'
    POINT_FLAGS = 'POINT_FLAGS'
    LINE_FLAGS = 'LINE_FLAGS'
    POLYGON_FLAGS = 'POLYGON_FLAGS'

    def __init__(self):
        super().__init__()
        self.valAlg = ValidationAlgorithm()
        self.flagFields = self.valAlg.getFlagFields()
        self.font = QFont()
        self.conditionalStyle = QgsConditionalStyle()

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
                defaultValue='.json'
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.RULEDATA,
                description=self.tr('JSON formatted rules:'),
                multiLine=True,
                defaultValue='{}'
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

        inputLyrList = self.parameterAsLayerList(parameters,
                                                 self.INPUT,
                                                 context)

        if inputLyrList is None or inputLyrList == []:
            raise QgsProcessingException(self.invalidSourceError(
                parameters, self.INPUT))

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

        inputData = self.loadRulesData(parameters, feedback)

        failedFeatures = self.checkedFeatures(
            inputData, inputLyrList, onlySelected)

        flags = self.flagsFromFailedList(failedFeatures,
                                         pointFlags,
                                         lineFlags,
                                         polygonFlags,
                                         feedback)
        return {
            self.POINT_FLAGS: ptId,
            self.LINE_FLAGS: lId,
            self.POLYGON_FLAGS: polId}

    def loadRulesData(self, parameters, feedback):
        """
        Loads a JSON file with a dictionary structured as described below
        {"0": {
            "layer": (str) layer name,
            "rule": (str) conditional rule,
            "attribute": (str) attribute name,
            "description": (str) description about the error,
            "type": (str) short description about the error,
            "color": (list) RGB [255, 0, 0],
            "features": (list) [] QgsFeature list
        }}
        :param (OS Path) path: path to the JSON file.
        :param (str) str: string formatted rule.
        """
        rulePath = parameters[self.RULEFILE]
        ruleData = parameters[self.RULEDATA]
        # to write a method to evaluate the rules and the
        # file format above

        if ruleData and ruleData != '{}':
            # self.validateRuleFormat(json.loads(ruleData), feedback)
            return json.loads(ruleData)
        elif rulePath and rulePath != '.json':
            with open(rulePath, 'r') as jsonFile:
                # return self.validateRuleFormat(json.load(jsonFile), feedback)
                return json.load(jsonFile)

    def checkedFeatures(self, rules, layerList, onlySelected):
        """
        Filters a layer or a set of selected features as from conditional rules,
        and the result is added to a list in a dictionary.
        :param (dict) rules: dictionary with conditional rules;
        :param (QgsVectorLayer) layerList: list from all loaded layers.
        :param (boolean) onlySelected: true or false.
        """

        # in order to improve efficiency in large databases or
        # in the most detailed scales, it's interesting to take
        # a look at NoGeometry and SubsetOfAttributes flags.

        # for some reason the request using as expression
        # ('is_selected() and {}'.format(rule)) in the
        # getFeatures() method as a param doesn't works, but
        # works on canvas TOC. So, to resolve, I've created a
        # new lyr with saveselectedfeatures alg and move on

        for keys, values in rules.items():
            for lyr in layerList:
                if lyr.name() == values['layer']:
                    if onlySelected:
                        parameters = {'INPUT': lyr,
                                      'OUTPUT': 'TEMPORARY_OUTPUT'}
                        selected = processing.run(
                            'native:saveselectedfeatures', parameters)
                        values['features'] = [
                            feature for feature in selected['OUTPUT'].getFeatures(values['rule'])]
                        self.addRuleToLayer(lyr, values)

                    else:
                        values['features'] = [
                            feature for feature in lyr.getFeatures(values['rule'])]
                        self.addRuleToLayer(lyr, values)

        return rules

    def flagsFromFailedList(self, featureDict, ptLayer, lLayer, polLayer, feedback):
        """
        Creates new features from a failed conditional rules dictionary.
        :param (Dict) featureDict: a dictionary with a list QgsFeatures selected by
            checkedFeatures() method;
        :param (QgsVectorLayer) ptLayer: output point vector layer;
        :param (QgsVectorLayer) lLayer: output line vector layer;
        :param (QgsVectorLayer) polLayer: output polygon vector layer;
        :param (QgsProcessingFeedback) feedback: processing feedback.
        """
        layerMap = {
            QgsWkbTypes.PointGeometry: ptLayer,
            QgsWkbTypes.LineGeometry: lLayer,
            QgsWkbTypes.PolygonGeometry: polLayer
        }

        for keys, values in featureDict.items():
            flagText = self.tr('{name}').format(name=values["description"])
            for flag in values["features"]:
                geom = flag.geometry()
                newFeature = QgsFeature(self.flagFields)
                newFeature["reason"] = flagText
                newFeature.setGeometry(geom)
                layerMap[geom.type()].addFeature(
                    newFeature, QgsFeatureSink.FastInsert
                )
        self.logResult(featureDict, feedback)
        return (ptLayer, lLayer, polLayer)

    def addRuleToLayer(self, lyr, values):
        """
        Applies a conditional style for each wrong attribute
        in the attribute table.
        """
        self.font.setBold(True)
        self.conditionalStyle.setRule(values['rule'])
        self.conditionalStyle.setFont(self.font)
        self.conditionalStyle.setTextColor(QColor(255, 255, 255))

        for field in lyr.fields():
            if field.name() == values['attribute']:
                self.conditionalStyle.setBackgroundColor(
                    QColor(
                        values['color'][0],
                        values['color'][1],
                        values['color'][2]))
                lyr.conditionalStyles().setFieldStyles(
                    field.name(), [self.conditionalStyle])
            # plus: to find a way to color an entire row with a different color
            # in order to highlight the row with the error
            # else:
            #     for rule in l:
            #         conditionalStyle.setRule(rule)
            #         conditionalStyle.setBackgroundColor(QColor(171,171,171))
            #         lyr.conditionalStyles().setRowStyles([conditionalStyle])

    def logResult(self, rules, feedback):
        """
        Creates a statistics text log from each layer and your
        respectively wrong attribute.
        """
        feedback.pushInfo('{0} {1} {0}\n'.format(
            '===' * 5, self.tr('LOG START')))

        for k, values in rules.items():
            if len(values['features']) > 0:
                row = "[RULE]: {0} - {1}\n{2}: {3} {4}\n".format(
                    values['attribute'],
                    values['type'],
                    values['layer'],
                    len(values['features']),
                    self.tr('features') if len(values['features']) > 1 else self.tr('feature'))
                feedback.pushInfo(row)
            else:
                pass

        feedback.pushInfo('{0} {1} {0}\n'.format(
            '===' * 5, self.tr('LOG END')))

    def validateRuleFormat(self, rules, feedback):
        """
        Verifies whether the given rule set is valid or not
        and notifies the user.
        """
        # TODO: a better way to validate rules

        # list_keys = ['layer', 'rule', 'attribute',
        #     'description', 'type', 'color', 'features']

        # if not isinstance(rules, dict):
        #     feedback.pushInfo(self.tr(
        #                 'The structure of the rules does not correspond to the standard format.'))
        # else:
        #     for k, v in rules.items():
        #         if isinstance(v, dict):
        #             for keys, values in v.items():
        #                 if keys in list_keys:

        #                     if isinstance(values, (str, list)):
        #                         if len(v['color']) == 3 and len(v['features']) == 0:
        #                             return rules
        #                         else:
        #                             feedback.pushInfo(self.tr('The key {} size is different than 3 and key {} size is different than 0.'.fomat(value))
        #                     else:
        #                         feedback.pushInfo(self.tr('The value {} is not a string or a list.'.fomat(value))

        #                 else:
        #                     feedback.pushInfo(self.tr('The key {} does not exist in the dictionary.'.fomat(keys))
        #         else:
        #             feedback.pushInfo(self.tr(
        #                 'The structure of the rules does not correspond to the standard format.'))


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
