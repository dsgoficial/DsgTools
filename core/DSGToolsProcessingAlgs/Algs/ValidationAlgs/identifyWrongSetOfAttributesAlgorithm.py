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
                defaultValue = '.json'
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.RULEDATA,
                description =  self.tr('JSON formatted rules:'),
                multiLine = True,
                defaultValue = '{}'
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
        
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUT, context)
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
        rulePath = self.parameterAsFile(parameters, self.RULEFILE, context)
        inputData = self.loadRulesData(rulePath)
        #teste = self.getSelected(inputLyrList)
        failedFeatures = self.checkedFeatures(inputData, inputLyrList, onlySelected)
        flags = self.flagsFromFailedList(failedFeatures, pointFlags, lineFlags,
            polygonFlags, context, feedback
        )
        return {
            self.POINT_FLAGS: ptId,
            self.LINE_FLAGS: lId,
            self.POLYGON_FLAGS: polId
        }

    def loadRulesData(self, path):
        """
        Loads a dict with the below data structure
            {
                rule description: {
                    layer name: {
                        all rules: [rule 1, ..., rule n]
                    }
                }
            }
        :param (OS Path) path: path to the rules JSON file.
        """
        with open(path, 'r') as jsonFile:
            ruleDict = json.load(jsonFile)
        return ruleDict

    def getSelected(self, layerList):
        selectedDict = dict()
        for lyr in layerList:
            featureList = self.lyrHandler.getFeatureList(lyr, onlySelected=True, returnIterator=False)
            if featureList:
                selectedDict[lyr] = featureList
        return selectedDict


    def checkedFeatures(self, rules, layerList, onlySelected, returnIterator=True):
        """
        Select features by conditional rules stored in the rules JSON file.
        :param (dict) rules: dictionary from conditional rules;
        :param (QgsVectorLayer) layerList: list from all loaded layers.
        """

        failedDict = {}
        for ruleName in rules:
            failedList = []
            for lyr in layerList:
                loadedLyrName = lyr.name()
                if loadedLyrName in rules[ruleName]:
                    allRules = rules[ruleName][loadedLyrName]['allRules']
                    for rule in allRules:
                        if onlySelected:
                            request = QgsFeatureRequest().setFilterExpression("is_selected() and {}".format(rule))
                            for feat in lyr.getFeatures(request):
                                failedList.append(feat)
                            """
                            why dont works???!?!?!ovvdvjsndvihdvhçvbivbvvkjbvjvbvbjphiowewvho
                            """
                        else:
                            request = QgsFeatureRequest().setFilterExpression(rule)
                            for feat in lyr.getFeatures(request):
                                failedList.append(feat)
            failedDict[ruleName] = failedList

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
            flagText = self.tr('{name}').format(name = ruleName)  # improve the flag description
            for flag in flagList:
                geom = flag.geometry()
                newFeature = QgsFeature(self.flagFields)
                newFeature["reason"] = flagText
                newFeature.setGeometry(geom)
                layerMap[geom.type()].addFeature(
                    newFeature, QgsFeatureSink.FastInsert
                )
        return (ptLayer, lLayer, polLayer)

    def evaluateExpressions(self):
        """
        exp = QgsExpression(rule)  validate expressions
        handle rule error
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
