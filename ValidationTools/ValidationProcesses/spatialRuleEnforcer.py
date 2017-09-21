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
    # signal to update flags
    ruleTested = pyqtSignal()
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
    
    necessity = {0:True,
                 1:False}
    
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.iface = iface
        self.rulesFile = os.path.join(os.path.dirname(__file__), '..', 'ValidationRules', 'ruleLibrary.rul')
        self.processAlias = self.tr('Spatial Rule Enforcer')
        
    def connectEditingSignals(self):
        """
        Connects all editing signals when the rule enforcer is turned on
        """
        self.abstractDb.deleteProcessFlags(self.getName()) #deleting old flags when we start the watch dog again
        for layer in self.iface.mapCanvas().layers():
            layer.geometryChanged.connect(self.enforceSpatialRulesForChanges)
            layer.featureAdded.connect(self.enforceSpatialRulesForAddition)

    def disconnectEditingSignals(self):
        """
        Disconnects all editing signals when the rule enforcer is turned off
        """
        for layer in self.iface.mapCanvas().layers():
            layer.geometryChanged.disconnect(self.enforceSpatialRulesForChanges)
            layer.featureAdded.disconnect(self.enforceSpatialRulesForAddition)
            
    def getFullLayerName(self, sender):
        """
        Gets the layer name as present in the rules
        """
        try:
            uri = sender.dataProvider().dataSourceUri()
            dsUri = QgsDataSourceURI(uri)
            name = '.'.join([dsUri.schema(), dsUri.table()])
        except:
            name = ''
        return name
    
    def getLayer(self, layername):
        """
        Gets the QgsVectorLayer involved in the rule that is about to be tested
        """
        for layer in self.iface.mapCanvas().layers():
            if layer.name() == layername:
                return layer
            
    def testRule(self, rule, featureId, geometry):
        """
        Tests the rule against the geometry passed as parameter
        """        
        layer1 = rule[0] #layer that defines the rule
        necessity = rule[1] #rule necessity
        predicate = rule[2] #spatial predicate
        layer2 = rule[3] #layer used to test the rule
        min_card = rule[4] #minimum cardinality
        max_card = rule[5] #maximum cardinality
        rule = rule[6] #rule string

        vectorlayer2 = self.getLayer(layer2.split('.')[-1]) #correspondent QgsVectorLayer
        
        method = getattr(geometry, predicate) #getting the correspondent QgsGeometry method to be used in the rule
        
        #querying the features that intersect the geometry's bounding box (i.e. our candidates)
        candidatesIter = vectorlayer2.getFeatures(QgsFeatureRequest(geometry.boundingBox()))
        
        #first, lets separate the problem in disjoint case and not disjoint
        #case 1: disjoint
        if predicate == 'disjoint':
            disjointBroken = False
            flagData = []
            #iterating over candidates
            for feature in candidatesIter:
                #for the same layer we need to avoid to test a feature against it self
                if layer1 == layer2 and featureId == feature.id():
                    continue
                #for each one of them we must execute the method
                #for the disjoint case one fail is sufficient to raise the flag
                if method(feature.geometry()) != necessity:
                    disjointBroken = True
                    #storing the geometry that represents the rule violation
                    flagData.append(self.getGeometryProblem(geometry, feature))
            
            if disjointBroken:
                for hexa in flagData:
                    self.makeBreaksPredicateFlag(layer1, featureId, rule, layer2, hexa)
        #case 2: not disjoint             
        else:    
            #checking the rule in the case the situation above does not happen
            occurrences = 0 #number of times the rule checks out
            flagData = []
            #iterating over candidates
            for feature in candidatesIter:
                #for the same layer we need to avoid to test a feature against it self
                if layer1 == layer2 and featureId == feature.id():
                    continue
                #for each one of them we must execute the method
                if method(feature.geometry()) == necessity:
                    #when this happens the rule is checked, but we still need to check the cardinality
                    occurrences += 1
                else:
                    #storing the geometry that represents the rule violation
                    flagData.append(self.getGeometryProblem(geometry, feature))
    
            # lets define when we should raise a flag from now on:
            # occurrences out of bounds.
            # We must stay like this: min_card <= occurrences <= max_card
            # there is the particular case when max_card = *, in this case we must stay like this: min_card <= occurrences
            # so, we can summarize like this:
            
            #cardinality broken case
            if max_card != '*':
                breaksCardinality = occurrences < int(min_card) or occurrences > int(max_card)
            else:
                breaksCardinality = occurrences < int(min_card)
    
            if breaksCardinality and necessity == True:
                self.makeBreaksCardinalityFlag(layer1, featureId, rule, min_card, max_card, layer2, binascii.hexlify(geometry.asWkb()))
    
            #predicate broken case
            if len(flagData) == 0:
                breaksPredicate = False
            else:
                breaksPredicate = True
    
            #we only raise a breaksPredicate flag if flagData has elements and if occurrences = 0
            if breaksPredicate and occurrences == 0:
                for hexa in flagData:
                    self.makeBreaksPredicateFlag(layer1, featureId, rule, layer2, hexa)

        # updating flags for real time use
        self.ruleTested.emit()
                    
    def getGeometryProblem(self, geometry, feature):
        """
        Gets geometry problems.
        When this happens the rule is broken and we need to get the geometry of the actual problem.
        geometry: geometry used during edition mode
        feature: feature related to the geometry
        """
        #geom must be the intersection
        geom = geometry.intersection(feature.geometry())
        #case the intersection is WKBUnknown or WKBNoGeometry, we should use the original geometry
        if geom.wkbType() in [0,7]:
            geom = geometry
        #hex geometry to be added as flag
        hexa = binascii.hexlify(geom.asWkb())
        return hexa
                
    def makeBreaksCardinalityFlag(self, layer1, featureId, rule, min_card, max_card, layer2, hexa):
        """
        Makes a flag when the cardinality is broken
        layer1: Layer1 name
        featureId: Id of the feature that violates the rule
        rule: Rule tested
        min_card: minimum cardinality
        max_card: maximum cardinality
        layer2: Layer2 name
        hexa: WKB geometry to be passed to the flag
        """
        #making the reason
        vectorlayer1 = self.getLayer(layer1.split('.')[-1]) #correspondent QgsVectorLayer
        geometryColumn = self.getGeometryColumnFromLayer(vectorlayer1)
        reason = self.tr('Feature id {0} from {1} violates cardinality {2}..{3} of rule: {4} {5}').format(featureId, layer1, min_card, max_card, rule.decode('utf-8'), layer2)
        self.addFlag([(layer1, str(featureId), reason, hexa, geometryColumn)])
                
    def makeBreaksPredicateFlag(self, layer1, featureId, rule, layer2, hexa):
        """
        Makes a flag when the predicate is broken
        layer1: Layer1 name
        featureId: Id of the feature that violates the rule
        rule: Rule tested
        layer2: Layer2 name
        hexa: WKB geometry to be passed to the flag
        """
        #making the reason
        vectorlayer1 = self.getLayer(layer1.split('.')[-1]) #correspondent QgsVectorLayer
        geometryColumn = self.getGeometryColumnFromLayer(vectorlayer1)
        reason = self.tr('Feature id {0} from {1} violates rule: {2} {3}').format(featureId, layer1, rule.decode('utf-8'), layer2)
        self.addFlag([(layer1, str(featureId), reason, hexa, geometryColumn)])

    @pyqtSlot(int, QgsGeometry)      
    def enforceSpatialRulesForChanges(self, featureId, geometry):
        """
        Slot that is activated when a feature is modified by the user
        """
        #layer that sent the signal
        layer = self.sender()
        #layer name as present in the rules
        layername = self.getFullLayerName(layer)
        #rules involving the layer
        rules = self.getRules(layername)
        #removing old flags for this featureId
        self.removeFeatureFlags(layername, featureId)
        # for each rule we must test what is happening
        for rule in rules:
            self.testRule(rule, featureId, geometry) #actual test
        self.iface.mapCanvas().refresh()
        for lyr in self.iface.mapCanvas().layers():
            lyr.triggerRepaint()

    @pyqtSlot(int)      
    def enforceSpatialRulesForAddition(self, featureId):
        """
        Slot that is activated when a feature is added by the user
        """
        #layer that sent the signal
        layer = self.sender()
        #layer name as present in the rules
        layername = self.getFullLayerName(layer)
        #rules involving the layer
        rules = self.getRules(layername)
        #removing old flags for this featureId
        self.removeFeatureFlags(layername, featureId)
        # for each rule we must test what is happening
        features = layer.editBuffer().addedFeatures()
        for key in features.keys():
            #just checking the newly added feature, the other were already tested
            if key != featureId:
                continue
            for rule in rules:
                self.testRule(rule, featureId, features[featureId].geometry()) #actual test
        self.iface.mapCanvas().refresh()
        for lyr in self.iface.mapCanvas().layers():
            lyr.triggerRepaint()        
                
    def getRules(self, layerName):
        """
        Get a list of tuples (rules) using the configuration file
        """
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
