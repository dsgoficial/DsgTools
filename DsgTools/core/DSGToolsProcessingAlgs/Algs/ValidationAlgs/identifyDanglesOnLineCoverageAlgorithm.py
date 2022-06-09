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


class IdentifyDanglesOnLineCoverageAlgorithm(ValidationAlgorithm):
    INPUT_LINES = "INPUT_LINES"
    SELECTED = "SELECTED"
    TOLERANCE = "TOLERANCE"
    LINEFILTERLAYERS = "LINEFILTERLAYERS"
    POLYGONFILTERLAYERS = "POLYGONFILTERLAYERS"
    TYPE = "TYPE"
    IGNOREINNER = "IGNOREINNER"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LINES, self.tr("Input lines"), [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE,
                self.tr("Search radius"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=2,
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
                self.TYPE, self.tr("Ignore dangle on unsegmented lines")
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNOREINNER, self.tr("Ignore search radius on inner layer search")
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
        inputLineLayers = self.parameterAsVectorLayer(
            parameters, self.INPUT_LINES, context
        )
        searchRadius = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        lineFilterLyrList = self.parameterAsLayerList(
            parameters, self.LINEFILTERLAYERS, context
        )
        polygonFilterLyrList = self.parameterAsLayerList(
            parameters, self.POLYGONFILTERLAYERS, context
        )
        ignoreNotSplit = self.parameterAsBool(parameters, self.TYPE, context)
        ignoreInner = self.parameterAsBool(parameters, self.IGNOREINNER, context)

        # Compute the number of steps to display within the progress bar and
        # get features from source
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Building unified lines layer..."))
        mergedLines = algRunner.runMergeVectorLayers(
            inputList=inputLineLayers, feedback=multiStepFeedback, context=context
        )
        multiStepFeedback.setCurrentStep(1)
        return {
            "FLAGS": algRunner.runIdentifyDangles(
                inputLayer=mergedLines,
                searchRadius=searchRadius,
                lineFilter=lineFilterLyrList,
                polygonFilter=polygonFilterLyrList,
                ignoreInner=ignoreInner,
                ignoreUnsegmented=ignoreNotSplit,
                feedback=multiStepFeedback,
                context=context
            )
        }


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifydanglesonlinecoverage"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Dangles on Line Coverage")

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
            "IdentifyDanglesOnLineCoverageAlgorithm", string
        )

    def createInstance(self):
        return IdentifyDanglesOnLineCoverageAlgorithm()
