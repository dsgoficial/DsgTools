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


from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from DsgTools.core.GeometricTools.featureHandler import FeatureHandler

from PyQt5.QtCore import QCoreApplication
import processing

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
    QgsProcessingParameterMultipleLayers,
    QgsWkbTypes,
    QgsProcessingUtils,
    QgsProject,
)


class DonutHoleExtractorAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    OUTERSHELL = "OUTERSHELL"
    DONUTHOLE = "DONUTHOLE"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input Polygon Layer"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTERSHELL, self.tr("Outer Shell"))
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.DONUTHOLE, self.tr("Donut Hole"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        featureHandler = FeatureHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )

        inputType = inputLyr.wkbType()
        isMulti = QgsWkbTypes.isMultiType(inputType)
        inputFields = inputLyr.fields()

        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        (outershell_sink, outershell_dest_id) = self.parameterAsSink(
            parameters,
            self.OUTERSHELL,
            context,
            inputFields,
            inputType,
            inputLyr.sourceCrs(),
        )
        if outershell_sink is None:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.OUTERSHELL)
            )

        (donuthole_sink, donuthole_dest_id) = self.parameterAsSink(
            parameters,
            self.DONUTHOLE,
            context,
            inputFields,
            inputType,
            inputLyr.sourceCrs(),
        )
        if outershell_sink is None:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.DONUTHOLE)
            )
        # Compute the number of steps to display within the progress bar and
        # get features from source
        featureList, total = self.getIteratorAndFeatureCount(
            inputLyr, onlySelected=onlySelected
        )  # only selected is not applied because we are using an inner layer, not the original ones

        for current, feat in enumerate(featureList):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
            (
                outerShellFeatList,
                donutHoleFeatList,
            ) = featureHandler.getFeatureOuterShellAndHoles(feat, isMulti)
            for feat in outerShellFeatList:
                outershell_sink.addFeature(feat, QgsFeatureSink.FastInsert)
            for feat in donutHoleFeatList:
                donuthole_sink.addFeature(feat, QgsFeatureSink.FastInsert)
            # # Update the progress bar
            feedback.setProgress(int(current * total))
        return {self.DONUTHOLE: donuthole_dest_id, self.OUTERSHELL: outershell_dest_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "donutholeextractor"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Donut Hole Extractor")

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
        return QCoreApplication.translate("DonutHoleExtractorAlgorithm", string)

    def createInstance(self):
        return DonutHoleExtractorAlgorithm()
