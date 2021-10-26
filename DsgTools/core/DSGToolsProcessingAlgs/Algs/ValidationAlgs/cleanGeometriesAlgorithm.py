# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-28
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
                       QgsProcessingException, QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer, QgsProcessingUtils,
                       QgsProject, QgsSpatialIndex, QgsWkbTypes)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class CleanGeometriesAlgorithm(ValidationAlgorithm):
    INPUT = 'INPUT'
    SELECTED = 'SELECTED'
    TOLERANCE = 'TOLERANCE'
    MINAREA = 'MINAREA'
    FLAGS = 'FLAGS'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input Layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
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
                minValue=-1.0, 
                defaultValue=1.0
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MINAREA,
                self.tr('Minimum area'),
                minValue=0,
                defaultValue=0.0001,
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
                self.tr('Cleaned original layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()

        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        snap = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        # if snap < 0 and snap != -1:
        #     raise QgsProcessingException(self.invalidParameterError(parameters, self.TOLERANCE))
        minArea = self.parameterAsDouble(parameters, self.MINAREA, context)
        self.prepareFlagSink(parameters, inputLyr, inputLyr.wkbType(), context)

        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr('Populating temp layer...'))
        auxLyr = layerHandler.createAndPopulateUnifiedVectorLayer([inputLyr], geomType=inputLyr.wkbType(), onlySelected = onlySelected, feedback=multiStepFeedback)
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr('Running clean...'))
        cleanedLyr, error = algRunner.runClean(auxLyr, \
                                                    [algRunner.RMSA, algRunner.Break, algRunner.RmDupl, algRunner.RmDangle], \
                                                    context, \
                                                    returnError=True, \
                                                    snap=snap, \
                                                    minArea=minArea,
                                                    feedback=multiStepFeedback)
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr('Updating original layer...'))
        layerHandler.updateOriginalLayersFromUnifiedLayer([inputLyr], cleanedLyr, feedback=multiStepFeedback, onlySelected=onlySelected)
        self.flagIssues(cleanedLyr, error, feedback)

        return {self.OUTPUT : inputLyr, self.FLAGS : self.flag_id}

    def flagIssues(self, cleanedLyr, error, feedback):
        overlapDict = dict()
        for feat in cleanedLyr.getFeatures():
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
                self.flagFeature(featList[0].geometry(), self.tr('Features from {0} overlap').format(txt))
            elif len(featList) == 1:
                attrList = featList[0].attributes()
                if attrList == len(attrList)*[None]:
                    self.flagFeature(featList[0].geometry(), self.tr('Gap in layer.'))

        if error:
            for feat in error.getFeatures():
                if feedback.isCanceled():
                    break
                self.flagFeature(feat.geometry(), self.tr('Clean error on layer.'))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'cleangeometries'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Clean Geometries')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Quality Assurance Tools (Manipulation Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Quality Assurance Tools (Manipulation Processes)'

    def tr(self, string):
        return QCoreApplication.translate('CleanGeometriesAlgorithm', string)

    def createInstance(self):
        return CleanGeometriesAlgorithm()
