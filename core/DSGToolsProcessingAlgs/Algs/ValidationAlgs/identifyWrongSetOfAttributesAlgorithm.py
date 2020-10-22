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

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.utils import iface
from qgis.gui import QgsMapCanvas
import json
import processing
from qgis.core import (edit,
                       Qgis,
                       QgsDataSourceUri,
                       QgsExpression,
                       QgsExpressionContext,
                       QgsExpressionContextUtils,
                       QgsFeature,
                       QgsFeatureRequest,
                       QgsFeatureSink,
                       QgsField,
                       QgsFields,
                       QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingException,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterString,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingUtils,
                       QgsProject,
                       QgsWkbTypes)

from .validationAlgorithm import ValidationAlgorithm
from ....GeometricTools.layerHandler import LayerHandler
from ....GeometricTools.geometryHandler import GeometryHandler


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
        self.lyrHandler = LayerHandler()
        self.geomHandler = GeometryHandler()
        self.flagFields = self.valAlg.getFlagFields()

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

        inputLyrList = self.parameterAsLayerList(
            parameters, self.INPUT, context)
        if inputLyrList is None or inputLyrList == []:
            raise QgsProcessingException(self.invalidSourceError(
                parameters, self.INPUT))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)

        crs = QgsProject.instance().crs()
        pointFlags, ptId = self.parameterAsSink(
            parameters, self.POINT_FLAGS, context,
            self.flagFields, QgsWkbTypes.Point, crs
        )
        if not pointFlags:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.POINT_FLAGS)
            )
        lineFlags, lId = self.parameterAsSink(
            parameters, self.LINE_FLAGS, context,
            self.flagFields, QgsWkbTypes.LineString, crs
        )
        if not lineFlags:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.LINE_FLAGS)
            )
        polygonFlags, polId = self.parameterAsSink(
            parameters, self.POLYGON_FLAGS, context,
            self.flagFields, QgsWkbTypes.Polygon, crs
        )
        if not polygonFlags:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.POLYGON_FLAGS)
            )
        # rulePath = self.parameterAsFile(parameters, self.RULEFILE, context)
        # ruleData = self.parameterAsString(parameters, self.RULEDATA, context)
        inputData = self.loadRulesData(parameters)

        failedFeatures = self.checkedFeatures(
            inputData, inputLyrList, onlySelected)

        flags = self.flagsFromFailedList(failedFeatures, pointFlags, lineFlags,
                                         polygonFlags, context, feedback
                                         )
        return {
            self.POINT_FLAGS: ptId,
            self.LINE_FLAGS: lId,
            self.POLYGON_FLAGS: polId}

    def loadRulesData(self, parameters):
        """
        Loads a dict with the below data structure
        {rule description: {
                layer name: {
                    all rules: [rule 1, ..., rule n]
        }}}
        :param (OS Path) path: path to the rules JSON file.
        """
        ruleDict = {}
        rulePath = parameters[self.RULEFILE]
        ruleData = parameters[self.RULEDATA]
        # to write a method to evaluate the rules and the
        # file format above
        if ruleData and ruleData != '{}':
            ruleDict = ruleData
            return ruleDict
        elif rulePath and rulePath != '.json':
            with open(rulePath, 'r') as jsonFile:
                ruleDict = json.load(jsonFile)
            return ruleDict
        # else:
        #     # return "error message"
        

        # else:
        #     with open(rulePath, 'r') as jsonFile:
        #         ruleDict = json.load(jsonFile)
        #     return ruleDict
            

    def checkedFeatures(self, rules, layerList, onlySelected):
        """
        This method filters a layer or a set of selected features from some
        conditional rules, and a result is a dictionary with rules and features.
        That means these features were filled with a wrong set of attributes.
        :param (dict) rules: dictionary from conditional rules;
        :param (QgsVectorLayer) layerList: list from all loaded layers.
        :param (boolean) onlySelected: list from all loaded layers.
        :param (dict) failedDict: dictionary with rules and features.
        """

        failedDict = {}
        for ruleName in rules:
            failedList = []
            for lyr in layerList:
                loadedLyrName = lyr.name()
                if loadedLyrName in rules[ruleName]:
                    allRules = rules[ruleName][loadedLyrName]['allRules']
                    for rule in allRules:
                        # in order to improve efficiency in large databases or
                        # in the most detailed scales, it's interesting to take
                        # a look at NoGeometry and SubsetOfAttributes flags.
                        request = QgsFeatureRequest().setFilterExpression(rule)
                        if onlySelected:
                            # for some reason the request using as expression
                            # ('is_selected() and {}'.format(rule)) in the
                            # getFeatures() method as a param doesn't works, but
                            # works on canvas TOC. So, to resolve I've created a
                            # new lyr with saveselectedfeatures alg and move on

                            parameters = {'INPUT': lyr,
                                          'OUTPUT': 'TEMPORARY_OUTPUT'}
                            selected = processing.run(
                                'native:saveselectedfeatures', parameters)

                            for res, features in selected.items():
                                for feature in features.getFeatures(rule):
                                    failedList.append(feature)

                        else:
                            for feature in lyr.getFeatures(request):
                                failedList.append(feature)

            failedDict[ruleName] = failedList
            # failedDict = {'ruleName_1': [QgsFeature_1,...,QgsFeature_n],
            #               'ruleName_n': [QgsFeature_1,...,QgsFeature_n]}

        return failedDict

    def flagsFromFailedList(self, featureDict, ptLayer, lLayer, polLayer, ctx, feedback):
        """
        Creates new features from a failed conditional rules dictionary.
        :param (Dict) featureDict: a dictionary with rule name and a list of selected QgsFeature;
        :param (QgsVectorLayer) ptLayer: output point vector layer;
        :param (QgsVectorLayer) lLayer: output line vector layer;
        :param (QgsVectorLayer) polLayer: output polygon vector layer;
        :param (QgsProcessingContext) ctx: processing context;
        :param (QgsProcessingFeedback) feedback: processing feedback.
        """
        layerMap = {
            QgsWkbTypes.PointGeometry: ptLayer,
            QgsWkbTypes.LineGeometry: lLayer,
            QgsWkbTypes.PolygonGeometry: polLayer
        }
        for ruleName, flagList in featureDict.items():
            # improve description in flagText
            flagText = self.tr('{name}').format(name=ruleName)
            for flag in flagList:
                geom = flag.geometry()
                newFeature = QgsFeature(self.flagFields)
                newFeature["reason"] = flagText
                newFeature.setGeometry(geom)
                layerMap[geom.type()].addFeature(
                    newFeature, QgsFeatureSink.FastInsert
                )
        return (ptLayer, lLayer, polLayer)

    def evaluateRuleFormat(self, ):
        """
        This function evaluates the rule format from both rules input
        and inform to user if it's ok or not.
        """

        return

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
