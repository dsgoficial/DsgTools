# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-03-15
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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsGeometry, QgsField, \
                      QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, \
                      QgsFeature, QgsSpatialIndex, Qgis, QgsCoordinateTransform, \
                      QgsWkbTypes
from qgis.PyQt.Qt import QObject

class AttributeHandler(QObject):
    def __init__(self, iface, parent = None):
        super(AttributeHandler, self).__init__()
        self.parent = parent
        self.iface = iface
    
    def createFeaturesWithAttributeDict(self, geomList, originalFeat, attributeDict, destinationLayer):
        """
        Creates a newFeatureList using each geom from geomList. attributeDict is used to set attributes
        """
        newFeatureList = []
        fields = destinationLayer.fields()
        for geom in geomList:
            newFeature = QgsFeature(fields)
            newFeature.setGeometry(geom)
            newFeature = self.setFeatureAttributes(newFeature, attributeDict, oldFeat = originalFeat)
            newFeatureList.append(newFeature)
        return newFeatureList

    def setFeatureAttributes(self, newFeature, attributeDict, editBuffer=None, oldFeat = None):
        """
        Changes attribute values according to the reclassification dict using the edit buffer
        newFeature: newly added
        editBuffer: layer edit buffer
        """
        #setting the attributes using the reclassification dictionary
        fields = newFeature.fields()
        for attribute in attributeDict:
            idx = fields.lookupField(attribute)
            if attribute == 'buttonProp' or idx == -1:
                continue
            #value to be changed
            reclass = attributeDict[attribute]
            if isinstance(reclass, dict):
                value = reclass['value']
                if reclass['isIgnored'] == '1': #ignore clause
                    if oldFeat:
                        value = oldFeat[attribute]
            else:
                value = reclass
            if value == '':
                continue
            #actual attribute change
            if editBuffer:
                #this way we are working with the edit buffer
                editBuffer.changeAttributeValue(newFeature.id(), idx, value)
            else:
                #this way are working with selected features and inserting a new one in the layer
                newFeature.setAttribute(idx, value)
        if not editBuffer:
            # we should return when under the normal behavior
            return newFeature
