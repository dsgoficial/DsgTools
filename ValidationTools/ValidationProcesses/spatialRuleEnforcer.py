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
import os

from PyQt4 import QtGui

from qgis.core import QgsMessageLog, QgsDataSourceURI

from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess

class SpatialRuleEnforcer(ValidationProcess):
    predicates = {'equal':'ST_Equals',
                  'disjoint':'ST_Disjoint',
                  'intersect':'ST_Intersects',
                  'touch':'ST_Touches',
                  'cross':'ST_Crosses',
                  'within':'ST_Within',
                  'overlap':'ST_Overlaps',
                  'contain':'ST_Contains',
                  'cover':'ST_Covers',
                  'covered by':'ST_CoveredBy'}
    
    necessity = {'must (be)':'\'f\'',
                 'must not (be)':'\'t\''}
    
    def __init__(self, postgisDb, codelist):
        super(self.__class__,self).__init__(postgisDb, codelist)
        
        self.rulesFile = os.path.join(os.path.dirname(__file__), '..', 'ValidationRules', 'ruleLibrary.rul')
        
    def connectEditingSignals(self, iface):
        for layer in iface.mapCanvas().layers():
            layer.geometryChanged.connect(self.enforceSpatialRulesForChanges)
            layer.featureAdded.connect(self.enforceSpatialRulesForAddition)
            layer.featureDeleted.connect(self.enforceSpatialRulesForDeletion)

    def disconnectEditingSignals(self, iface):
        for layer in iface.mapCanvas().layers():
            layer.geometryChanged.disconnect(self.enforceSpatialRulesForChanges)
            layer.featureAdded.disconnect(self.enforceSpatialRulesForAddition)
            layer.featureDeleted.disconnect(self.enforceSpatialRulesForDeletion)
            
    def enforceSpatialRulesForChanges(self):
        layer = self.sender()
        uri = layer.dataProvider().dataSourceUri()
        dsUri = QgsDataSourceURI(uri)
        name = '.'.join([dsUri.schema(), dsUri.table()])
        rules = self.getRules(name)
        print rules

    def enforceSpatialRulesForAddition(self):
        layer = self.sender()
        print layer.name()
    
    def enforceSpatialRulesForDeletion(self):
        layer = self.sender()
        print layer.name()
    
    def enforceSpatialRulesForMultipleDeletion(self):
        layer = self.sender()
        print layer.name()
        
    def getRules(self, layerName):
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
