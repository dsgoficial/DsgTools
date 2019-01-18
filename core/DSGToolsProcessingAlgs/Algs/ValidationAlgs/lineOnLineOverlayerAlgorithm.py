# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-06
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
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer, QgsProcessingUtils,
                       QgsSpatialIndex, QgsWkbTypes)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class LineOnLineOverlayerAlgorithm(ValidationAlgorithm):
    INPUT = 'INPUT'
    SELECTED = 'SELECTED'
    TOLERANCE = 'TOLERANCE'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorLine ]
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.TOLERANCE, 
                self.tr('Snap radius'), 
                parentParameterName=self.INPUT,                                         
                minValue=0, 
                defaultValue=1.0
            )
        )
        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT,
                self.tr('Original layer with overlayed lines')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        tol = self.parameterAsDouble(parameters, self.TOLERANCE, context)

        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(
            self.tr(
                'Identifying dangles on {layer}...'
                ).format(layer=inputLyr.name()))
        dangleLyr = algRunner.runIdentifyDangles(
            inputLyr,
            tol,
            context,
            feedback=multiStepFeedback,
            onlySelected=onlySelected
            )

        multiStepFeedback.setCurrentStep(1)
        layerHandler.filterDangles(
            dangleLyr,
            tol,
            feedback=multiStepFeedback
            )

        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(
            self.tr(
                'Snapping layer {layer} to dangles...'
                ).format(layer=inputLyr.name()))
        algRunner.runSnapLayerOnLayer(
            inputLyr,
            dangleLyr,
            tol,
            context,
            feedback=multiStepFeedback,
            onlySelected=onlySelected
            )

        multiStepFeedback.setCurrentStep(3)
        multiStepFeedback.pushInfo(
            self.tr(
                'Cleanning layer {layer}...'
                ).format(layer=inputLyr.name()))
        algRunner.runDsgToolsClean(
            inputLyr,
            context,
            snap=tol,
            feedback=multiStepFeedback,
            onlySelected=onlySelected
            )

        return {self.OUTPUT: inputLyr}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'lineonlineoverlayer'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Line on line overlayer')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Validation Tools (Manipulation Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Validation Tools (Manipulation Processes)'

    def tr(self, string):
        return QCoreApplication.translate('LineOnLineOverlayerAlgorithm', string)

    def createInstance(self):
        return LineOnLineOverlayerAlgorithm()
