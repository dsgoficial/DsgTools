# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-04-12
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luizclaudio.andrade@eb.mil.br
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
)

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.GeometricTools.featureHandler import FeatureHandler


class DeaggregatorAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"

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

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        source = self.parameterAsSource(parameters, self.INPUT, context)
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        target = self.parameterAsVectorLayer(parameters, self.INPUT, context)

        target.startEditing()
        target.beginEditCommand("Updating layer")
        fields = target.fields()
        paramDict = LayerHandler().getDestinationParameters(target)
        featHandler = FeatureHandler()
        featuresToAdd = []
        if onlySelected:
            total = (
                100.0 / target.selectedFeatureCount()
                if target.selectedFeatureCount()
                else 0
            )
            features = target.getSelectedFeatures()
        else:
            total = 100.0 / target.featureCount() if target.featureCount() else 0
            features = target.getFeatures()

        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break
            if not feature.geometry():
                target.deleteFeature(feature.id())
                feedback.setProgress(int(current * total))
                continue
            updtGeom, newFeatList, update = featHandler.handleFeature(
                [feature], feature, target, paramDict
            )
            if not update:
                feature.setGeometry(updtGeom)
                target.updateFeature(feature)
                featuresToAdd += newFeatList
            feedback.setProgress(int(current * total))
        if featuresToAdd:
            target.addFeatures(featuresToAdd, QgsFeatureSink.FastInsert)
        target.endEditCommand()
        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "deaggregategeometries"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Deaggregate Geometries")

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
        return QCoreApplication.translate("DeaggregatorAlgorithm", string)

    def createInstance(self):
        return DeaggregatorAlgorithm()
