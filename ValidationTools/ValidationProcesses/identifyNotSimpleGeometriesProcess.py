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
        email                : borba.philipe@eb.mil.br
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
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

class IdentifyNotSimpleGeometriesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating=False)
        self.processAlias = self.tr('Identify Not Simple Geometries')

        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a', 'l'], withElements=True, excludeValidation = True)
            # adjusting process parameters
            interfaceDictList = []
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDictList.append({self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType})
            self.parameters = {'Classes': interfaceDictList}

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithElem = self.parameters['Classes']
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            classesWithGeom = []
            recordFlagList = []
            for key in classesWithElem:
                # preparation
                classAndGeom = self.classesWithElemDict[key]
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                localProgress.step()
                processTableName, lyr, keyColumn = self.prepareExecution(classAndGeom)
                localProgress.step()
                    
                # running the process
                localProgress = ProgressWidget(0, 1, self.tr('Running process ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                localProgress.step()
                result = self.abstractDb.getNotSimpleRecords(processTableName, classAndGeom['geom'], keyColumn)
                localProgress.step()
                # dropping temp table
                self.abstractDb.dropTempTable(processTableName)
                #storing flags
                if len(result) > 0:
                    if classAndGeom['tableSchema'] not in ('validation'):
                        for r in result:
                            id, geom = r
                            recordFlagList.append((classAndGeom['tableSchema']+'.'+classAndGeom['tableName'], id, self.tr('Not simple geometry.'), geom, classAndGeom['geom']))

            # storing flags
            if len(recordFlagList) > 0:
                numberOfProblems = self.addFlag(recordFlagList)
                msg = str(numberOfProblems) + self.tr(' features are not simple. Check flags.')        
                self.setStatus(msg, 4) #Finished with flags
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            else:
                msg = self.tr('All features are simple.')
                self.setStatus(msg, 1) #Finished
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0