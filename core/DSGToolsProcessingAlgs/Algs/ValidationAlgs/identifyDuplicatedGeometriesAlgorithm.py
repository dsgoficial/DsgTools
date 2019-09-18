# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-06-08
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

from collections import defaultdict
from itertools import combinations

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean, QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterVectorLayer, QgsWkbTypes)

from .validationAlgorithm import ValidationAlgorithm
from DsgTools.core.GeometricTools.layerHandler import LayerHandler

class IdentifyDuplicatedGeometriesAlgorithm(ValidationAlgorithm):
    FLAGS = 'FLAGS'
    INPUT = 'INPUT'
    SELECTED = 'SELECTED'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorAnyGeometry ]
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
                self.FLAGS,
                self.tr('{0} Flags').format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        isMulti = QgsWkbTypes.isMultiType(int(inputLyr.wkbType()))
        if inputLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        self.prepareFlagSink(parameters, inputLyr, inputLyr.wkbType(), context)
        # Compute the number of steps to display within the progress bar and
        # get features from source
        featureList, total = self.getIteratorAndFeatureCount(inputLyr, onlySelected=onlySelected)
        geomDict = defaultdict(set)
        featureList = tuple(featureList)
        layerHandler = LayerHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        geomDict = layerHandler.getDuplicatedFeaturesDict(inputLyr, onlySelected=onlySelected, feedback=multiStepFeedback)
        multiStepFeedback.setCurrentStep(1)
        self.raiseDuplicatedFeaturesFlags(inputLyr, geomDict, multiStepFeedback)
        multiStepFeedback.setCurrentStep(2)
        
        return {self.FLAGS: self.flag_id}

    def raiseDuplicatedFeaturesFlags(self, inputLyr, geomDict, feedback):
        size = 100/len(geomDict) if geomDict else 0
        for current, featList in enumerate(geomDict.values()):
            if feedback.isCanceled():
                break
            if len(featList) > 1:
                idStrList = ', '.join(map(str, [feat.id() for feat in featList]))
                flagText = self.tr('Features from layer {0} with ids=({1}) have the same set of attributes.').format(inputLyr.name(), idStrList)
                self.flagFeature(featList[0].geometry(), flagText)
            feedback.setProgress(size * current)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifyduplicatedgeometries'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Duplicated Geometries')

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
        return QCoreApplication.translate('IdentifyDuplicatedGeometriesAlgorithm', string)

    def createInstance(self):
        return IdentifyDuplicatedGeometriesAlgorithm()
