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
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface)
        self.processAlias = self.tr('Identify Duplicated Geometries')
        
        # getting tables with elements
        classesWithElemDictList = self.abstractDb.listGeomClassesFromDatabase(withElements=True, getGeometryColumn=True)
        # creating a list of tuples (layer names, geometry columns)
        classesWithElem = ['{0}:{1}'.format(i['layerName'], i['geometryColumn']) for i in classesWithElemDictList]
        # adjusting process parameters
        self.parameters = {'Classes': classesWithElem}

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithGeom = []
            for classAndGeom in self.parameters['Classes']:
                # preparation
                cl, geometryColumn = classAndGeom.split(':')
                processTableName, lyr = self.prepareExecution(cl, geometryColumn)
                if processTableName not in classesWithGeom:
                    classesWithGeom.append(processTableName)
                    
            # running the process
            duplicated = self.abstractDb.getDuplicatedGeomRecords(classesWithGeom)
            
            # dropping temp table
            for processTableName in classesWithGeom:
                self.abstractDb.dropTempTable(processTableName)
                
            # storing flags
            if len(duplicated.keys()) > 0:
                dupGeomRecordList = []
                for cl in duplicated.keys():
                    tableSchema, tableName = self.abstractDb.getTableSchema(cl)
                    # the flag should store the original table name
                    tableName = tableName.replace('_temp', '')
                    if tableSchema not in ('validation'):
                        for id in duplicated[cl].keys():
                            dupGeomRecordList.append((tableSchema+'.'+tableName, id, self.tr('Duplicated Geometry'), duplicated[cl][id]))
                numberOfDupGeom = self.addFlag(dupGeomRecordList)
                for tuple in dupGeomRecordList:
                    self.addClassesToBeDisplayedList(tuple[0])
                msg =  self.tr('{} features are duplicated. Check flags.').format(numberOfDupGeom)     
                self.setStatus(msg, 4) #Finished with flags
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            else:
                msg = self.tr('There are no duplicated geometries.')
                self.setStatus(msg, 1) #Finished
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0