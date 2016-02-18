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

from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess

class IdentifyInvalidGeometriesProcess(ValidationProcess):
    def __init__(self, postgisDb):
        super(self.__class__,self).__init__(postgisDb)
    
    def execute(self):
        #abstract method. MUST be reimplemented.
        self.addLogMessage('Starting '+self.getName()+'Process.\n')
        try:
            invalidGeomRecordList = self.abstractDb.getInvalidGeomRecords() #list only classes with elements.
        except Exception as e:
            self.addLogMessage(str(e.args[0]))
            self.finishedWithError()
            return

        if len(invalidGeomRecordList) > 0:
            numberOfInvGeom = self.addFlag(invalidGeomRecordList)
            self.addLogMessage('%s features are invalid. Check flags.\n' % numberOfInvGeom)
            for tuple in invalidGeomRecordList:
                self.addClassesToBeDisplayedList(tuple[0])
        
            self.setStatus(4) #Finished with flags
            return
        else:
            self.addLogMessage('All features are invalid.\n')
            self.setStatus(0) #Finished

