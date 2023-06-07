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
from PyQt5.QtCore import QCoreApplication

from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from qgis.core import (
    QgsDataSourceUri,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingException,
)

from .validationAlgorithm import ValidationAlgorithm
from ..Help.algorithmHelpCreator import HTMLHelpCreator as help


class IdentifyAnglesInInvalidRangeAlgorithm(ValidationAlgorithm):
    FLAGS = "FLAGS"
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    MIN_ANGLE = "MIN_ANGLE"
    MAX_ANGLE = "MAX_ANGLE"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input layer"),
                [QgsProcessing.TypeVectorLine, QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_ANGLE, self.tr("Minimum angle"), minValue=0, defaultValue=80
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MAX_ANGLE, self.tr("Maximum angle"), minValue=0, defaultValue=100
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
        geometryHandler = GeometryHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        minAngle = self.parameterAsDouble(parameters, self.MIN_ANGLE, context)
        maxAngle = self.parameterAsDouble(parameters, self.MAX_ANGLE, context)
        if maxAngle <= minAngle:
            raise QgsProcessingException(self.tr("Invalid Range"))
        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.Point, context)
        # Compute the number of steps to display within the progress bar and
        # get features from source
        featureList, total = self.getIteratorAndFeatureCount(
            inputLyr, onlySelected=onlySelected
        )

        for current, feat in enumerate(featureList):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
            outOfBoundsList = geometryHandler.getOutOfBoundsAngle(
                feat, 0, invalidRange=[minAngle, maxAngle]
            )
            if outOfBoundsList:
                for item in outOfBoundsList:
                    flagText = self.tr(
                        "Feature from layer {0} with id={1} has angle of value {2} degrees, which is in invalid interval [{3},{4}]."
                    ).format(
                        inputLyr.name(),
                        item["feat_id"],
                        item["angle"],
                        minAngle,
                        maxAngle,
                    )
                    self.flagFeature(item["geom"], flagText)
            # Update the progress bar
            feedback.setProgress(int(current * total))

        return {self.FLAGS: self.flag_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyanglesininvalidrangealgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Angles in Invalid Range")

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
            "IdentifyAnglesInInvalidRangeAlgorithm", string
        )

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    def helpUrl(self):
        return  help().helpUrl(self.name())

    def createInstance(self):
        return IdentifyAnglesInInvalidRangeAlgorithm()
