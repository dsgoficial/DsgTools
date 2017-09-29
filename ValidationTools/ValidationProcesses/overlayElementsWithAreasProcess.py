# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-09-28
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsMapLayerRegistry, QgsGeometry, QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, QgsFeature
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from collections import deque, OrderedDict
import processing, binascii

class OverlayElementsWithAreasProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Overlay Elements with Areas')
        
        if not self.instantiating:
            # getting tables with elements
            overlayAreasDictList = self.abstractDb.listGeomClassesFromDatabase(withElements=True, primitiveFilter = ['a'], getGeometryColumn=True)
            overlayAreas = ['{0}:{1}'.format(i['layerName'], i['geometryColumn']) for i in overlayAreasDictList]
            classesWithElemDictList = self.abstractDb.listGeomClassesFromDatabase(withElements=True, primitiveFilter = ['l','a'], getGeometryColumn=True)
            # creating a list of tuples (layer names, geometry columns)
            classesWithElem = ['{0}:{1}'.format(i['layerName'], i['geometryColumn']) for i in classesWithElemDictList]
            # adjusting process parameters
            self.opTypeDict = OrderedDict([(self.tr('Overlay and Keep Elements'),-1), (self.tr('Remove outside elements'),0), (self.tr('Remove inside elements'),1)])
            self.parameters = {'Snap': 1.0, 'MinArea': 0.001, 'Overlayer and Layers': (overlayAreas, classesWithElem), 'Overlay Type':deque(self.opTypeDict.keys())}
        
    def runProcessinAlg(self, layerA, layerB):
        """
        Runs the actual grass process
        """
        alg = 'grass7:v.overlay'

        #getting table extent (bounding box)
        extentA = layerA.extent()
        (xAmin, xAmax, yAmin, yAmax) = extentA.xMinimum(), extentA.xMaximum(), extentA.yMinimum(), extentA.yMaximum()
        extentB = layerB.extent()
        (xmin, xmax, ymin, ymax) = min(extentB.xMinimum(),xAmin), max(extentB.xMaximum(), xAmax), min(extentB.yMinimum(), yAmin), max(extentB.yMaximum(), yAmax)
        
        extent = '{0},{1},{2},{3}'.format(xmin, xmax, ymin, ymax)
        
        snap = self.parameters['Snap']
        minArea = self.parameters['MinArea']
        
        ret = processing.runalg(alg, layer, tools, threshold, extent, snap, minArea, None, None)
        if not ret:
            raise Exception(self.tr('Problem executing grass7:v.clean.advanced. Check your installed libs.\n'))
        
        #updating original layer
        outputLayer = processing.getObject(ret['output'])
        self.updateOriginalLayer(layer, outputLayer)

        #getting error flags
        errorLayer = processing.getObject(ret['error'])
        return self.getProcessingErrors(errorLayer)

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
            error = False
            for key in classesWithElem:
                # preparation
                classAndGeom = self.classesWithElemDict[key]
                lyr = self.loadLayerBeforeValidationProcess(classAndGeom)
                # specific EPSG search
                parameters = {'tableSchema': classAndGeom['tableSchema'], 'tableName': classAndGeom['tableName'], 'geometryColumn': classAndGeom['geom']}
                srid = self.abstractDb.findEPSG(parameters=parameters)                        

                # running the process in the temp table
                result = self.runProcessinAlg(lyr)
                
                # storing flags
                if len(result) > 0:
                    error = True
                    recordList = []
                    for tupple in result:
                        recordList.append(('{0}.{1}'.format(classAndGeom['tableSchema'], classAndGeom['tableName']), tupple[0], self.tr('Cleaning error.'), tupple[1], classAndGeom['geom']))
                    numberOfProblems = self.addFlag(recordList)
                    QgsMessageLog.logMessage(str(numberOfProblems) + self.tr(' feature(s) from ') + classAndGeom['lyrName'] + self.tr(' with cleaning errors. Check flags.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                else:
                    QgsMessageLog.logMessage(self.tr('There are no cleaning errors on ') + classAndGeom['lyrName'] +'.', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            if error:
                self.setStatus(self.tr('There are cleaning errors. Check log.'), 4) #Finished with errors
            else:
                self.setStatus(self.tr('There are no cleaning errors.'), 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0
