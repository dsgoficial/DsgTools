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
from builtins import str
from qgis.core import QgsMessageLog, Qgis
from DsgTools.core.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget

class IdentifyVertexNearEdgeProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating = False, withElements = True):
        """
        Constructor
        """
        super(IdentifyVertexNearEdgeProcess, self).__init__(postgisDb, iface, instantiating, withElements)
        self.processAlias = self.tr('Identify Vertex Near Edge')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['l','a'], withElements = withElements, excludeValidation = True)
            # adjusting process parameters
            interfaceDictList = []
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDictList.append({self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType})
            self.parameters = {self.tr('Tolerance'): 1.0, 'Classes': interfaceDictList, 'Only Selected':False}

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", Qgis.Critical)
        self.startTimeCount()
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithElem = self.parameters['Classes']
            self.startTimeCount()
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                return 1            
            tol = self.parameters[self.tr('Tolerance')]
            error = False
            for key in classesWithElem:
                # preparation
                classAndGeom = self.classesWithElemDict[key]
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                localProgress.step()
                processTableName, lyr, keyColumn = self.prepareExecution(classAndGeom, selectedFeatures = self.parameters['Only Selected'])
                tableSchema, tableName = self.abstractDb.getTableSchema(processTableName)
                localProgress.step()
                
                #running the process
                localProgress = ProgressWidget(0, 1, self.tr('Running process on ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                localProgress.step()
                result = self.abstractDb.getVertexNearEdgesRecords(tableSchema, tableName, tol, classAndGeom['geom'], keyColumn, classAndGeom['geomType'])
                localProgress.step()
                
                # dropping temp table
                self.abstractDb.dropTempTable(processTableName)
                
                # storing flags
                if len(result) > 0:
                    error = True
                    recordList = []
                    for tupple in result:
                        recordList.append((classAndGeom['tableSchema']+'.'+classAndGeom['tableName'], tupple[0], self.tr('Vertex near edge.'), tupple[1], classAndGeom['geom']))
                        self.addClassesToBeDisplayedList(tupple[0]) 
                    numberOfProblems = self.addFlag(recordList)
                    QgsMessageLog.logMessage(str(numberOfProblems) + self.tr(' features from') + classAndGeom['tableName'] +self.tr(' have vertex(es) near edge(s). Check flags.'), "DSG Tools Plugin", Qgis.Critical)
                else:
                    QgsMessageLog.logMessage(self.tr('There are no vertexes near edges on ') + classAndGeom['tableName'] +'.', "DSG Tools Plugin", Qgis.Critical)
                self.logLayerTime(classAndGeom['tableSchema']+'.'+classAndGeom['tableName'])
            if error:
                self.setStatus(self.tr('There are vertexes near edges. Check log.'), 4) #Finished with errors
            else:
                self.setStatus(self.tr('There are no vertexes near edges.'), 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
            self.finishedWithError()
            return 0