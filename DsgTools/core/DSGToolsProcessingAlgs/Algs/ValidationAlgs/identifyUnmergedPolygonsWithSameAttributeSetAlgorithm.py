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
from typing import Dict, Set, List, Tuple
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools import graphHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsFeatureRequest,
    QgsGeometry,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessing,
    QgsProject,
    QgsFields,
    QgsProcessingFeatureSourceDefinition,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterField,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingException,
    QgsProcessingParameterNumber,
    QgsProcessingParameterDefinition,
    QgsVectorLayer,
    Qgis,
)

from .validationAlgorithm import ValidationAlgorithm
from ..Help.algorithmHelpCreator import HTMLHelpCreator as help


class IdentifyUnmergedPolygonsWithSameAttributeSetAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    ATTRIBUTE_BLACK_LIST = "ATTRIBUTE_BLACK_LIST"
    IGNORE_VIRTUAL_FIELDS = "IGNORE_VIRTUAL_FIELDS"
    IGNORE_PK_FIELDS = "IGNORE_PK_FIELDS"
    LINE_FILTER_LAYERS = "LINE_FILTER_LAYERS"
    AREA_FILTER = "AREA_FILTER"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input layer"),
                [
                    QgsProcessing.TypeVectorPolygon,
                ],
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.ATTRIBUTE_BLACK_LIST,
                self.tr("Fields to ignore"),
                None,
                "INPUT",
                QgsProcessingParameterField.Any,
                allowMultiple=True,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_VIRTUAL_FIELDS,
                self.tr("Ignore virtual fields"),
                defaultValue=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_PK_FIELDS,
                self.tr("Ignore primary key fields"),
                defaultValue=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.LINE_FILTER_LAYERS,
                self.tr("Line Filter Layers"),
                QgsProcessing.TypeVectorLine,
                optional=True,
            )
        )
        areaFilter = QgsProcessingParameterNumber(
            self.AREA_FILTER,
            self.tr("Minimum area polygon filter"),
            QgsProcessingParameterNumber.Double,
            defaultValue=None,
            optional=True,
            minValue=0.0
        )
        areaFilter.setFlags(
            areaFilter.flags() | QgsProcessingParameterDefinition.FlagAdvanced
        )
        self.addParameter(areaFilter)
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        area_filter = self.parameterAsDouble(parameters, 'AREA_FILTER', context)
        self.layerHandler = LayerHandler()
        self.algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        onlySelected = self.parameterAsBoolean(parameters, self.SELECTED, context)
        lineFilterLyrList = self.parameterAsLayerList(
            parameters, self.LINE_FILTER_LAYERS, context
        )
        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.LineString, context)
        if inputLyr is None or inputLyr.featureCount() == 0:
            return {"FLAGS": self.flag_id}
        attributeBlackList = self.parameterAsFields(
            parameters, self.ATTRIBUTE_BLACK_LIST, context
        )
        
        multiStepFeedback = QgsProcessingMultiStepFeedback(14, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Building local cache on input layer...")
        )
        localCache = self.algRunner.runCreateFieldWithExpression(
            inputLyr=inputLyr
            if not onlySelected
            else QgsProcessingFeatureSourceDefinition(inputLyr.id(), True),
            expression="$id",
            fieldName="featid",
            fieldType=AlgRunner.FieldTypeInteger,
            context=context,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Calculating polygon areas...")
        )
        localCache = self.algRunner.runCreateFieldWithExpression(
            inputLyr=localCache,
            expression="$area",
            fieldName="area",
            fieldType=AlgRunner.FieldTypeDecimal,
            context=context,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Building boundary of polygons..."))
        boundaryPolygonLyr = self.algRunner.runBoundary(
            inputLayer=localCache,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Explodes boundary lines of polygons..."))
        explodeLinesLyr = self.algRunner.runExplodeLines(
            inputLyr=boundaryPolygonLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Finding the attributes that will be analyzed..."))
        attributeNameList = self.layerHandler.getAttributesFromBlackList(
            localCache,
            attributeBlackList,
            ignoreVirtualFields=self.parameterAsBoolean(
                parameters, self.IGNORE_VIRTUAL_FIELDS, context
            ),
            excludePrimaryKeys=self.parameterAsBoolean(
                parameters, self.IGNORE_PK_FIELDS, context
            ),
        )
        attributeNameList = attributeNameList + ["area"] if area_filter > 0 else attributeNameList
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        if len(lineFilterLyrList) > 1:
            lineFilterLyr = self.algRunner.runMergeVectorLayers(
                inputList=lineFilterLyrList,
                context=context,
                feedback=multiStepFeedback,
            )
        elif len(lineFilterLyrList) == 1:
            lineFilterLyr = lineFilterLyrList[0]
        else:
            lineFilterLyr = None
        if lineFilterLyr is not None:
            self.algRunner.runCreateSpatialIndex(lineFilterLyr, context, is_child_algorithm=True)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        idAttributesDictList = self.getValuesAttributesForEachFeat(
            attributeNameList=attributeNameList, 
            lyr=localCache,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        featidAndFeatDict = self.getFeatForEachFeatid(
            lyr=localCache,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating spatial index in explode lines layer..."))
        self.algRunner.runCreateSpatialIndex(explodeLinesLyr, context, is_child_algorithm=True)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Join attributes by location..."))
        joinAttributesByLocationLyr = self.algRunner.runJoinAttributesByLocation(
            inputLyr=explodeLinesLyr,
            joinLyr=explodeLinesLyr,
            context=context,
            predicateList=[AlgRunner.Equals],
            joinFields=attributeNameList,
            method=0,
            discardNonMatching=False,
            prefix='join_',
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        duplicateLinesDict = self.getDuplicatesLines(
            lyr=joinAttributesByLocationLyr, 
            attributeNameList=attributeNameList,
            area_filter=area_filter,
            feedback=multiStepFeedback,
        )
        
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        flagLinesGeomSet = self.verifyDesconnectedPolygons(
            duplicateLinesDict=duplicateLinesDict, 
            idAttributesDictList=idAttributesDictList, 
            featidAndFeatDict=featidAndFeatDict,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        flagLinesGeomList = self.verifyReallyFlagFeatures(
            flagLinesGeomSet=flagLinesGeomSet, 
            lineFilterLyr=lineFilterLyr,
            feedback=multiStepFeedback,
        )
        
        def flagLambda(x):
            return self.flagFeature(
                flagGeom=x,
                flagText=self.tr("Polygons with same attribute set that are not merged."),
                fromWkb=False,
            )
        
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Raising flags"))
        list(map(flagLambda, flagLinesGeomList))
        return {"FLAGS": self.flag_id}

    def verifyReallyFlagFeatures(
        self, 
        flagLinesGeomSet: Set[QgsGeometry], 
        lineFilterLyr: QgsVectorLayer,
        feedback: QgsProcessingMultiStepFeedback,
    ) -> List[QgsGeometry]:
        flagLinesGeomList = []
        size = 100 / len(flagLinesGeomSet) if flagLinesGeomSet else 0
        for current, geomFlag in enumerate(flagLinesGeomSet):
            if feedback.isCanceled():
                break
            bbox = geomFlag.boundingBox()
            if lineFilterLyr is not None and any(geomFlag.intersection(f.geometry()).type() == QgsWkbTypes.LineGeometry and geomFlag.intersection(f.geometry()).length() > 0 for f in lineFilterLyr.getFeatures(bbox)):
                continue
            flagLinesGeomList.append(geomFlag)
            feedback.setProgress(size * current)
        return flagLinesGeomList
    
    def getFeatForEachFeatid(
        self,
        lyr: QgsVectorLayer,
        feedback: QgsProcessingMultiStepFeedback,
    ) -> Dict[int, QgsFeature]:
        featidAndFeatDict = dict()
        size = 100 / lyr.featureCount() if lyr else 0
        for current, feat in enumerate(lyr.getFeatures()):
            if feedback.isCanceled():
                break
            featidAndFeatDict[feat["featid"]] = feat
            feedback.setProgress(size * current)
        return featidAndFeatDict

    def getValuesAttributesForEachFeat(self, 
        attributeNameList: List[str], 
        lyr:QgsVectorLayer,
        feedback: QgsProcessingMultiStepFeedback,
    ) -> Dict[int, List[str]]:
        idAttributesDictList = dict()
        size = 100 / lyr.featureCount() if lyr else 0
        for current, feat in enumerate(lyr.getFeatures()):
            if feedback.isCanceled():
                break
            idAttributesDictList[feat["featid"]] = []
            for attr in attributeNameList:
                if attr == "featid" or attr == "area":
                    continue
                idAttributesDictList[feat["featid"]].append(feat[attr])
            feedback.setProgress(size * current)
        return idAttributesDictList            

    def getDuplicatesLines(
        self, 
        lyr: QgsVectorLayer,
        attributeNameList: List[str],
        area_filter: float,
        feedback: QgsProcessingMultiStepFeedback,
    ) -> Dict[Tuple[int, int], Set[int]]:
        duplicateLinesDict = defaultdict(set)
        size = 100 / lyr.featureCount() if lyr else 0
        for current, feat in enumerate(lyr.getFeatures()):
            if feedback.isCanceled():
                break
            if (feat["featid"] == feat["join_featid"]) or ("area" in attributeNameList and feat["area"] > area_filter and feat["join_area"] > area_filter):
                continue
            duplicateLinesDict[tuple(sorted([feat["featid"], feat["join_featid"]]))].add(feat.id())
            feedback.setProgress(size * current)
        return duplicateLinesDict
    
    def getBoundaryOfPolygon(
            self, 
            feat: QgsFeature,
        ) -> QgsGeometry:
        geom = feat.geometry()
        boundary = QgsGeometry(geom.constGet().boundary())
        return boundary
    
    def verifyDesconnectedPolygons(
        self, 
        duplicateLinesDict: Dict[Tuple[int, int], Set[int]], 
        idAttributesDictList: Dict[int, QgsFeature], 
        featidAndFeatDict: Dict[int, QgsFeature],
        feedback: QgsProcessingMultiStepFeedback,
    ) -> Set[QgsGeometry]:
        flagLinesGeomSet = set()
        size = 100 / len(duplicateLinesDict) if duplicateLinesDict else 0
        for current, (id1, id2) in enumerate(duplicateLinesDict):
            if feedback.isCanceled():
                break
            attributes1 = idAttributesDictList[id1]
            attributes2 = idAttributesDictList[id2]
            if attributes1 != attributes2:
                continue
            feat1 = featidAndFeatDict[id1]
            feat2 = featidAndFeatDict[id2]
            boundary1 = self.getBoundaryOfPolygon(feat1)
            boundary2 = self.getBoundaryOfPolygon(feat2)
            flagGeomIntersection: QgsGeometry = boundary1.intersection(boundary2)
            if flagGeomIntersection.isNull() or flagGeomIntersection.isEmpty() or flagGeomIntersection.type() != QgsWkbTypes.LineGeometry:
                continue
            flagLinesGeomSet.add(flagGeomIntersection)
            feedback.setProgress(size * current)
        return flagLinesGeomSet

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyunmergedpolygonswithsameattributesetalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Unmerged Polygons With Same Attribute Set")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Polygon Handling")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Polygon Handling"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifyUnmergedPolygonsWithSameAttributeSetAlgorithm", string
        )

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    def helpUrl(self):
        return help().helpUrl(self.name())

    def createInstance(self):
        return IdentifyUnmergedPolygonsWithSameAttributeSetAlgorithm()
