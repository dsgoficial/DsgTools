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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsGeometry, QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, QgsFeature
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.CustomWidgets.progressWidget import ProgressWidget
import processing, binascii

class SnapGeometriesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating = False, withElements = True):
        """
        Constructor
        """
        super(SnapGeometriesProcess, self).__init__(postgisDb, iface, instantiating, withElements)
        self.processAlias = self.tr('Snap Geometries')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(withElements = withElements, excludeValidation = True)
            # adjusting process parameters
            interfaceDictList = []
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDictList.append({self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType})
            #self.parameters = {'Snap': 1.0, 'MinArea': 0.001, 'Classes': interfaceDictList}
            self.parameters = {'Snap': 1.0, 'Classes': interfaceDictList}
        
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
        self.updateOriginalLayerV2(layer, outputLayer)
          
        #getting error flags
        errorLayer = processing.getObject(ret['error'])
        #removing from registry
        return self.getProcessingErrors(errorLayer)

    # def execute(self):
    #     """
    #     Reimplementation of the execute method from the parent class
    #     """
    #     #abstract method. MUST be reimplemented.
    #     QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    #     self.startTimeCount()
    #     try:
    #         self.setStatus(self.tr('Running'), 3) #now I'm running!
    #         self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
    #         classesWithElem = self.parameters['Classes']
    #         if len(classesWithElem) == 0:
    #             self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
    #             QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    #             return 1
    #         error = False
    #         for key in classesWithElem:
    #             self.startTimeCount()
    #             # preparation
    #             classAndGeom = self.classesWithElemDict[key]
    #             lyr = self.loadLayerBeforeValidationProcess(classAndGeom)
    #             # specific EPSG search
    #             parameters = {'tableSchema': classAndGeom['tableSchema'], 'tableName': classAndGeom['tableName'], 'geometryColumn': classAndGeom['geom']}
    #             srid = self.abstractDb.findEPSG(parameters=parameters)                        

    #             # running the process in the temp table
    #             result = self.runProcessinAlg(lyr)
    #             # storing flags
    #             if len(result) > 0:
    #                 error = True
    #                 recordList = []
    #                 for tupple in result:
    #                     recordList.append((classAndGeom['tableSchema'] +'.'+classAndGeom['tableName'], tupple[0], self.tr('Snapping error.'), tupple[1], classAndGeom['geom'])) 
    #                 numberOfProblems = self.addFlag(recordList)
    #                 QgsMessageLog.logMessage(str(numberOfProblems) + self.tr(' feature(s) of layer ') + classAndGeom['tableName'] + self.tr(' with snapping errors. Check flags.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    #             else:
    #                 QgsMessageLog.logMessage(self.tr('There are no snapping errors on ') + classAndGeom['tableName'] +'.', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    #             self.logLayerTime(classAndGeom['tableSchema']+'.'+classAndGeom['tableName'])
    #         if error:
    #             self.setStatus(self.tr('There are snapping errors. Check log.'), 4) #Finished with errors
    #         else:
    #             self.setStatus(self.tr('There are no snapping errors.'), 1) #Finished
    #         return 1
    #     except Exception as e:
    #         QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    #         self.finishedWithError()
    #         return 0

    def execute(self):
            """
            Reimplementation of the execute method from the parent class
            """
            QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr('Process.\n'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            try:
                self.setStatus(self.tr('Running'), 3) #now I'm running!
                classesWithElem = self.parameters['Classes']
                snap = self.parameters['Snap']
                self.startTimeCount()
                if len(classesWithElem) == 0:
                    self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                    QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                    return 1
                for key in classesWithElem:
                    # preparation
                    classAndGeom = self.classesWithElemDict[key]
                    localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                    localProgress.step()
                    processTableName, lyr, keyColumn = self.prepareExecution(classAndGeom)
                    localProgress.step()
                    # running the process
                    localProgress = ProgressWidget(0, 1, self.tr('Running process for ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                    localProgress.step()
                    self.abstractDb.recursiveSnap([processTableName], snap, classAndGeom['geom'], keyColumn)
                    localProgress.step()
                    self.logLayerTime(key) #check this time later (I guess time will be counted twice due to postProcess)
                    # finalization
                    self.postProcessSteps(processTableName, lyr)
                    QgsMessageLog.logMessage(self.tr('All features from {} were snapped.').format(key), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                self.setStatus(self.tr('All features were snapped.'), 1) #Finished
                return 1
            except Exception as e:
                QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                self.finishedWithError()
                return 0            
