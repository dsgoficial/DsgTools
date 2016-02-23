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

class ValidationProcess(object):
    def __init__(self, postgisDb):
        object.__init__(self)
        self.abstractDb = postgisDb
        self.log = ''
        self.classesToBeDisplayedAfterProcess = []
        self.setStatus(0)
    
    def execute(self):
        #abstract method. MUST be reimplemented.
        pass
    
    def shouldBeRunAgain(self):
        #Abstract method. Should be reimplemented if necessary.
        return False
    
    def getName(self):
        return str(self.__class__).split('.')[-1].split('Process')[0]
    
    def getProcessGroup(self):
        return 'Ungrouped'
    
    def getClassesToBeDisplayedAfterProcess(self):
        #returns classes to be loaded to TOC after executing this process.
        return self.classesToBeDisplayedAfterProcess
    
    def addClassesToBeDisplayedList(self,className):
        if className not in self.classesToBeDisplayedAfterProcess:
            self.classesToBeDisplayedAfterProcess.append(className)
    
    def clearClassesToBeDisplayedAfterProcess(self):
        self.classesToBeDisplayedAfterProcess = []
    
    def dependsOn(self):
        #Abstract method. Should be reimplemented if necessary.
        return []
    
    def addLogMessage(self,msg):
        self.log += str(msg)
    
    def getLog(self):
        return self.log
    
    def addFlag(self,flagTupleList):
        try:
            return self.abstractDb.insertFlags(flagTupleList)
        except Exception as e:
            self.addLogMessage(str(e.args[0]))
    
    def getStatus(self):
        return self.abstractDb.getValidationStatus(self.getName())
    
    def getStatusMessage(self):
        return self.abstractDb.getValidationStatusText(self.getName())
    
    def setStatus(self,status):
        self.abstractDb.setValidationProcessStatus(self.getName(),self.getLog(),status)
    
    def finishedWithError(self):
        self.addLogMessage('Process finished with errors.\n')
        self.setStatus(2) #Failed status
        self.clearClassesToBeDisplayedAfterProcess()
    
    def checkIdle(self):
        return self.abstractDb.checkIdle()
        