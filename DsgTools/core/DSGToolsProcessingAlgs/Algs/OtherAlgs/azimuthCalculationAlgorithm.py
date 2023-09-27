# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-08-22
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Matheus Alves Silva - Cartographic Engineer @ Brazilian Army
        email                : matheus.silva@ime.eb.br
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

from qgis import core
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingException,
)
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.Qt import QVariant


class AzimuthCalculationAlgorithm(QgsProcessingAlgorithm):

    INPUT_LAYER = "INPUT_LAYER"
    ATTRIBUTE = "ATTRIBUTE"
    FEATURES_SELECTED = "FEATURES_SELECTED"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LAYER,
                self.tr("Input layer"),
                [QgsProcessing.TypeVectorLine, QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.FEATURES_SELECTED, self.tr("Change filled values")
            )
        )

        self.addParameter(
            core.QgsProcessingParameterField(
                self.ATTRIBUTE,
                self.tr("Select the attribute that will receive the azimuth"),
                type=core.QgsProcessingParameterField.Any,
                parentLayerParameterName=self.INPUT_LAYER,
                allowMultiple=False,
                defaultValue=None,
                optional=False,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)

        filledFeatures = self.parameterAsBool(
            parameters, self.FEATURES_SELECTED, context
        )

        if inputLyr is None:
            raise QgsProcessingException("Choose a layer for azimuth calculation")

        attributeAzim = self.parameterAsFields(parameters, self.ATTRIBUTE, context)[0]

        inputLyr.startEditing()
        inputLyr.beginEditCommand(f'Updating the attribute "{attributeAzim}"')

        nSteps = inputLyr.featureCount()
        if nSteps == 0:
            return {self.OUTPUT: ""}

        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)

        for current, feat in enumerate(inputLyr.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            multiStepFeedback.setCurrentStep(current)
            orientMiniBBox = self.orientedMinimunBBoxFeat(feat)

            angAzim = orientMiniBBox[2]
            if orientMiniBBox[3] < orientMiniBBox[4]:
                angAzim = orientMiniBBox[2] - 90
                if angAzim < 0:
                    angAzim = orientMiniBBox[2] + 90

            if feat[f"{attributeAzim}"] != QVariant(None):
                if not filledFeatures:
                    continue
                feat[f"{attributeAzim}"] = round(angAzim)
            else:
                feat[f"{attributeAzim}"] = round(angAzim)

            inputLyr.updateFeature(feat)

        inputLyr.endEditCommand()

        return {self.OUTPUT: ""}

    def orientedMinimunBBoxFeat(self, feat):
        geom = feat.geometry()
        orientMiniBBox = geom.orientedMinimumBoundingBox()
        return orientMiniBBox

    def name(self):
        """
        Here is where the processing itself takes place.
        """
        return "azimuthcalculation"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Azimuth Calculation")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Other Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Other Algorithms"

    def tr(self, string):
        return QCoreApplication.translate(
            "The algorithm calculates the azimuth of each feature", string
        )

    def createInstance(self):
        return AzimuthCalculationAlgorithm()
