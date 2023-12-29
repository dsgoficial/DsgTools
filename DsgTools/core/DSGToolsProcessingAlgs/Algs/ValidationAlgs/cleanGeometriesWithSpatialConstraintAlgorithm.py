# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-12-29
        git sha              : $Format:%H$
        copyright            : (C) 2013 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
    QgsWkbTypes,
    QgsProcessingParameterVectorLayer,
)

from ...algRunner import AlgRunner
from .cleanGeometriesAlgorithm import CleanGeometriesAlgorithm


class CleanGeometriesWithSpatialConstraintAlgorithm(CleanGeometriesAlgorithm):
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        super().initAlgorithm(config)
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr("Geographic Bounds Layer"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()

        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        if inputLyr.geometryType() == QgsWkbTypes.PolygonGeometry:
            raise NotImplementedError(self.tr("Method not implemented yet"))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        snap = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        # if snap < 0 and snap != -1:
        #     raise QgsProcessingException(self.invalidParameterError(parameters, self.TOLERANCE))
        minArea = self.parameterAsDouble(parameters, self.MINAREA, context)
        geographicBoundsLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )
        self.prepareFlagSink(parameters, inputLyr, inputLyr.wkbType(), context)

        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Populating temp layer..."))
        auxLyr = layerHandler.createAndPopulateUnifiedVectorLayer(
            [inputLyr],
            geomType=inputLyr.wkbType(),
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(1)
        (
            insideLyr,
            outsideLyr,
        ) = layerHandler.prepareAuxLayerForSpatialConstrainedAlgorithm(
            inputLyr=auxLyr,
            geographicBoundaryLyr=geographicBoundsLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr("Running clean..."))
        cleanedLyr, error = algRunner.runClean(
            insideLyr,
            [algRunner.RMSA, algRunner.Break, algRunner.RmDupl, algRunner.RmDangle],
            context,
            returnError=True,
            snap=snap,
            minArea=minArea,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(3)
        outputLyr = (
            layerHandler.integrateSpatialConstrainedAlgorithmOutputAndOutsideLayer(
                algOutputLyr=cleanedLyr,
                outsideLyr=outsideLyr,
                tol=snap,
                context=context,
                feedback=multiStepFeedback,
            )
        )
        multiStepFeedback.setCurrentStep(4)
        multiStepFeedback.pushInfo(self.tr("Updating original layer..."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [inputLyr],
            outputLyr,
            feedback=multiStepFeedback,
            onlySelected=onlySelected,
        )
        self.flagIssues(cleanedLyr, error, feedback)

        return {self.OUTPUT: inputLyr, self.FLAGS: self.flag_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "cleangeometrieswithspatialconstraintalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Clean Geometries With Spatial Constraint")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Snap Processes")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Snap Processes"

    def tr(self, string):
        return QCoreApplication.translate(
            "CleanGeometriesWithSpatialConstraintAlgorithm", string
        )

    def createInstance(self):
        return CleanGeometriesWithSpatialConstraintAlgorithm()
