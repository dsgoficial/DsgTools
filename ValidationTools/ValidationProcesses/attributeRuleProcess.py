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
from collections import deque

from PyQt4 import QtGui

from qgis.core import QgsMessageLog, QgsDataSourceURI

from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

class AttributeRuleProcess(ValidationProcess):
    
    def __init__(self, postgisDb, iface, instantiating=False, withElements = True):
        """
        Constructor
        """
        super(AttributeRuleProcess, self).__init__(postgisDb, iface, instantiating, withElements)
        
        self.processAlias = self.tr('Attribute Rule Checker')
        if not instantiating:
            self.propertyDict = self.postgisDb.getPropertyDict('AttributeRules')
            self.parameters = {'Rules Setting': deque(self.propertyDict.keys())}

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        self.startTimeCount()
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName())
            selectedRuleDict = self.parameters['Rules Setting']

            if len(invalidGeomRecordList) > 0:
                numberOfInvGeom = self.addFlag(invalidGeomRecordList)
                for tuple in invalidGeomRecordList:
                    self.addClassesToBeDisplayedList(tuple[0])
                msg = str(numberOfInvGeom) + self.tr(' features are invalid. Check flags.')
                self.setStatus(msg, 4) #Finished with flags
            else:
                msg = self.tr('All features are valid.')
                self.setStatus(msg, 1) #Finished
            return 1             
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0

