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
import os
from qgis.core import QgsMessageLog
from DsgTools.ValidationTools.processParametersDialog import ProcessParametersDialog

from PyQt4.QtGui import QMessageBox
from PyQt4.Qt import QObject

class ValidationManager(QObject):
    def __init__(self,postgisDb, iface):
        """
        Constructor
        """
        super(ValidationManager, self).__init__()
        self.processList = []
        self.postgisDb = postgisDb
        self.iface = iface
        self.processDict = dict()
        try:
            #creating validation structure
            self.postgisDb.checkAndCreateValidationStructure()
            #setting available processes
            self.setAvailableProcesses()
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            

    def setAvailableProcesses(self):
        """
        Sets all available processes.
        This method is a dynamic method that scans the processes folder for .py files.
        All .py files within the folder (minus the ignored ones) are listed as available processes
        """
        ignoredFiles = ['__init__.py', 'validationProcess.py', 'spatialRuleEnforcer.py']
        for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), 'ValidationProcesses')):
            files.sort()
            for file in files:
                if file in ignoredFiles or file.split('.')[-1] != 'py':
                    continue
                fileBaseName = file.split('.')[0]
                chars = list(fileBaseName)
                chars[0] = chars[0].upper()
                processClass = ''.join(chars)
                self.processList.append(processClass)
                self.processDict[self.instantiateProcessByName(processClass).processAlias] = processClass 
            
    def instantiateProcessByName(self, processName):
        """
        This method instantiate a process by its name.
        The import is made dynamically using the __import__ function.
        The class to be import is obtained using the getattr function.
        The class instance is made using: klass(self.postgisDb, self.iface)
        """
        currProc = None
        for processClass in self.processList:
            if processClass == processName:
                chars = list(processClass)
                #adjusting first character case
                chars[0] = chars[0].lower()
                #making file name
                fileBaseName = ''.join(chars)
                #setting up the module to be imported
                mod = __import__('DsgTools.ValidationTools.ValidationProcesses.'+fileBaseName, fromlist=[processClass])
                #obtaining the class name
                klass = getattr(mod, processClass)
                #instantiating the class
                currProc = klass(self.postgisDb, self.iface)
                return currProc

    def executeProcess(self, process):
        """
        Executes a process by its name
        processName: process name
        """
        #checking for running processes
        processName = self.processDict[process]
        runningProc = None
        try:
            runningProc = self.postgisDb.getRunningProc()
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 0
            
        #if there is a running process we should stop
        if runningProc != None:
            QgsMessageLog.logMessage('Unable to run process %s. Process %s is already running.\n' % (processName, runningProc), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 0
        else:
            currProc = self.instantiateProcessByName(processName)
            #checking for existing pre process
            preProcessName = currProc.preProcess()
            if preProcessName:
                self.executeProcess(preProcessName)
            # setting parameters
            if currProc.parameters:
                dlg = ProcessParametersDialog(None, currProc.parameters, None, 'Process parameters setter')
                if dlg.exec_() == 0:
                    return -1
                # get parameters
                params = dlg.values
                # adjusting the parameters in the process
                currProc.setParameters(params)
            #check status
            QgsMessageLog.logMessage('Process %s Log:\n' % currProc.getName(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            ret = currProc.execute() #run bitch run!
            #status = currProc.getStatus() #must set status
            QgsMessageLog.logMessage('Process ran with status %s\n' % currProc.getStatusMessage(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            #checking for existing post process
            postProcessName = currProc.postProcess()
            if postProcessName:
                self.executeProcess(postProcessName)
            return ret
    
if __name__ == '__main__':
    from DsgTools.Factories.DbFactory.dbFactory import DbFactory
    abstractDb = DbFactory().createDbFactory('QPSQL')
    manager = ValidationManager(abstractDb)
    print manager
    pass