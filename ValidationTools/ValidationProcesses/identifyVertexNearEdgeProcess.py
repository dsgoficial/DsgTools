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

class IdentifyVertexNearEdgeProcess(ValidationProcess):
    def __init__(self, postgisDb, iface):
        '''
        Constructor
        '''
        super(self.__class__,self).__init__(postgisDb, iface)
        self.processAlias = self.tr('Identify Vertex Near Edge')
        self.parameters = {'Tolerance': 1.0}

    def execute(self):
        '''
        Reimplementation of the execute method from the parent class
        '''
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithGeom = self.abstractDb.listClassesWithElementsFromDatabase()
            if len(classesWithElem) == 0:
                self.setStatus('Empty database.', 1) #Finished
                QgsMessageLog.logMessage('Empty database.', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            tol = self.parameters['Tolerance']
            error = False
            for cl in classesWithGeom:
                tableSchema, tableName = self.abstractDb.getTableSchema(cl)
                if cl[-1] in ['l','a']:
                    result = self.abstractDb.getVertexNearEdgesRecords(tableSchema, tableName, tol) #list only classes with elements.
                    if len(result) > 0:
                        error = True
                        recordList = []
                        for tupple in result:
                            recordList.append((tableSchema+'.'+tableName,tupple[0],'Vertex near edge.',tupple[1]))
                            self.addClassesToBeDisplayedList(tupple[0]) 
                        numberOfProblems = self.addFlag(recordList)
                        self.setStatus('{0} features from {1} have vertex(es) near edge(s). Check flags.'.format(numberOfProblems, cl), 4) #Finished with flags
                        QgsMessageLog.logMessage('{0} features from {1} have vertex(es) near edge(s). Check flags.'.format(numberOfProblems, cl), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                    else:
                        self.setStatus('There are no vertexes near edges on {}.'.format(cl), 1) #Finished
                        QgsMessageLog.logMessage('There are no vertexes near edges on {}.'.format(cl), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            if error:
                self.setStatus('There are vertexes near edges. Check log.', 4) #Finished with errors
            else:
                self.setStatus('There are no vertexes near edges.', 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0