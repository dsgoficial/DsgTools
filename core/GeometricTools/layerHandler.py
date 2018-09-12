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
from builtins import range
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsGeometry, QgsField, QgsVectorDataProvider, \
                      QgsFeatureRequest, QgsExpression, QgsFeature, QgsSpatialIndex, Qgis, \
                      QgsCoordinateTransform, QgsWkbTypes, edit, QgsCoordinateReferenceSystem, QgsProject, \
                      QgsProcessingMultiStepFeedback
from qgis.PyQt.Qt import QObject, QVariant

from .featureHandler import FeatureHandler

class LayerHandler(QObject):
    def __init__(self, iface = None, parent = None):
        super(LayerHandler, self).__init__()
        self.parent = parent
        self.iface = iface
        if iface:
            self.canvas = iface.mapCanvas()
        self.featureHandler = FeatureHandler(iface)
    
    def getFeatureList(self, lyr, onlySelected = False, returnIterator = True, returnSize = True):
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
        for lyr, featureList in selectedDict.items():
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
    
    def createAndPopulateUnifiedVectorLayer(self, layerList, geomType = None, epsg = None, attributeTupple = False, attributeBlackList = '', onlySelected = False, feedback = None, progressDelta = 100):
        if not epsg:
            epsg = layerList[0].crs().authid().split(':')[-1]
        if not geomType:
            geomType = layerList[0].geometryType()
        unified_layer = self.createUnifiedVectorLayer(geomType, epsg, \
                                                      attributeTupple = attributeTupple)
        parameterDict = self.getDestinationParameters(unified_layer)
        featList = self.getUnifiedLayerFeatures(unified_layer, layerList, \
                                                      attributeTupple=attributeTupple, \
                                                      attributeBlackList=attributeBlackList, \
                                                      onlySelected=onlySelected, \
                                                      parameterDict=parameterDict, \
                                                      feedback = feedback, \
                                                      progressDelta = progressDelta)
        self.addFeaturesToLayer(unified_layer, featList, msg='Populating unified layer')
        return unified_layer

    def createUnifiedVectorLayer(self, geomType, srid, attributeTupple = False):
        """
        Creates a unified vector layer for validation purposes.
        """
        fields = self.getUnifiedVectorFields(attributeTupple=attributeTupple)
        lyrUri = "{0}?crs=epsg:{1}".format(QgsWkbTypes.displayString(geomType),srid)
        lyr = QgsVectorLayer(lyrUri, "unified_layer", "memory")
        lyr.startEditing()
        fields = self.getUnifiedVectorFields(attributeTupple=attributeTupple)
        lyr.dataProvider().addAttributes(fields)
        lyr.updateFields()
        return lyr
    
    def getUnifiedVectorFields(self, attributeTupple = False):
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
    

    def getUnifiedLayerFeatures(self, unifiedLyr, layerList, attributeTupple = False, attributeBlackList = '', onlySelected = False, parameterDict = None, feedback = None, progressDelta = 100):
        parameterDict = {} if parameterDict is None else parameterDict
        featList = []
        blackList = attributeBlackList.split(',') if ',' in attributeBlackList else []
        if feedback:
            currentValue = feedback.progress()
            totalFeatures = sum([lyr.featureCount() for lyr in layerList])
            currentTotal = progressDelta/totalFeatures if totalFeatures else 0
        for layer in layerList:
            # recording class name
            layername = layer.name()
            coordinateTransformer = self.getCoordinateTransformer(unifiedLyr, layer)
            iterator = self.getFeatureList(layer, onlySelected=onlySelected, returnSize=False)
            for current, feature in enumerate(iterator):
                newFeats = self.featureHandler.createUnifiedFeature(unifiedLyr, feature, layername,\
                                                                   bList=blackList, \
                                                                   attributeTupple=attributeTupple, \
                                                                   parameterDict=parameterDict, \
                                                                   coordinateTransformer=coordinateTransformer)
                featList += newFeats
                if feedback:
                    feedback.setProgress(currentValue + int(current*currentTotal))
        return featList

    def addFeaturesToLayer(self, lyr, featList, commitChanges = True, msg = ''):
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
    
    def buildInputDict(self, inputLyr, pk = None, feedback = None, progressDelta = 100, onlySelected = False):
        """
        Maps inputLyr into a dict with its attributes.
        """
        inputDict = dict()
        currentProgress = feedback.progress() if feedback else None
        if onlySelected:
            iterator = inputLyr.getSelectedFeatures()
            localTotal = progressDelta/inputLyr.selectedFeatureCount() if inputLyr.selectedFeatureCount() else 0
        else:
            request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
            iterator = inputLyr.getFeatures(request)
            localTotal = progressDelta/inputLyr.featureCount() if inputLyr.featureCount() else 0
        for current, feature in enumerate(iterator):
            if feedback:
                if feedback.isCanceled():
                    break            
            key = feature[pk] if pk else feature.id()
            inputDict[key] = dict()
            inputDict[key]['featList'] = []
            inputDict[key]['featWithoutGeom'] = feature
            if feedback:
                feedback.setProgress(currentProgress + (localTotal*current))
        return inputDict
    
    def populateInputDictFeatList(self, lyr, inputDict, pk = None, request = None, feedback = None, progressDelta = 100):
        iterator = lyr.getFeatures(request) if request else lyr.getFeatures()
        currentProgress = feedback.progress() if feedback else None
        localTotal = progressDelta/lyr.featureCount() if lyr.featureCount() else 0
        for current, feat in enumerate(iterator):
            if feedback:
                if feedback.isCanceled():
                    break  
            fid = feat[pk] if pk else feat.id()
            if fid in inputDict:
                inputDict[fid]['featList'].append(feat)
            if feedback:
                feedback.setProgress(currentProgress + (localTotal*current))

    
    def updateOriginalLayer(self, originalLayer, resultLayer, field=None, feedback = None, progressDelta = 100, keepFeatures = False, onlySelected = True):
        #1- build inputDict structure to store the original state of the layer
        inputDict = self.buildInputDict(originalLayer, pk = field, feedback = feedback, progressDelta = progressDelta/5, onlySelected = onlySelected) 
        #2- populate the inputDict with the features from the resultLayer
        self.populateInputDictFeatList(resultLayer, inputDict, pk=field, feedback = feedback, progressDelta = progressDelta/5)
        #3- get information from originalLayer and resultLayer
        parameterDict = self.getDestinationParameters(originalLayer)
        coordinateTransformer = self.getCoordinateTransformer(resultLayer, originalLayer)
        #4- run update original layer
        self.updateOriginalLayerFeatures(originalLayer, inputDict, parameterDict = parameterDict, coordinateTransformer = coordinateTransformer, keepFeatures = keepFeatures, feedback = feedback, progressDelta = 3*progressDelta/5)

    def updateOriginalLayersFromUnifiedLayer(self, lyrList, unifiedLyr, feedback = None, progressDelta = 100, onlySelected = False):
        lenList = len(lyrList)
        parameterDict = self.getDestinationParameters(unifiedLyr)
        for lyr in lyrList:
            inputDict = self.buildInputDict(lyr, onlySelected=onlySelected)
            request = QgsFeatureRequest(QgsExpression("layer = '{0}'".format(lyr.name())))
            self.populateInputDictFeatList(unifiedLyr, inputDict, pk = 'featid', request = request, feedback=feedback, progressDelta=progressDelta/(2*lenList))
            coordinateTransformer = self.getCoordinateTransformer(unifiedLyr, lyr)
            self.updateOriginalLayerFeatures(lyr, inputDict, parameterDict = parameterDict, coordinateTransformer = coordinateTransformer, feedback=feedback, progressDelta=progressDelta/(2*lenList))
    
    def updateOriginalLayerFeatures(self, lyr, inputDict, parameterDict = None, coordinateTransformer = None, keepFeatures = False, feedback = None, progressDelta = 100):
        """
        Updates lyr using inputDict
        """
        parameterDict = {} if parameterDict is None else parameterDict
        idsToRemove, featuresToAdd, idsToRemove = [], [], []
        lyr.startEditing()
        lyr.beginEditCommand('Updating layer {0}'.format(lyr.name()))
        currentProgress = feedback.progress() if feedback else None
        localTotal = progressDelta/len(inputDict)
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
                feedback.setProgress(currentProgress + int(localTotal*current))
        lyr.addFeatures(featuresToAdd)
        if not keepFeatures:
            lyr.deleteFeatures(idsToRemove)
        lyr.endEditCommand()
    
    def mergeLinesOnLayer(self, lyr, onlySelected = False, feedback = None, ignoreVirtualFields = True, attributeBlackList = None, excludePrimaryKeys = True):
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
        mergeLines = lambda x : self.featureHandler.mergeLineFeatures(featList=x[0], lyr=lyr, idsToRemove=x[1], parameterDict=parameterDict, feedback=x[2], networkDict=networkDict)

        for current, (key, featList) in enumerate(attributeFeatDict.items()):
            if feedback:
                if feedback.isCanceled():
                    break
                mergeFeedback.setCurrentStep(current)
            mergeLines([featList,idsToRemove, mergeFeedback])
        lyr.deleteFeatures(idsToRemove)
        lyr.endEditCommand()
    
    def buildAttributeFeatureDict(self, lyr, onlySelected = False, feedback = None, ignoreVirtualFields = True, attributeBlackList = None, excludePrimaryKeys = True):
        attributeBlackList = [] if attributeBlackList is None else attributeBlackList
        currentProgress = feedback.progress() if feedback else None
        iterator, size = self.getFeatureList(lyr, onlySelected=onlySelected)
        localTotal = 100/size if size != 0 else 0
        attributeFeatDict = dict()
        pkIndexes = lyr.primaryKeyAttributes() if excludePrimaryKeys else []
        typeBlackList = [6] if ignoreVirtualFields else []
        columns = [field.name() for idx, field in enumerate(lyr.fields()) if idx not in pkIndexes and field.type() not in typeBlackList and field.name() not in attributeBlackList]
        for current, feat in enumerate(iterator):
            if feedback:
                if feedback.isCanceled():
                    break
            attrKey = ','.join(['{}'.format(feat[column]) for column in columns])
            if attrKey not in attributeFeatDict:
                attributeFeatDict[attrKey] = []
            attributeFeatDict[attrKey].append(feat)
            if feedback:
                feedback.setProgress(localTotal*current)
        return attributeFeatDict
    
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

    def addFeatToDict(self, endVerticesDict, line, featid):
        self.addPointToDict(line[0], endVerticesDict, featid)
        self.addPointToDict(line[len(line) - 1], endVerticesDict, featid)
    
    def addPointToDict(self, point, pointDict, featid):
        if point not in pointDict:
            pointDict[point] = []
        pointDict[point].append(featid)
                
    def addDissolveField(self, layer, tol):
        #add temp field
        idField = QgsField('d_id',QVariant.Int)
        layer.dataProvider().addAttributes([idField])
        layer.updateFields()
        #small feature list
        smallFeatureList = []
        bigFeatureList = []
        bigFeatIndex = QgsSpatialIndex()
        for feat in layer.getFeatures():
            feat['d_id'] = feat['featid']
            if feat.geometry().area() < float(tol):
                smallFeatureList.append(feat)
            else:
                bigFeatIndex.insertFeature(feat)
                bigFeatureList.append(feat)
        
        # using spatial index to speed up the process
        for sfeat in smallFeatureList:
            candidates = bigFeatIndex.intersects(sfeat.geometry().boundingBox())
            for candidate in candidates:
                bfeat = [i for i in layer.dataProvider().getFeatures(QgsFeatureRequest(candidate))][0]
                if sfeat['d_id'] == sfeat['featid'] and sfeat.geometry().intersects(bfeat.geometry()) and sfeat['tupple'] == bfeat['tupple']:
                    sfeat['d_id'] = bfeat['featid']

        idx = layer.fieldNameIndex('tupple')
        updateDict = dict()
        for feat in smallFeatureList + bigFeatureList:
            newValue = u'{0},{1}'.format(feat['tupple'], feat['d_id'])
            updateDict[feat.id()] = {idx:newValue}
        layer.dataProvider().changeAttributeValues(updateDict)
        return layer
    
    def getCandidates(self, idx, bbox):
        return idx.intersects(bbox)