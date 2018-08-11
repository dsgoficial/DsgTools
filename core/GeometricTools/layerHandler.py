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
                      QgsCoordinateTransform, QgsWkbTypes, edit
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
    
    def createAndPopulateUnifiedVectorLayer(self, layerList, geomType, epsg, attributeTupple = False, attributeBlackList = '', onlySelected = False):
        unified_layer = self.createUnifiedVectorLayer(geomType, epsg, \
                                                      attributeTupple = attributeTupple)
        parameterDict = self.getDestinationParameters(unified_layer)
        featList = self.getUnifiedLayerFeatures(unified_layer, layerList, \
                                                      attributeTupple=attributeTupple, \
                                                      attributeBlackList=attributeBlackList, \
                                                      onlySelected=onlySelected, \
                                                      parameterDict=parameterDict)
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
                      QgsField('layername', QVariant.String)
                    ]
        else:
            fields = [QgsField('featid', QVariant.Int), 
                      QgsField('layername', QVariant.String), 
                      QgsField('tupple', QVariant.String), 
                      QgsField('blacklist', QVariant.String)
                      ]
        return fields
    

    def getUnifiedLayerFeatures(self, unifiedLyr, layerList, attributeTupple = False, attributeBlackList = '', onlySelected = False, parameterDict = {}):
        featList = []
        blackList = attributeBlackList.split(',') if ',' in attributeBlackList else []
        for layer in layerList:
            # recording class name
            layername = layer.name()
            coordinateTransformer = self.getCoordinateTransformer(unifiedLyr, layer)
            iterator = self.getFeatureList(layer, onlySelected=onlySelected, returnSize=False)
            for feature in iterator:
                newFeats = self.featureHandler.createUnifiedFeature(unifiedLyr, feature, layername,\
                                                                   bList=blackList, \
                                                                   attributeTupple=attributeTupple, \
                                                                   parameterDict=parameterDict, \
                                                                   coordinateTransformer=coordinateTransformer)
                featList += newFeats
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
    
    def buildInputDict(self, inpytLyr):
        """
        Maps inputLyr into a dict with its attributes.
        """
        inputDict = dict()
        request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
        for feature in inpytLyr.getFeatures(request):
            inputDict[feature.id()] = dict()
            inputDict[feature.id()]['featList'] = []
            inputDict[feature.id()]['featWithoutGeom'] = feature
        return inputDict
    
    def updateOriginalLayerFromUnifiedLayer(self, lyr, unifiedLyr):
        inputDict = self.buildInputDict(lyr)
        request = QgsFeatureRequest(QgsExpression('layername = {0}'.format(lyr.name())))
        for feat in unifiedLyr.getFeatures(request):
            fid = feat['featid']
            if fid in inputDict:
                inputDict[fid]['featList'].append(feat)
        parameterDict = self.getDestinationParameters(unifiedLyr)
        coordinateTransformer = self.getCoordinateTransformer(unifiedLyr, layer)
        self.updateOriginalLayerFeatures(lyr, inputDict, parameterDict = parameterDict, coordinateTransformer = coordinateTransformer)
    
    def updateOriginalLayerFeatures(self, lyr, inputDict, parameterDict = {}, coordinateTransformer = None):
        """
        Updates lyr using inputDict
        """
        idsToRemove, featuresToAdd, idsToRemove = [], [], []
        lyr.startEditing()
        lyr.beginEditCommand('Updating layer {0}'.format(lyr.name()))
        for id in inputDict:
            outFeats = inputDict[id]['featList']
            if len(outFeats) == 0 and id not in idsToRemove: #no output, must delete feature
                idsToRemove.append(id)
                continue
            for feat in outFeats:
                geomToUpdate, addedFeatures, deleteId = self.featureHandler.handleFeature(feat.geometry(), \
                                                                                            inputDict[id]['featWithoutGeom'], \
                                                                                            parameterDict = parameterDict, \
                                                                                            coordinateTransformer = coordinateTransformer)
                if geomToUpdate is not None:
                    lyr.changeGeometry(id, geomToUpdate) #faster according to the api
                featuresToAdd += addedFeatures
                idsToRemove += [id] if deleteId else []
        lyr.addFeatures(featuresToAdd)
        lyr.deleteFeatures(idsToRemove)
        lyr.endEditCommand()
