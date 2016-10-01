# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-04-06
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
from qgis.core import QgsMessageLog, QgsVectorLayer
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess

class ForceValidityGeometriesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface):
        '''
        Constructor
        '''
        super(self.__class__,self).__init__(postgisDb, iface)
        
    def preProcess(self):
        '''
        Gets the process that should be execute before this one
        '''
        return 'IdentifyInvalidGeometriesProcess'
        
    def postProcess(self):
        '''
        Gets the process that should be execute after this one
        '''
        return 'DeaggregateGeometriesProcess'

    def execute(self):
        '''
        Reimplementation of the execute method from the parent class
        '''
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr('Process.\n'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            flagsDict = self.abstractDb.getFlagsDictByProcess('IdentifyInvalidGeometriesProcess')
            numberOfProblems = 0
            for cl in flagsDict.keys():
                #creating vector layer
                schema, layer_name = self.abstractDb.getTableSchema(cl)
                lyr = self.layerLoader.load([layer_name],uniqueLoad=True)[layer_name]
                #getting feature map including the edit buffer
                featureMap = self.mapInputLayer(lyr)
                #getting table name with schema
                tableName = self.getTableNameFromLayer(lyr)
                #setting temp table name
                processTableName = tableName+'_temp'
                #creating temp table
                self.prepareWorkingStructure(tableName, featureMap)
                #running the process in the temp table
                numberOfProblems += self.abstractDb.forceValidity(processTableName, flagsDict[cl])
                #getting the output as a QgsVectorLayer
                outputLayer = QgsVectorLayer(self.abstractDb.getURI(processTableName, True).uri(), processTableName, "postgres")
                #updating the original layer (lyr)
                self.updateOriginalLayer(lyr, outputLayer)
                #dropping the temp table as we don't need it anymore
                self.abstractDb.dropTempTable(processTableName)
            self.setStatus('{} features were changed.\n'.format(numberOfProblems), 1) #Finished with flags
            QgsMessageLog.logMessage('{} features were changed.\n'.format(numberOfProblems), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0