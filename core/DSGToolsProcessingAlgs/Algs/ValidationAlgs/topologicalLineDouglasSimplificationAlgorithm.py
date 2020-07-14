# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-21
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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


class TopologicalLineDouglasSimplificationAlgorithm(ValidationAlgorithm):
    """
    Implements a Douglas Peucker algorithm to simplify lines taking into
    consideration the topological behavior for lines between layers.
    """
    INPUTLAYERS = 'INPUTLAYERS'
    SELECTED = 'SELECTED'
    SNAP = 'SNAP'
    DOUGLASPARAMETER = 'DOUGLASPARAMETER'
    FLAGS = 'FLAGS'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUTLAYERS,
                self.tr('Linestring Layers'),
                QgsProcessing.TypeVectorLine
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.DOUGLASPARAMETER,
                self.tr('Douglas Deucker threshold'),
                minValue=0,
                defaultValue=2,
                type=QgsProcessingParameterNumber.Double
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SNAP,
                self.tr('Snap radius'),
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

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()

        inputLyrList = self.parameterAsLayerList(parameters,
                                                 self.INPUTLAYERS, context)
        if inputLyrList is None or inputLyrList == []:
            raise QgsProcessingException(self.invalidSourceError(
                parameters, self.INPUTLAYERS))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        snap = self.parameterAsDouble(parameters, self.SNAP, context)
        threshold = self.parameterAsDouble(parameters,
                                           self.DOUGLASPARAMETER, context)
        self.prepareFlagSink(parameters, inputLyrList[0],
                             QgsWkbTypes.MultiLineString, context)

        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr('Building unified layer...'))
        coverage = layerHandler.createAndPopulateUnifiedVectorLayer(
            inputLyrList, geomType=QgsWkbTypes.MultiLineString,
            onlySelected=onlySelected, feedback=multiStepFeedback)

        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr('Running clean on unified layer...'))
        simplifiedCoverage, error = algRunner.runDouglasSimplification(
            coverage,
            threshold,
            context,
            returnError=True,
            snap=snap,
            feedback=multiStepFeedback)

        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr('Updating original layer...'))
        
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            inputLyrList, simplifiedCoverage, feedback=multiStepFeedback)
        self.flagCoverageIssues(simplifiedCoverage, error, feedback)

        return {self.INPUTLAYERS : inputLyrList, self.FLAGS : self.flag_id}

    def flagCoverageIssues(self, cleanedCoverage, error, feedback):
        """
        From lines, this method grabs its overlaps.
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
        return 'topologicallinedouglaspeuckersimplification'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Topological Line Douglas Peucker Simplification')

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
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate(
            'TopologicalLineDouglasSimplificationAlgorithm', string)

    def createInstance(self):
        """
        Must return a new copy of your algorithm.
        """
        return TopologicalLineDouglasSimplificationAlgorithm()
