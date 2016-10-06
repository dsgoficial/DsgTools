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
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess

class IdentifyNotSimpleGeometriesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface):
        '''
        Constructor
        '''
        super(self.__class__,self).__init__(postgisDb, iface)
        self.processAlias = self.tr('Identify Not Simple Geometries Process')

    def execute(self):
        '''
        Reimplementation of the execute method from the parent class
        '''
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithGeom = self.abstractDb.listClassesWithElementsFromDatabase()
            result = self.abstractDb.getNotSimpleRecords(classesWithGeom) #list only classes with elements.
            if len(result.keys()) > 0:
                recordList = []
                for cl in result.keys():
                    tableSchema, tableName = self.abstractDb.getTableSchema(cl)
                    for id in result[cl].keys():
                        recordList.append((tableSchema+'.'+tableName,id,'Not simple geometry.',result[cl][id]))
                numberOfProblems = self.addFlag(recordList)
                for tuple in recordList:
                    self.addClassesToBeDisplayedList(tuple[0])        
                self.setStatus('{} features are not simple. Check flags.'.format(numberOfProblems), 4) #Finished with flags
                QgsMessageLog.logMessage('{} features are not simple. Check flags.'.format(numberOfProblems), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            else:
                self.setStatus(self.tr('All features are simple.\n'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('All features are simple.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0