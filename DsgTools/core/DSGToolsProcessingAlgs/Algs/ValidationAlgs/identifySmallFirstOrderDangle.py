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
from ..Help.algorithmHelpCreator import HTMLHelpCreator as help
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterNumber,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingMultiStepFeedback,
    QgsFeatureRequest,
    QgsWkbTypes,
)


class IdentifySmallFirstOrderDanglesAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    SEARCH_RADIUS = "SEARCH_RADIUS"
    MIN_LENGTH = "MIN_LENGTH"
    LINEFILTERLAYERS = "LINEFILTERLAYERS"
    POLYGONFILTERLAYERS = "POLYGONFILTERLAYERS"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT, self.tr("Input layer"), [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_LENGTH,
                self.tr("Minimum size"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.001,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SEARCH_RADIUS,
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
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr(
                    "Geographic Boundary (this layer only filters the output dangles)"
                ),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
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
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        minLength = self.parameterAsDouble(parameters, self.MIN_LENGTH, context)
        searchRadius = self.parameterAsDouble(parameters, self.SEARCH_RADIUS, context)
        lineFilterLyrList = self.parameterAsLayerList(
            parameters, self.LINEFILTERLAYERS, context
        )
        polygonFilterLyrList = self.parameterAsLayerList(
            parameters, self.POLYGONFILTERLAYERS, context
        )
        geographicBoundsLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )
        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.LineString, context)
        if inputLyr is None:
            return {self.FLAGS: self.flag_id}
        # Compute the number of steps to display within the progress bar and
        # get features from source
        feedbackTotal = 2
        multiStepFeedback = QgsProcessingMultiStepFeedback(feedbackTotal, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(self.tr("Getting Dangles..."))
        dangleLyr = AlgRunner().runIdentifyDangles(
            inputLayer=inputLyr,
            searchRadius=searchRadius,
            context=context,
            onlySelected=onlySelected,
            lineFilter=lineFilterLyrList,
            polygonFilter=polygonFilterLyrList,
            ignoreDanglesOnUnsegmentedLines=True,
            inputIsBoundaryLayer=True,
            geographicBoundsLyr=geographicBoundsLyr,
            feedback=multiStepFeedback,
        )

        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.setProgressText(self.tr("Raising flags..."))
        nDangles = dangleLyr.featureCount()
        if nDangles == 0:
            return {self.FLAGS: self.flag_id}
        # currentValue = feedback.progress()
        currentTotal = 100 / nDangles
        for current, feat in enumerate(dangleLyr.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            dangleGeom = feat.geometry()
            dangleBB = dangleGeom.boundingBox()
            request = QgsFeatureRequest().setNoAttributes().setFilterRect(dangleBB)
            lineGeometry = [
                i.geometry()
                for i in inputLyr.getFeatures(request)
                if i.geometry().intersects(dangleGeom)
            ][0]
            if lineGeometry.length() > minLength:
                continue
            self.flagFeature(
                lineGeometry,
                self.tr(
                    f"First order dangle on {inputLyr.name()} smaller than {minLength}"
                ),
            )
            multiStepFeedback.setProgress(current * currentTotal)
        return {self.FLAGS: self.flag_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifysmallfirstorderdangles"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Small First Order Dangles")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Small Object Handling")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Small Object Handling"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifySmallFirstOrderDanglesAlgorithm", string
        )

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    def helpUrl(self):
        return  help().helpUrl(self.name())

    def createInstance(self):
        return IdentifySmallFirstOrderDanglesAlgorithm()
