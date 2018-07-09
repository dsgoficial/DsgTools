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
from builtins import str
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsGeometry, \
                      QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, \
                      QgsFeature, Qgis, QgsProcessingUtils
from DsgTools.core.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
import processing

class CleanGeometriesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False, withElements = True):
        """
        Constructor
        """
        super(CleanGeometriesProcess,self).__init__(postgisDb, iface, instantiating, withElements)
        self.processAlias = self.tr('Clean Geometries')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a', 'l'], withElements=withElements, excludeValidation = True)
            # adjusting process parameters
            interfaceDictList = []
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDictList.append({self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType})
            self.parameters = {'Snap': 1.0, 'MinArea': 0.001, 'Classes': interfaceDictList, 'Only Selected':False}
        
    def runProcessinAlg(self, layer):
        """
        Runs the actual grass process
        """
        alg = 'grass7:v.clean' #api changed, used to be v.clean.advanced

        #setting tools
        tools = 'rmsa,break,rmdupl,rmdangle'
        threshold = -1

        #getting table extent (bounding box)
        extent = layer.extent()
        (xmin, xmax, ymin, ymax) = extent.xMinimum(), extent.xMaximum(), extent.yMinimum(), extent.yMaximum()
        extent = '{0},{1},{2},{3}'.format(xmin, xmax, ymin, ymax)
        
        snap = self.parameters['Snap']
        minArea = self.parameters['MinArea']
        
        ret = processing.runalg(alg, layer, tools, threshold, extent, snap, minArea, None, None)
        if not ret:
            raise Exception(self.tr('Problem executing grass7:v.clean.advanced. Check your installed libs.\n'))
        
        #updating original layer
        outputLayer = processing.getObject(ret['output'])
        #self.updateOriginalLayerV2(layer, outputLayer)

        #getting error flags
        errorLayer = processing.getObject(ret['error'])
        return self.getProcessingErrors(errorLayer), outputLayer

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
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", Qgis.Critical)
                return 1
            error = False
            for key in classesWithElem:
                # preparation
                classAndGeom = self.classesWithElemDict[key]
                lyr = self.loadLayerBeforeValidationProcess(classAndGeom)
                # specific EPSG search
                parameters = {'tableSchema': classAndGeom['tableSchema'], 'tableName': classAndGeom['tableName'], 'geometryColumn': classAndGeom['geom']}
                srid = self.abstractDb.findEPSG(parameters=parameters)                        

                # running the process in the temp table
                coverage = self.createUnifiedLayer([lyr])
                result, output = self.runProcessinAlg(coverage)
                self.splitUnifiedLayer(output, [lyr])
                try:
                    QgsProject.instance().removeMapLayer(coverage.id())
                except:
                    QgsMessageLog.logMessage(self.tr('Error while trying to remove coverage layer.'), "DSG Tools Plugin", Qgis.Critical)
                
                # storing flags
                if len(result) > 0:
                    error = True
                    recordList = []
                    for tupple in result:
                        recordList.append(('{0}.{1}'.format(classAndGeom['tableSchema'], classAndGeom['tableName']), tupple[0], self.tr('Cleaning error.'), tupple[1], classAndGeom['geom']))
                    numberOfProblems = self.addFlag(recordList)
                    QgsMessageLog.logMessage(str(numberOfProblems) + self.tr(' feature(s) from ') + classAndGeom['lyrName'] + self.tr(' with cleaning errors. Check flags.'), "DSG Tools Plugin", Qgis.Critical)
                else:
                    QgsMessageLog.logMessage(self.tr('There are no cleaning errors on ') + classAndGeom['lyrName'] +'.', "DSG Tools Plugin", Qgis.Critical)
                self.logLayerTime(classAndGeom['lyrName'])
            if error:
                self.setStatus(self.tr('There are cleaning errors. Check log.'), 4) #Finished with errors
            else:
                self.setStatus(self.tr('There are no cleaning errors.'), 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
            self.finishedWithError()
            return 0
