# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-05-01
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

from __future__ import absolute_import

from collections import defaultdict
from functools import partial
from itertools import combinations

from processing.tools import dataobjects

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.Utils.FrameTools.map_index import UtmGrid
from qgis.analysis import QgsGeometrySnapper, QgsInternalGeometrySnapper
from qgis.core import (edit, Qgis, QgsCoordinateReferenceSystem, QgsCoordinateTransform,
    QgsExpression, QgsFeature, QgsFeatureRequest, QgsField, QgsGeometry, QgsMessageLog,
    QgsProcessingContext, QgsProcessingMultiStepFeedback, QgsProcessingUtils, QgsProject,
    QgsSpatialIndex, QgsVectorDataProvider, QgsVectorLayer, QgsVectorLayerUtils, QgsWkbTypes,
    QgsProcessingFeatureSourceDefinition)
from qgis.PyQt.Qt import QObject, QVariant

from .featureHandler import FeatureHandler
from .geometryHandler import GeometryHandler


class LayerHandler(QObject):
    def __init__(self, iface = None, parent = None):
        super(LayerHandler, self).__init__()
        self.parent = parent
        self.iface = iface
        if iface:
            self.canvas = iface.mapCanvas()
        self.featureHandler = FeatureHandler(iface)
        self.geometryHandler = GeometryHandler(iface)
    
    def getFeatureList(self, lyr, onlySelected=False, returnIterator=True, returnSize=True):
        """
        Gets the features from lyr acording to parameters.
        :param (QgsVectorLayer) lyr: layer;
        :param (bool) onlySelected: if true, only fetches selected features from layer;
        :param (bool) returnIterator: if true, returns the iterator object;
        :param (bool) returnSize: if true, return the featureList and size.
        """
        if onlySelected:
            featureList = lyr.getSelectedFeatures() if returnIterator else [i for i in lyr.getSelectedFeatures()]
            size = lyr.selectedFeatureCount()
        else:
            featureList = lyr.getFeatures() if returnIterator else [i for i in lyr.getFeatures()]
            size = lyr.featureCount()
        if returnSize:
            return featureList, size
        else:
            return featureList
    
    def getSelectedFeatures(self, lyr):
        return lyr.selectedFeatures()
    
    def getSelectedFeaturesFromCanvasLayers(self):
        """
        looks on iface and returns a dict where key is lyr and value is a list of features
        """
        selectedDict = dict()
        for lyr in self.canvas.layers():
            if not isinstance(lyr, QgsVectorLayer):
                continue
            featureList = self.getFeatureList(lyr, onlySelected=True, returnIterator=False)
            if featureList:
                selectedDict[lyr] = featureList
        return selectedDict
    
    def reclassifySelectedFeatures(self, destinationLayer, reclassificationDict):
        """
        Gets a destination layer and uses reclassificationDict to reclassify each selected feature
        """
        selectedDict = self.getSelectedFeaturesFromCanvasLayers()
        parameterDict = self.getDestinationParameters(destinationLayer)
        reclassifyCount = 0
        destinationLayer.startEditing()
        destinationLayer.beginEditCommand(self.tr('DsgTools reclassification'))
        for lyr, featureList in [(k, v) for k, v in selectedDict.items() if len(v[0]) > 0]:
            featureList = featureList[0] if isinstance(featureList, tuple) else featureList
            coordinateTransformer = self.getCoordinateTransformer(lyr, destinationLayer)
            newFeatList, deleteList = self.featureHandler.reclassifyFeatures(featureList, lyr, reclassificationDict, coordinateTransformer, parameterDict)
            featuresAdded = destinationLayer.addFeatures(newFeatList)
            if featuresAdded:
                lyr.startEditing()
                lyr.deleteFeatures(deleteList)
                reclassifyCount += len(deleteList)
        return reclassifyCount

    def getDestinationParameters(self, destinationLayer):
        """
        Gets the layer parameters such as geometryType (geomType), if it
        has m-values (hasMValues), if it has z-values (hasZValues) and
        if it is a multi-geometry (isMulti)
        """
        parameterDict = dict()
        parameterDict['geomType'] = destinationLayer.geometryType()
        parameterDict['hasMValues'] =  QgsWkbTypes.hasM(int(destinationLayer.wkbType()))    #generic check (not every database is implemented as ours)
        parameterDict['hasZValues'] =  QgsWkbTypes.hasZ(int(destinationLayer.wkbType()))    #
        parameterDict['isMulti'] = QgsWkbTypes.isMultiType(int(destinationLayer.wkbType()))
        return parameterDict
    
    def getCoordinateTransformer(self, inputLyr, outputLyr):
        """
        If inputLyr and outputLyr have different crs, creates a Coordinate Transform
        and returns it. Otherwise, returns None.
        """
        inputAuthId = inputLyr.crs().authid()
        outputAuthId = outputLyr.crs().authid()
        if inputAuthId == outputAuthId:
            return None
        inputSrc = QgsCoordinateReferenceSystem(inputAuthId)
        outputSrc = QgsCoordinateReferenceSystem(outputAuthId)
        coordinateTransformer = QgsCoordinateTransform(inputSrc, outputSrc, QgsProject.instance())
        return coordinateTransformer
    
    def createAndPopulateUnifiedVectorLayer(self, layerList, geomType=None, epsg=None, attributeTupple=False, attributeBlackList='', onlySelected=False, feedback=None):
        if not epsg:
            epsg = layerList[0].crs().authid().split(':')[-1]
        if not geomType:
            geomType = layerList[0].geometryType()
        unified_layer = self.createUnifiedVectorLayer(geomType, epsg, \
                                                      attributeTupple=attributeTupple)
        parameterDict = self.getDestinationParameters(unified_layer)
        featList = self.getUnifiedLayerFeatures(unified_layer, layerList, \
                                                      attributeTupple=attributeTupple, \
                                                      attributeBlackList=attributeBlackList, \
                                                      onlySelected=onlySelected, \
                                                      parameterDict=parameterDict, \
                                                      feedback=feedback)
        self.addFeaturesToLayer(unified_layer, featList, msg='Populating unified layer')
        return unified_layer

    def createUnifiedVectorLayer(self, geomType, srid, attributeTupple=False):
        """
        Creates a unified vector layer for validation purposes.
        """
        fields = self.getUnifiedVectorFields(attributeTupple=attributeTupple)
        lyrUri = "{0}?crs=epsg:{1}".format(QgsWkbTypes.displayString(geomType), srid)
        lyr = QgsVectorLayer(lyrUri, "unified_layer", "memory")
        lyr.startEditing()
        fields = self.getUnifiedVectorFields(attributeTupple=attributeTupple)
        lyr.dataProvider().addAttributes(fields)
        lyr.updateFields()
        return lyr
    
    def getUnifiedVectorFields(self, attributeTupple=False):
        if not attributeTupple:
            fields = [QgsField('featid', QVariant.Int), 
                      QgsField('layer', QVariant.String)
                    ]
        else:
            fields = [QgsField('featid', QVariant.Int), 
                      QgsField('layer', QVariant.String), 
                      QgsField('tupple', QVariant.String), 
                      QgsField('blacklist', QVariant.String)
                      ]
        return fields
    

    def getUnifiedLayerFeatures(self, unifiedLyr, layerList, attributeTupple=False, attributeBlackList=None, onlySelected=False, parameterDict=None, feedback=None):
        parameterDict = {} if parameterDict is None else parameterDict
        featList = []
        blackList = attributeBlackList.split(',') if attributeBlackList is not None and ',' in attributeBlackList else []
        if feedback:
            multiStepFeedback = QgsProcessingMultiStepFeedback(len(layerList), feedback)
        for i, layer in enumerate(layerList):
            if feedback:
                if feedback.isCanceled():
                    break
                multiStepFeedback.setCurrentStep(i)
            # recording class name
            layername = layer.name()
            coordinateTransformer = self.getCoordinateTransformer(unifiedLyr, layer)
            iterator, size = self.getFeatureList(layer, onlySelected=onlySelected, returnSize=True)
            for current, feature in enumerate(iterator):
                if feedback:
                    if multiStepFeedback.isCanceled():
                        break
                newFeats = self.featureHandler.createUnifiedFeature(unifiedLyr, feature, layername,\
                                                                   bList=blackList, \
                                                                   attributeTupple=attributeTupple, \
                                                                   parameterDict=parameterDict, \
                                                                   coordinateTransformer=coordinateTransformer)
                featList += newFeats
                if feedback:
                    multiStepFeedback.setProgress(current*size)
        return featList

    def addFeaturesToLayer(self, lyr, featList, commitChanges=True, msg=None):
        msg = '' if msg is None else msg
        lyr.startEditing()
        lyr.beginEditCommand(msg)
        res = lyr.addFeatures(featList)
        lyr.endEditCommand()
        if commitChanges:
            lyr.commitChanges()
        return res
    
    def splitUnifiedLayer(self, unifiedLyr, lyrList):
        """
        Updates layers from lyrList with features from unifiedLyr
        """

        for lyr in lyrList:
            self.updateOriginalLayerFromUnifiedLayer(lyr, unifiedLyr)
    
    def buildInputDict(self, inputLyr, pk=None, feedback=None, onlySelected=False):
        """
        Maps inputLyr into a dict with its attributes.
        """
        inputDict = dict()
        if onlySelected:
            iterator = inputLyr.getSelectedFeatures()
            localTotal = 100/inputLyr.selectedFeatureCount() if inputLyr.selectedFeatureCount() else 0
        else:
            request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
            iterator = inputLyr.getFeatures(request)
            localTotal = 100/inputLyr.featureCount() if inputLyr.featureCount() else 0
        for current, feature in enumerate(iterator):
            if feedback:
                if feedback.isCanceled():
                    break            
            key = feature[pk] if pk else feature.id()
            inputDict[key] = dict()
            inputDict[key]['featList'] = []
            inputDict[key]['featWithoutGeom'] = feature
            if feedback:
                feedback.setProgress(localTotal*current)
        return inputDict
    
    def populateInputDictFeatList(self, lyr, inputDict, pk=None, request=None, feedback=None):
        iterator = lyr.getFeatures(request) if request else lyr.getFeatures()
        localTotal = 100/lyr.featureCount() if lyr.featureCount() else 0
        for current, feat in enumerate(iterator):
            if feedback:
                if feedback.isCanceled():
                    break  
            fid = feat[pk] if pk else feat.id()
            if fid in inputDict:
                inputDict[fid]['featList'].append(feat)
            if feedback:
                feedback.setProgress(localTotal*current)

    
    def updateOriginalLayer(self, originalLayer, resultLayer, field=None, feedback=None, keepFeatures=False, onlySelected=True):
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback) if feedback else None
        #1- build inputDict structure to store the original state of the layer
        if feedback:
            multiStepFeedback.setCurrentStep(0)
        inputDict = self.buildInputDict(originalLayer, pk = field, feedback = multiStepFeedback, onlySelected = onlySelected) 
        #2- populate the inputDict with the features from the resultLayer
        if feedback:
            multiStepFeedback.setCurrentStep(1)
        self.populateInputDictFeatList(resultLayer, inputDict, pk=field, feedback = multiStepFeedback)
        #3- get information from originalLayer and resultLayer
        if feedback:
            multiStepFeedback.setCurrentStep(2)
        parameterDict = self.getDestinationParameters(originalLayer)
        coordinateTransformer = self.getCoordinateTransformer(resultLayer, originalLayer)
        #4- run update original layer
        self.updateOriginalLayerFeatures(originalLayer, inputDict, parameterDict = parameterDict, coordinateTransformer = coordinateTransformer, keepFeatures = keepFeatures, feedback = multiStepFeedback)

    def updateOriginalLayersFromUnifiedLayer(self, lyrList, unifiedLyr, feedback = None, onlySelected = False):
        lenList = len(lyrList)
        parameterDict = self.getDestinationParameters(unifiedLyr)
        multiStepFeedback = QgsProcessingMultiStepFeedback(lenList, feedback) if feedback else None
        for i, lyr in enumerate(lyrList):
            if feedback:
                if multiStepFeedback.isCanceled():
                    break
                multiStepFeedback.setCurrentStep(i)
            innerFeedback = QgsProcessingMultiStepFeedback(3, multiStepFeedback) if multiStepFeedback else None
            innerFeedback.setCurrentStep(0)
            inputDict = self.buildInputDict(lyr, onlySelected=onlySelected, feedback=innerFeedback)
            if innerFeedback:
                if innerFeedback.isCanceled():
                    break
            request = QgsFeatureRequest(QgsExpression("layer = '{0}'".format(lyr.name())))
            innerFeedback.setCurrentStep(1)
            self.populateInputDictFeatList(unifiedLyr, inputDict, pk = 'featid', request = request, feedback=innerFeedback)
            if innerFeedback:
                if innerFeedback.isCanceled():
                    break
            coordinateTransformer = self.getCoordinateTransformer(unifiedLyr, lyr)
            innerFeedback.setCurrentStep(2)
            self.updateOriginalLayerFeatures(lyr, inputDict, parameterDict = parameterDict, coordinateTransformer = coordinateTransformer, feedback=innerFeedback)
    
    def updateOriginalLayerFeatures(self, lyr, inputDict, parameterDict=None, coordinateTransformer=None, keepFeatures=False, feedback=None):
        """
        Updates lyr using inputDict
        """
        parameterDict = {} if parameterDict is None else parameterDict
        idsToRemove, featuresToAdd, idsToRemove = [], [], []
        lyr.startEditing()
        lyr.beginEditCommand('Updating layer {0}'.format(lyr.name()))
        localTotal = 100/len(inputDict) if inputDict else 0
        for current, id in enumerate(inputDict):
            if feedback:
                if feedback.isCanceled():
                    break
            outFeats = inputDict[id]['featList']
            if len(outFeats) == 0 and id not in idsToRemove: #no output, must delete feature
                idsToRemove.append(id)
                continue
            geomToUpdate, addedFeatures, deleteId = self.featureHandler.handleFeature(outFeats, \
                                                                                 inputDict[id]['featWithoutGeom'], \
                                                                                 lyr, \
                                                                                 parameterDict = parameterDict, \
                                                                                 coordinateTransformer = coordinateTransformer)
            if geomToUpdate is not None:
                lyr.changeGeometry(id, geomToUpdate) #faster according to the api
            featuresToAdd += addedFeatures
            idsToRemove += [id] if deleteId else []
            if feedback:
                feedback.setProgress(localTotal*current)
        lyr.addFeatures(featuresToAdd)
        if not keepFeatures:
            lyr.deleteFeatures(idsToRemove)
        lyr.endEditCommand()
    
    def mergeLinesOnLayer(self, lyr, onlySelected=False, feedback=None, ignoreVirtualFields=True, attributeBlackList=None, excludePrimaryKeys=True):
        attributeBlackList = [] if attributeBlackList is None else attributeBlackList
        if feedback:
            localFeedback = QgsProcessingMultiStepFeedback(3, feedback)
            localFeedback.setCurrentStep(0)
        #build attribute dict
        attributeFeatDict = self.buildAttributeFeatureDict(lyr, onlySelected=onlySelected, feedback=localFeedback, attributeBlackList=attributeBlackList)
        
        #build network dict
        if feedback:
            localFeedback.setCurrentStep(1)
        networkDict = self.buildInitialAndEndPointDict(lyr, onlySelected=onlySelected, feedback=localFeedback)
        
        parameterDict = self.getDestinationParameters(lyr)

        idsToRemove = []
        if feedback:
            localFeedback.setCurrentStep(2)
            localTotal = 100/(len(attributeFeatDict)) if len(attributeFeatDict) != 0 else 0
            mergeFeedback = QgsProcessingMultiStepFeedback(len(attributeFeatDict), localFeedback)
        lyr.startEditing()
        lyr.beginEditCommand(self.tr('Merging Lines'))

        for current, (key, featList) in enumerate(attributeFeatDict.items()):
            if feedback:
                if feedback.isCanceled():
                    break
                mergeFeedback.setCurrentStep(current)
            self.featureHandler.mergeLineFeatures(
                featList=featList,
                lyr=lyr,
                idsToRemove=idsToRemove,
                parameterDict=parameterDict,
                feedback=mergeFeedback,
                networkDict=networkDict
            )
        lyr.deleteFeatures(idsToRemove)
        lyr.endEditCommand()
    
    def buildAttributeFeatureDict(self, lyr, onlySelected = False, feedback = None, ignoreVirtualFields = True, attributeBlackList = None, excludePrimaryKeys = True):
        iterator, size = self.getFeatureList(lyr, onlySelected=onlySelected)
        localTotal = 100/size if size != 0 else 0
        attributeFeatDict = dict()
        columns = self.getAttributesFromBlackList(lyr, attributeBlackList=attributeBlackList, ignoreVirtualFields=ignoreVirtualFields, excludePrimaryKeys=excludePrimaryKeys)
        for current, feat in enumerate(iterator):
            if feedback:
                if feedback.isCanceled():
                    break
            self.appendFeatOnAttrsDict(attributeFeatDict, feat, columns)
            if feedback:
                feedback.setProgress(localTotal*current)
        return attributeFeatDict
    
    def getAttributesFromBlackList(self, lyr, attributeBlackList=None, ignoreVirtualFields=True, excludePrimaryKeys=True):
        attributeBlackList = [] if attributeBlackList is None else attributeBlackList
        pkIndexes = lyr.primaryKeyAttributes() if excludePrimaryKeys else []
        typeBlackList = [6] if ignoreVirtualFields else []
        columns = [field.name() for idx, field in enumerate(lyr.fields()) if idx not in pkIndexes and field.type() not in typeBlackList and field.name() not in attributeBlackList]
        return columns
    
    def appendFeatOnAttrsDict(self, inputDict, feat, columns):
        attrKey = ','.join(['{}'.format(feat[column]) for column in columns])
        if attrKey not in inputDict:
            inputDict[attrKey] = []
        inputDict[attrKey].append(feat)
    
    def buildInitialAndEndPointDict(self, lyr, onlySelected = False, feedback = None):
        """
        Calculates initial point and end point from each line from lyr.
        """
        # start and end points dict
        endVerticesDict = dict()
        # iterating over features to store start and end points
        iterator, size = self.getFeatureList(lyr, onlySelected=onlySelected)
        for current, feat in enumerate(iterator):
            if feedback:
                if feedback.isCanceled():
                    break
            geom = feat.geometry()
            lineList = geom.asMultiPolyline() if geom.isMultipart() else [geom.asPolyline()]
            for line in lineList:
                self.addFeatToDict(endVerticesDict, line, feat.id())
            if feedback:
                feedback.setProgress(size*current)
        return endVerticesDict
    
    def getDuplicatedFeaturesDict(self, lyr, onlySelected = False, attributeBlackList = None, ignoreVirtualFields = True, excludePrimaryKeys = True, useAttributes=False, feedback = None):
        """
        returns geomDict = {
            'bbox_geom' : {geomKey : -list of duplicated feats-}
        }
        """
        geomDict = dict()
        isMulti = QgsWkbTypes.isMultiType(int(lyr.wkbType()))
        iterator, featCount = self.getFeatureList(lyr, onlySelected=onlySelected)
        size = 100/featCount if featCount else 0
        columns = self.getAttributesFromBlackList(lyr, attributeBlackList=attributeBlackList, ignoreVirtualFields=ignoreVirtualFields, excludePrimaryKeys=excludePrimaryKeys)
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback) if feedback else None
        multiStepFeedback.setCurrentStep(0)
        #builds bounding box dict to do a geos comparison for each feat in list
        bbDict = self.getFeaturesWithSameBoundingBox(iterator, isMulti, featCount, columns=columns, feedback=feedback)
        multiStepFeedback.setCurrentStep(1)
        for current, (key, featList) in enumerate(bbDict.items()):
            if feedback is not None and feedback.isCanceled():
                break
            if len(featList) > 1:
                duplicatedDict = self.searchDuplicatedFeatures(featList, columns=columns, useAttributes=useAttributes)
                geomDict.update(duplicatedDict)
            if feedback is not None:
                feedback.setProgress(size * current)
        return geomDict
    
    def getFeaturesWithSameBoundingBox(self, iterator, isMulti, size, columns=None, feedback=None):
        """
        Iterates over iterator and gets 
        """
        bbDict = defaultdict(list)
        for current, feat in enumerate(iterator):
            if feedback is not None and feedback.isCanceled():
                break
            geom = feat.geometry()
            if isMulti and not geom.isMultipart():
                geom.convertToMultiType()
            geomKey = geom.asWkb()
            geomBB_key = geom.boundingBox().asWktPolygon()
            attrKey = ','.join(['{}'.format(feat[column]) for column in columns]) if columns is not None else ''
            bbDict[geomBB_key].append({'geom':geom, 'feat':feat, 'attrKey':attrKey})
            if feedback is not None:
                feedback.setProgress(size * current)
        return bbDict
    
    def searchDuplicatedFeatures(self, featList, columns, useAttributes=False):
        """
        featList = list of {'geom': geom, 'feat':feat}
        returns {geomKey : -list of duplicated feats-}
        """
        duplicatedDict = dict()
        if featList:
            fields = [f.name() for f in featList[0]['feat'].fields()]
        for dict_feat1, dict_feat2 in combinations(featList, 2):
            geom1 = dict_feat1['geom']
            geom2 = dict_feat2['geom']
            feat1 = dict_feat1['feat']
            feat2 = dict_feat2['feat']
            wkb1 = geom1.asWkb()
            wkb2 = geom2.asWkb()
            if not geom1.isGeosEqual(geom2):
                continue
            elif useAttributes:
                # do things to check attributes
                try:
                    for attr in fields:
                        if attr not in columns:
                            continue
                        elif feat1[attr] != feat2[attr]:
                            raise Exception('Skip outter loop')
                except:
                    continue
            if wkb1 in duplicatedDict:
                duplicatedDict[wkb1].append(feat2)
            elif wkb2 in duplicatedDict:
                duplicatedDict[wkb2].append(feat1)
            else:
                duplicatedDict[wkb1] = [feat1, feat2]
        return duplicatedDict

    def addFeatToDict(self, endVerticesDict, line, featid):
        self.addPointToDict(line[0], endVerticesDict, featid)
        self.addPointToDict(line[len(line) - 1], endVerticesDict, featid)
    
    def addPointToDict(self, point, pointDict, featid):
        if point not in pointDict:
            pointDict[point] = []
        pointDict[point].append(featid)
                
    def addDissolveField(self, layer, tol, feedback = None):
        #add temp field
        idField = QgsField('d_id',QVariant.Int)
        layer.dataProvider().addAttributes([idField])
        layer.updateFields()
        #small feature list
        
        if feedback:
            multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
            multiStepFeedback.setCurrentStep(0)
        else:
            multiStepFeedback = None
        smallFeatureList, bigFeatureList, bigFeatIndex = self.buildSizeSearchStructure(layer, tol, feedback=multiStepFeedback)

        if multiStepFeedback:
            multiStepFeedback.setCurrentStep(1)
        self.populateSizeSearchStructure(layer, smallFeatureList, bigFeatIndex, feedback=multiStepFeedback)

        if multiStepFeedback:
            multiStepFeedback.setCurrentStep(2)
        updateDict = self.updateFeaturesWithSize(layer, smallFeatureList, bigFeatureList, feedback=multiStepFeedback)
        return layer
    
    def getCandidates(self, idx, bbox):
        return idx.intersects(bbox)

    def buildSizeSearchStructure(self, layer, tol, feedback = None):
        """
        Builds search structure according to layer and tol.

        Returns a list with small features, another list with big features and the spatial index of the big feats.
        """
        smallFeatureList = []
        bigFeatureList = []
        bigFeatIndex = QgsSpatialIndex()

        featSize = layer.featureCount()
        size = 100 / featSize if featSize else 0

        for current, feat in enumerate(layer.getFeatures()):
            if feedback:
                if feedback.isCanceled():
                    break
            feat['d_id'] = feat['featid']
            if feat.geometry().area() < float(tol):
                smallFeatureList.append(feat)
            else:
                bigFeatIndex.insertFeature(feat)
                bigFeatureList.append(feat)
            if feedback:
                feedback.setProgress(size * current)
        return smallFeatureList, bigFeatureList, bigFeatIndex
    
    def populateSizeSearchStructure(self, layer, smallFeatureList, bigFeatIndex, feedback = None):
        # using spatial index to speed up the process
        featSize = len(smallFeatureList)
        size = 100 / featSize if featSize else 0
        for current, sfeat in enumerate(smallFeatureList):
            if feedback:
                if feedback.isCanceled():
                    break
            candidates = bigFeatIndex.intersects(sfeat.geometry().boundingBox())
            for candidate in candidates:
                bfeat = [i for i in layer.dataProvider().getFeatures(QgsFeatureRequest(candidate))][0]
                if sfeat['d_id'] == sfeat['featid'] and sfeat.geometry().intersects(bfeat.geometry()) and sfeat['tupple'] == bfeat['tupple']:
                    sfeat['d_id'] = bfeat['featid']
            if feedback:
                feedback.setProgress(size * current)
    
    def updateFeaturesWithSize(self, layer, smallFeatureList, bigFeatureList, feedback = None):
        updateDict = dict()
        idx = layer.fieldNameIndex('tupple')
        featList = smallFeatureList + bigFeatureList
        featSize = len(featList)
        size = 100 / featSize if featSize else 0
        for current, feat in enumerate(featList):
            if feedback:
                if feedback.isCanceled():
                    break
            newValue = u'{0},{1}'.format(feat['tupple'], feat['d_id'])
            updateDict[feat.id()] = {idx:newValue}
            if feedback:
                feedback.setProgress(size * current)
        return updateDict
    
    def filterDangles(self, lyr, searchRadius, feedback = None):
        deleteList = []
        if feedback is not None:
            multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
            multiStepFeedback.setCurrentStep(0)
        else:
            multiStepFeedback = None
        spatialIdx, idDict = self.buildSpatialIndexAndIdDict(lyr, feedback=multiStepFeedback)
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
        featSize = len(idDict)
        size = 100 / featSize if featSize else 0
        for current, (id, feat) in enumerate(idDict.items()):
            if feedback is not None and feedback.isCanceled():
                break
            if id not in deleteList:
                buffer = feat.geometry().buffer(searchRadius, -1)
                bufferBB = buffer.boundingBox()
                #gets candidates from spatial index
                candidateIds = spatialIdx.intersects(bufferBB)
                for fid in candidateIds:
                    if fid != id and fid not in deleteList and buffer.intersects(feat.geometry()):
                        deleteList.append(fid)
            if feedback is not None:
                multiStepFeedback.setProgress(size * current)
        
        lyr.startEditing()
        lyr.beginEditCommand('Filter dangles')
        lyr.deleteFeatures(deleteList)
        lyr.commitChanges()


    def buildSpatialIndexAndIdDict(self, inputLyr, feedback = None, featureRequest=None):
        """
        creates a spatial index for the input layer
        :param inputLyr: (QgsVectorLayer) input layer;
        :param feedback: (QgsProcessingFeedback) processing feedback;
        :param featureRequest: (QgsFeatureRequest) optional feature request;
        """
        spatialIdx = QgsSpatialIndex()
        idDict = {}
        featCount = inputLyr.featureCount()
        size = 100/featCount if featCount else 0
        iterator = inputLyr.getFeatures() if featureRequest is None else inputLyr.getFeatures(featureRequest)
        addFeatureAlias = lambda x : self.addFeatureToSpatialIndex(
            current=x[0],
            feat=x[1],
            spatialIdx=spatialIdx,
            idDict=idDict,
            size=size,
            feedback=feedback
        )
        list(map(addFeatureAlias, enumerate(iterator)))
        return spatialIdx, idDict
    
    def addFeatureToSpatialIndex(self, current, feat, spatialIdx, idDict, size, feedback):
        """
        Adds feature to spatial index. Used along side with a python map operator
        to improve performance.
        :param current : (int) current index
        :param feat : (QgsFeature) feature to be added on spatial index and on idDict
        :param spatialIdx: (QgsSpatialIndex) spatial index
        :param idDict: (dict) dictionary with format {feat.id(): feat}
        :param size: (int) size to be used to update feedback
        :param feedback: (QgsProcessingFeedback) feedback to be used on processing
        """
        if feedback is not None and feedback.isCanceled():
            return
        idDict[feat.id()] = feat
        spatialIdx.insertFeature(feat)
        if feedback is not None:
            feedback.setProgress(size * current)
    
    def getFrameOutterBounds(self, frameLayer, algRunner, context, feedback = None):
        """
        Gets the outter bounds of all frame features composing frame layer.
        :param frameLayer: (QgsVectorLayer) frame layer.
        :return: (list-of-QgsGeometry) list of all disjuncts outter bounds of features in frame layer.
        """
        frameGeomList = []
        if feedback is not None:
            multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
            multiStepFeedback.setCurrentStep(0)
        else:
            multiStepFeedback = None
        # dissolve every feature into a single one
        outputLayer = algRunner.runDissolve(frameLayer, context, feedback = multiStepFeedback)
        if feedback is not None:
            multiStepFeedback.setCurrentStep(1)
        boundaryLayer = algRunner.runBoundary(outputLayer, context, feedback = multiStepFeedback)
        # get all frame outter layer found
        if feedback is not None:
            multiStepFeedback.setCurrentStep(2)
            featCount = boundaryLayer.featureCount()
            size = 100/featCount if featCount else 0
        for current, feat in enumerate(boundaryLayer.getFeatures()):
            if feedback is not None and feedback.isCanceled():
                break
            geom = feat.geometry()
            # deaggregate geometry, if necessary
            frameGeomList += self.geometryHandler.deaggregateGeometry(multiGeom=geom)
            if feedback is not None:
                multiStepFeedback.setProgress(size * current)
        return frameGeomList
    
    def identifyAllNodes(self, networkLayer):
        """
        Identifies all nodes from a given layer (or selected features of it). The result is returned as a dict of dict.
        :param networkLayer: target layer to which nodes identification is required.
        :return: { node_id : { start : [feature_which_starts_with_node], end : feature_which_ends_with_node } }.
        """
        nodeDict = dict()
        isMulti = QgsWkbTypes.isMultiType(int(networkLayer.wkbType()))
        if self.parameters['Only Selected']:
            features = networkLayer.selectedFeatures()
        else:
            features = [feat for feat in networkLayer.getFeatures()]
        for feat in features:
            nodes = self.DsgGeometryHandler.getFeatureNodes(networkLayer, feat)
            if nodes:
                if isMulti:
                    if len(nodes) > 1:
                        # if feat is multipart and has more than one part, a flag should be raised
                        continue # CHANGE TO RAISE FLAG
                    elif len(nodes) == 0:
                        # if no part is found, skip feature
                        continue
                    else:
                        # if feat is multipart, "nodes" is a list of list
                        nodes = nodes[0]                
                # initial node
                pInit, pEnd = nodes[0], nodes[-1]
                # filling starting node information into dictionary
                if pInit not in nodeDict:
                    # if the point is not already started into dictionary, it creates a new item
                    nodeDict[pInit] = { 'start' : [], 'end' : [] }
                if feat not in nodeDict[pInit]['start']:
                    nodeDict[pInit]['start'].append(feat)                            
                # filling ending node information into dictionary
                if pEnd not in nodeDict:
                    nodeDict[pEnd] = { 'start' : [], 'end' : [] }
                if feat not in nodeDict[pEnd]['end']:
                    nodeDict[pEnd]['end'].append(feat)
        return nodeDict
    
    def snapToLayer(self, inputLyr, refLyr, tol, behavior, onlySelected=False, feedback=None):
        """
        Snaps and updates inpytLyr
        """
        snapper = QgsGeometrySnapper(refLyr) if inputLyr != refLyr and behavior != 7 else QgsInternalGeometrySnapper(tol, behavior)
        iterator, featCount = self.getFeatureList(inputLyr, onlySelected=onlySelected)
        size = 100/featCount if featCount else 0
        deleteList = []
        inputLyr.startEditing()
        inputLyr.beginEditCommand('Snapping Features')
        for current, feat in enumerate(iterator):
            featid = feat.id()
            geom = feat.geometry()
            if feedback is not None and feedback.isCanceled():
                break
            elif not feat.hasGeometry() or geom.isNull() or geom.isEmpty():
                deleteList.append(featid)
            elif geom.type() == QgsWkbTypes.LineGeometry and geom.length() < tol:
                deleteList.append(featid)
            else:
                # remove duplicate nodes to avoid problem in snapping
                geom.removeDuplicateNodes()
                fixedGeom = geom.makeValid()
                if not fixedGeom.isNull():
                    outputGeom = snapper.snapGeometry(fixedGeom, tol, behavior) if inputLyr != refLyr and behavior != 7 else snapper.snapFeature(feat)
                    if geom is None:
                        deleteList.append(featid)
                    else:
                        inputLyr.changeGeometry(featid, outputGeom)
            if feedback is not None:
                feedback.setProgress(size * current)
        inputLyr.deleteFeatures(deleteList)
        inputLyr.endEditCommand()
    
    def getContourLineOutOfThreshold(self, contourLyr, terrainPolygonLyr, threshold, refLyr=None, feedback=None):
        """
        todo
        """
        #1. Build contour spatial index

        #2. 
        pass

    def filterByExpression(self, layer, expression, context, feedback=None):
        """
        Filters a given layer using a filtering expression. The original layer is not modified.
        :param layer: (QgsVectorLayer) layer to be filtered.
        :param expression: (str) expression to be used as filter.
        :param context: (QgsProcessingContext) processing context in which algorithm should be executed.
        :param feedback: (QgsFeedback) QGIS feedback component (progress bar).
        :return: (QgsVectorLayer) filtered layer.
        """
        return AlgRunner().runFilterExpression(
                inputLyr=layer,
                context=context,
                expression = expression,
                feedback=feedback
            )

    def prepareConversion(self, inputLyr, context, inputExpression=None, filterLyr=None,\
                         behavior=None, bufferRadius=None, conversionMap=None, feedback=None):
        bufferRadius = 0 if bufferRadius is None else bufferRadius
        algRunner = AlgRunner()
        if feedback is not None:
            count = 0
            if inputExpression is not None:
                count += 1
            if filterLyr is not None:
                count += 1
                if behavior == 3:
                    count += 1
            elif count == 0:
                return inputLyr
            multiStepFeedback = QgsProcessingMultiStepFeedback(count, feedback)
        else:
            multiStepFeedback = None
        localLyr = inputLyr
        currentStep = 0
        if inputExpression is not None and inputExpression != '':
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(currentStep)
            localLyr = algRunner.runFilterExpression(
                inputLyr=localLyr,
                context=context,
                expression = inputExpression,
                feedback=multiStepFeedback
            )
            currentStep+=1
        if filterLyr is not None:
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(currentStep)
            if behavior == 3:
                filterLyr = algRunner.runBuffer(filterLyr, bufferRadius, context, feedback=multiStepFeedback)
                currentStep += 1
            localLyr = algRunner.runIntersection(localLyr, context, overlayLyr=filterLyr)
        return localLyr
    
    def identifyAndFixInvalidGeometries(self, inputLyr, fixInput=False, onlySelected=False, feedback=None):
        iterator, featCount = self.getFeatureList(inputLyr, onlySelected=onlySelected)
        stepSize = 100/featCount if featCount else 0
        flagDict = dict()
        parameterDict = self.getDestinationParameters(inputLyr)
        geometryType = inputLyr.geometryType()
        newFeatSet = set()
        if fixInput:
            inputLyr.startEditing()
            inputLyr.beginEditCommand('Fixing geometries')
        for current, feat in enumerate(iterator):
            if feedback is not None and feedback.isCanceled():
                break
            geom = feat.geometry()
            id = feat.id()
            attrMap = { idx : feat[field.name()] for idx, field in enumerate(feat.fields()) if idx not in inputLyr.primaryKeyAttributes()}
            for i, validate_type in enumerate(['GEOS', 'QGIS']):
                if feedback is not None and feedback.isCanceled():
                    break
                for error in geom.validateGeometry(i):
                    if feedback is not None and feedback.isCanceled():
                        break

                    if error.hasWhere():
                        errorPointXY = error.where()
                        flagGeom = QgsGeometry.fromPointXY(errorPointXY)
                        if geom.type() == QgsWkbTypes.LineGeometry and self.isClosedAndFlagIsAtStartOrEnd(geom, flagGeom):
                            continue
                        if errorPointXY not in flagDict:
                            flagDict[errorPointXY] = {
                                'geom' : flagGeom,
                                'reason' : ''
                            }
                        flagDict[errorPointXY]['reason'] += '{type} invalid reason: {text}\n'.format(
                            type=validate_type,
                            text=error.what()
                        )
            if fixInput:
                geom.removeDuplicateNodes(useZValues=parameterDict['hasZValues'])
                fixedGeom = geom.makeValid()
                for idx, newGeom in enumerate(self.geometryHandler.handleGeometryCollection(fixedGeom, geometryType, parameterDict=parameterDict)):
                    if idx == 0:
                        inputLyr.changeGeometry(id, newGeom)
                    else:
                        newFeat = QgsVectorLayerUtils.createFeature(inputLyr, newGeom, attrMap)
                        newFeatSet.add(newFeat)
            if feedback is not None:
                feedback.setProgress(stepSize*current)
        if fixInput:
            inputLyr.addFeatures(newFeatSet)
            inputLyr.endEditCommand()

        return flagDict
    
    def isClosedAndFlagIsAtStartOrEnd(self, geom, flagGeom):
        for part in geom.asGeometryCollection():
            startPoint, endPoint = self.geometryHandler.getFirstAndLastNodeFromGeom(part)
            if flagGeom.equals(QgsGeometry.fromPointXY(startPoint)) or flagGeom.equals(QgsGeometry.fromPointXY(endPoint)):
                return True
        return False

    def runGrassDissolve(self, inputLyr, context, feedback=None, column=None, outputLyr=None, onFinish=None):
        """
        Runs dissolve from GRASS algorithm provider.
        :param inputLyr: (QgsVectorLayer) layer to be dissolved.
        :param context: (QgsProcessingContext) processing context.
        :param feedback: (QgsProcessingFeedback) QGIS object to keep track of progress/cancelling option.
        :param column: ()
        :param outputLyr: (str) URI to output layer.
        :param onFinish: (list-of-str) sequence of algs to be run after dissolve is executed, in execution order.
        :return: (QgsVectorLayer) dissolved (output) layer.
        """
        return AlgRunner().runGrassDissolve(inputLyr, context, feedback=None, column=None, outputLyr=None, onFinish=None)
    
    def getVertexNearEdgeDict(self, inputLyr, tol, onlySelected=False, feedback=None, context=None):
        """
        Identifies vertexes that are too close to a vertex.
        :param inputLyr: (QgsVectorLayer) layer to run the identification.
        :param onlySelected: (Boolean) If true, gets only selected layer
        :param tol: (float) search radius
        :param feedback (QgsProcessingFeedback) QGIS object to keep track of progress/cancelling option.
        """
        if inputLyr.geometryType() == QgsWkbTypes.PointGeometry:
            raise Exception('Vertex near edge not defined for point geometry') 
        algRunner = AlgRunner()
        context = dataobjects.createContext(feedback=feedback) if context is None else context
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr('Creating index'))
        usedInput = inputLyr if not onlySelected else QgsProcessingFeatureSourceDefinition(inputLyr.id(), True)
        incrementedLayer = algRunner.runAddAutoIncrementalField(
            usedInput,
            context,
            feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr('Building auxiliar search structures'))
        edgeSpatialIdx, edgeIdDict = self.buildEdgesAuxStructure(
            incrementedLayer,
            feedback=multiStepFeedback,
            algRunner=algRunner
        )
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr('Getting flags'))
        vertexNearEdgeFlagDict = self.getVertexNearEdgeFlagDict(
            incrementedLayer,
            edgeSpatialIdx,
            edgeIdDict,
            tol,
            feedback=multiStepFeedback,
            algRunner=algRunner
        )
        return vertexNearEdgeFlagDict

    def buildEdgesAuxStructure(self, inputLyr, algRunner=None, feedback=None, context=None):
        """
        returns a spatialIndex of lines and a dict of the features
        :param inputLyr: (QgsVectorLayer) layer to run build the aux structure.
        :param feedback (QgsProcessingFeedback) QGIS object to keep track of progress/cancelling option.
        """
        nSteps = 3 if inputLyr.geometryType() == QgsWkbTypes.PolygonGeometry else 2
        algRunner = AlgRunner() if algRunner is None else algRunner
        context = dataobjects.createContext(feedback=feedback) if context is None else context
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        edgeLyr = inputLyr if inputLyr.geometryType() == QgsWkbTypes.LineGeometry \
            else algRunner.runPolygonsToLines(
                    inputLyr,
                    context,
                    feedback=multiStepFeedback
                )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        explodedEdges = algRunner.runExplodeLines(
            edgeLyr,
            context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        spatialIdx, idDict = self.buildSpatialIndexAndIdDict(
            explodedEdges,
            feedback=multiStepFeedback
        )
        return spatialIdx, idDict

    def getVertexNearEdgeFlagDict(self, inputLyr, edgeSpatialIdx, edgeIdDict, searchRadius, feedback=None, algRunner=None, context=None):
        """
        returns a dict in the following format:
            {'featid':{
                'vertexWkt': {
                    'flagGeom' : --geometry of the flag--,
                    'edges' : set of edges (QgsGeometry)
                }

            }
            } 
        :param inputLyr: (QgsVectorLayer) layer to run build the aux structure.
        :param edgeSpatialIdx: (QgsSpatialIndex) spatial index to perform the search
        :param edgeIdDict: (dict) dictionary in the format {featid:QgsFeature}
        :param searchRadius: (float) search radius
        :param feedback (QgsProcessingFeedback) QGIS object to keep track of progress/cancelling option.
        """
        flagDict = defaultdict(lambda :defaultdict(lambda : {'edges': set()}) )
        algRunner = AlgRunner() if algRunner is None else algRunner
        context = dataobjects.createContext(feedback=feedback) if context is None else context
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        # step 1: extract vertexes
        multiStepFeedback.setCurrentStep(0)
        vertexLyr = algRunner.runExtractVertices(
            inputLyr,
            context,
            feedback=multiStepFeedback
        )
        # step 2: for each vertex, get the buffer, the buffer BoundingBox and 
        # assess wich edge intersects the buffer. If there is any, this is a flag
        multiStepFeedback.setCurrentStep(1)
        iterator, size = self.getFeatureList(vertexLyr, returnIterator=True, onlySelected=False)
        if size == 0:
            return {}
        stepSize = 100/size
        for current, pointFeat in enumerate(iterator):
            if multiStepFeedback.isCanceled():
                break
            pointGeom = pointFeat.geometry()
            buffer = pointGeom.buffer(searchRadius, -1)
            bufferBB = buffer.boundingBox()
            featId = pointFeat['featid']
            #pointWkt is used as a key because it is unique and hashable
            pointWkt = pointGeom.asWkt()
            for candidateId in edgeSpatialIdx.intersects(bufferBB):
                if multiStepFeedback.isCanceled():
                    break
                edgeGeom = edgeIdDict[candidateId].geometry()
                #must maintain search within the same feature and 
                # must be with not adjacent edges
                if pointGeom.touches(edgeGeom):
                    continue
                if buffer.intersects(edgeGeom):
                    flagDict[featId][pointWkt]['flagGeom'] = pointGeom
                    flagDict[featId][pointWkt]['edges'].add(edgeGeom)
            #make progress
            multiStepFeedback.setProgress(current * stepSize)
        return flagDict
