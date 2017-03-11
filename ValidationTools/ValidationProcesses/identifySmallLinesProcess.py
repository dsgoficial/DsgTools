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
    def __init__(self, postgisDb, iface):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface)
        self.processAlias = self.tr('Identify Small Lines')
        
        classesWithElemDictList = self.abstractDb.listGeomClassesFromDatabase(primitiveFilter=['l'], withElements=True, getGeometryColumn=True)
        classesWithElem = ['{0}:{1}'.format(i['layerName'], i['geometryColumn']) for i in classesWithElemDictList]
        self.parameters = {self.tr('Length'): 5.0, 'Classes': classesWithElem}

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            tol = self.parameters[self.tr('Length')]
            classesWithGeom = []
            for classAndGeom in self.parameters['Classes']:
                # preparation
                cl, geometryColumn = classAndGeom.split(':')
                processTableName, lyr = self.prepareExecution(cl, geometryColumn)
                if processTableName not in classesWithGeom:
                    classesWithGeom.append(processTableName)

            # running the process
            result = self.abstractDb.getSmallLinesRecords(classesWithGeom, tol)
            
            # dropping temp table
            for processTableName in classesWithGeom:
                self.abstractDb.dropTempTable(processTableName)
                
            # storing flags
            if len(result.keys()) > 0:
                recordList = []
                for cl in result.keys():
                    tableSchema, tableName = self.abstractDb.getTableSchema(cl)
                    # the flag should store the original table name
                    tableName = tableName.replace('_temp', '')
                    for id in result[cl].keys():
                        recordList.append((tableSchema+'.'+tableName, id, self.tr('Small Length.'), result[cl][id]))
                numberOfProblems = self.addFlag(recordList)
                for tuple in recordList:
                    self.addClassesToBeDisplayedList(tuple[0])    
                msg = self.tr('{0} features have small length. Check flags.').format(numberOfProblems)
                self.setStatus(msg, 4) #Finished with flags
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            else:
                msg = self.tr('There are no small lines.')
                self.setStatus(msg, 1) #Finished
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0