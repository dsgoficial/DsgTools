# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-07-19
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import concurrent.futures
from collections import defaultdict
import os

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsFeatureRequest, QgsGeometry, QgsProcessing,
                       QgsProcessingFeatureSourceDefinition,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterField,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterVectorLayer, QgsWkbTypes)

from .validationAlgorithm import ValidationAlgorithm


class IdentifyUnmergedLinesWithSameAttributeSetAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    ATTRIBUTE_BLACK_LIST = 'ATTRIBUTE_BLACK_LIST'
    IGNORE_VIRTUAL_FIELDS = 'IGNORE_VIRTUAL_FIELDS'
    IGNORE_PK_FIELDS = 'IGNORE_PK_FIELDS'
    POINT_FILTER_LAYERS = 'POINT_FILTER_LAYERS'
    LINE_FILTER_LAYERS = 'LINE_FILTER_LAYERS'
    FLAGS = 'FLAGS'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer'),
                [
                    QgsProcessing.TypeVectorLine,
                ]
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
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
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.POINT_FILTER_LAYERS,
                self.tr('Point Filter Layers'),
                QgsProcessing.TypeVectorPoint,
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.LINE_FILTER_LAYERS,
                self.tr('Line Filter Layers'),
                QgsProcessing.TypeVectorLine,
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.layerHandler = LayerHandler()
        algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        onlySelected = self.parameterAsBoolean(parameters, self.SELECTED, context)
        pointFilterLyrList = self.parameterAsLayerList(
            parameters, self.POINT_FILTER_LAYERS, context)
        lineFilterLyrList = self.parameterAsLayerList(
            parameters, self.LINE_FILTER_LAYERS, context)
        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.Point, context)
        if inputLyr is None:
            return {
                "FLAGS": self.flag_id
            }
        attributeBlackList = self.parameterAsFields(parameters, self.ATTRIBUTE_BLACK_LIST, context)
        fieldList = self.layerHandler.getAttributesFromBlackList(
            inputLyr,
            attributeBlackList,
            ignoreVirtualFields=self.parameterAsBoolean(parameters, self.IGNORE_VIRTUAL_FIELDS, context),
            excludePrimaryKeys=self.parameterAsBoolean(parameters, self.IGNORE_PK_FIELDS, context)
        )
        fieldIdList = [i for i, field in enumerate(inputLyr.fields()) if field.name() in fieldList]
        multiStepFeedback = QgsProcessingMultiStepFeedback(6, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(self.tr("Building local cache..."))
        localLyr = algRunner.runAddAutoIncrementalField(
            inputLyr=inputLyr if not onlySelected else QgsProcessingFeatureSourceDefinition(
            inputLyr.id(), True),
            fieldName='AUTO',
            context=context,
            feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.setProgressText(self.tr("Building initial and end point dict..."))
        initialAndEndPointDict = self.buildInitialAndEndPointDict(
            localLyr, algRunner=algRunner, context=context, feedback=multiStepFeedback
        )
        multiStepFeedback.setProgressText(self.tr("Building aux structure..."))
        multiStepFeedback.setCurrentStep(2)
        mergedPointLyr = algRunner.runMergeVectorLayers(pointFilterLyrList, context, multiStepFeedback) if pointFilterLyrList else None
        multiStepFeedback.setCurrentStep(3)
        mergedLineLyr = algRunner.runMergeVectorLayers(lineFilterLyrList, context, multiStepFeedback) if lineFilterLyrList else None
        multiStepFeedback.setCurrentStep(4)
        if mergedLineLyr is not None:
            algRunner.runCreateSpatialIndex(mergedLineLyr, context, multiStepFeedback)
        dictSize = len(initialAndEndPointDict)
        if dictSize == 0:
            return {"FLAGS": self.flag_id}
        filterPointSet = set(i.geometry().asWkb() for i in mergedPointLyr.getFeatures()) if mergedPointLyr is not None else set()
        multiStepFeedback.setCurrentStep(5)
        multiStepFeedback.setProgressText(self.tr("Evaluating candidates"))
        self.evaluateFlagCandidates(
            fieldList, fieldIdList, multiStepFeedback, localLyr, \
            initialAndEndPointDict, mergedLineLyr, dictSize, filterPointSet)
        return {
            "FLAGS": self.flag_id
        }

    def evaluateFlagCandidates(self, fieldList, fieldIdList, multiStepFeedback, localLyr, initialAndEndPointDict, mergedLineLyr, dictSize, filterPointSet):
        stepSize = 100 / dictSize
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, multiStepFeedback)
        multiStepFeedback.setCurrentStep(0)
        def evaluate(pointXY, idSet):
            if multiStepFeedback.isCanceled():
                return None
            geom = QgsGeometry.fromPointXY(pointXY)
            geomWkb = geom.asWkb()
            if geomWkb in filterPointSet:
                return None
            if len(idSet) != 2:
                return None
            if mergedLineLyr is not None:
                bbox = geom.boundingBox()
                nIntersects = len([i for i in mergedLineLyr.getFeatures(bbox) if i.geometry().intersects(geom)])
                if nIntersects > 0:
                    return None
            request = QgsFeatureRequest()\
                .setFilterExpression(f"AUTO in {tuple(idSet)}")\
                .setFlags(QgsFeatureRequest.NoGeometry)\
                .setSubsetOfAttributes(fieldIdList)
            f1, f2 = [i for i in localLyr.getFeatures(request)]
            differentFeats = any(f1[k] != f2[k] for k in fieldList)
            return geomWkb if not differentFeats else None
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()-1)
        futures = set()

        for current, (pointXY, idSet) in enumerate(initialAndEndPointDict.items()):
            if multiStepFeedback.isCanceled():
                break
            futures.add(pool.submit(evaluate, pointXY, idSet))
            multiStepFeedback.setProgress(current * stepSize)
        
        multiStepFeedback.setCurrentStep(1)
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                break
            geomWkb = future.result()
            if geomWkb is not None:
                self.flagFeature(
                    flagGeom=geomWkb,
                    flagText=self.tr("Not merged lines with same attribute set"),
                    fromWkb=True
                )
            multiStepFeedback.setProgress(current * stepSize)
    
    def buildInitialAndEndPointDict(self, lyr, algRunner, context, feedback):
        pointDict = defaultdict(set)
        nSteps = 3
        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        multiStepFeedback.setCurrentStep(currentStep)
        boundaryLyr = algRunner.runBoundary(
            inputLayer=lyr,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        boundaryLyr = algRunner.runMultipartToSingleParts(
            inputLayer=boundaryLyr,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        featCount = boundaryLyr.featureCount()
        if featCount == 0:
            return pointDict
        step = 100/featCount
        for current, feat in enumerate(boundaryLyr.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            geom = feat.geometry()
            if geom is None or not geom.isGeosValid():
                continue
            id = feat["AUTO"]
            pointList = geom.asMultiPoint() if geom.isMultipart() else [
                geom.asPoint()]
            for point in pointList:
                pointDict[point].add(id)
            multiStepFeedback.setProgress(current * step)
        return pointDict

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyunmergedlineswithsameattributeset"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Unmerged Lines With Same Attribute Set")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Identification Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Identification Processes)"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifyUnmergedLinesWithSameAttributeSetAlgorithm", string
        )

    def createInstance(self):
        return IdentifyUnmergedLinesWithSameAttributeSetAlgorithm()
