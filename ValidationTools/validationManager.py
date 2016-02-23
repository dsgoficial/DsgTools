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

from DsgTools.ValidationTools.ValidationProcesses.identifyInvalidGeometriesProcess import IdentifyInvalidGeometriesProcess

class ValidationManager(object):
    def __init__(self,postgisDb):
        object.__init__(self)
        self.postgisDb = postgisDb
        self.currProc = None
        self.log = ''
        try:
            self.postgisDb.checkAndCreateValidationStructure()
            self.processList = []
            self.processList.append(IdentifyInvalidGeometriesProcess(self.postgisDb))
        except Exception as e:
            self.log+= e.args[0]
            print self.log

    def executeProcess(self, processName):
        idx = self.getProcessIndex(processName)
        if self.currProc <> None:
            self.log += 'Unable to run process %s. Process %s is already running.\n' % (processName, self.currProc.getName())
            return 0
        else:
            if idx <> None:
                self.currProc = self.processList[idx]
                if len(self.currProc.dependsOn())>0:
                    #check dependency
                    unmetDep = []
                    for dep in self.currProc.dependsOn():
                        procDep = self.processList[self.getProcessIndex(dep)]
                        #possible status: (0,'Not yet ran'), (1,'Finished'), (2,'Failed'), (3,'Running'), (4,'Finished with flags')
                        #must check if each dependency is met, so status must be 1
                        if procDep.getStatus() <> 1: 
                            unmetDep.append(dep)
                    if len(unmetDep) > 0:
                        self.log += 'Unable to run process due to the following dependencies: %s\n' % ','.join(unmetDep)
                        return 0
                else:
                    #check status
                    runningProc = self.getRunningProc()
                    if runningProc == None: #process is idle, I can now execute it.
                        self.currProc.execute() #run bitch run!
                        status = self.currProc.getStatus() #must set status
                        self.log += 'Process ran with status %s\n' % self.currProc.getStatusMessage()
                        self.log += 'Process Log:\n'
                        self.log += self.currProc.getLog()
                        self.currProc = None
                        return 1
                        #self.getClassesToBeDisplayedAfterProcess()
                    else:
                        self.log += 'Unable to run process due to process %s being executed.' % runningProc
                        return 0
                    pass
            else:
                self.log += 'Unable to run process.\n'
                self.log += self.currProc.getLog()
                return 0
    
    def getRunningProc(self):
        return self.postgisDb.getRunningProc()
    
    def getLog(self):
        return self.log
    
    def clearLog(self):
        self.log = ''
    
    def getProcessIndex(self, processName):
        procNameList = []
        for proc in self.processList:
             procNameList.append(proc.getName())
        if processName not in procNameList:
            self.log += 'Unable to find process. Process %s not implemented.\n' % processName
            return None
        else:
            return procNameList.index(processName)
    
    def clearLog(self):
        self.log = ''
    
    def currentProcess(self):
        return self.currProc

if __name__ == '__main__':
    from DsgTools.Factories.DbFactory.dbFactory import DbFactory
    abstractDb = DbFactory().createDbFactory('QPSQL')
    manager = ValidationManager(abstractDb)
    print manager
    pass