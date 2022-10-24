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

from qgis.core import (QgsProject,
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
        self.layerHandler = LayerHandler()
        self.algRunner = AlgRunner()
        snapDictList = self.parameterAsSnapHierarchy(parameters, self.SNAP_HIERARCHY, context)

        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)

        behavior = self.parameterAsEnum(parameters, self.BEHAVIOR, context)
        nSteps = 0
        for item in snapDictList:
            nSteps += len(item['snapLayerList'])
        multiStepFeedback = QgsProcessingMultiStepFeedback(2*nSteps + 2, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        snapStructure = self.buildSnapStructure(snapDictList, onlySelected, context, multiStepFeedback)
        currentStep += 1
        for item in snapDictList:
            multiStepFeedback.setCurrentStep(currentStep)
            referenceLayerName = item['referenceLayer'] 
            if referenceLayerName not in snapStructure:
                currentStep += 2
                continue
            multiStepFeedback.pushInfo(
                self.tr(f"Performing snap internally on {referenceLayerName}.")
            )
            snapStructure[referenceLayerName]['tempLayer'] = self.snapToReferenceAndUpdateSpatialIndex(
                inputLayer=snapStructure[referenceLayerName]['tempLayer'],
                referenceLayer=snapStructure[referenceLayerName]['tempLayer'],
                tol=item['snap'],
                behavior=item['mode'],
                context=context,
                feedback=multiStepFeedback
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            lyrList = [i for i in item['snapLayerList'] if i in snapStructure]
            multiStepFeedback.pushInfo(
                self.tr(f"Starting snapping with reference layer {referenceLayerName}.")
            )
            self.snapLayersToReference(
                refLyrName=referenceLayerName,
                snapStructure=snapStructure,
                lyrList=lyrList,
                tol=item['snap'],
                behavior=item['mode'],
                context=context,
                feedback=multiStepFeedback
            )
            currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.updateOriginalLayers(snapStructure, onlySelected=onlySelected, context=context, feedback=multiStepFeedback)

        return {}

    def snapLayersToReference(self, refLyrName, snapStructure, lyrList, tol, behavior, context, feedback):
        nSteps = len(lyrList)
        if nSteps == 0:
            return
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        refLyr = snapStructure[refLyrName]['tempLayer']
        for current, lyrName in enumerate(lyrList):
            multiStepFeedback.setCurrentStep(current)
            if multiStepFeedback.isCanceled():
                return
            lyr = snapStructure[lyrName]['tempLayer']
            multiStepFeedback.pushInfo(
                self.tr(
                    'Snapping geometries from layer {input} to {reference} with snap {snap}...'
                ).format(
                    input=refLyrName,
                    reference=lyrName,
                    snap=tol
                )
            )
            snappedLyr = self.snapToReferenceAndUpdateSpatialIndex(
                inputLayer=lyr,
                referenceLayer=refLyr,
                tol=tol,
                behavior=behavior,
                context=context,
                feedback=multiStepFeedback
            )
            snapStructure[lyrName]['tempLayer'] = snappedLyr   

    def buildSnapStructure(self, snapDictList, onlySelected, context, feedback):
        snapStructure = dict()
        nItems = len(snapDictList)
        if nItems == 0:
            return snapStructure
        multiStepFeedback = QgsProcessingMultiStepFeedback(2*nItems, feedback)
        currentStep = 0
        for item in snapDictList:
            multiStepFeedback.setCurrentStep(currentStep)
            if multiStepFeedback.isCanceled():
                break
            lyr = self.layerFromProject(item['referenceLayer'])
            featCount = lyr.featureCount() if not onlySelected else lyr.selectedFeatureCount()
            if featCount == 0:
                continue
            auxLyr = self.layerHandler.createAndPopulateUnifiedVectorLayer(
                [lyr],
                geomType=lyr.wkbType(),
                onlySelected=onlySelected,
                feedback=multiStepFeedback
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            self.algRunner.runCreateSpatialIndex(
                auxLyr, context, multiStepFeedback
            )
            currentStep += 1
            snapStructure[item['referenceLayer']] = {
                'originalLayer': lyr,
                'tempLayer': auxLyr
            }
        return snapStructure

    def snapToReferenceAndUpdateSpatialIndex(self, inputLayer, referenceLayer, tol, behavior, context, feedback):
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        snappedLyr = self.algRunner.runSnapGeometriesToLayer(
            inputLayer=inputLayer,
            referenceLayer=referenceLayer,
            tol=tol,
            behavior=behavior,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True
        )
        multiStepFeedback.setCurrentStep(1)
        self.algRunner.runCreateSpatialIndex(snappedLyr, context, multiStepFeedback, is_child_algorithm=True)
        return snappedLyr
    
    def updateOriginalLayers(self, snapStructure, onlySelected, context, feedback):
        multiStepFeedback = QgsProcessingMultiStepFeedback(len(snapStructure), feedback)
        for current, (lyrName, auxDict) in enumerate(snapStructure.items()):
            multiStepFeedback.setCurrentStep(current)
            multiStepFeedback.pushInfo(self.tr(f'Updating changes on {lyrName}'))
            tempLyr = QgsProcessingUtils.mapLayerFromString(auxDict['tempLayer'], context)
            self.layerHandler.updateOriginalLayersFromUnifiedLayer(
                [auxDict['originalLayer']],
                tempLyr,
                feedback=multiStepFeedback,
                onlySelected=onlySelected
            )
            QgsProject.instance().removeMapLayer(tempLyr.id())
    
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
        return self.tr('Quality Assurance Tools (Manipulation Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Quality Assurance Tools (Manipulation Processes)'

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
