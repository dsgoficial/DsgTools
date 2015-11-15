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

from qgis.core import QgsFeatureRequest, QgsGeometry, QGis, QgsSpatialIndex, QgsCoordinateTransform

class ContourTool():
    def updateReference(self, referenceLayer):
        self.reference = referenceLayer
        self.populateIndex()

    def populateIndex(self):
        #spatial index
        self.index = QgsSpatialIndex()
        for feat in self.reference.getFeatures():
            self.index.insertFeature(feat)
            
    def getCandidates(self, bbox):
        #features that might satisfy the query
        ids = self.index.intersects(bbox)
        candidates = []
        for id in ids:
            candidates.append(self.reference.getFeatures(QgsFeatureRequest().setFilterFid(id)).next())
        return candidates            
            
    def getFeatures(self, geom):
        #features that satisfy the query
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
        #sorting by distance
        distances = []
        
        firstPoint = geom.asPolyline()[0]
        pointGeom = QgsGeometry.fromPoint(firstPoint)

        for intersected in features:
            intersection = geom.intersection(intersected.geometry())
            if intersection.type() == QGis.Point:
                distance = intersection.distance(pointGeom)
                distances.append((distance, intersected))
        
        ordered = sorted(distances, key=self.getKey)
        #returning a list of tuples (distance, feature)
        return ordered

    def reproject(self, geom, canvasCrs):
        destCrs = self.reference.crs()
        if canvasCrs.authid() != destCrs.authid():
            coordinateTransformer = QgsCoordinateTransform(canvasCrs, destCrs)
            geom.transform(coordinateTransformer)
    
    def assignValues(self, attribute, pace, geom, canvasCrs):
        self.reproject(geom, canvasCrs)
        features = self.getFeatures(geom)
        ordered = self.sortFeatures(geom, features)

        #the first feature must have the initial value already assigned
        first_feature = ordered[0][1]
        #getting the initial value
        first_value = first_feature.attribute(attribute)

        #getting the filed index that must be updated
        fieldIndex = [i for i in range(len(self.reference.dataProvider().fields())) if self.reference.dataProvider().fields()[i].name() == attribute]


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