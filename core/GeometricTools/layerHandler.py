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
        if onlySelected:
            featureList = lyr.getSelectedFeatures()
            size = len(featureList)
        else:
            featureList = [i for i in lyr.getFeatures()] if not returnIterator else lyr.getFeatures()
            size = len(lyr.allFeatureIds())
        if returnIterator:
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
        parameterDict = dict()
        parameterDict['geomType'] = destinationLayer.geometryType()
        parameterDict['hasMValues'] =  QgsWkbTypes.hasM(int(destinationLayer.wkbType()))    #generic check (not every database is implemented as ours)
        parameterDict['hasZValues'] =  QgsWkbTypes.hasZ(int(destinationLayer.wkbType()))    #
        parameterDict['isMulti'] = QgsWkbTypes.isMultiType(int(destinationLayer.wkbType()))
        return parameterDict
    
    def getCoordinateTransformer(self, inputLyr, outputLyr):
        inputAuthId = inputLyr.crs().authid()
        outputAuthId = outputLyr.crs().authid()
        if inputAuthId == outputAuthId:
            return None
        inputSrc = QgsCoordinateReferenceSystem(inputAuthId)
        outputSrc = QgsCoordinateReferenceSystem(outputAuthId)
        coordinateTransformer = QgsCoordinateTransform(inputSrc, outputSrc, QgsProject.instance())
        return coordinateTransformer
    
    def createUnifiedVectorLayer(self, geomType, srid, attributeTupple = False):
        """
        Creates a unified vector layer for validation purposes.
        """
        fields = self.getUnifiedVectorFields(attributeTupple=attributeTupple)
        lyrUri = "{0}?crs=epsg:{1}".format(self.getGeometryTypeText(geomtype),srid)
        lyr = QgsVectorLayer(lyrUri, "unified_layer", "memory")
        lyr.startEditing()
        fields = self.getUnifiedVectorFields(attributeTupple=attributeTupple)
        provider.addAttributes(fields)
        lyr.updateFields()
        return lyr
    
    def getUnifiedVectorFields(self, attributeTupple = False):
        if not attributeTupple:
            fields = [QgsField('featid', QVariant.Int), 
                      QgsField('classname', QVariant.String)
                    ]
        else:
            fields = [QgsField('featid', QVariant.Int), 
                      QgsField('classname', QVariant.String), 
                      QgsField('tupple', QVariant.String), 
                      QgsField('blacklist', QVariant.String)
                      ]
        return fields
    
    def addFeaturesToLayer(self, lyr, featList, msg = ''):
        with edit(lyr):
            lyr.beginEditCommand(msg)
            res = lyr.addFeatures(featList)
            lyr.endEditCommand()
        return res

    def getUnifiedLayerFeatures(self, unifiedLyr, layerList, attributeTupple = False, attributeBlackList = '', onlySelected = False, parameterDict = {}):
        featList = []
        for layer in layerList:
            # recording class name
            classname = layer.name()
            iterator, total = self.getIteratorAndFeatureCount(layer, onlySelected=onlySelected)
            for feature in iterator:
                newFeat = self.createUnifiedFeature(unifiedLyr, feature, classname, bList=)
                featlist.append(newfeat)
        return featList
    
    def createAndPopulateUnifiedVectorLayer(self, layerList, geomType, epsg, attributeTupple = False, attributeBlackList = '', onlySelected = False):
        unified_layer = self.createUnifiedVectorLayer(geomType, epsg, attributeTupple = attributeTupple)
        parameterDict = self.getDestinationParameters(unified_layer)
        featList = self.getUnifiedLayerFeatures(unified_layer, layerList, attributeTupple=attributeTupple, attributeBlackList=attributeBlackList, onlySelected=onlySelected, parameterDict=parameterDict)
        self.addFeaturesToLayer(unified_layer, featList, msg='Populating unified layer')




