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

from PyQt5.QtCore import QCoreApplication

from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterVectorLayer, QgsWkbTypes)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class RemoveDuplicatedGeometriesAlgorithm(ValidationAlgorithm):
    FLAGS = 'FLAGS'
    INPUT = 'INPUT'
    SELECTED = 'SELECTED'
    OUTPUT = 'OUTPUT'

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
        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT,
                self.tr('Original layer without duplicated geometries')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(
                    parameters,
                    self.INPUT
                    )
                )
        onlySelected = self.parameterAsBool(
            parameters,
            self.SELECTED,
            context
            )
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(
            self.tr(
                'Identifying duplicated geometries in layer {0}...'
                ).format(inputLyr.name()))
        flagLyr = algRunner.runIdentifyDuplicatedGeometries(
            inputLyr,
            context,
            feedback=multiStepFeedback,
            onlySelected=onlySelected
            )

        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(
            self.tr(
                'Removing duplicated geometries in layer {0}...'
                ).format(inputLyr.name()))
        self.removeFeatures(inputLyr, flagLyr, multiStepFeedback)

        return {self.OUTPUT: inputLyr}
    
    def removeFeatures(self, inputLyr, flagLyr, feedback):
        featureList, total = self.getIteratorAndFeatureCount(flagLyr)
        localTotal = 100/total if total else 0
        inputLyr.startEditing()
        for current, feat in enumerate(featureList):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
            idRemoveList = [i for i in map(int, feat['reason'].split('(')[-1].split(')')[0].split(','))][1::]
            inputLyr.deleteFeatures(idRemoveList)
            feedback.setProgress(current * localTotal)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'removeduplicatedgeometries'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Remove Duplicated Geometries')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Quality Assurance Tools (Correction Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Quality Assurance Tools (Correction Processes)'

    def tr(self, string):
        return QCoreApplication.translate('RemoveDuplicatedGeometriesAlgorithm', string)

    def createInstance(self):
        return RemoveDuplicatedGeometriesAlgorithm()
