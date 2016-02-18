# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-10-21
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
        self.statusDict = {0:'Not Runned yet', 1:'Finished', 2:'Failed', 3:'Running', 4:'Finished with flags'}
        self.status = 0
    
    def execute(self):
        #abstract method. MUST be reimplemented.
        pass
    
    def shouldBeRunAgain(self):
        #Abstract method. Should be reimplemented if necessary.
        return False
    
    def getName(self):
        return str(self.__class__).split('.')[1].split('Process')[0]
    
    def getProcessGroup(self):
        return 'Ungrouped'
    
    def getClassesToBeDisplayedAfterProcess(self):
        #returns classes to be loaded to TOC after executing this process.
        return []
    
    def dependsOn(self):
        #Abstract method. Should be reimplemented if necessary.
        return []
    
    def addLogMessage(self,msg):
        self.log += str(msg)
    
    def getLog(self):
        return self.log
    
    def addFlag(self,layer,feat_id,reason,geom):
        try:
            self.abstractDb.insertFlag(layer,feat_id,reason,geom)
        except Exception as e:
            self.addLogMessage(str(e))
    
    def getStatus(self):
        self.status = self.abstractDb.getValidationStatus(self.getName())
        return self.status
    
    def getStatusMessage(self):
        return self.statusDict[self.status]
    
    

if __name__ == '__main__':
    
    teste = ValidationProcess(None)
    print teste.getName()