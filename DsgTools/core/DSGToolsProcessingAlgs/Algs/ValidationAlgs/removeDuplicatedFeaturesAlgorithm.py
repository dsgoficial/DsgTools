# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-10-06
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
    QgsDataSourceUri,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
)
from .validationAlgorithm import ValidationAlgorithm


class RemoveDuplicatedFeaturesAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    ATTRIBUTE_BLACK_LIST = "ATTRIBUTE_BLACK_LIST"
    IGNORE_VIRTUAL_FIELDS = "IGNORE_VIRTUAL_FIELDS"
    IGNORE_PK_FIELDS = "IGNORE_PK_FIELDS"
    OUTPUT = "OUTPUT"

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
            QgsProcessingParameterField(
                self.ATTRIBUTE_BLACK_LIST,
                self.tr("Fields to ignore"),
                None,
                "INPUT",
                QgsProcessingParameterField.Any,
                allowMultiple=True,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_VIRTUAL_FIELDS,
                self.tr("Ignore virtual fields"),
                defaultValue=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_PK_FIELDS,
                self.tr("Ignore primary key fields"),
                defaultValue=True,
            )
        )
        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT, self.tr("Original layer without duplicated features")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        attributeBlackList = self.parameterAsFields(
            parameters, self.ATTRIBUTE_BLACK_LIST, context
        )
        ignoreVirtual = self.parameterAsBool(
            parameters, self.IGNORE_VIRTUAL_FIELDS, context
        )
        ignorePK = self.parameterAsBool(parameters, self.IGNORE_PK_FIELDS, context)
        # Compute the number of steps to display within the progress bar and
        # get features from source
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        duplicatedGeomDict = layerHandler.getDuplicatedFeaturesDict(
            inputLyr,
            onlySelected=onlySelected,
            attributeBlackList=attributeBlackList,
            excludePrimaryKeys=ignorePK,
            ignoreVirtualFields=ignoreVirtual,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(1)
        self.deleteDuplicatedFeaturesFlags(
            inputLyr, duplicatedGeomDict, multiStepFeedback
        )

        return {self.OUTPUT: inputLyr}

    def deleteDuplicatedFeaturesFlags(self, inputLyr, duplicatedGeomDict, feedback):
        size = 100 / len(duplicatedGeomDict) if duplicatedGeomDict else 0
        deleteList = []
        for current, (bboxKey, featList) in enumerate(duplicatedGeomDict.items()):
            if feedback.isCanceled():
                break
            if len(featList) > 1:
                deleteList += [feat.id() for feat in featList[1::]]
            feedback.setProgress(size * current)
        inputLyr.startEditing()
        inputLyr.beginEditCommand("Deleting features")
        inputLyr.deleteFeatures(deleteList)
        inputLyr.endEditCommand()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "removeduplicatedfeatures"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Remove Duplicated Features")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Correction Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Correction Processes)"

    def tr(self, string):
        return QCoreApplication.translate("RemoveDuplicatedFeaturesAlgorithm", string)

    def createInstance(self):
        return RemoveDuplicatedFeaturesAlgorithm()
