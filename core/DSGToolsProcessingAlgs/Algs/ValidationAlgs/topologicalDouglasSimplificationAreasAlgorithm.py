# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2020-05-08
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Francisco A. Camello N. - Software Engineer @ Brazilian Army
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
from PyQt5.QtCore import QCoreApplication # qgis.PyQt

import processing
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsGeometry, QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer, QgsProcessingUtils,
                       QgsProject, QgsSpatialIndex, QgsWkbTypes)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class TopologicalDouglasSimplificationAreasAlgorithm(ValidationAlgorithm):
    """
    Algorithm to simplify areas using the Douglas Peucker algorithm.
    """
    INPUTLAYERS = 'INPUTLAYERS'
    SELECTED = 'SELECTED'
    METHOD = 'METHOD'
    TOLERANCE = 'TOLERANCE'
    FLAGS = 'FLAGS'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUTLAYERS,
                self.tr('Linestring Layers'),
                QgsProcessing.TypeVectorPolygon
            )
        )
        """
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.METHOD,
                self.tr('Simplification method'),
                {'Distance (Douglas Peucker)': 0, 'Snap to grid': 1,
                    'Area (Visvalingam)': 2},
                allowMultiple=False,
                defaultValue=0
            )
        )
        """
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE,
                self.tr('Tolerance'),
                minValue=0,
                defaultValue=1,
                type=QgsProcessingParameterNumber.Double
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr('{0} Flags').format(self.displayName())
            )
        )

        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT,
                self.tr('Original layer simplifyed')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()

        inputLyrList = self.parameterAsLayerList(
            parameters, self.INPUTLAYERS, context)
        if inputLyrList is None or inputLyrList == []:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUTLAYERS))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        method = 0  # self.parameterAsEnum(parameters, self.METHOD, context)
        tolerance = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        self.prepareFlagSink(
            parameters, inputLyrList[0], QgsWkbTypes.MultiPolygon, context)


        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr('Building unified layer...'))
        coverage = layerHandler.createAndPopulateUnifiedVectorLayer(
            inputLyrList, geomType=QgsWkbTypes.MultiPolygon,
            onlySelected=onlySelected, feedback=multiStepFeedback)
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(
            self.tr('Running clean on unified layer...'))

        simplifiedCoverage, error = algRunner.runDouglasLinesSimplification(
            coverage,
            method,
            tolerance,
            context,
            feedback=multiStepFeedback,
            #onlySelected=onlySelected
        )
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr('Updating original layer...'))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            inputLyrList, simplifiedCoverage, feedback=multiStepFeedback)
        self.flagCoverageIssues(simplifiedCoverage, error, feedback)

        return {self.INPUTLAYERS : inputLyrList, self.FLAGS : self.flag_id}

    def flagCoverageIssues(self, cleanedCoverage, error, feedback):
        """
        flags overlaps and gaps in the coverage
        """
        overlapDict = dict()
        for feat in cleanedCoverage.getFeatures():
            if feedback.isCanceled():
                break
            geom = feat.geometry()
            geomKey = geom.asWkb()
            if geomKey not in overlapDict:
                overlapDict[geomKey] = []
            overlapDict[geomKey].append(feat)
        for geomKey, featList in overlapDict.items():
            if feedback.isCanceled():
                break
            if len(featList) > 1:
                txtList = []
                for i in featList:
                    txtList += ['{0} (id={1})'.format(i['layer'], i['featid'])]
                txt = ', '.join(txtList)
                self.flagFeature(featList[0].geometry(), self.tr(
                    'Features from {0} overlap').format(txt))
            elif len(featList) == 1:
                attrList = featList[0].attributes()
                if attrList == len(attrList)*[None]:
                    self.flagFeature(featList[0].geometry(), self.tr(
                        'Gap in coverage.'))

        if error:
            for feat in error.getFeatures():
                if feedback.isCanceled():
                    break
                self.flagFeature(feat.geometry(), self.tr(
                    'Clean error on coverage.'))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'topologicaldouglaspeuckerareasimplification'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Topological Douglas Peucker Areas Simplification')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Quality Assurance Tools (Topological Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Quality Assurance Tools (Topological Processes)'

    def tr(self, string):
        return QCoreApplication.translate(
            'TopologicalDouglasSimplificationAreasAlgorithm', string)

    def createInstance(self):
        return TopologicalDouglasSimplificationAreasAlgorithm()
