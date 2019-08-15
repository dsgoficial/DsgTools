# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-08-14
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import processing
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsGeometry, QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer, QgsProcessingUtils,
                       QgsSpatialIndex, QgsWkbTypes)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class FixNetworkAlgorithm(ValidationAlgorithm):
    INPUT = 'INPUT'
    SELECTED = 'SELECTED'
    TOLERANCE = 'TOLERANCE'
    ATTRIBUTE_BLACK_LIST = 'ATTRIBUTE_BLACK_LIST'
    IGNORE_VIRTUAL_FIELDS = 'IGNORE_VIRTUAL_FIELDS'
    IGNORE_PK_FIELDS = 'IGNORE_PK_FIELDS'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
         self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorLine ]
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.TOLERANCE,
                self.tr('Topology radius'),
                parentParameterName=self.INPUT,
                minValue=0,
                defaultValue=1.0
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.ATTRIBUTE_BLACK_LIST, 
                self.tr('Fields to ignore'),
                None, 
                'INPUT', 
                QgsProcessingParameterField.Any,
                allowMultiple=True,
                optional = True
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
        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT,
                self.tr('Original layer with merged lines')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()

        layerHandler = LayerHandler()
        inputLyr = self.parameterAsVectorLayer(
            parameters,
            self.INPUT,
            context
            )
        onlySelected = self.parameterAsBool(
            parameters,
            self.SELECTED,
            context
            )
        tol = self.parameterAsDouble(
            parameters,
            self.TOLERANCE,
            context
            )
        attributeBlackList = self.parameterAsFields(
            parameters,
            self.ATTRIBUTE_BLACK_LIST,
            context
            )
        ignoreVirtual = self.parameterAsBool(
            parameters,
            self.IGNORE_VIRTUAL_FIELDS,
            context
            )
        ignorePK = self.parameterAsBool(
            parameters,
            self.IGNORE_PK_FIELDS,
            context
            )

        layerHandler.mergeLinesOnLayer(
            inputLyr,
            feedback=feedback,
            onlySelected=onlySelected,
            ignoreVirtualFields=ignoreVirtual,
            attributeBlackList=attributeBlackList,
            excludePrimaryKeys=ignorePK
            )
        #aux layer
        multiStepFeedback = QgsProcessingMultiStepFeedback(8, feedback)
        multiStepFeedback.setCurrentStep(0)
        if onlySelected:
            multiStepFeedback.pushInfo(self.tr('Building auxiliar layer...'))
            coverage = layerHandler.createAndPopulateUnifiedVectorLayer(
                [inputLyr],
                geomType=QgsWkbTypes.MultiPolygon,
                onlySelected=onlySelected,
                feedback=multiStepFeedback
                )
        else:
            coverage = inputLyr
        #dangles
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr('Identifying dangles on {layer}...').format(layer=coverage.name()))
        dangleLyr = algRunner.runIdentifyDangles(
            inputLayer=coverage,
            searchRadius=tol,
            context=context,
            feedback=multiStepFeedback,
            onlySelected=False
            )
        #filter dangles
        multiStepFeedback.setCurrentStep(2)
        layerHandler.filterDangles(
            dangleLyr,
            tol,
            feedback=multiStepFeedback
            )
        #snap layer to dangles
        multiStepFeedback.setCurrentStep(3)
        multiStepFeedback.pushInfo(self.tr('Snapping layer {layer} to dangles...').format(layer=coverage.name()))
        algRunner.runSnapLayerOnLayer(
            coverage,
            dangleLyr,
            tol,
            context,
            feedback=multiStepFeedback,
            onlySelected=False, #this is done due to the aux layer usage
            behavior=0
            )
        #inner layer snap
        multiStepFeedback.setCurrentStep(4)
        multiStepFeedback.pushInfo(self.tr('Snapping layer {layer} with {layer}...').format(layer=coverage.name()))
        algRunner.runSnapLayerOnLayer(
            coverage,
            coverage,
            tol,
            context,
            feedback=multiStepFeedback,
            onlySelected=False, #this is done due to the aux layer usage
            behavior=0
            )
        #clean to break lines
        multiStepFeedback.setCurrentStep(5)
        multiStepFeedback.pushInfo(self.tr('Running clean on {layer}...').format(layer=coverage.name()))
        multiStepFeedback.pushInfo(self.tr('Running clean on unified layer...'))
        cleanedCoverage, error = algRunner.runClean(
            coverage,
            [
                algRunner.RMSA,
                algRunner.Break,
                algRunner.RmDupl,
                algRunner.RmDangle
                ],
            context,
            returnError=True,
            snap=snap,
            minArea=minArea,
            feedback=multiStepFeedback
            )
        #remove duplicated features
        multiStepFeedback.setCurrentStep(6)
        multiStepFeedback.pushInfo(self.tr('Removing duplicated features from {layer}...').format(layer=coverage.name()))
        algRunner.runRemoveDuplicatedFeatures(
            inputLyr=cleanedCoverage,
            context=context,
            onlySelected=False,
            attributeBlackList=attributeBlackList,
            excludePrimaryKeys=excludePrimaryKeys,
            ignorePK=ignorePK,
            ignoreVirtual=ignoreVirtual
        )
        #merging lines with same attributes
        multiStepFeedback.setCurrentStep(6)
        multiStepFeedback.pushInfo(self.tr('Merging lines from {layer} with same attribute set...').format(layer=coverage.name()))

        multiStepFeedback.setCurrentStep(7)
        multiStepFeedback.pushInfo(self.tr('Updating original layers...'))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [inputLyr],
            coverage,
            feedback=multiStepFeedback,
            onlySelected=onlySelected
            )

        return {self.INPUTLAYERS : inputLyrList}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'topologicallineconnectivityadjustment'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Topological adjustment of the connectivity of lines')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Validation Tools (Network Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Validation Tools (Network Processes)'

    def tr(self, string):
        return QCoreApplication.translate('TopologicalLineConnectivityAdjustment', string)

    def createInstance(self):
        return TopologicalLineConnectivityAdjustment()
