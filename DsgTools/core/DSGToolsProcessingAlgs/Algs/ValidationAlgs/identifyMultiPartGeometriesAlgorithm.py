# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-06-30
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from PyQt5.QtCore import QCoreApplication
import os
import processing
import concurrent.futures
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterVectorLayer, QgsProcessingUtils,
                       QgsProject, QgsWkbTypes, QgsProcessingFeatureSourceDefinition, QgsExpression, QgsFeatureRequest)

from .validationAlgorithm import ValidationAlgorithm


class IdentifyMultiPartGeometriesAlgorithm(ValidationAlgorithm):
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
                [
                    QgsProcessing.TypeVectorAnyGeometry,
                ]
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
        if inputLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        self.prepareFlagSink(parameters, inputLyr, inputLyr.wkbType(), context)
        request = QgsFeatureRequest()
        if onlySelected:
            request.setFilterFids(inputLyr.selectedFeatureIds())
        request.setFilterExpression("num_geometries( $geometry ) > 1")
        featuresWithProblem = [feat for feat in inputLyr.getFeatures(request)]
        problemCount = len(featuresWithProblem)
        if problemCount == 0:
            return {self.FLAGS: self.flag_id}
        stepSize = 100 / problemCount
        for current, feat in enumerate(featuresWithProblem):
            if feedback is not None and feedback.isCanceled():
                break
            self.flagFeature(feat.geometry(), flagText=self.tr('Geometry with multi part.'))
            if feedback is not None:
                feedback.setProgress(current * stepSize)

        return {self.FLAGS: self.flag_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifymultigeometries'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Multipart Geometries')

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
        return QCoreApplication.translate('IdentifyMultiPartGeometriesAlgorithm', string)

    def createInstance(self):
        return IdentifyMultiPartGeometriesAlgorithm()
