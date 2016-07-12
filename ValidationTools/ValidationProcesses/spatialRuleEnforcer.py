# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2016-07-11
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
import os, binascii

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot, pyqtSignal

from qgis.core import QgsMessageLog, QgsDataSourceURI, QgsGeometry, QgsFeatureRequest, QgsVectorLayerEditBuffer

from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess

class SpatialRuleEnforcer(ValidationProcess):
    #this relates the predicate with the methods present in the QgsGeometry class
    predicates = {'equal':'equals',
                  'disjoint':'disjoint',
                  'intersect':'intersects',
                  'touch':'touches',
                  'cross':'crosses',
                  'within':'within',
                  'overlap':'overlaps',
                  'contain':'contains',
                  'cover':'overlaps',#we still must check what to do here
                  'covered by':'overlaps'}#we still must check what to do here
    
    #we must check is this is violated to raise flags, hence the opposite idea
    necessity = {'must (be)':False,
                 'must not (be)':True}
    
    def __init__(self, postgisDb, codelist, iface):
        super(self.__class__,self).__init__(postgisDb, codelist)
        self.iface = iface
        self.rulesFile = os.path.join(os.path.dirname(__file__), '..', 'ValidationRules', 'ruleLibrary.rul')
        
    def connectEditingSignals(self):
        '''
        Connects all editing signals when the rule enforcer is turned on
        '''
        self.abstractDb.deleteProcessFlags(self.getName()) #deleting old flags when we start the watch dog again
        for layer in self.iface.mapCanvas().layers():
            layer.geometryChanged.connect(self.enforceSpatialRulesForChanges)
            layer.featureAdded.connect(self.enforceSpatialRulesForAddition)

    def disconnectEditingSignals(self):
        '''
        Disconnects all editing signals when the rule enforcer is turned off
        '''
        for layer in self.iface.mapCanvas().layers():
            layer.geometryChanged.disconnect(self.enforceSpatialRulesForChanges)
            layer.featureAdded.disconnect(self.enforceSpatialRulesForAddition)
            
    def getFullLayerName(self, sender):
        '''
        Gets the layer name as present in the rules
        '''
        uri = sender.dataProvider().dataSourceUri()
        dsUri = QgsDataSourceURI(uri)
        name = '.'.join([dsUri.schema(), dsUri.table()])
        return name
    
    def getLayer(self, layername):
        '''
        Gets the QgsVectorLayer involved in the rule that is about to be tested
        '''
        for layer in self.iface.mapCanvas().layers():
            if layer.name() == layername:
                return layer
            
    def testRule(self, rule, featureId, geometry):
        '''
        Tests the rule against the geometry passed as parameter
        '''
        layer1 = rule[0] #layer that defines the rule
        necessity = rule[1] #rule necessity
        predicate = rule[2]
        layer2 = rule[3] #layer used to test the rule
        rule = rule[6]
        
        vectorlayer2 = self.getLayer(layer2.split('.')[-1]) #correspondent QgsVectorLayer
        
        method = getattr(geometry, predicate) #getting the correspondent QgsGeometry method to be used in the rule

        #querying the features that intersect the geometry's bounding box
        for feature in vectorlayer2.dataProvider().getFeatures(QgsFeatureRequest(geometry.boundingBox())):
            if layer1 == layer2 and featureId == feature['id']:
                continue
            #for each one of them we must execute the method
            if method(feature.geometry()) == necessity:
                #making the reason
                reason = 'Feature id %s from %s violates rule %s %s' % (str(featureId), layer1, rule, layer2)
                #geom must be the intersection
                geom = geometry.intersection(feature.geometry())
                #case the intersection in None, we should use the original geometry
                if not geom:
                    geom = geometry
                #creating the flag
                flagTuple = (layer1, str(featureId), reason, binascii.hexlify(geom.asWkb()))
                #adding the flag individually
                self.addFlag([flagTuple])
      
    @pyqtSlot(int, QgsGeometry)      
    def enforceSpatialRulesForChanges(self, featureId, geometry):
        '''
        Slot that is activated when a feature is modified by the user
        '''
        #layer that sent the signal
        layer = self.sender()
        #layer name as present in the rules
        layername = self.getFullLayerName(layer)
        #rules involving the layer
        rules = self.getRules(layername)
        # for each rule we must test what is happening
        for rule in rules:
            self.testRule(rule, featureId, geometry) #actual test

    @pyqtSlot(int)      
    def enforceSpatialRulesForAddition(self, featureId):
        '''
        Slot that is activated when a feature is added by the user
        '''
        #layer that sent the signal
        layer = self.sender()
        #layer name as present in the rules
        layername = self.getFullLayerName(layer)
        #rules involving the layer
        rules = self.getRules(layername)
        # for each rule we must test what is happening
        features = layer.editBuffer().addedFeatures()
        for key in features.keys():
            #just checking the newly added feature, the other were already tested
            if key != featureId:
                continue
            for rule in rules:
                self.testRule(rule, featureId, features[featureId].geometry()) #actual test
                
    def getRules(self, layerName):
        '''
        Get a list of tuples (rules) using the configuration file
        '''
        try:
            with open(self.rulesFile, 'r') as f:
                rules = [line.rstrip('\n') for line in f]
        except Exception as e:
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Problem reading file! \n'))
            return
        
        ret = list()
        for line in rules:
            split = line.split(',')
            layer1 = split[0]    
            necessity = self.necessity[split[1]]
            predicate = self.predicates[split[2]]
            layer2 = split[3]
            cardinality = split[4]
            min_card = cardinality.split('..')[0]
            max_card = cardinality.split('..')[1]
            rule = split[1]+' '+split[2]
            if layer1 == layerName or layer2 == layerName:
                ret.append((layer1, necessity, predicate, layer2, min_card, max_card, rule))
            
        return ret
