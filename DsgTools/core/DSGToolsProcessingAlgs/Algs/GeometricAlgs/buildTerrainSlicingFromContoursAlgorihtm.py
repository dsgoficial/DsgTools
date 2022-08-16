# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-08-16
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

from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsGeometry, QgsProcessing, QgsProcessingException, QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink, QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField, QgsProject, QgsField, QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterNumber, QgsFeatureSink,
                       QgsProcessingParameterVectorLayer, QgsWkbTypes, QgsProcessingAlgorithm,
                       QgsFields)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class BuildTerrainSlicingFromContoursAlgorihtm(QgsProcessingAlgorithm):

    INPUT = 'INPUT'
    ELEVATION_FIELD = 'ELEVATION_FIELD'
    CONTOUR_INTERVAL = 'CONTOUR_INTERVAL'
    GEOGRAPHIC_BOUNDARY = 'GEOGRAPHIC_BOUNDARY'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input contour'),
                types=[QgsProcessing.TypeVectorLine]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.ELEVATION_FIELD,
                self.tr('Contour elevation field'), 
                type=QgsProcessingParameterField.Numeric, 
                parentLayerParameterName='INPUT', 
                allowMultiple=False, 
                defaultValue='cota')
            )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.CONTOUR_INTERVAL,
                self.tr('Equidistance value'), 
                type=QgsProcessingParameterNumber.Double, 
                minValue=0)
            )
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr('Geographic bounds layer'),
                [QgsProcessing.TypeVectorPolygon],
                optional=False
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output polygons')
            )
        )
    
    def processAlgorithm(self, parameters, context, feedback):
        algRunner = AlgRunner()
        source = self.parameterAsSource(parameters, self.INPUT, context)
        elevationField = self.parameterAsFields(
            parameters, self.ELEVATION_FIELD, context)[0]
        threshold = self.parameterAsDouble(
            parameters, self.CONTOUR_INTERVAL, context)
        geoBoundsSource = self.parameterAsSource(
            parameters, self.GEOGRAPHIC_BOUNDARY, context)
        (output_sink, output_sink_id) = self.getOutputSink(source, elevationField, parameters, context)

        multiStepFeedback = QgsProcessingMultiStepFeedback(7, feedback) #ajustar depois
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Building polygons lines..."))
        
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        boundaryLines = algRunner.runPolygonsToLines(
            parameters[self.GEOGRAPHIC_BOUNDARY],
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        linesLyr = algRunner.runMergeVectorLayers(
            inputList=[boundaryLines, parameters[self.INPUT]],
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        splitLinesLyr = algRunner.runSplitLinesWithLines(
            linesLyr,
            linesLyr,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        polygonLyr = algRunner.runPolygonize(
            splitLinesLyr,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        polygonsWithoutHoles = algRunner.runDeleteHoles(
            polygonLyr,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        addFeaturesToSink = lambda x: output_sink.addFeature(x, QgsFeatureSink.FastInsert)
        list(map(addFeaturesToSink, polygonsWithoutHoles.getFeatures()))

        return {"OUTPUT": output_sink_id}

    
    def getOutputSink(self, source, elevationField, parameters, context):
        outputFields = self.getOutputFields(elevationField)
        return self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            outputFields,
            QgsWkbTypes.Polygon,
            source.sourceCrs() if source is not None else QgsProject.instance().crs()
        )
    
    def getOutputFields(self, elevationField):
        fields = QgsFields()
        fields.append(QgsField(elevationField, QVariant.Int))
        fields.append(QgsField('class', QVariant.String))
        fields.append(QgsField('class_min', QVariant.Int))
        fields.append(QgsField('class_max', QVariant.Int))

        return fields


    def tr(self, string):
        return QCoreApplication.translate('BuildTerrainSlicingFromContoursAlgorihtm', string)

    def createInstance(self):
        return BuildTerrainSlicingFromContoursAlgorihtm()

    def name(self):
        return 'buildterrainslicingfromcontours'

    def displayName(self):
        return self.tr('Build Terrain Slicing from Contours')

    def group(self):
        return self.tr('Geometric Algorithms')

    def groupId(self):
        return 'DSGTools: Geometric Algorithms'

    def shortHelpString(self):
        return self.tr("O algoritmo constrói o fatiamento do terreno baseado nas curvas de nível.")
