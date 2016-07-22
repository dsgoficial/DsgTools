# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba@dsg.eb.mil.br
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
from qgis.core import QgsMessageLog
from PyQt4.QtGui import QMessageBox
from PyQt4.Qt import QObject

class ValidationProcess(QObject):
    def __init__(self, postgisDb, codelist):
        '''
        Constructor
        '''
        super(ValidationProcess, self).__init__()
        self.abstractDb = postgisDb
        if self.getStatus() == None:
            self.setStatus('Instantianting process', 0)
        self.classesToBeDisplayedAfterProcess = []
        self.parameters = None
        self.codelist = codelist
        
    def setParameters(self, params):
        '''
        Define the process parameteres
        '''
        self.parameters = params

    def execute(self):
        '''
        Abstract method. MUST be reimplemented.
        '''
        pass
    
    def shouldBeRunAgain(self):
        '''
        Defines if the method should run again later
        '''
        return False
    
    def getName(self):
        '''
        Gets the process name
        '''
        return str(self.__class__).split('.')[-1].replace('\'>', '')
    
    def getProcessGroup(self):
        '''
        Returns the process group
        '''
        return 'Ungrouped'
    
    def getClassesToBeDisplayedAfterProcess(self):
        #returns classes to be loaded to TOC after executing this process.
        return self.classesToBeDisplayedAfterProcess
    
    def addClassesToBeDisplayedList(self,className):
        if className not in self.classesToBeDisplayedAfterProcess:
            self.classesToBeDisplayedAfterProcess.append(className)
    
    def clearClassesToBeDisplayedAfterProcess(self):
        self.classesToBeDisplayedAfterProcess = []
    
    def preProcess(self):
        '''
        Returns the name of the pre process that must run before, must be reimplemented in each process
        '''
        return None
    
    def postProcess(self):
        '''
        Returns the name of the post process that must run after, must be reimplemented in each process
        '''        
        return None
    
    def addFlag(self, flagTupleList):
        try:
            return self.abstractDb.insertFlags(flagTupleList, self.getName())
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            
    def removeFeatureFlags(self, layer, featureId):
        try:
            return self.abstractDb.removeFeatureFlags(layer, featureId, self.getName())
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
    def getStatus(self):
        try:
            return self.abstractDb.getValidationStatus(self.getName())
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
    def getStatusMessage(self):
        try:
            return self.abstractDb.getValidationStatusText(self.getName())
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
    def setStatus(self, msg, status):
        try:
            self.abstractDb.setValidationProcessStatus(self.getName(), msg, status)
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
    def finishedWithError(self):
        self.setStatus('Process finished with errors.', 2) #Failed status
        self.clearClassesToBeDisplayedAfterProcess()        
    
    def outputData(self, inputClass, dataLyr):
        edgvLayer = self.layerFactory.makeLayer(self.abstractDb, self.codeList, inputClass)
        crs = self.abstractDb.getSrid()
        lyr = edgvLayer.load(crs, uniqueLoad = True)
        updateList = []
        addList = []
        deleteList = []
        