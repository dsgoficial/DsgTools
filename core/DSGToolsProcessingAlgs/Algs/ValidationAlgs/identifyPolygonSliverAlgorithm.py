# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2021-05-24
        git sha              : $Format:%H$
        copyright            : (C) 2021 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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

from qgis.core import (QgsProcessing,
                       QgsProcessingException,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterBoolean,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterMultipleLayers)
from qgis.PyQt.QtCore import QCoreApplication

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs\
       .validationAlgorithm import ValidationAlgorithm


class IdentifyPolygonSliverAlgorithm(ValidationAlgorithm):
    """
    Identifies sliver polygons, which often are characterised by long,
    elongated areas which do not represent an entity in reality and,
    therefore, need to be removed.
    """
    FLAGS = "FLAGS"
    INPUT_LAYERS = "INPUT_LAYERS"
    SELECTED = "SELECTED"
    RATIO_TOL = "RATIO_TOL"

    def initAlgorithm(self, config):
        """
        Sets all parameters to be used and displayed on algorithm's GUI.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr("Polygons to be checked"),
                QgsProcessing.TypeVectorPolygon
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr("Process only selected features")
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.RATIO_TOL,
                self.tr("Tolerance area-perimeter ratio"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=10
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr("{0} flags").format(self.displayName())
            )
        )

    def getParameters(self, parameters, context, feedback):
        """
        Reads the algorithm's parameters from its mapping.
        :param parameters: (dict) mapping from algorithms input's name to its
                           value.
        :param context: (QgsProcessingContext) execution's environmental info.
        :param feeback: (QgsProcessingFeedback) QGIS object to keep track of
                        algorithm's progress/status.
        :return: (tuple) input parameters provided.
        """
        layers = self.parameterAsLayerList(
            parameters,
            self.INPUT_LAYERS,
            context
        )
        selected = self.parameterAsBoolean(
            parameters,
            self.SELECTED,
            context
        )
        ratio = self.parameterAsDouble(parameters, self.RATIO_TOL, context)
        return (layers, selected, ratio)

    def processAlgorithm(self, parameters, context, feedback):
        """
        Method that triggers the data processing algorithm.
        :param parameters: (dict) mapping from algorithms input's name to its
                           value.
        :param context: (QgsProcessingContext) execution's environmental info.
        :param feedback: (QgsProcessingFeedback) QGIS object to keep track of
                         algorithm's progress/status.
        :return: (dict) output mapping for identified flags.
        """
        layers, selected, ratio = self.getParameters(
            parameters, context, feedback)
        if not layers:
            raise QgsProcessingException(self.tr("No layers were provided."))
        for layer in layers:
            if layer.featureCount() > 0:
                geomType = next(layer.getFeatures()).geometry().wkbType()
                break
        else:
            raise QgsProcessingException(self.tr("All layers are empty."))
        self.prepareFlagSink(parameters, layers[0], geomType, context)
        flags = dict()
        lh = LayerHandler()
        flagCount = 0
        # a step for each input + 1 for loading flags into sink
        multiStepFeedback = QgsProcessingMultiStepFeedback(
            len(layers) + 1, feedback)
        multiStepFeedback.setCurrentStep(0)
        for step, layer in enumerate(layers):
            if multiStepFeedback.isCanceled():
                break
            # running polygon slivers to purposely raise an exception if an
            # empty geometry is found
            multiStepFeedback.pushInfo(
                self.tr("Checking {0}...").format(layer.name()))
            slivers = lh.getPolygonSlivers(
                layer, ratio, selected, False, multiStepFeedback)
            if slivers:
                # pushWarnign is only avalailable on 3.16.2+
                # multiStepFeedback.pushWarning(
                multiStepFeedback.pushDebugInfo(
                    self.tr("{0} slivers were found on {1}!")\
                        .format(len(slivers), layer.name())
                )
                flags[layer] = slivers
                flagCount += len(slivers)
            multiStepFeedback.setCurrentStep(step + 1)
        self.tr("Populating flags layer...")
        self.flagPolygonSlivers(flags, flagCount, multiStepFeedback)
        multiStepFeedback.setCurrentStep(step + 2)
        return {self.FLAGS: self.flag_id}

    def flagPolygonSlivers(self, flags, flagCount, feedback):
        """
        Creates and inserts flag features in feature sink to be used as flag
        layer.
        :param flags: (dict) map from layer to its polygon slivers.
        :param flagCount: (int) count of flags, in total, found.
        :param feeback: (QgsProcessingFeedback) QGIS object to keep track of
                        algorithm's progress/status.
        """
        stepSize = 100 / flagCount if flagCount > 0 else 0
        current = 0
        for layer, slivers in flags.items():
            if feedback.isCanceled():
                break
            layername = layer.name()
            for feat in slivers:
                if feedback.isCanceled():
                    break
                self.flagFeature(
                    feat.geometry(), self.tr("Clean error on unified layer."))
                current += 1
                feedback.setProgress(current * stepSize)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifypolygonsliver"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify polygon slivers")

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
            "IdentifyPolygonSliverAlgorithm", string)

    def createInstance(self):
        return IdentifyPolygonSliverAlgorithm()
