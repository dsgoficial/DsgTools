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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsMapLayerRegistry, QgsGeometry, QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, QgsFeature
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
import processing, binascii

class CleanGeometriesProcess(ValidationProcess):
    def __init__(self, postgisDb, codelist):
        '''
        Constructor
        '''
        super(self.__class__,self).__init__(postgisDb, codelist)
        self.parameters = {'Snap': 1.0, 'MinArea':0.001}
        
    def runProcessinAlg(self, cl):
        '''
        Runs the actual process
        '''
        alg = 'grass7:v.clean.advanced'
        
        #creating vector layer
        input = QgsVectorLayer(self.abstractDb.getURI(cl, True).uri(), cl, "postgres")
        crs = input.crs()
        epsg = self.abstractDb.findEPSG()
        crs.createFromId(epsg)
        input.setCrs(crs)
        
        #Adding to registry
        QgsMapLayerRegistry.instance().addMapLayer(input)
        
        #setting tools
        tools = 'break,rmsa,rmdangle'
        threshold = -1

        #getting table extent (bounding box)
        tableSchema, tableName = self.abstractDb.getTableSchema(cl)        
        (xmin, xmax, ymin, ymax) = self.abstractDb.getTableExtent(tableSchema, tableName)
        extent = '{0},{1},{2},{3}'.format(xmin, xmax, ymin, ymax)
        
        snap = self.parameters['Snap']
        minArea = self.parameters['MinArea']
        
        ret = processing.runalg(alg, input, tools, threshold, extent, snap, minArea, None, None)

        #updating original layer
        outputLayer = processing.getObject(ret['output'])
        self.updateOriginalLayer(input, outputLayer)

        #getting error flags
        errorLayer = processing.getObject(ret['error'])
        #removing from registry
        QgsMapLayerRegistry.instance().removeMapLayer(input.id())
        return self.getProcessingErrors(errorLayer)

    def execute(self):
        '''
        Reimplementation of the execute method from the parent class
        '''
        QgsMessageLog.logMessage('Starting '+self.getName()+'Process.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            lyrs = self.inputData()
            if lyrs.__len__() == 0:
                self.setStatus('No layers loaded!\n', 1) #Finished
                QgsMessageLog.logMessage('No layers loaded!\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return
            for lyr in lyrs:
                featureMap = self.mapInputLayer(lyr)
                tableName = self.getTableNameFromLayer(lyr)
                self.prepareWorkingStructure(tableName, featureMap)
                if tableName[-1] in ['a', 'l']:
                    result = self.runProcessinAlg(tableName+'_temp')
                    if len(result) > 0:
                        recordList = []
                        for tupple in result:
                            recordList.append((cl, tupple[0],'Cleaning error.', tupple[1]))
                            self.addClassesToBeDisplayedList(tableName)
                        numberOfProblems = self.addFlag(recordList)
                        self.setStatus('{} feature(s) of class '+tableName+' with cleaning errors. Check flags.\n'.format(numberOfProblems), 4) #Finished with flags
                        QgsMessageLog.logMessage('{} feature(s) of class '+tableName+' with cleaning errors. Check flags.\n'.format(numberOfProblems), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                    else:
                        self.setStatus('There are no cleaning errors on '+tableName+'.\n', 1) #Finished
                        QgsMessageLog.logMessage('There are no cleaning errors on '+tableName+'.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0
