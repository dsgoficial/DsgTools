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
    predicates = {0:'equals',
                  1:'disjoint',
                  2:'intersects',
                  3:'touches',
                  4:'crosses',
                  5:'within',
                  6:'overlaps',
                  7:'contains',
                  8:'overlaps',#we still must check what to do here
                  9:'overlaps'}#we still must check what to do here
    
    #we must check is this is violated to raise flags, hence the opposite idea
    necessity = {0:True,
                 1:False}
    
    def __init__(self, postgisDb, codelist, iface):
        super(self.__class__,self).__init__(postgisDb, codelist)
        self.iface = iface
        self.rulesFile = os.path.join(os.path.dirname(__file__), '..', 'ValidationRules', 'ruleLibrary.rul')
        self.flags = {}
        
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
        predicate = rule[2] #spatial predicate
        layer2 = rule[3] #layer used to test the rule
        min_card = rule[4] #minimum cardinality
        max_card = rule[5] #maximum cardinality
        rule = rule[6] #rule string

        vectorlayer2 = self.getLayer(layer2.split('.')[-1]) #correspondent QgsVectorLayer
        
        method = getattr(geometry, predicate) #getting the correspondent QgsGeometry method to be used in the rule

        occurrences = 0 #number of times the rule checks out
        flagData = []
        #querying the features that intersect the geometry's bounding box
        for feature in vectorlayer2.dataProvider().getFeatures(QgsFeatureRequest(geometry.boundingBox())):
            if layer1 == layer2 and featureId == feature['id']:
                continue
            #for each one of them we must execute the method
            if method(feature.geometry()) == necessity:
                #when this happens the rule is checked, but we still need to check the cardinality
                occurrences += 1
            else:
                #when this happens the rule is broken and we need to get the geometry of the actual problem
                #geom must be the intersection
                geom = geometry.intersection(feature.geometry())
                #case the intersection is WKBUnknown or  WKBNoGeometry, we should use the original geometry
                if geom.wkbType() in [0,7]:
                    geom = geometry
                #hex geometry to be added as flag
                hexa = binascii.hexlify(geom.asWkb())
                #storing the geometry that represents the rule violation
                flagData.append(hexa)

        # lets define when we should raise a flag:
        # no occurrences or number of occurrences out of bounds.
        # We must stay like this: min_card <= occurrences <= max_card
        # there is the particular case when max_card = *, in this case we must stay like this: min_card <= occurrences
        # so, we can summarize like this:
        if max_card != '*':
            breaksCardinality = occurrences < int(min_card) or occurrences > int(max_card)
        else:
            breaksCardinality = occurrences < int(min_card)

        if len(flagData) == 0:
            breaksPredicate = False
        else:
            breaksPredicate = True

        if breaksCardinality:
            #making the reason
            reason = self.tr('Feature id ') + str(featureId) + self.tr(' from ') + layer1 + self.tr(" violates cardinality ")
            reason += min_card + '..' + max_card + self.tr(' of rule: ') + rule + ' ' + layer2
            #creating the flag
            flagTuple = (layer1, str(featureId), reason)
            #hex geometry to be added as flag
            hexa = binascii.hexlify(geometry.asWkb())
            self.createFlag(layer1, featureId, reason, hexa)

        if breaksPredicate:
            #making the reason
            reason = self.tr('Feature id ') + str(featureId) + self.tr(' from ') + layer1 + self.tr(' violates rule: ') + rule + ' ' + layer2
            for hexa in flagData:
                self.createFlag(layer1, featureId, reason, hexa)

    def createFlag(self, layer1, featureId, reason, hexa):
        '''
        Makes a flag and checks if it needs to be updated
        layer1: Layer name
        featureId: Id of the feature that violates the rule
        reason: Reason for which the rule was broken
        hexa: WKB geometry to be passed to the flag
        '''
        #creating the flag
        flagTuple = (layer1, str(featureId), reason)
        if flagTuple not in self.flags.keys():#if the flag is not already set we must set it and insert it into the DB
            self.flags[flagTuple] = True
            #adding the flag individually
            self.addFlag([(layer1, str(featureId), reason, hexa)])
        else:
            #removing the old flag and inserting a new one adjusted
            self.updateFlag((layer1, str(featureId), reason, hexa))

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
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Problem reading file!'))
            return
        
        ret = list()
        for line in rules:
            split = line.split(',')
            layer1 = split[0]    
            necessity = self.necessity[int(split[1].split('_')[0])]
            predicate = self.predicates[int(split[2].split('_')[0])]
            layer2 = split[3]
            cardinality = split[4]
            min_card = cardinality.split('..')[0]
            max_card = cardinality.split('..')[1]
            rule = split[1]+' '+split[2]
            if layer1 == layerName:
                ret.append((layer1, necessity, predicate, layer2, min_card, max_card, rule))
            
        return ret
