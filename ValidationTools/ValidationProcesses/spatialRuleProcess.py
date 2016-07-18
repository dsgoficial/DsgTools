# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-09-10
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

from qgis.core import QgsMessageLog

from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess

class SpatialRuleProcess(ValidationProcess):
    #this relates the predicate with the PostGIS ST functions
    predicates = {0:'ST_Equals',
                  1:'ST_Disjoint',
                  2:'ST_Intersects',
                  3:'ST_Touches',
                  4:'ST_Crosses',
                  5:'ST_Within',
                  6:'ST_Overlaps',
                  7:'ST_Contains',
                  8:'ST_Covers',
                  9:'ST_CoveredBy'}
    
    #we must check is this is violated to raise flags, hence the opposite idea
    necessity = {0:'\'f\'',
                 1:'\'t\''}
    
    def __init__(self, postgisDb, codelist):
        super(self.__class__,self).__init__(postgisDb, codelist)
        
        self.rulesFile = os.path.join(os.path.dirname(__file__), '..', 'ValidationRules', 'ruleLibrary.rul')
        
    def getRules(self):
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
            ret.append((layer1, necessity, predicate, layer2, min_card, max_card, rule))
            
        return ret

    def execute(self):
        #abstract method. MUST be reimplemented.
        QgsMessageLog.logMessage('Starting '+self.getName()+'Process.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName())
            
            rules = self.getRules()
            for rule in rules:
                invalidGeomRecordList = self.abstractDb.testSpatialRule(rule[0], rule[1], rule[2], rule[3], rule[4], rule[5], rule[6])
                if len(invalidGeomRecordList) > 0:
                    numberOfInvGeom = self.addFlag(invalidGeomRecordList)
                    for tuple in invalidGeomRecordList:
                        self.addClassesToBeDisplayedList(tuple[0])        
                    self.setStatus('%s features are invalid. Check flags.\n' % numberOfInvGeom, 4) #Finished with flags
                    QgsMessageLog.logMessage('%s features are invalid. Check flags.\n' % numberOfInvGeom, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                else:
                    self.setStatus('All features are valid.\n', 1) #Finished
                    QgsMessageLog.logMessage('All features are valid.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)   
            return 1             
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0

