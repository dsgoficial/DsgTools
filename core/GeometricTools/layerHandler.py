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
                      QgsCoordinateTransform, QgsWkbTypes, edit, QgsCoordinateReferenceSystem, QgsProject
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
            size = len(featureList)
        else:
            featureList = lyr.getFeatures() if returnIterator else [i for i in lyr.getFeatures()]
            size = len(lyr.allFeatureIds())
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
    

    def getUnifiedLayerFeatures(self, unifiedLyr, layerList, attributeTupple = False, attributeBlackList = '', onlySelected = False, parameterDict = {}, feedback = None, progressDelta = 100):
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
    
    def buildInputDict(self, inpytLyr, pk = None, feedback = None, progressDelta = 100):
        """
        Maps inputLyr into a dict with its attributes.
        """
        inputDict = dict()
        request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
        currentProgress = feedback.progress() if feedback else None
        localTotal = progressDelta/inpytLyr.featureCount() if inpytLyr.featureCount() else 0
        for current, feature in enumerate(inpytLyr.getFeatures(request)):
            if feedback:
                if feedback.isCanceled():
                    break            
            key = feature[pk] if pk else feature.id()
            inputDict[key] = dict()
            inputDict[key]['featList'] = []
            inputDict[key]['featWithoutGeom'] = feature
            if feedback:
                feedback.setProgress(currentProgress + int(localTotal*current))
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
                feedback.setProgress(currentProgress + int(localTotal*current))
    
    def updateOriginalLayer(self, originalLayer, resultLayer, field=None, feedback = None, progressDelta = 100, keepFeatures = False):
        #1- build inputDict structure to store the original state of the layer
        inputDict = self.buildInputDict(originalLayer, pk = field, feedback = feedback, progressDelta = progressDelta/5) 
        #2- populate the inputDict with the features from the resultLayer
        self.populateInputDictFeatList(resultLayer, inputDict, pk=field, feedback = feedback, progressDelta = progressDelta/5)
        #3- get information from originalLayer and resultLayer
        parameterDict = self.getDestinationParameters(originalLayer)
        coordinateTransformer = self.getCoordinateTransformer(resultLayer, originalLayer)
        #4- run update original layer
        self.updateOriginalLayerFeatures(originalLayer, inputDict, parameterDict = parameterDict, coordinateTransformer = coordinateTransformer, keepFeatures = keepFeatures, feedback = feedback, progressDelta = 3*progressDelta/5)

    def updateOriginalLayersFromUnifiedLayer(self, lyrList, unifiedLyr, feedback = None, progressDelta = 100):
        lenList = len(lyrList)
        parameterDict = self.getDestinationParameters(unifiedLyr)
        for lyr in lyrList:
            inputDict = self.buildInputDict(lyr)
            request = QgsFeatureRequest(QgsExpression("layer = '{0}'".format(lyr.name())))
            self.populateInputDictFeatList(unifiedLyr, inputDict, pk = 'featid', request = request, feedback=feedback, progressDelta=progressDelta/(2*lenList))
            coordinateTransformer = self.getCoordinateTransformer(unifiedLyr, lyr)
            self.updateOriginalLayerFeatures(lyr, inputDict, parameterDict = parameterDict, coordinateTransformer = coordinateTransformer, feedback=feedback, progressDelta=progressDelta/(2*lenList))
    
    def updateOriginalLayerFeatures(self, lyr, inputDict, parameterDict = {}, coordinateTransformer = None, keepFeatures = False, feedback = None, progressDelta = 100):
        """
        Updates lyr using inputDict
        """
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
            for feat in outFeats:
                geomToUpdate, addedFeatures, deleteId = self.featureHandler.handleFeature(feat.geometry(), \
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
