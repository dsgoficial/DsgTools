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
from collections import defaultdict
import itertools
import json
import gc

from PyQt5.QtCore import QCoreApplication

from qgis.core import (
    QgsProject,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingUtils,
    QgsProcessingContext,
    QgsProcessingParameterType,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterDefinition,
    QgsWkbTypes,
    QgsVectorLayer,
)

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class HierarchicalSnapLayerOnLayerAndUpdateAlgorithm(ValidationAlgorithm):
    SELECTED = "SELECTED"
    SNAP_HIERARCHY = "SNAP_HIERARCHY"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """

        hierarchy = ParameterSnapHierarchy(
            self.SNAP_HIERARCHY, description=self.tr("Snap hierarchy")
        )
        hierarchy.setMetadata(
            {
                "widget_wrapper": "DsgTools.gui.ProcessingUI.snapHierarchyWrapper.SnapHierarchyWrapper"
            }
        )
        self.addParameter(hierarchy)

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr("Geographic Boundary"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
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
        gc.collect()
        gc.disable()
        self.layerHandler = LayerHandler()
        self.algRunner = AlgRunner()
        snapDictList = self.parameterAsSnapHierarchy(
            parameters, self.SNAP_HIERARCHY, context
        )

        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        geographicBoundaryLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )

        nSteps = 0
        for item in snapDictList:
            if (
                geographicBoundaryLyr is not None
                and item["referenceLayer"] == geographicBoundaryLyr.name()
            ):
                raise QgsProcessingException(
                    self.tr("The Geographic Layer must not be in snap list.")
                )
            if item["snapLayerList"] is None:
                item["snapLayerList"] = []
            nSteps += len(item["snapLayerList"])
        multiStepFeedback = QgsProcessingMultiStepFeedback(3 * nSteps + 4, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        snapStructure = self.buildSnapStructure(
            snapDictList,
            onlySelected,
            context,
            multiStepFeedback,
            geographicBoundaryLyr=geographicBoundaryLyr,
        )
        currentStep += 1
        if geographicBoundaryLyr is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            auxGeoBounds = self.buildAuxGeographicBoundary(
                geographicBoundaryLyr, context=context, feedback=multiStepFeedback
            )
            currentStep += 1
            for item in snapDictList:
                multiStepFeedback.setCurrentStep(currentStep)
                referenceLayerName = item["referenceLayer"]
                multiStepFeedback.pushInfo(
                    self.tr(f"Snapping {referenceLayerName} to geographic boundary.")
                )
                if referenceLayerName not in snapStructure:
                    continue
                snapStructure[referenceLayerName][
                    "tempLayer"
                ] = self.snapToReferenceAndUpdateSpatialIndex(
                    inputLayer=snapStructure[referenceLayerName]["tempLayer"],
                    referenceLayer=auxGeoBounds,
                    tol=item["snap"],
                    behavior=self.algRunner.MoveEndPointsOnlyPreferClosestPoint
                    if snapStructure[referenceLayerName]["originalLayer"].geometryType()
                    == QgsWkbTypes.LineGeometry
                    else item["snap"],
                    context=context,
                    feedback=multiStepFeedback,
                )

        for item in snapDictList:
            multiStepFeedback.setCurrentStep(currentStep)
            referenceLayerName = item["referenceLayer"]
            if referenceLayerName not in snapStructure:
                currentStep += 2
                continue
            multiStepFeedback.pushInfo(
                self.tr(f"Performing snap internally on {referenceLayerName}.")
            )
            snapStructure[referenceLayerName][
                "tempLayer"
            ] = self.snapToReferenceAndUpdateSpatialIndex(
                inputLayer=snapStructure[referenceLayerName]["tempLayer"],
                referenceLayer=snapStructure[referenceLayerName]["tempLayer"],
                tol=item["snap"],
                behavior=item["mode"],
                context=context,
                feedback=multiStepFeedback,
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            lyrList = [i for i in item["snapLayerList"] if i in snapStructure]
            if lyrList == []:
                continue
            multiStepFeedback.pushInfo(
                self.tr(f"Starting snapping with reference layer {referenceLayerName}.")
            )
            self.snapLayersToReference(
                refLyrName=referenceLayerName,
                snapStructure=snapStructure,
                lyrList=lyrList,
                tol=item["snap"],
                behavior=item["mode"],
                context=context,
                feedback=multiStepFeedback,
            )
            currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.updateOriginalLayers(
            snapStructure,
            onlySelected=onlySelected,
            context=context,
            feedback=multiStepFeedback,
            geographicBoundaryLyr=geographicBoundaryLyr,
        )
        gc.enable()
        gc.collect()
        return {}

    def buildAuxGeographicBoundary(self, geographicBoundary, context, feedback):
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        lineBounds = self.algRunner.runPolygonsToLines(
            inputLyr=geographicBoundary,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        multiStepFeedback.setCurrentStep(1)
        explodedLines = self.algRunner.runExplodeLines(
            inputLyr=lineBounds,
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(2)
        self.algRunner.runCreateSpatialIndex(
            explodedLines,
            feedback=multiStepFeedback,
            context=context,
            is_child_algorithm=True,
        )
        return explodedLines

    def snapLayersToReference(
        self, refLyrName, snapStructure, lyrList, tol, behavior, context, feedback
    ):
        nSteps = len(lyrList)
        if nSteps == 0:
            return
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        refLyr = snapStructure[refLyrName]["tempLayer"]
        for current, lyrName in enumerate(lyrList):
            multiStepFeedback.setCurrentStep(current)
            if multiStepFeedback.isCanceled():
                return
            lyr = snapStructure[lyrName]["tempLayer"]
            multiStepFeedback.pushInfo(
                self.tr(
                    "Snapping geometries from layer {input} to {reference} with snap {snap}..."
                ).format(input=refLyrName, reference=lyrName, snap=tol)
            )
            snappedLyr = self.snapToReferenceAndUpdateSpatialIndex(
                inputLayer=lyr,
                referenceLayer=refLyr,
                tol=tol,
                behavior=behavior,
                context=context,
                feedback=multiStepFeedback,
            )
            snapStructure[lyrName]["tempLayer"] = snappedLyr

    def buildSnapStructure(
        self, snapDictList, onlySelected, context, feedback, geographicBoundaryLyr=None
    ):
        snapStructure = dict()
        nItems = len(snapDictList)
        if nItems == 0:
            return snapStructure
        multiStepFeedback = QgsProcessingMultiStepFeedback(3 * nItems, feedback)
        currentStep = 0
        for item in snapDictList:
            multiStepFeedback.setCurrentStep(currentStep)
            if multiStepFeedback.isCanceled():
                break
            lyr = self.layerFromProject(item["referenceLayer"])
            if lyr is None:
                continue
            featCount = (
                lyr.featureCount() if not onlySelected else lyr.selectedFeatureCount()
            )
            if featCount == 0:
                continue
            auxLyr = self.layerHandler.createAndPopulateUnifiedVectorLayer(
                [lyr],
                geomType=lyr.wkbType(),
                onlySelected=onlySelected,
                feedback=multiStepFeedback,
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            if geographicBoundaryLyr is not None:
                (
                    insideLyr,
                    outsideLyr,
                ) = self.layerHandler.prepareAuxLayerForSpatialConstrainedAlgorithm(
                    inputLyr=auxLyr,
                    geographicBoundaryLyr=geographicBoundaryLyr,
                    context=context,
                    feedback=multiStepFeedback,
                )
            else:
                insideLyr = auxLyr
                outsideLyr = None
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            self.algRunner.runCreateSpatialIndex(
                insideLyr, context, multiStepFeedback, is_child_algorithm=True
            )
            currentStep += 1
            snapStructure[item["referenceLayer"]] = {
                "originalLayer": lyr,
                "tempLayer": insideLyr.clone(),
                "outsideLayer": outsideLyr.clone(),
                "snap": item["snap"],
                "insideFeatureCount": insideLyr.featureCount(),
            }
        return snapStructure

    def snapToReferenceAndUpdateSpatialIndex(
        self, inputLayer, referenceLayer, tol, behavior, context, feedback
    ):
        nSteps = 2 if behavior not in [0, 1] else 4
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(nSteps, feedback)
            if feedback is not None
            else None
        )
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        snappedLyr = self.algRunner.runSnapGeometriesToLayer(
            inputLayer=inputLayer,
            referenceLayer=referenceLayer,
            tol=tol,
            behavior=behavior,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        if behavior not in [0, 1]:
            self.algRunner.runCreateSpatialIndex(
                snappedLyr, context, multiStepFeedback, is_child_algorithm=True
            )
            return snappedLyr
        primitiveDict = {
            QgsWkbTypes.PointGeometry: [],
            QgsWkbTypes.LineGeometry: [],
            QgsWkbTypes.PolygonGeometry: [],
        }
        for lyrName in [snappedLyr, referenceLayer]:
            lyr = (
                self.layerFromProject(lyrName) if isinstance(lyrName, str) else lyrName
            )
            if lyr is None:
                lyr = QgsProcessingUtils.mapLayerFromString(lyrName, context)
            primitiveDict[lyr.geometryType()].append(lyr)
        self.algRunner.runAddUnsharedVertexOnSharedEdges(
            inputLinesList=primitiveDict[QgsWkbTypes.LineGeometry],
            inputPolygonsList=primitiveDict[QgsWkbTypes.PolygonGeometry],
            searchRadius=tol,
            context=context,
            feedback=multiStepFeedback,
        )
        for lyr in itertools.chain.from_iterable(list(primitiveDict.values())):
            lyr.commitChanges()
            currentStep += 1
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(currentStep)
            self.algRunner.runCreateSpatialIndex(
                lyr, context, multiStepFeedback, is_child_algorithm=True
            )
        return snappedLyr

    def updateOriginalLayers(
        self, snapStructure, onlySelected, context, feedback, geographicBoundaryLyr=None
    ):
        multiStepFeedback = QgsProcessingMultiStepFeedback(len(snapStructure), feedback)
        for current, (lyrName, auxDict) in enumerate(snapStructure.items()):
            multiStepFeedback.setCurrentStep(current)
            multiStepFeedback.pushInfo(self.tr(f"Updating changes on {lyrName}"))
            tempLyr = QgsProcessingUtils.mapLayerFromString(
                auxDict["tempLayer"], context
            )
            if geographicBoundaryLyr is None:
                self.layerHandler.updateOriginalLayersFromUnifiedLayer(
                    [auxDict["originalLayer"]],
                    tempLyr,
                    feedback=multiStepFeedback,
                    onlySelected=onlySelected,
                )
                continue
            outputLyr = self.algRunner.runRenameField(
                inputLayer=tempLyr,
                field="featid",
                newName="oldfeatid",
                context=context,
            )
            outsideLyr = self.algRunner.runRenameField(
                inputLayer=auxDict["outsideLayer"],
                field="featid",
                newName="oldfeatid",
                context=context,
            )
            outputLyr = self.layerHandler.integrateSpatialConstrainedAlgorithmOutputAndOutsideLayer(
                algOutputLyr=outputLyr.clone(),
                outsideLyr=outsideLyr,
                tol=auxDict["snap"],
                context=context,
                geographicBoundaryLyr=geographicBoundaryLyr,
            )
            outputLyr = self.algRunner.runRenameField(
                inputLayer=outputLyr.clone(),
                field="oldfeatid",
                newName="featid",
                context=context,
            )
            originalLyr = (
                auxDict["originalLayer"]
                if isinstance(auxDict["originalLayer"], QgsVectorLayer)
                else QgsProcessingUtils.mapLayerFromString(
                    auxDict["originalLayer"], context
                )
            )
            self.layerHandler.updateOriginalLayersFromUnifiedLayer(
                [originalLyr],
                outputLyr,
                feedback=multiStepFeedback,
                onlySelected=onlySelected,
            )

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "hierarchicalsnaplayeronlayer"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Hierarchical Snap layer on layer")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Snap Processes")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Snap Processes"

    def tr(self, string):
        return QCoreApplication.translate(
            "HierarchicalSnapLayerOnLayerAndUpdateAlgorithm", string
        )

    def createInstance(self):
        return HierarchicalSnapLayerOnLayerAndUpdateAlgorithm()


class ParameterSnapHierarchyType(QgsProcessingParameterType):
    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterSnapHierarchy(name)  # mudar

    def metadata(self):
        return {
            "widget_wrapper": "DsgTools.gui.ProcessingUI.snapHierarchyWrapper.SnapHierarchyWrapper"
        }  # mudar

    def name(self):
        return QCoreApplication.translate("Processing", "Snap Hierarchy")

    def id(self):
        return "snap_hierarchy"

    def description(self):
        return QCoreApplication.translate(
            "Processing",
            "An hierarchical snapping type. Used in the Hierarchical Snap Layer on Layer algorithm.",
        )


class ParameterSnapHierarchy(QgsProcessingParameterDefinition):
    def __init__(self, name, description=""):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterSnapHierarchy(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return "snap_hierarchy"

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
