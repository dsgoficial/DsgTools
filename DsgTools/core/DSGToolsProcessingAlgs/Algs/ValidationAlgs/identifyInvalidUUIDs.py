# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-11
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Eliton / Pedro Martins - Cartographic Engineer @ Brazilian Army
        email                : eliton.filho / @eb.mil.br
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

import uuid

from qgis.core import (QgsField, QgsFields, QgsProcessing,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterString, QgsWkbTypes)
from qgis.PyQt.QtCore import QCoreApplication, QVariant

from .validationAlgorithm import ValidationAlgorithm


class IdentifyInvalidUUIDs(ValidationAlgorithm):

    INPUT_LAYERS = 'INPUT_LAYERS'
    ATTRIBUTE_NAME = 'ATTRIBUTE_NAME'
    CORRECT = 'CORRECT'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr('Input layer(s)'),
                QgsProcessing.TypeVectorAnyGeometry
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.ATTRIBUTE_NAME,
                description =  self.tr('Attribute name'),
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.CORRECT,
                self.tr('Fix?')
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Flags')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        inputLyrList = self.parameterAsLayerList(
            parameters,
            self.INPUT_LAYERS,
            context
        )
        attributeName = self.parameterAsFile(
            parameters,
            self.ATTRIBUTE_NAME,
            context
        )
        correct = self.parameterAsBool(
            parameters,
            self.CORRECT,
            context
        )
        output_dest_id = ''
        uuids = []
        errors = []
        listSize = len(inputLyrList)
        progressStep = 100/listSize if listSize else 0
        for step, layer in enumerate(inputLyrList):
            attributeIndex = self.getAttributeIndex(attributeName, layer)
            if attributeIndex < 0:
                continue
            if correct:
                layer.startEditing()
            for feature in layer.getFeatures():
                if feedback.isCanceled():
                    return {self.OUTPUT: output_dest_id}
                attributeValue = feature[attributeIndex]
                isValidUuid = self.isValidUuid(attributeValue)
                hasDuplicateValues = self.hasDuplicateValues(attributeValue, uuids)
                if isValidUuid and not hasDuplicateValues:
                    uuids.append(attributeValue)
                    continue
                if correct:
                    feature[attributeIndex] = str(uuid.uuid4())
                    layer.updateFeature(feature)
                    continue
                [
                    errors.append({
                        'geometry': self.getFlagGeometry(feature),
                        'fields' : {'erro': descr, 'classe': layer.name(), 'feature_id': feature['id']}
                    })
                    for descr, hasError in [
                        ('uuid inválido', not isValidUuid),
                        ('uuid duplicado', hasDuplicateValues)
                    ]
                    if hasError
                ]
            feedback.setProgress(step*progressStep)
        if not correct and len(errors) > 0:
            (output_sink, output_dest_id) = self.createFlagLayer(parameters, context)
            for error in errors:
                output_sink.addFeature(
                    self.createFlagFeature(error['fields'], error['geometry'])
                )
        return {self.OUTPUT: output_dest_id}

    def getFlagWkbType(self):
        return QgsWkbTypes.Point

    def getFlagFields(self):
        sinkFields = QgsFields()
        sinkFields.append(QgsField('erro', QVariant.String))
        sinkFields.append(QgsField('classe', QVariant.String))
        sinkFields.append(QgsField('feature_id', QVariant.Int))
        return sinkFields

    def hasDuplicateValues(self, value, valueList):
        return value in valueList

    def isValidUuid(self, uuidToTest, version=4):
        try:
            uuidObj = uuid.UUID(uuidToTest, version=version)
        except:
            return False
        return str(uuidObj) == uuidToTest


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifyinvaliduuids'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Verifies feature\'s UUIDs')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Quality Assurance Tools (Identification Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Quality Assurance Tools (Identification Processes)'

    def tr(self, string):
        return QCoreApplication.translate('IdentifyInvalidUUIDs', string)

    def createInstance(self):
        return IdentifyInvalidUUIDs()
