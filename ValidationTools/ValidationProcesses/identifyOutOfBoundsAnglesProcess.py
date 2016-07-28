# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
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
from qgis.core import QgsMessageLog
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess

class IdentifyOutOfBoundsAnglesProcess(ValidationProcess):
    def __init__(self, postgisDb, codelist):
        '''
        Constructor
        '''
        super(self.__class__,self).__init__(postgisDb, codelist)
        self.parameters = {'Angle': 10.0}

    def execute(self):
        '''
        Reimplementation of the execute method from the parent class
        '''
        QgsMessageLog.logMessage('Starting '+self.getName()+'Process.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithGeom = self.abstractDb.listClassesWithElementsFromDatabase()
            tol = self.parameters['Angle']
            for cl in classesWithGeom:
                tableSchema, tableName = self.abstractDb.getTableSchema(cl)
                if cl[-1] in ['l','a']:
                    result = self.abstractDb.getOutOfBoundsAnglesRecords(tableSchema, tableName, tol) #list only classes with elements.
                    if len(result) > 0:
                        recordList = []
                        for tupple in result:
                            recordList.append((tableSchema+'.'+tableName,tupple[0],'Angle out of bound.',tupple[1]))
                            self.addClassesToBeDisplayedList(tupple[0]) 
                        numberOfProblems = self.addFlag(recordList)
                        self.setStatus('%s feature(s) have out of bounds angle(s). Check flags.\n' % numberOfProblems, 4) #Finished with flags
                        QgsMessageLog.logMessage('%s feature(s) have out of bounds angle(s). Check flags.\n' % numberOfProblems, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                    else:
                        self.setStatus('There are no out of bounds angles.\n', 1) #Finished
                        QgsMessageLog.logMessage('There are no out of bounds angles.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0