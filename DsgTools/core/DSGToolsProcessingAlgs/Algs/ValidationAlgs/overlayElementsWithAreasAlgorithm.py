# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-17
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

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterEnum,
    QgsProcessingParameterVectorLayer,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class OverlayElementsWithAreasAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    OVERLAY = "OVERLAY"
    SELECTED_OVERLAY = "SELECTED_OVERLAY"
    BEHAVIOR = "BEHAVIOR"
    OUTPUT = "OUTPUT"
    RemoveOutside, RemoveInside, OverlayAndKeep = list(range(3))

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input Layer"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.OVERLAY,
                self.tr("Polygon overlay Layer"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED_OVERLAY,
                self.tr("Use only selected features from overlay layer"),
            )
        )
        self.modes = [
            self.tr("Remove outside elements"),
            self.tr("Remove inside elements"),
            self.tr("Overlay and Keep Elements"),
        ]

        self.addParameter(
            QgsProcessingParameterEnum(
                self.BEHAVIOR, self.tr("Behavior"), options=self.modes, defaultValue=0
            )
        )
        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT, self.tr("Original layer with overlayed elements")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        self.algRunner = AlgRunner()

        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        overlayLyr = self.parameterAsVectorLayer(parameters, self.OVERLAY, context)
        if overlayLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.OVERLAY)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        onlySelectedOverlay = self.parameterAsBool(
            parameters, self.SELECTED_OVERLAY, context
        )
        behavior = self.parameterAsEnum(parameters, self.BEHAVIOR, context)

        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Populating temp layer..."))
        auxLyr = layerHandler.createAndPopulateUnifiedVectorLayer(
            [inputLyr],
            geomType=inputLyr.wkbType(),
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(1)
        if onlySelectedOverlay:
            overlayLyr = layerHandler.createAndPopulateUnifiedVectorLayer(
                [overlayLyr],
                geomType=overlayLyr.wkbType(),
                onlySelected=onlySelectedOverlay,
                feedback=multiStepFeedback,
            )
            overlayLyr.startEditing()
            overlayLyr.renameAttribute(0, "fid")
            overlayLyr.renameAttribute(1, "cl")
            overlayLyr.commitChanges()
            self.algRunner.runCreateSpatialIndex(overlayLyr, context=context)
        # 1- check method
        # 2- if overlay and keep, use clip and symetric difference
        # 3- if remove outside, use clip
        # 4- if remove inside, use symetric difference
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr("Running overlay..."))
        outputLyr = self.runOverlay(
            auxLyr, overlayLyr, behavior, context, multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(3)
        multiStepFeedback.pushInfo(self.tr("Updating original layer..."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [inputLyr], outputLyr, feedback=multiStepFeedback, onlySelected=onlySelected
        )

        return {self.OUTPUT: inputLyr}

    def runOverlay(self, lyr, overlayLyr, behavior, context, feedback):
        nSteps = 2 if behavior == 2 else 1
        localFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        localFeedback.setCurrentStep(0)
        # Intentional ifs not if else.
        if behavior in [
            OverlayElementsWithAreasAlgorithm.RemoveOutside,
            OverlayElementsWithAreasAlgorithm.OverlayAndKeep,
        ]:
            outputLyr = self.algRunner.runClip(
                lyr, overlayLyr, context, feedback=localFeedback
            )
            if behavior == OverlayElementsWithAreasAlgorithm.RemoveOutside:
                return outputLyr
            localFeedback.setCurrentStep(1)
        if behavior in [
            OverlayElementsWithAreasAlgorithm.RemoveInside,
            OverlayElementsWithAreasAlgorithm.OverlayAndKeep,
        ]:
            outputDiffLyr = self.algRunner.runSymDiff(
                lyr, overlayLyr, context, feedback=localFeedback
            )
            if behavior == OverlayElementsWithAreasAlgorithm.RemoveInside:
                return outputDiffLyr
        if behavior == OverlayElementsWithAreasAlgorithm.OverlayAndKeep:
            outputLyr.startEditing()
            outputLyr.beginEditCommand("")
            outputLyr.addFeatures(outputDiffLyr.getFeatures())
            outputLyr.endEditCommand()
            outputLyr.commitChanges()
            return outputLyr

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "overlayelementswithareas"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Overlay Elements With Areas")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Geometric Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Geometric Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("OverlayElementsWithAreasAlgorithm", string)

    def createInstance(self):
        return OverlayElementsWithAreasAlgorithm()
