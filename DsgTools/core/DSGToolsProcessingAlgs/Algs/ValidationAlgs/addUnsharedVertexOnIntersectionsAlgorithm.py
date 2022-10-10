# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-12-07
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from itertools import chain
from PyQt5.QtCore import QCoreApplication

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterVectorLayer, QgsWkbTypes)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class AddUnsharedVertexOnIntersectionsAlgorithm(ValidationAlgorithm):
    FLAGS = 'FLAGS'
    INPUT_POINTS = 'INPUT_POINTS'
    INPUT_LINES = 'INPUT_LINES'
    INPUT_POLYGONS = 'INPUT_POLYGONS'
    SELECTED = 'SELECTED'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_POINTS,
                self.tr('Point Layers'),
                QgsProcessing.TypeVectorPoint,
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LINES,
                self.tr('Linestring Layers'),
                QgsProcessing.TypeVectorLine,
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_POLYGONS,
                self.tr('Polygon Layers'),
                QgsProcessing.TypeVectorPolygon,
                optional=True
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
        algRunner = AlgRunner()
        inputPointLyrList = self.parameterAsLayerList(
            parameters,
            self.INPUT_POINTS,
            context
        )
        inputLineLyrList = self.parameterAsLayerList(
            parameters,
            self.INPUT_LINES,
            context
        )
        inputPolygonLyrList = self.parameterAsLayerList(
            parameters,
            self.INPUT_POLYGONS,
            context
        )
        if inputPointLyrList + inputLineLyrList + inputPolygonLyrList == []:
            raise QgsProcessingException(
                self.tr('Select at least one layer')
            )
        onlySelected = self.parameterAsBool(
            parameters,
            self.SELECTED,
            context
        )
        lyrList = list(chain(inputPointLyrList, inputLineLyrList, inputPolygonLyrList))
        nLyrs = len(lyrList)
        multiStepFeedback = QgsProcessingMultiStepFeedback(nLyrs + 2, feedback)
        multiStepFeedback.setCurrentStep(0)
        flagsLyr = algRunner.runIdentifyUnsharedVertexOnIntersectionsAlgorithm(
            pointLayerList=inputPointLyrList,
            lineLayerList=inputLineLyrList,
            polygonLayerList=inputPolygonLyrList,
            onlySelected=onlySelected,
            context=context,
            feedback=multiStepFeedback
        )
        snapToGridLyr = algRunner.runSnapToGrid(
            inputLayer=flagsLyr,
            tol=1e-6,
            feedback=multiStepFeedback,
            context=context
        )
        multiStepFeedback.setCurrentStep(1)
        for current, lyr in enumerate(lyrList):
            if feedback.isCanceled():
                break
            multiStepFeedback.setCurrentStep(current + 1)
            algRunner.runSnapLayerOnLayer(
                inputLayer=lyr,
                referenceLayer=snapToGridLyr,
                tol=1e-5,
                context=context,
                onlySelected=onlySelected,
                feedback=multiStepFeedback,
                behavior=1,
                buildCache=False
            )

        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'addunsharedvertexonintersectionsalgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Add Unshared Vertex on Intersections')

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
        return 'Quality Assurance Tools (Correction Processes)'

    def tr(self, string):
        return QCoreApplication.translate('AddUnsharedVertexOnIntersectionsAlgorithm', string)

    def createInstance(self):
        return AddUnsharedVertexOnIntersectionsAlgorithm()
