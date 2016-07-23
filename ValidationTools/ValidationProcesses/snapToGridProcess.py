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
from qgis.core import QgsMessageLog
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess

class SnapToGridProcess(ValidationProcess):
    def __init__(self, postgisDb, codelist, iface):
        super(self.__class__,self).__init__(postgisDb, codelist, iface  )
        self.parameters = {'Snap': 0.001}

    def execute(self):
        #abstract method. MUST be reimplemented.
        QgsMessageLog.logMessage('Starting '+self.getName()+'Process.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            lyrs = self.inputData()
            for lyr in lyrs:
                featureMap = self.mapInputLayer(lyr)
                tableName = self.getTableNameFromLayer(lyr)
                self.prepareWorkingStructure(tableName,featureMap)
                tol = self.parameters['Snap']
                srid = self.abstractDb.findEPSG()
                result = self.abstractDb.snapToGrid(tableName+'_temp', tol, srid) #list only classes with elements.
                self.abstractDb.db.close()
                self.abstractDb.dropTempTable(tableName)
                dataDict = dict()
                dataDict['UPDATE'] = dict()
                for key in result.keys():
                    dataDict['UPDATE'][key] = result[key]
                self.outputData('postgis', tableName, dataDict)
            self.setStatus('All features snapped succesfully.\n', 1) #Finished
            QgsMessageLog.logMessage('All features snapped succesfully.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0