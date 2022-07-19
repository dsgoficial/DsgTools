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
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from .validationAlgorithm import ValidationAlgorithm
import processing
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
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
    QgsProcessingMultiStepFeedback,
)


class IdentifyNetworkConstructionIssuesAlgorithm(ValidationAlgorithm):
    INPUT_LINES = "INPUT_LINES"
    SELECTED = 'SELECTED'
    TOLERANCE = "TOLERANCE"
    LINEFILTERLAYERS = "LINEFILTERLAYERS"
    POLYGONFILTERLAYERS = "POLYGONFILTERLAYERS"
    IGNORE_DANGLES_ON_UNSEGMENTED_LINES = 'IGNORE_DANGLES_ON_UNSEGMENTED_LINES'
    INPUT_IS_BOUDARY_LAYER = 'INPUT_IS_BOUDARY_LAYER'
    GEOGRAPHIC_BOUNDARY = 'GEOGRAPHIC_BOUNDARY'
    FLAGS = 'FLAGS'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LINES,
                self.tr("Input lines"),
                QgsProcessing.TypeVectorLine,
                optional=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.INPUT_IS_BOUDARY_LAYER,
                self.tr(
                    'Input is a boundary layer (every line must be connected '
                    'to an element of either the input layer or the filters)'
                )
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE,
                self.tr("Search radius"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.0001,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.LINEFILTERLAYERS,
                self.tr("Linestring Filter Layers"),
                QgsProcessing.TypeVectorLine,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.POLYGONFILTERLAYERS,
                self.tr("Polygon Filter Layers"),
                QgsProcessing.TypeVectorPolygon,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_DANGLES_ON_UNSEGMENTED_LINES,
                self.tr('Ignore dangle on unsegmented lines')
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr('Geographic Boundary (this layer only filters the output dangles)'),
                [QgsProcessing.TypeVectorPolygon],
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.layerHandler = LayerHandler()
        algRunner = AlgRunner()
        lineLyrList = self.parameterAsLayerList(
            parameters, self.INPUT_LINES, context
        )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        searchRadius = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        lineFilterLyrList = self.parameterAsLayerList(parameters, self.LINEFILTERLAYERS, context)
        polygonFilterLyrList = self.parameterAsLayerList(parameters, self.POLYGONFILTERLAYERS, context)
        ignoreDanglesOnUnsegmentedLines = self.parameterAsBool(
            parameters, self.IGNORE_DANGLES_ON_UNSEGMENTED_LINES, context)
        inputIsBoundaryLayer = self.parameterAsBool(
            parameters, self.INPUT_IS_BOUDARY_LAYER, context)
        geographicBoundsLyr = self.parameterAsVectorLayer(parameters, self.GEOGRAPHIC_BOUNDARY, context)
        self.prepareFlagSink(parameters, lineLyrList[0], QgsWkbTypes.Point, context)
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Building unified lines layer..."))
        mergedLines = self.getInputLineLayers(context, algRunner, lineLyrList, onlySelected, multiStepFeedback)
        multiStepFeedback.setCurrentStep(1)
        outputLyr = algRunner.runIdentifyDangles(
            inputLayer=mergedLines,
            searchRadius=searchRadius,
            lineFilter=lineFilterLyrList,
            polygonFilter=polygonFilterLyrList,
            ignoreDanglesOnUnsegmentedLines=ignoreDanglesOnUnsegmentedLines,
            inputIsBoundaryLayer=inputIsBoundaryLayer,
            geographicBoundsLyr=geographicBoundsLyr,
            feedback=multiStepFeedback,
            context=context,
        )
        multiStepFeedback.setCurrentStep(2)
        self.flagSink.addFeatures(outputLyr.getFeatures(), QgsFeatureSink.FastInsert)
        return {
            "FLAGS": self.flag_id
        }

    def getInputLineLayers(self, context, algRunner, lineLyrList, onlySelected, feedback):
        nSteps = 2 if not onlySelected else 2 + len(lyrList)
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        def getLineLayer(currentStep, lineLyr):
            multiStepFeedback.setCurrentStep(currentStep)
            return lineLyr if not onlySelected \
                else algRunner.runSaveSelectedFeatures(
                    lineLyr,
                    context,
                    feedback=multiStepFeedback
                )
            
        lyrList = [
            getLineLayer(currentStep, lineLyr)
            for currentStep, lineLyr in enumerate(lineLyrList)
        ]
        multiStepFeedback.setCurrentStep(nSteps-1)
        mergedLines = algRunner.runMergeVectorLayers(
            inputList=lyrList, feedback=multiStepFeedback, context=context
        )
        return mergedLines

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifynetworkconstructionissues"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Network Construction Issues")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Identification Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Identification Processes)"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifyNetworkConstructionIssuesAlgorithm", string
        )

    def createInstance(self):
        return IdentifyNetworkConstructionIssuesAlgorithm()
