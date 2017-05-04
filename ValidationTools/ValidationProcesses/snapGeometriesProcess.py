# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-09-14
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

class SnapGeometriesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Snap Geometries')
        
        if not self.instantiating:
            # getting tables with elements
            classesWithElemDictList = self.abstractDb.listGeomClassesFromDatabase(primitiveFilter=['a', 'l'], withElements=True, getGeometryColumn=True)
            # creating a list of tuples (layer names, geometry columns)
            classesWithElem = ['{0}:{1}'.format(i['layerName'], i['geometryColumn']) for i in classesWithElemDictList]
            # adjusting process parameters
            self.parameters = {'Snap': 1.0, 'MinArea': 0.001, 'Classes': classesWithElem}
        
    def runProcessinAlg(self, layer):
        """
        Runs the actual grass process
        """
        alg = 'grass7:v.clean.advanced'
        
        #setting tools
        tools = 'snap'
        threshold = -1
        minArea = self.parameters['MinArea']
        snap = self.parameters['Snap']

        #getting table extent (bounding box)
        extent = layer.extent()
        (xmin, xmax, ymin, ymax) = extent.xMinimum(), extent.xMaximum(), extent.yMinimum(), extent.yMaximum()
        extent = '{0},{1},{2},{3}'.format(xmin, xmax, ymin, ymax)
        
        ret = processing.runalg(alg, layer, tools, threshold, extent, snap, minArea, None, None)
        if not ret:
            raise Exception(self.tr('Problem executing grass7:v.clean.advanced. Check your installed libs.\n'))
            
        #updating original layer
        outputLayer = processing.getObject(ret['output'])
        self.updateOriginalLayer(layer, outputLayer)
          
        #getting error flags
        errorLayer = processing.getObject(ret['error'])
        #removing from registry
        return self.getProcessingErrors(errorLayer)

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        #abstract method. MUST be reimplemented.
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithElem = self.parameters['Classes']
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            error = False
            for classAndGeom in classesWithElem:
                # preparation
                cl, geometryColumn = classAndGeom.split(':')
                lyr = self.loadLayerBeforeValidationProcess(cl)
                
                tableSchema, tableName = cl.split('.')
                # specific EPSG search
                parameters = {'tableSchema': tableSchema, 'tableName': tableName, 'geometryColumn': geometryColumn}
                srid = self.abstractDb.findEPSG(parameters=parameters)                        

                # running the process in the temp table
                result = self.runProcessinAlg(lyr)
                
                # storing flags
                if len(result) > 0:
                    error = True
                    recordList = []
                    for tupple in result:
                        recordList.append((cl, tupple[0], self.tr('Snapping error.'), tupple[1], geometryColumn))
                        self.addClassesToBeDisplayedList(cl) 
                    numberOfProblems = self.addFlag(recordList)
                    QgsMessageLog.logMessage(str(numberOfProblems) + self.tr(' feature(s) of layer ') + cl + self.tr(' with snapping errors. Check flags.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                else:
                    QgsMessageLog.logMessage(self.tr('There are no snapping errors on ') + cl +'.', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            if error:
                self.setStatus(self.tr('There are snapping errors. Check log.'), 4) #Finished with errors
            else:
                self.setStatus(self.tr('There are no snapping errors.'), 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0
