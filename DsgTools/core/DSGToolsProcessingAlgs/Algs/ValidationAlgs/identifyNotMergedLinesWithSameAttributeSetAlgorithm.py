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

from collections import defaultdict
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from .validationAlgorithm import ValidationAlgorithm
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSink,
    QgsWkbTypes,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorLayer,
    QgsFeatureRequest,
    QgsProcessingFeatureSourceDefinition,
    QgsGeometry
)


class IdentifyNotMergedLinesWithSameAttributeSetAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    ATTRIBUTE_BLACK_LIST = 'ATTRIBUTE_BLACK_LIST'
    IGNORE_VIRTUAL_FIELDS = 'IGNORE_VIRTUAL_FIELDS'
    IGNORE_PK_FIELDS = 'IGNORE_PK_FIELDS'
    POINT_FILTER_LAYERS = 'POINT_FILTER_LAYERS'
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
        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.Point, context)
        attributeBlackList = self.parameterAsFields(parameters, self.ATTRIBUTE_BLACK_LIST, context)
        fieldList = self.layerHandler.getAttributesFromBlackList(
            inputLyr,
            attributeBlackList,
            ignoreVirtualFields=self.parameterAsBoolean(parameters, self.IGNORE_VIRTUAL_FIELDS, context),
            excludePrimaryKeys=self.parameterAsBoolean(parameters, self.IGNORE_PK_FIELDS, context)
        )
        fieldIdList = [i for i, field in enumerate(inputLyr.fields()) if field.name() in fieldList]
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
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
        dictSize = len(initialAndEndPointDict)
        if dictSize == 0:
            return {"FLAGS": self.flag_id}
        filterPointSet = set(i.geometry().asWkb() for i in mergedPointLyr.getFeatures()) if mergedPointLyr is not None else set()
        multiStepFeedback.setCurrentStep(3)
        stepSize = 100 / dictSize
        for current, (pointXY, idSet) in enumerate(initialAndEndPointDict.items()):
            if multiStepFeedback.isCanceled():
                break
            geom = QgsGeometry.fromPointXY(pointXY)
            geomWkb = geom.asWkb()
            if geomWkb in filterPointSet:
                continue
            if len(idSet) != 2:
                continue
            request = QgsFeatureRequest()\
                .setFilterExpression(f"AUTO in {tuple(idSet)}")\
                .setFlags(QgsFeatureRequest.NoGeometry)\
                .setSubsetOfAttributes(fieldIdList)
            f1, f2 = [i for i in localLyr.getFeatures(request)]
            differentFeats = any(f1[k] != f2[k] for k in fieldList)
            if not differentFeats:
                self.flagFeature(
                    flagGeom=geomWkb,
                    flagText=self.tr("Not merged lines with same attribute set"),
                    fromWkb=True
                )
            multiStepFeedback.setProgress(current * stepSize)
            
        
        return {
            "FLAGS": self.flag_id
        }
    
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
        return "identifynotmergedlineswithsameattributeset"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Not Merged Lines With Same Attribute Set")

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
            "IdentifyNotMergedLinesWithSameAttributeSetAlgorithm", string
        )

    def createInstance(self):
        return IdentifyNotMergedLinesWithSameAttributeSetAlgorithm()
