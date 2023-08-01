# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-07-24
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsWkbTypes,
    QgsVectorLayerUtils,
    QgsProcessingException,
)


class AppendFeaturesToLayerAlgorithm(ValidationAlgorithm):
    DESTINATION_LAYER = "DESTINATION_LAYER"
    LAYER_WITH_FEATURES_TO_APPEND = "LAYER_WITH_FEATURES_TO_APPEND"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.DESTINATION_LAYER,
                self.tr("Destination Layer"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.LAYER_WITH_FEATURES_TO_APPEND,
                self.tr("Layer with features to append to original layer"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        destinationLayer = self.parameterAsVectorLayer(
            parameters, self.DESTINATION_LAYER, context
        )
        inputSource = self.parameterAsSource(
            parameters, self.LAYER_WITH_FEATURES_TO_APPEND, context
        )
        geometryHandler = GeometryHandler()
        if QgsWkbTypes.geometryType(
            destinationLayer.wkbType()
        ) != QgsWkbTypes.geometryType(inputSource.wkbType()):
            raise QgsProcessingException(
                self.tr(
                    "Geometry type missmatch between inputs. Both original layer and layer with features to append must have same geometry type."
                )
            )
        featCount = inputSource.featureCount()
        if featCount == 0:
            return {}
        stepSize = 100 / featCount
        primaryKeyFieldNames = self.getLayerPrimaryKeyAttributeNames(destinationLayer)
        destinationLayerNameToIdxMap = {
            field.name(): idx
            for idx, field in enumerate(destinationLayer.fields())
            if field.name() not in primaryKeyFieldNames
        }
        isDestinationMulti = QgsWkbTypes.isMultiType(destinationLayer.wkbType())

        def get_attr_map(feat):
            attrMap = dict()
            for fieldName, fieldValue in feat.attributeMap().items():
                if fieldName not in destinationLayerNameToIdxMap:
                    continue
                attrMap[destinationLayerNameToIdxMap[fieldName]] = fieldValue
            return attrMap

        destinationLayer.startEditing()
        destinationLayer.beginEditCommand(
            f"Appending features to layer {destinationLayer.name()}"
        )
        for current, feat in enumerate(inputSource.getFeatures()):
            if feedback.isCanceled():
                break
            if feat.geometry().isNull() or feat.geometry().isEmpty():
                continue
            attrMap = get_attr_map(feat)
            for geom in geometryHandler.handleGeometry(
                geom=feat.geometry(), parameterDict={"isMulti": isDestinationMulti}
            ):
                newFeat = QgsVectorLayerUtils.createFeature(
                    layer=destinationLayer, geometry=geom, attributes=attrMap
                )
                destinationLayer.addFeature(newFeat)
            feedback.setProgress(current * stepSize)
        destinationLayer.endEditCommand()
        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "appendfeaturestolayeralgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Append Features to Layer")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Data Management Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Data Management Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("AppendFeaturesToLayerAlgorithm", string)

    def createInstance(self):
        return AppendFeaturesToLayerAlgorithm()
