# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-13
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
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsGeometry, QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer, QgsProcessingUtils,
                       QgsSpatialIndex, QgsWkbTypes, QgsVectorLayerUtils)

import processing
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.GeometricTools.spatialRelationsHandler import SpatialRelationsHandler

from .validationAlgorithm import ValidationAlgorithm


class IdentifyContourLineOutOfThresholdAlgorithm(ValidationAlgorithm):
    INPUT = 'INPUT'
    SELECTED = 'SELECTED'
    TOPOLOGY_RADIUS = 'TOPOLOGY_RADIUS'
    TOLERANCE = 'TOLERANCE'
    REFERENCE_LYR = 'REFERENCE_LYR'
    CONTOUR_ATTR = 'CONTOUR_ATTR'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.CONTOUR_ATTR, 
                self.tr('Contour value field'),
                None, 
                'INPUT', 
                QgsProcessingParameterField.Any
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOPOLOGY_RADIUS,
                self.tr('Topology radius'),
                minValue=0,
                defaultValue=2
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.REFERENCE_LYR,
                self.tr('Reference layer'),
                [QgsProcessing.TypeVectorPolygon],
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE,
                self.tr('Threshold'),
                minValue=0,
                defaultValue=10
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
        spatialRealtionsHandler = SpatialRealtionsHandler()
        algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        contourFieldName = self.parameterAsField(parameters, self.CONTOUR_ATTR, context)
        threshold = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        topology_radius = self.parameterAsDouble(parameters, self.TOPOLOGY_RADIUS, context)
        refLyr = self.parameterAsVectorLayer(parameters, self.REFERENCE_LYR, context)
        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.Polygon, context)

        #1. Get all lines into one line lyr
        currentStep = 0
        if refLyr is not None:
            multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr('Identifying dangles...'))
            dangles = algRunner.runIdentifyDangles(
                inputLayer=inputLayer,
                searchRadius=topology_radius,
                context=context,
                onlySelected=onlySelected,
                polygonFilter=refLyr,
                feedback=multiStepFeedback
            )
            currentStep += 1
            #2. Snap frame to dangles
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr('Adjusting frame lyr...'))
            snappedFrame = algRunner.runSnapGeometriesToLayer(
                inputLayer=inputLyr,
                referenceLayer=dangles,
                tol=topology_radius,
                context=context
                feedback=multiStepFeedback
            )
            currentStep += 1
        else:
            multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)

        #3. Validate contour lines
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr('Validating contour lines...'))
        invalidDict = spatialRealtionsHandler.validateContourLines(
            contourLyr=inputLyr,
            contourAttrName=contourFieldName,
            refLyr=refLyr,
            feedback=multiStepFeedback
        )
        currentStep+=1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr('Raising flags...'))
        nFlags = len(invalidDict)
        step = 100/nFlags if nFlags else 0
        for current, (geom, text) in enumerate(invalidDict.items()):
            self.flagFeature(geom, text, fromWkb=True)
            multiStepFeedback.setProgress(step * current)
            
        return {self.FLAGS: self.flag_id}
    

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifycontourlineoutofthreshold'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Contour Line Out of Threshhold')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Validation Tools (Identification Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Validation Tools (Identification Processes)'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return IdentifyContourLineOutOfThresholdAlgorithm()
