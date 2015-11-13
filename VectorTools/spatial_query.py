# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-11-10
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
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
import os

from qgis.core import QgsFeatureRequest, QgsVectorLayer, QgsGeometry, QGis

class SpatialQuery():
    def __init__(self, referenceLayer, attribute):
        self.reference = referenceLayer
        self.attribute = attribute
        
        self.populateIndex()
        
    def populateIndex(self):
        #spatial index
        self.index = QgsSpatialIndex()
        for feat in self.reference.getFeatures():
            self.index.insertFeature(feat)
            
    def getCandidates(self, bbox):
        ids = self.index.intersects(bbox)
        candidates = []
        for id in ids:
            candidates.append(self.reference.getFeatures(QgsFeatureRequest().setFilterFid(id)).next())
        return candidates            
            
    def makeQuery(self, geom):
        ret = []
        
        rect = geom.boundingBox()
        candidates = self.getCandidates(rect)
        for candidate in candidates:
            featGeom = candidate.geometry()
            if featGeom.intersects(geom):
                ret.append(candidate)
                
        return ret
    
    def getKey(self, item):
        return item[0]
                
    def sortFeatures(self, geom, features):
        distances = []
        
        firstPoint = geom.asPolyline()[0]
        pointGeom = QgsGeometry.fromPoint(firstPoint)
        for intersected in features:
            intersection = geom.intersection(intersected.geometry())
            if intersection.type() == QGis.Point:
                distance = intersection.distance(pointGeom)
                distances.append((distance, intersected))
        
        ordered = sorted(distances, key=self.getKey)
        return ordered
    
    def assignValues(self, pace, ordered):
        first = ordered[0][1]
        first_value = first.attribute(self.attribute)
        fieldIndex = [i for i in range(len(self.reference.dataProvider().fields())) if self.reference.dataProvider().fields()[i].name() == self.attribute]
        
        if not self.reference.isEditable():
            return False
        else:
            self.reference.startEditing()
        for i in range(1, len(ordered)):
            value = first_value + pace*i
            feature = ordered[i][1]
            #feature id that will be updated
            id = feature.id()
            #attribute pair that will be changed
            attrs = {fieldIndex[0]:value}
            #actual update in the database
            self.reference.dataProvider().changeAttributeValues({id:attrs})
            
        return self.reference.commitChanges()