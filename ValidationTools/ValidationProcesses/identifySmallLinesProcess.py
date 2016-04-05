# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-04-05
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
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess

class IdentifySmallLinesProcess(ValidationProcess):
    def __init__(self, postgisDb):
        super(self.__class__,self).__init__(postgisDb)
        self.parameters = {'Length': 5.0}

    def execute(self):
        #abstract method. MUST be reimplemented.
        QgsMessageLog.logMessage('Starting '+self.getName()+'Process.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithGeom = self.abstractDb.listClassesWithElementsFromDatabase()
            lines = []
            for c in classesWithGeom:
                if c[-1] == 'l':
                    areas.append(c)
            tol = self.parameters['Length']
            result = self.abstractDb.getSmallLinesRecords(lines, tol) #list only classes with elements.
            if len(result.keys()) > 0:
                recordList = []
                for cl in result.keys():
                    tableSchema, tableName = self.abstractDb.getTableSchema(cl)
                    for id in result[cl].keys():
                        recordList.append((tableSchema+'.'+tableName,id,'Small Length.',result[cl][id]))
                numberOfProblems = self.addFlag(recordList)
                for tuple in recordList:
                    self.addClassesToBeDisplayedList(tuple[0])        
                self.setStatus('%s features have small length. Check flags.\n' % numberOfProblems, 4) #Finished with flags
                QgsMessageLog.logMessage('%s features have small length. Check flags.\n' % numberOfProblems, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return
            else:
                self.setStatus('There are no small lines.\n', 1) #Finished
                QgsMessageLog.logMessage('There are no small lines.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return