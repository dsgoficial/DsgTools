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

class IdentifyDuplicatedGeometriesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface):
        '''
        Constructor
        '''
        super(self.__class__,self).__init__(postgisDb, iface)

    def execute(self):
        '''
        Reimplementation of the execute method from the parent class
        '''
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithGeom = self.abstractDb.listClassesWithElementsFromDatabase()
            duplicated = self.abstractDb.getDuplicatedGeomRecords(classesWithGeom) #list only classes with elements.
            if len(duplicated.keys()) > 0:
                dupGeomRecordList = []
                for cl in duplicated.keys():
                    tableSchema, tableName = self.abstractDb.getTableSchema(cl)
                    if tableSchema not in ('validation'):
                        for id in duplicated[cl].keys():
                            dupGeomRecordList.append((tableSchema+'.'+tableName,id,'Duplicated Geometry',duplicated[cl][id]))
                numberOfDupGeom = self.addFlag(dupGeomRecordList)
                for tuple in dupGeomRecordList:
                    self.addClassesToBeDisplayedList(tuple[0])        
                self.setStatus('{} features are duplicated. Check flags.'.format(numberOfDupGeom), 4) #Finished with flags
                QgsMessageLog.logMessage('{} features are duplicated. Check flags.'.format(numberOfDupGeom), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            else:
                self.setStatus('There are no duplicated geometries.', 1) #Finished
                QgsMessageLog.logMessage('There are no duplicated geometries.', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0