# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
import processing

class CleanAreasProcess(ValidationProcess):
    def __init__(self, postgisDb):
        super(self.__class__,self).__init__(postgisDb)
        self.parameters = {'Snap': 0.5}
        
    def runProcessinAlg(self, cl):
        alg = 'grass7:v.clean.advanced'
        
        input = QgsVectorLayer(self.abstractDb.getURI(cl).uri(), cl, "postgres")
        crs = input.crs()
        crs.createFromId(self.abstractDb.findEPSG())
        input.setCrs(crs)        
        
        tools = 'break,rmsa,rmdangle'
        threshold = -1

        tableSchema, tableName = self.abstractDb.getTableSchema(cl)        
        (xmin, xmax, ymin, ymax) = self.abstractDb.getTableExtent(tableSchema, tableName)
        extent = '{0},{1},{2},{3}'.format(xmin, xmax, ymin, ymax)
        
        snap = self.parameters['Snap']
        
        minArea = 0.0001
        
        ret = processing.runalg(alg, input, tools, threshold, extent, snap, minArea, None, None)
        errorLayer = processing.getObject(ret['error'])
        outputLayer = processing.getObject(ret['output'])
        
        return self.getProcessingErrors(tableSchema, tableName, errorLayer)
        
    def getProcessingErrors(self, tableSchema, tableName, layer):
        recordList = []
        for feature in layer.getFeatures():
            recordList.append((feature.id(), feature.geometry()))
        return recordList
        
    def execute(self):
        #abstract method. MUST be reimplemented.
        QgsMessageLog.logMessage('Starting '+self.getName()+'Process.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithGeom = self.abstractDb.listClassesWithElementsFromDatabase()
            for cl in classesWithGeom:
                if cl[-1] in ['l','a']:
                    result = self.runProcessinAlg(cl)
                    if len(result) > 0:
                        recordList = []
                        for tupple in result:
                            recordList.append((tableSchema+'.'+tableName,tupple[0],'Cleaning error.',tupple[1]))
                            self.addClassesToBeDisplayedList(tupple[0]) 
                        numberOfProblems = self.addFlag(recordList)
                        self.setStatus('%s feature(s) with cleaning errors. Check flags.\n' % numberOfProblems, 4) #Finished with flags
                        QgsMessageLog.logMessage('%s feature(s) with cleaning errors. Check flags.\n' % numberOfProblems, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                    else:
                        self.setStatus('There are cleaning errors.\n', 1) #Finished
                        QgsMessageLog.logMessage('There are cleaning errors.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return