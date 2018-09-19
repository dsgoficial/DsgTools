# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-18
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
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from .validationAlgorithm import ValidationAlgorithm
from ...algRunner import AlgRunner
import processing
from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
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
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingUtils,
                       QgsSpatialIndex,
                       QgsGeometry,
                       QgsProcessingParameterField,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterType)

class HierarchicalSnapLayerOnLayerAndUpdateAlgorithm(ValidationAlgorithm):
    INPUTLYRLIST = 'INPUTLYRLIST'
    SELECTED = 'SELECTED'
    SNAP_HIERARCHY = 'SNAP_HIERARCHY'
    BEHAVIOR = 'BEHAVIOR'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """

        hierarchy = hierarchicalSnapLayerOnLayerAndUpdateAlgorithm.ParameterSnapHierarchy(self.SNAP_HIERARCHY,
                                                             description=self.tr('Snap hierarchy'))
        hierarchy.setMetadata({
            'widget_wrapper': 'DsgTools.gui.ProcessingUI.snapHierarchyWrapper.SnapHierarchyWrapper'
        })
        self.addParameter(hierarchy)

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )

        self.modes = [self.tr('Prefer aligning nodes, insert extra vertices where required'),
                      self.tr('Prefer closest point, insert extra vertices where required'),
                      self.tr('Prefer aligning nodes, don\'t insert new vertices'),
                      self.tr('Prefer closest point, don\'t insert new vertices'),
                      self.tr('Move end points only, prefer aligning nodes'),
                      self.tr('Move end points only, prefer closest point'),
                      self.tr('Snap end points to end points only')]

        self.addParameter(
            QgsProcessingParameterEnum(
                self.BEHAVIOR,
                self.tr('Behavior'),
                options=self.modes,
                defaultValue=0
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()
        
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        refLyr = self.parameterAsVectorLayer(parameters, self.REFERENCE_LAYER, context)
        if refLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.REFERENCE_LAYER))
        tol = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        behavior = self.parameterAsEnum(parameters, self.BEHAVIOR, context)
        
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr('Populating temp layer...'))
        auxLyr = layerHandler.createAndPopulateUnifiedVectorLayer([inputLyr], geomType=inputLyr.wkbType(), onlySelected = onlySelected, feedback=multiStepFeedback)
        
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr('Snapping geometries from layer {input} to {reference}...').format(input=inputLyr.name(), reference=refLyr.name()))
        snappedLayer = algRunner.runSnapGeometriesToLayer(auxLyr, refLyr, tol, context, feedback=multiStepFeedback, behavior=behavior)

        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr('Updating original layer...'))
        layerHandler.updateOriginalLayersFromUnifiedLayer([inputLyr], snappedLayer, feedback=multiStepFeedback, onlySelected=onlySelected)

        return {self.INPUT: inputLyr}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'hierarchicalsnaplayeronlayer'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Hierarchical Snap layer on layer')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Validation Tools (Manipulation Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Validation Tools (Manipulation Processes)'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return HierarchicalSnapLayerOnLayerAndUpdateAlgorithm()

    class ParameterSnapHierarchyType(QgsProcessingParameterType):

        def __init__(self):
            super(QgsProcessingParameterType).__init__()

        def create(self, name):
            return hierarchicalSnapLayerOnLayerAndUpdateAlgorithm.ParameterSnapHierarchy(name) #mudar

        def metadata(self):
            return {'widget_wrapper': 'processing.algs.qgis.ui.FieldsMappingPanel.FieldsMappingWidgetWrapper'} #mudar

        def name(self):
            return QCoreApplication.translate('Processing', 'Snap Hierarchy')

        def id(self):
            return 'snap_hierarchy'

        def description(self):
            return QCoreApplication.translate('Processing', 'An hierarchical snapping type. Used in the Hierarchical Snap Layer on Layer algorithm.')

    class ParameterSnapHierarchy(QgsProcessingParameterDefinition):

        def __init__(self, name, description=''):
            super(QgsProcessingParameterDefinition).__init__(name, description)

        def clone(self):
            copy = hierarchicalSnapLayerOnLayerAndUpdateAlgorithm.ParameterFieldsMapping(self.name(), self.description())
            return copy

        def type(self):
            return self.typeName()

        @staticmethod
        def typeName():
            return 'snap_hierarchy'

        def checkValueIsAcceptable(self, value, context=None):
            if not isinstance(value, list):
                return False
            for field_def in value:
                if not isinstance(field_def, dict):
                    return False
                if 'name' not in field_def.keys():
                    return False
                if 'type' not in field_def.keys():
                    return False
                if 'expression' not in field_def.keys():
                    return False
            return True

        def valueAsPythonString(self, value, context):
            return str(value)

        def asScriptCode(self):
            raise NotImplementedError()

        @classmethod
        def fromScriptCode(cls, name, description, isOptional, definition):
            raise NotImplementedError()