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
from collections import defaultdict
from PyQt5.QtCore import QCoreApplication

import math
import processing
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsDataSourceUri,
    QgsFeature,
    QgsFeatureSink,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
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
    QgsProcessingParameterVectorLayer,
    QgsProcessingUtils,
    QgsSpatialIndex,
    QgsWkbTypes,
    QgsProcessingException,
    QgsGeometry,
    QgsPoint,
    QgsPointXY,
    QgsWkbTypes,
    QgsFeedback,
    QgsVectorLayer,
    QgsProcessingContext,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class TopologicalLineConnectivityAdjustment(ValidationAlgorithm):
    INPUT_LAYERS = "INPUT_LAYERS"
    SELECTED = "SELECTED"
    TOLERANCE = "TOLERANCE"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr("Linestring Layers"),
                QgsProcessing.TypeVectorLine,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        param = QgsProcessingParameterDistance(
            self.TOLERANCE,
            self.tr("Search Radius"),
            parentParameterName=self.INPUT_LAYERS,
            defaultValue=1e-6,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 8}})
        self.addParameter(param)

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        self.algRunner = AlgRunner()
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUT_LAYERS, context)
        if inputLyrList is None or inputLyrList == []:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT_LAYERS)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        tol = self.parameterAsDouble(parameters, self.TOLERANCE, context)

        multiStepFeedback = QgsProcessingMultiStepFeedback(20, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Building unified layer..."))
        coverage = layerHandler.createAndPopulateUnifiedVectorLayer(
            inputLyrList,
            geomType=QgsWkbTypes.MultiLineString,
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Removing small lines..."))
        self.algRunner.runRemoveSmallLines(
            inputLyr=coverage,
            tol=tol,
            context=context,
            feedback=multiStepFeedback,
        )
        coverage.commitChanges()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Running snap within unified layer..."))
        outputLyr = self.algRunner.runSnapGeometriesToLayer(
            coverage,
            coverage,
            tol,
            context,
            feedback=multiStepFeedback,
            behavior=self.algRunner.SnapToAnchorNodes,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Removing small lines post snap on unified layer..."))
        self.algRunner.runRemoveSmallLines(
            inputLyr=outputLyr,
            tol=tol,
            context=context,
            feedback=multiStepFeedback,
        )
        outputLyr.commitChanges()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Running adjust network connectivity..."))
        self.algRunner.runAdjustNetworkConnectivityAlgorithm(
            inputLyr=outputLyr,
            tol=tol,
            context=context,
            feedback=multiStepFeedback
        )
        outputLyr.commitChanges()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Running identify dangles after removing small lines post snap on unified layer..."))
        dangleLyr = self.algRunner.runIdentifyDangles(
            outputLyr,
            tol,
            context,
            ignoreDanglesOnUnsegmentedLines=False,
            inputIsBoundaryLayer=False,
            feedback=multiStepFeedback,
            onlySelected=onlySelected,
        )
        currentStep += 1
        if dangleLyr.featureCount() == 0:
            multiStepFeedback.pushInfo(self.tr("No more remaining dangles. Ending process."))
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Updating original layers..."))
            layerHandler.updateOriginalLayersFromUnifiedLayer(
                inputLyrList, outputLyr, feedback=multiStepFeedback
            )
            return {}

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Removing duplicated dangles..."))
        dangleSnappedToGrid = self.algRunner.runSnapToGrid(
            inputLayer=dangleLyr,
            tol=tol,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        dangleSnappedToItself = self.algRunner.runSnapGeometriesToLayer(
            dangleSnappedToGrid,
            dangleSnappedToGrid,
            tol,
            context,
            feedback=multiStepFeedback,
            behavior=self.algRunner.SnapToAnchorNodes,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runRemoveDuplicatedGeometries(
            inputLyr=dangleSnappedToItself,
            context=context,
            feedback=multiStepFeedback,
        )
        dangleSnappedToItself.commitChanges()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Removing duplicated dangles after duplicate filter..."))
        layerHandler.filterDangles(dangleSnappedToItself, tol, feedback=multiStepFeedback)
        dangleSnappedToItself.commitChanges()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Performing individual snap on remaining dangles..."))
        fixedLines = self.fixDanglesWithIndividualSnap(
            dangleLyr=dangleSnappedToItself,
            lineLyr=outputLyr,
            context=context,
            feedback=multiStepFeedback,
            tol=tol,
        )
        multiStepFeedback.pushInfo(self.tr(f"{dangleSnappedToItself.featureCount()} remaining. Final fix remaining dangles..."))
        self.fixRemainingDangles(
            dangleLyr=dangleSnappedToItself,
            lineLyr=fixedLines,
            context=context,
            feedback=multiStepFeedback,
            tol=tol,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Updating original layers..."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            inputLyrList, fixedLines, feedback=multiStepFeedback
        )

        return {}
    
    def fixDanglesWithIndividualSnap(self, dangleLyr: QgsVectorLayer, lineLyr: QgsVectorLayer, context: QgsProcessingContext, feedback: QgsFeedback, tol: float):
        nDangles = dangleLyr.featureCount()
        if nDangles == 0:
            return lineLyr
        multiStepFeedback = QgsProcessingMultiStepFeedback(nDangles, feedback)
        layerHandler = LayerHandler()
        currentLyr = lineLyr
        for currentStep, dangleFeat in enumerate(dangleLyr.getFeatures()):
            multiStepFeedback.setCurrentStep(currentStep)
            if multiStepFeedback.isCanceled():
                break
            currentDangleLyr = layerHandler.createMemoryLayerWithFeature(
                dangleLyr, dangleFeat, context
            )
            currentLyr = self.algRunner.runSnapGeometriesToLayer(
                inputLayer=currentLyr,
                referenceLayer=currentDangleLyr,
                tol=tol,
                behavior=AlgRunner.AlignNodesDoNotInsertNewVertices,
                context=context,
            )
        return currentLyr
    
    def fixRemainingDangles(self, dangleLyr: QgsVectorLayer, lineLyr: QgsVectorLayer, context: QgsProcessingContext, feedback: QgsFeedback, tol: float):
        multiStepFeedback = QgsProcessingMultiStepFeedback(10, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        if dangleLyr.featureCount() == 0:
            return
        danglesWithId = self.algRunner.runCreateFieldWithExpression(
            inputLyr=dangleLyr,
            expression="$id",
            fieldName="dangle_featid",
            fieldType=AlgRunner.FieldTypeInteger,
            context=context,
            feedback=multiStepFeedback,
        )
        danglePointDict = {f["dangle_featid"]: f.geometry().asPoint() for f in danglesWithId.getFeatures()}
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        dangleBuffer = self.algRunner.runBuffer(danglesWithId, distance=2*tol, dissolve=True, context=context, feedback=multiStepFeedback)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(dangleBuffer, context, feedback=multiStepFeedback)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        lineLyrWithId = self.algRunner.runCreateFieldWithExpression(
            inputLyr=lineLyr,
            expression="$id",
            fieldName="line_featid",
            fieldType=AlgRunner.FieldTypeInteger,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(lineLyrWithId, context, feedback=multiStepFeedback)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        candidateLines = self.algRunner.runExtractByLocation(
            inputLyr=lineLyrWithId,
            intersectLyr=dangleBuffer,
            predicate=AlgRunner.Intersects,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        verticeLyr = self.algRunner.runExtractVertices(
            inputLyr=candidateLines,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(verticeLyr, context, feedback=multiStepFeedback)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        joinned = self.algRunner.runJoinAttributesByLocation(
            inputLyr=dangleBuffer,
            joinLyr=verticeLyr,
            predicateList=[AlgRunner.Intersects],
            joinFields=['line_featid','vertex_index','vertex_part','vertex_part_index','distance','angle'],
            context=context,
            feedback=multiStepFeedback,
        )
        
        nFeats = joinned.featureCount()
        if nFeats == 0:
            return
        joinnedDict = defaultdict(set)
        for feat in joinned.getFeatures():
            joinnedDict[feat.id()].add(feat['line_featid'])
        lineLyrDict = {f['line_featid']:f for f in lineLyrWithId.getFeatures()}
        stepSize = 100/nFeats
        lineLyr.startEditing()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        for current, feat in enumerate(joinned.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            if len(joinnedDict[feat.id()]) == 1:
                multiStepFeedback.setProgress(current * stepSize)
                continue
            lineFeat = lineLyrDict.get(feat["line_featid"], None)
            if lineFeat is None:
                multiStepFeedback.setProgress(current * stepSize)
                continue
            lineGeom = lineFeat.geometry()
            danglePoint = danglePointDict[feat["dangle_featid"]]
            if danglePoint.distance(feat.geometry()) > tol:
                multiStepFeedback.setProgress(current * stepSize)
                continue
            lineGeom.moveVertex(danglePoint.x(), danglePoint.y(), feat["vertex_index"])
            lineLyr.dataProvider().changeGeometryValues({feat["line_featid"]: lineGeom})
            lineFeat.setGeometry(lineGeom)
            lineLyrDict[feat["line_featid"]] = lineFeat
            multiStepFeedback.setProgress(current * stepSize)
        lineLyr.commitChanges()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "topologicallineconnectivityadjustment"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Topological adjustment of the connectivity of lines")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Network Processes")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Network Processes"

    def tr(self, string):
        return QCoreApplication.translate(
            "TopologicalLineConnectivityAdjustment", string
        )

    def createInstance(self):
        return TopologicalLineConnectivityAdjustment()
