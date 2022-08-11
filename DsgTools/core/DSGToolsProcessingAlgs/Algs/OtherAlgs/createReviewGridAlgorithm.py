# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-08-11
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
from DsgTools.core.GeometricTools.featureHandler import FeatureHandler
from DsgTools.core.Utils.FrameTools.map_index import UtmGrid
from ...algRunner import AlgRunner
import processing, os, requests
from time import sleep
from qgis.PyQt.Qt import QVariant
from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsFeature,
                       QgsDataSourceUri,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsWkbTypes,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingUtils,
                       QgsSpatialIndex,
                       QgsGeometry,
                       QgsProcessingParameterField,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterExpression,
                       QgsProcessingException,
                       QgsProcessingParameterString,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterType,
                       QgsProcessingParameterCrs,
                       QgsCoordinateTransform,
                       QgsProject,
                       QgsCoordinateReferenceSystem,
                       QgsField,
                       QgsFields)

class CreateReviewGridAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    STOP_SCALE = 'STOP_SCALE'
    X_GRID_SIZE = 'X_GRID_SIZE'
    Y_GRID_SIZE = 'Y_GRID_SIZE'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input Polygon Layer'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.X_GRID_SIZE,
                self.tr('Grid size on x-axis'),
                defaultValue=0.005,
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.Y_GRID_SIZE,
                self.tr('Grid size on y-axis'),
                defaultValue=0.005,
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Created Review Grid')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(
            parameters,
            self.INPUT,
            context
        )
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(
                    parameters, self.INPUT
                )
            )
        stopScaleIdx = self.parameterAsEnum(
            parameters,
            self.STOP_SCALE,
            context
        )
        fields = self.getOutputFields()

        xGridSize = self.parameterAsDouble(parameters, self.X_GRID_SIZE, context)
        yGridSize = self.parameterAsDouble(parameters, self.Y_GRID_SIZE, context)
        (output_sink, output_sink_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.Polygon,
            inputLyr.crs()
        )
        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        multiStepFeedback.setCurrentStep(0)
        grid = algRunner.runCreateGrid(
            extent=inputLyr.extent(),
            crs=inputLyr.crs(),
            hSpacing=xGridSize,
            vSpacing=yGridSize,
            feedback=multiStepFeedback,
            context=context
        )
        multiStepFeedback.setCurrentStep(1)
        algRunner.runCreateSpatialIndex(
            inputLyr=grid, context=context, feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(2)
        filteredGrid = algRunner.runExtractByLocation(
            inputLyr=grid,
            intersectLyr=inputLyr,
            context=context,
            feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(3)
        sortedFeatures = self.sortGrid(filteredGrid, fields, feedback=multiStepFeedback)
        multiStepFeedback.setCurrentStep(4)
        list(
            map(
                lambda x: output_sink.addFeature(
                    x,
                    QgsFeatureSink.FastInsert)
                ,
                sortedFeatures
            )
        )


        return {'OUTPUT':output_sink_id}

    def getOutputFields(self):
        fields = QgsFields()
        fields.append(QgsField('rank', QVariant.Int))
        fields.append(QgsField('visited', QVariant.Bool))
        return fields
    
    def buildSortCriteria(self, feat):
        geom = feat.geometry()
        firstVertex = geom.vertexAt(0)
        return (firstVertex.x(), firstVertex.y())

    
    def sortGrid(self, grid, fields, feedback):
        featList = [feat for feat in grid.getFeatures()]
        criteria = lambda feat: self.buildSortCriteria(feat)
        outputFeatList = []
        nSteps = len(featList)
        if nSteps == 0:
            return outputFeatList
        stepSize = 100/nSteps
        for current, feat in enumerate(
            sorted(
                sorted(featList, key=lambda feat: feat.geometry().vertexAt(0).x(), reverse=False),
                key=lambda feat: feat.geometry().vertexAt(0).y(),
                reverse=True
            )
        ):
            if feedback.isCanceled():
                break
            newFeat = QgsFeature(fields)
            newFeat['visited'] = False
            newFeat['rank'] = current
            newFeat.setGeometry(feat.geometry())
            outputFeatList.append(newFeat)
            feedback.setProgress(current * stepSize)
        return outputFeatList

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'createreviewgridalgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Create Review Grid')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Other Algorithms')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Other Algorithms'

    def tr(self, string):
        return QCoreApplication.translate('CreateReviewGridAlgorithm', string)

    def createInstance(self):
        return CreateReviewGridAlgorithm()
