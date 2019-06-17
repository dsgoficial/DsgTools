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
import itertools
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsGeometry, QgsField, QgsVectorDataProvider, \
                      QgsFeatureRequest, QgsExpression, QgsFeature, QgsSpatialIndex, Qgis, \
                      QgsCoordinateTransform, QgsWkbTypes, QgsProcessingMultiStepFeedback, QgsVectorLayerUtils
from qgis.PyQt.Qt import QObject, QVariant

from .geometryHandler import GeometryHandler
from .attributeHandler import AttributeHandler
from DsgTools.core.Utils.FrameTools.map_index import UtmGrid

class FeatureHandler(QObject):
    def __init__(self, iface = None, parent = None):
        super(FeatureHandler, self).__init__()
        self.parent = parent
        self.iface = iface
        if iface:
            self.canvas = iface.mapCanvas()
        self.geometryHandler = GeometryHandler(iface)
        self.attributeHandler = AttributeHandler(iface)
        self.utmGrid = UtmGrid()
        self.stepsTotal = 0
    
    def reclassifyFeatures(self, featureList, destinationLayer, reclassificationDict, coordinateTransformer, parameterDict):
        newFeatList = []
        deleteList = []
        for feat in featureList:
            geom = self.geometryHandler.reprojectWithCoordinateTransformer(feat.geometry(), coordinateTransformer)
            geomList = self.geometryHandler.adjustGeometry(geom, parameterDict)
            newFeatList += self.createFeaturesWithAttributeDict(geomList, feat, reclassificationDict, destinationLayer)
            deleteList.append(feat.id())
        return newFeatList, deleteList
    
    def createFeaturesWithAttributeDict(self, geomList, originalFeat, attributeDict, destinationLayer):
        """
        Creates a newFeatureList using each geom from geomList. attributeDict is used to set attributes
        """
        newFeatureList = []
        fields = destinationLayer.fields()
        for geom in geomList:
            newFeature = QgsFeature(fields)
            newFeature.setGeometry(geom)
            newFeature = self.attributeHandler.setFeatureAttributes(newFeature, attributeDict, oldFeat = originalFeat)
            newFeatureList.append(newFeature)
        return newFeatureList

    def createUnifiedFeature(self, unifiedLyr, feature, classname, bList = None, attributeTupple = False, coordinateTransformer = None, parameterDict = None):
        parameterDict = {} if parameterDict is None else parameterDict
        bList = [] if bList is None else bList
        newFeats = []
        for geom in self.geometryHandler.handleGeometry(feature.geometry(), parameterDict=parameterDict, coordinateTransformer=coordinateTransformer):
            newfeat = QgsFeature(unifiedLyr.fields())
            newfeat.setGeometry(feature.geometry())
            newfeat['featid'] = feature.id()
            newfeat['layer'] = classname
            if attributeTupple:
                newfeat['tupple'] = self.attributeHandler.getTuppleAttribute(feature, unifiedLyr, bList=bList)
            newFeats.append(newfeat)
        return newFeats
    
    def getNewFeatureWithoutGeom(self, referenceFeature, lyr):
        newFeat = QgsFeature(referenceFeature)
        # provider = lyr.dataProvider()
        for idx in lyr.primaryKeyAttributes():
            newFeat.setAttribute(idx, None)
        return newFeat
    
    def handleFeature(self, featList, featureWithoutGeom, lyr, parameterDict = None, coordinateTransformer = None):
        parameterDict = {} if parameterDict is None else parameterDict
        geomList = []
        for feat in featList:
            geomList += self.geometryHandler.handleGeometry(feat.geometry(), parameterDict, coordinateTransformer)
        geomToUpdate = None
        newFeatList = []
        if not geomList:
            return geomToUpdate, [], True
        for idx, geom in enumerate(geomList):
            if idx == 0:
                geomToUpdate = geom
                continue
            else:
                newFeat = self.getNewFeatureWithoutGeom(featureWithoutGeom, lyr)
                newFeat.setGeometry(geom)
                newFeatList.append(newFeat)
        return geomToUpdate, newFeatList, False

    def handleConvertedFeature(self, feat, lyr, parameterDict = None, coordinateTransformer = None):
        parameterDict = {} if parameterDict is None else parameterDict
        geomList = self.geometryHandler.handleGeometry(feat.geometry(), parameterDict, coordinateTransformer)
        newFeatSet = set()
        for geom in geomList:
            attrMap = { idx : feat[field.name()] for idx, field in enumerate(feat.fields()) if idx not in lyr.primaryKeyAttributes()}
            newFeat = QgsVectorLayerUtils.createFeature(lyr, geom, attrMap)
            newFeatSet.add(newFeat)
        return newFeatSet

    def getFeatureOuterShellAndHoles(self, feat, isMulti):
        geom = feat.geometry()
        
        outershells, donutholes = self.geometryHandler.getOuterShellAndHoles(geom, isMulti)
        outershellList = []
        for shell in outershells:
            outerShellFeat = QgsFeature(feat)
            outerShellFeat.setGeometry(shell)
            outershellList.append(outerShellFeat)

        donutHoleList = []
        for hole in donutholes:
            newFeat = QgsFeature(feat)
            newFeat.setGeometry(hole)
            donutHoleList.append(newFeat)
        return outershellList, donutHoleList
    
    def mergeLineFeatures(self, featList, lyr, idsToRemove, networkDict, parameterDict = None, feedback = None, ignoreNetwork = False):
        parameterDict = {} if parameterDict is None else parameterDict
        changeDict = dict()
        size = 100 / len(featList)
        for current, feat_a in enumerate(featList):
            if feedback:
                if feedback.isCanceled():
                    break
            id_a = feat_a.id()
            if id_a in idsToRemove:
                continue
            for feat_b in featList:
                if feedback:
                    if feedback.isCanceled():
                        break
                id_b = feat_b.id()
                if id_a == id_b or id_b in idsToRemove:
                    continue
                geom_a = feat_a.geometry()
                geom_b = feat_b.geometry()
                if geom_a.touches(geom_b):
                    intersectionPoint = geom_a.intersection(geom_b)
                    for pointPart in intersectionPoint.asGeometryCollection():
                        point = pointPart.asPoint()
                        if ignoreNetwork or (point in networkDict and len(networkDict[point]) == 2):
                            newGeom = self.geometryHandler.handleGeometry(geom_a.combine(geom_b).mergeLines(), parameterDict)[0] #only one candidate is possible because features are touching
                            feat_a.setGeometry(newGeom)
                            idsToRemove.append(id_b)
                            changeDict[id_a] = newGeom
            if feedback:
                feedback.setProgress(size*current)
        for id, geom in changeDict.items():
            lyr.changeGeometry(id, geom)
    
    def getNewGridFeat(self, index, geom, fields):
        feat = QgsFeature(fields)
        feat['inom'] = index
        feat['mi'] = self.utmGrid.get_MI_MIR_from_inom(index)
        feat.setGeometry(geom)
        return feat
    
    def getSystematicGridFeatures(self, featureList, index, stopScale, coordinateTransformer, fields, feedback=None):
        if feedback is not None and feedback.isCanceled():
            return
        scale = self.utmGrid.getScale(index)
        if (self.stepsTotal == 0):
            self.stepsTotal = self.utmGrid.computeNumberOfSteps(self.utmGrid.getScaleIdFromScale(scale), self.utmGrid.getScaleIdFromScale(stopScale))
            self.stepsDone = 0
            self.stepPerc = 100/self.stepsTotal
        if scale == stopScale:
            frameGeom = self.utmGrid.getQgsPolygonFrame(index)
            frameGeom.transform(coordinateTransformer)
            newFeat = self.getNewGridFeat(index, frameGeom, fields)
            featureList.append(newFeat)
            self.stepsDone += 1
            feedback.setProgress(self.stepPerc * self.stepsDone)
        else:
            scaleId = self.utmGrid.getScaleIdFromiNomen(index)
            sufixIterator = itertools.chain.from_iterable(self.utmGrid.scaleText[scaleId+1]) #flatten list into one single list
            for line in sufixIterator:
                if feedback is not None:
                    if feedback.isCanceled():
                        break
                inomen2 = '{oldInomem}-{newPart}'.format(oldInomem=index, newPart=line)
                self.getSystematicGridFeatures(featureList, inomen2, stopScale, coordinateTransformer, fields, feedback=feedback)

