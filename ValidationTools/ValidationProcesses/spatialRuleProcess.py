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
    predicates = {'equal':'ST_Equals',
                  'disjoint':'ST_Disjoint',
                  'intersect':'ST_Intersects',
                  'touch':'ST_Touches',
                  'cross':'ST_Crosses',
                  'within':'ST_Within',
                  'overlap':'ST_Overlaps',
                  'contains':'ST_Contains',
                  'cover':'ST_Covers',
                  'covered by':'ST_CoveredBy'}
    
    necessity = {'must (be)':'\'f\'',
                 'must not (be)':'\'t\''}
    
    def __init__(self, postgisDb):
        super(self.__class__,self).__init__(postgisDb)
        
        self.rulesFile = os.path.join(os.path.dirname(__file__), '..', 'ValidationRules', 'ruleLibrary.rul')
        
    def getRules(self):
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
            ret.append((layer1, necessity, predicate, layer2))
            
        return ret

    def execute(self):
        #abstract method. MUST be reimplemented.
        QgsMessageLog.logMessage('Starting '+self.getName()+'Process.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName())
            
            rules = self.getRules()
            for rule in rules:
                invalidGeomRecordList = self.abstractDb.testSpatialRule(rule[0], rule[1], rule[2], rule[3])
                
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return

        if len(invalidGeomRecordList) > 0:
            numberOfInvGeom = self.addFlag(invalidGeomRecordList)
            for tuple in invalidGeomRecordList:
                self.addClassesToBeDisplayedList(tuple[0])        
            self.setStatus('%s features are invalid. Check flags.\n' % numberOfInvGeom, 4) #Finished with flags
            QgsMessageLog.logMessage('%s features are invalid. Check flags.\n' % numberOfInvGeom, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return
        else:
            self.setStatus('All features are valid.\n', 1) #Finished
            QgsMessageLog.logMessage('All features are valid.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)