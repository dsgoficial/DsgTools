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

class ValidationManager(object):
    def __init__(self,postgisDb):
        object.__init__(self)
        self.processList = []
        self.postgisDb = postgisDb
        try:
            self.postgisDb.checkAndCreateValidationStructure()
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        self.setAvailableProcesses()

    def setAvailableProcesses(self):
        ignoredFiles = ['__init__.py', 'validationProcess.py']
        for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), 'ValidationProcesses')):
            for file in files:
                if file in ignoredFiles or file.split('.')[-1] != 'py':
                    continue
                fileBaseName = file.split('.')[0]
                chars = list(fileBaseName)
                chars[0] = chars[0].upper()
                processClass = ''.join(chars)
                self.processList.append(processClass)
            
    def instantiateProcessByName(self, processName):
        currProc = None
        for processClass in self.processList:
            if processClass == processName:
                chars = list(processClass)
                chars[0] = chars[0].lower()
                fileBaseName = ''.join(chars)
                mod = __import__('DsgTools.ValidationTools.ValidationProcesses.'+fileBaseName, fromlist=[processClass])
                klass = getattr(mod, processClass)
                currProc = klass(self.postgisDb)
                return currProc

    def executeProcess(self, processName):
        runningProc = self.getRunningProc()
        if runningProc != None:
            QgsMessageLog.logMessage('Unable to run process %s. Process %s is already running.\n' % (processName, runningProc), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 0
        else:
            currProc = self.instantiateProcessByName(processName)
            if len(currProc.dependsOn()) > 0:
                #check dependency
                unmetDep = []
                for dep in currProc.dependsOn():
                    procDep = self.instantiateProcessByName(dep)
                    #possible status: (0,'Not yet ran'), (1,'Finished'), (2,'Failed'), (3,'Running'), (4,'Finished with flags')
                    #must check if each dependency is met, so status must be 1
                    if procDep.getStatus() != 1: 
                        unmetDep.append(dep)
                if len(unmetDep) > 0:
                    QgsMessageLog.logMessage('Unable to run process due to the following dependencies: %s\n' % ','.join(unmetDep), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                    return 0
            else:
                # setting parameters
                if currProc.parameters:
                    dlg = ProcessParametersDialog(None, currProc.parameters, None, 'Process parameters setter')
                    dlg.exec_()
                    # get parameters
                    params = dlg.values
                    # adjusting the parameters in the process
                    currProc.setParameters(params)
                #check status
                QgsMessageLog.logMessage('Process %s Log:\n' % currProc.getName(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                currProc.execute() #run bitch run!
                status = currProc.getStatus() #must set status
                QgsMessageLog.logMessage('Process ran with status %s\n' % currProc.getStatusMessage(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
    
    #this method gets the process name
    def getRunningProc(self):
        return self.postgisDb.getRunningProc()

if __name__ == '__main__':
    from DsgTools.Factories.DbFactory.dbFactory import DbFactory
    abstractDb = DbFactory().createDbFactory('QPSQL')
    manager = ValidationManager(abstractDb)
    print manager
    pass