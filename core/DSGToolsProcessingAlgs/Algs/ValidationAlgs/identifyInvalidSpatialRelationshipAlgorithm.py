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
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterVectorLayer, QgsWkbTypes)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class IdentifyInvalidSpatialRelationshipAlgorithm(ValidationAlgorithm):
    FLAGS = 'FLAGS'
    INPUT_A = 'INPUT_A'
    SELECTED_A = 'SELECTED_A'
    EXPRESSION_A = 'EXPRESSION_A'
    GROUPBY_A = 'GROUPBY_A'
    PREDICATE = 'PREDICATE'
    INPUT_B = 'INPUT_B'
    EXPRESSION_B = 'EXPRESSION_B'
    SELECTED_B = 'SELECTED_B'
    GROUPBY_B = 'GROUPBY_B'
    MIN_CASES = 'MIN_CASES'
    MAX_CASES = 'MAX_CASES'
    FEATID_ON_GROUPBY = FEATID_ON_GROUPBY

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_A,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED_A,
                self.tr('Process only selected features from input')
            )
        )

        self.addParameter(
            QgsProcessingParameterExpression(
                self.EXPRESSION_A, 
                self.tr('Filter expression for input'),
                None, 
                'INPUT_A', 
                optional = True
            )
        )
        self.predicates = [
                        self.tr('Prefer aligning nodes, insert extra vertices where required'),
                        self.tr('Prefer closest point, insert extra vertices where required'),
                        self.tr('Prefer aligning nodes, don\'t insert new vertices'),
                        self.tr('Prefer closest point, don\'t insert new vertices'),
                        self.tr('Move end points only, prefer aligning nodes'),
                        self.tr('Move end points only, prefer closest point'),
                        self.tr('Snap end points to end points only')
                        ]

        self.addParameter(
            QgsProcessingParameterEnum(
                self.BEHAVIOR,
                self.tr('Behavior'),
                options=self.modes,
                defaultValue=0
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_VIRTUAL_FIELDS,
                self.tr('Ignore virtual fields'),
                defaultValue=True
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_PK_FIELDS,
                self.tr('Ignore primary key fields'),
                defaultValue=True
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr('{0} Flags').format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        attributeBlackList = self.parameterAsFields(parameters, self.ATTRIBUTE_BLACK_LIST, context)
        ignoreVirtual = self.parameterAsBool(parameters, self.IGNORE_VIRTUAL_FIELDS, context)
        ignorePK = self.parameterAsBool(parameters, self.IGNORE_PK_FIELDS, context)
        self.prepareFlagSink(parameters, inputLyr, inputLyr.wkbType(), context)
        # Compute the number of steps to display within the progress bar and
        # get features from source
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        geomDict = layerHandler.getDuplicatedFeaturesDict(inputLyr, onlySelected=onlySelected, attributeBlackList=attributeBlackList, excludePrimaryKeys=ignorePK, ignoreVirtualFields=ignoreVirtual, feedback=multiStepFeedback)
        multiStepFeedback.setCurrentStep(1)
        self.raiseDuplicatedFeaturesFlags(inputLyr, geomDict, multiStepFeedback)

        return {self.FLAGS: self.flag_id}

    def raiseDuplicatedFeaturesFlags(self, inputLyr, geomDict, feedback):
        size = 100/len(geomDict) if geomDict else 0
        for current, attrDict in enumerate(geomDict.values()):
            if feedback.isCanceled():
                break
            for featList in attrDict.values():
                if feedback.isCanceled():
                    break
                if len(featList) > 1:
                    idStrList = ','.join(map(str, [feat.id() for feat in featList]))
                    flagText = self.tr('Features from layer {0} with ids=({1}) have the same set of attributes.').format(inputLyr.name(), idStrList)
                    self.flagFeature(featList[0].geometry(), flagText)
            feedback.setProgress(size * current)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifyinvalidspatialrelationship'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Invalid Spatial Relationship Features')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Validation Tools (Identification Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Validation Tools (Identification Processes)'

    def tr(self, string):
        return QCoreApplication.translate('IdentifyInvalidSpatialRelationshipAlgorithm', string)

    def createInstance(self):
        return IdentifyInvalidSpatialRelationshipAlgorithm()
