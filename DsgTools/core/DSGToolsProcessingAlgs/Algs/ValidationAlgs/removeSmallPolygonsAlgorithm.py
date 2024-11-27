# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-06-08
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

from qgis.core import (
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class RemoveSmallPolygonsAlgorithm(ValidationAlgorithm):
    FLAGS = "FLAGS"
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    TOLERANCE = "TOLERANCE"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input layer"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE, self.tr("Area tolerance"), QgsProcessingParameterNumber.Double, minValue=0, defaultValue=625
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        tol = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        featureList, total = self.getIteratorAndFeatureCount(
            inputLyr, onlySelected=onlySelected
        )
        if total == 0:
            return {}
        stepSize = 100 / total
        idRemoveSet = set()
        for current, feat in enumerate(featureList):
            geometry = feat.geometry()
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
            if geometry.area() > tol:
                continue
            idRemoveSet.add(feat.id())
            feedback.setProgress(current * stepSize)
        inputLyr.startEditing()
        inputLyr.beginEditCommand(f"Deleting features on layer {inputLyr.name()}.")
        inputLyr.deleteFeatures(list(idRemoveSet))
        inputLyr.endEditCommand()
        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "removesmallpolygons"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Remove Small Polygons")

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
        return QCoreApplication.translate("RemoveSmallPolygonsAlgorithm", string)

    def createInstance(self):
        return RemoveSmallPolygonsAlgorithm()
