# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-05-23
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from typing import List
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsFeature,
    QgsFields,
    QgsProcessingException,
    QgsFeatureSink,
    QgsProcessingParameterField,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsWkbTypes,
    QgsVectorLayer,
    QgsProcessingContext,
    QgsFeedback,
    QgsProcessingParameterDistance,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class OverlayLinesWithLinesAndUpdate(QgsProcessingAlgorithm):
    """
    Algorithm that splits input lines at intersections with reference lines.
    It also ensures that intersection points are added as vertices to reference lines
    if they don't already exist there.
    """

    INPUT = "INPUT"
    SELECTED = "SELECTED"
    REFERENCE_LINES = "REFERENCE_LINES"
    SNAP_TOLERANCE = "SNAP_TOLERANCE"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"

    def initAlgorithm(self, config=None):
        """
        Define the inputs and outputs of the algorithm.
        """
        # Add the input line features source
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input line layer"),
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )

        # Add the reference line layers parameter
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.REFERENCE_LINES,
                self.tr("Reference line layers"),
                QgsProcessing.TypeVectorLine,
            )
        )

        # Add snap tolerance parameter for vertex insertion
        param = QgsProcessingParameterNumber(
            self.SNAP_TOLERANCE,
            self.tr("Snap tolerance for vertex insertion"),
            QgsProcessingParameterNumber.Double,
            defaultValue=0.001,
            minValue=0.0,
            optional=True,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 8}})
        self.addParameter(param)

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr("Geographic Bounds Layer"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        # Initialize algRunner for processing operations
        algRunner = AlgRunner()

        # Retrieve the feature sources
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)

        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)

        # Get reference line layers
        referenceLyrList = self.parameterAsLayerList(
            parameters, self.REFERENCE_LINES, context
        )

        # Get snap tolerance
        snap_tolerance = self.parameterAsDouble(
            parameters, self.SNAP_TOLERANCE, context
        )

        geographicBoundsLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )

        self.layerHandler = LayerHandler()

        self.runLineOnLineOverlayerWithoutGeographicBounds(
            inputLyr=inputLyr,
            referenceLyrList=referenceLyrList,
            tol=snap_tolerance,
            onlySelected=onlySelected,
            context=context,
            feedback=feedback,
        ) if geographicBoundsLyr is None else self.runLineOnLineOverlayerWithGeographicBounds(
            inputLyr=inputLyr,
            referenceLyrList=referenceLyrList,
            tol=snap_tolerance,
            onlySelected=onlySelected,
            context=context,
            feedback=feedback,
            geographicBoundsLyr=geographicBoundsLyr,
        )

        return {}

    def runLineOnLineOverlayerWithoutGeographicBounds(
        self,
        inputLyr: QgsVectorLayer,
        referenceLyrList: List[QgsVectorLayer],
        tol: float,
        onlySelected: bool,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> None:
        multiStepFeedback = QgsProcessingMultiStepFeedback(6, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Building unified layer..."))
        inputLyrList = [inputLyr]
        auxInputLyr = self.layerHandler.createAndPopulateUnifiedVectorLayer(
            inputLyrList,
            geomType=inputLyr.wkbType(),
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        auxReferenceLyr = self.layerHandler.createAndPopulateUnifiedVectorLayer(
            referenceLyrList,
            geomType=QgsWkbTypes.MultiLineString,
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        outputLinesLyr, outputReferenceLinesLyr = AlgRunner().runLineOnLineOverlayer(
            inputLyr=auxInputLyr,
            referenceLayers=[auxReferenceLyr],
            tol=tol,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        self.layerHandler.updateOriginalLayersFromUnifiedLayer(
            [inputLyr],
            outputLinesLyr,
            feedback=multiStepFeedback,
            onlySelected=onlySelected,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        self.layerHandler.updateOriginalLayersFromUnifiedLayer(
            referenceLyrList,
            outputReferenceLinesLyr,
            feedback=multiStepFeedback,
            onlySelected=False,
        )

    def runLineOnLineOverlayerWithGeographicBounds(
        self,
        inputLyr: QgsVectorLayer,
        referenceLyrList: List[QgsVectorLayer],
        tol: float,
        onlySelected: bool,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
        geographicBoundsLyr: QgsVectorLayer,
    ) -> None:
        pass

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate("LineOnLineOverlayerAlgorithm", string)

    def createInstance(self):
        return OverlayLinesWithLinesAndUpdate()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm.
        """
        return "overlaylineswithlinesandupdate"

    def displayName(self):
        """
        Returns the translated algorithm name.
        """
        return self.tr("Overlay input line to reference layers and update")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to.
        """
        return self.tr("QA Tools: Line Handling")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to.
        """
        return "DSGTools - QA Tools: Line Handling"

    def shortHelpString(self):
        """
        Returns a short helper string for the algorithm.
        """
        return self.tr(
            "This algorithm splits input lines at every intersection with reference lines "
            "and ensures that intersection points are added as vertices to reference lines. "
            "It preserves the original attributes from the input lines in the split output. "
            "Finally, it updates the input data with the computed values. If a geographic boundary is input, it only modifies data inside the geographic boundary."
        )
