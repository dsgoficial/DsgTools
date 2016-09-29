# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-06-22
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

class SnapToGridProcess(ValidationProcess):
    def __init__(self, postgisDb, codelist, iface):
        '''
        Constructor
        '''
        super(self.__class__,self).__init__(postgisDb, codelist, iface  )
        self.parameters = {'Snap': 0.001}

    def execute(self):
        '''
        Reimplementation of the execute method from the parent class
        '''
        QgsMessageLog.logMessage('Starting '+self.getName()+'Process.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            lyrs = self.inputData()
            for lyr in lyrs:
                #getting feature map including the edit buffer
                featureMap = self.mapInputLayer(lyr)
                #getting table name with schema
                tableName = self.getTableNameFromLayer(lyr)
                #setting temp table name
                processTableName = tableName+'_temp'
                #creating temp table
                self.prepareWorkingStructure(tableName, featureMap)
                #getting parameters
                tol = self.parameters['Snap']
                srid = self.abstractDb.findEPSG()
                #running the process in the temp table
                self.abstractDb.snapToGrid([processTableName], tol, srid)
                #getting the output as a QgsVectorLayer
                outputLayer = QgsVectorLayer(self.abstractDb.getURI(processTableName, True).uri(), processTableName, "postgres")
                #updating the original layer (lyr)
                self.updateOriginalLayer(lyr, outputLayer)
                #dropping the temp table as we don't need it anymore
                self.abstractDb.dropTempTable(tableName)
            #setting status
            self.setStatus('All features snapped succesfully.\n', 1) #Finished
            QgsMessageLog.logMessage('All features snapped succesfully.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            #returning success
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            #returning error
            return 0