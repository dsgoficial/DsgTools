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
import json

from PyQt5.QtCore import QCoreApplication

import processing
from qgis.core import (QgsProject,
                       QgsFeature,
                       QgsProcessing,
                       QgsProcessingUtils,
                       QgsProcessingContext,
                       QgsProcessingParameterType,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterBoolean,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterDefinition)

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm

class HierarchicalSnapLayerOnLayerAndUpdateAlgorithm(ValidationAlgorithm):
    SELECTED = 'SELECTED'
    SNAP_HIERARCHY = 'SNAP_HIERARCHY'
    BEHAVIOR = 'BEHAVIOR'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """

        hierarchy = ParameterSnapHierarchy(
            self.SNAP_HIERARCHY,
            description=self.tr('Snap hierarchy')
            )
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
    
    def parameterAsSnapHierarchy(self, parameters, name, context):
        return parameters[name]

    def layerFromProject(self, layerName):
        """
        Retrieves map layer from its name, considering project context.
        :param layerName: (str) target layer's name.
        :return: (QgsMapLayer) layer object.
        """
        ctx = QgsProcessingContext()
        ctx.setProject(QgsProject.instance())
        return QgsProcessingUtils.mapLayerFromString(layerName, ctx)

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        snapDict = self.parameterAsSnapHierarchy(parameters, self.SNAP_HIERARCHY, context)

        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)

        behavior = self.parameterAsEnum(parameters, self.BEHAVIOR, context)
        nSteps = 0
        for item in snapDict:
            nSteps += len(item['snapLayerList'])
        currStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        for current, item in enumerate(snapDict):
            refLyr = self.layerFromProject(item['referenceLayer'])
            for i, lyr in enumerate(item['snapLayerList']):
                lyr = self.layerFromProject(lyr)
                if multiStepFeedback.isCanceled():
                    break
                multiStepFeedback.setCurrentStep(currStep)
                multiStepFeedback.pushInfo(
                    self.tr('Snapping geometries from layer {input} to {reference} with snap {snap}...').format(
                        input=lyr.name(),
                        reference=refLyr.name(),
                        snap=item['snap']
                        )
                    )
                layerHandler.snapToLayer(
                    lyr,
                    refLyr,
                    item['snap'],
                    behavior,
                    onlySelected=onlySelected,
                    feedback=multiStepFeedback
                    )
                currStep += 1
        return {}

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
        return QCoreApplication.translate('HierarchicalSnapLayerOnLayerAndUpdateAlgorithm', string)

    def createInstance(self):
        return HierarchicalSnapLayerOnLayerAndUpdateAlgorithm()

class ParameterSnapHierarchyType(QgsProcessingParameterType):

    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterSnapHierarchy(name) #mudar

    def metadata(self):
        return {'widget_wrapper': 'DsgTools.gui.ProcessingUI.snapHierarchyWrapper.SnapHierarchyWrapper'} #mudar

    def name(self):
        return QCoreApplication.translate('Processing', 'Snap Hierarchy')

    def id(self):
        return 'snap_hierarchy'

    def description(self):
        return QCoreApplication.translate('Processing', 'An hierarchical snapping type. Used in the Hierarchical Snap Layer on Layer algorithm.')

class ParameterSnapHierarchy(QgsProcessingParameterDefinition):

    def __init__(self, name, description=''):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterSnapHierarchy(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return 'snap_hierarchy'

    def checkValueIsAcceptable(self, value, context=None):
        # if not isinstance(value, list):
        #     return False
        # for field_def in value:
        #     if not isinstance(field_def, dict):
        #         return False
        #     if 'name' not in field_def.keys():
        #         return False
        #     if 'type' not in field_def.keys():
        #         return False
        #     if 'expression' not in field_def.keys():
        #         return False
        return True

    def valueAsPythonString(self, value, context):
        return json.dumps(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()
