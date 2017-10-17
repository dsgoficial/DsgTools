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
            self.overlayElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a'], withElements=True, excludeValidation = True)
            # adjusting overlayer process parameters
            overlayInterfaceDict = dict()
            for key in self.overlayElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                overlayInterfaceDict[key] = {self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType}            
            #getting overlayees
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a', 'l'], withElements=True, excludeValidation = True)
            # adjusting process parameters
            interfaceDict = dict()
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDict[key] = {self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType}
            self.opTypeDict = OrderedDict([(self.tr('Overlay and Keep Elements'),-1), (self.tr('Remove outside elements'),0), (self.tr('Remove inside elements'),1)])
            self.parameters = {'Snap': 1.0, 'MinArea': 0.001, 'Overlayer and Layers': OrderedDict({'referenceDictList':overlayInterfaceDict, 'layersDictList':interfaceDict}), 'Overlay Type':deque(self.opTypeDict.keys())}

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            overlayerKey, lyrListKeys = self.parameters['Overlayer and Layers']
            if len(lyrListKeys) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            if not overlayerKey:
                self.setStatus(self.tr('One overlayer must be selected! Stopping.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('One reference must be selected! Stopping.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            error = False
            overlayer = self.overlayElemDict[overlayerKey]
            overLyr = self.loadLayerBeforeValidationProcess(overlayer)
            for lyrKey in lyrListKeys:
                # preparation
                cl = self.classesWithElemDict[lyrKey]
                lyr = self.loadLayerBeforeValidationProcess(cl)                   

                # running the process in the temp table
                result = self.runProcessinAlg(lyr, overLyr)
                
                # storing flags
                if len(result) > 0:
                    error = True
                    recordList = []
                    for tupple in result:
                        recordList.append((cl, tupple[0], self.tr('Overlay error.'), tupple[1], cl['geom']))
                    numberOfProblems = self.addFlag(recordList)
                    QgsMessageLog.logMessage(str(numberOfProblems) + self.tr(' feature(s) from {0}.{1}').format(cl['tableSchema'], cl['tableName']) + self.tr(' with overlay errors. Check flags.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                else:
                    QgsMessageLog.logMessage(self.tr('All features from {0}.{1} overlayed to elements from {2}.{3}.').format(cl['tableSchema'], cl['tableName'], overlayer['tableSchema'], overlayer['tableName']), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            if error:
                self.setStatus(self.tr('There are overlay errors. Check log.'), 4) #Finished with errors
            else:
                self.setStatus(self.tr('Overlay process complete.'), 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0

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
        overlayType = self.opTypeDict[self.parameters['Overlay Type']]
        inputType = layerA.geometryType()
        
        ret = processing.runalg(alg, layerA, inputType, layerB, overlayType, False, extent, snap, minArea, inputType, None)
        if not ret:
            raise Exception(self.tr('Problem executing grass7:v.overlay. Check your installed libs.\n'))
        
        #updating original layer
        outputLayer = processing.getObject(ret['output'])
        outputLayer.startEditing()
        for field in outputLayer.pendingFields():
            if 'a_' == field.name()[0:2]:
                idx = outputLayer.fieldNameIndex(field.name())
                outputLayer.renameAttribute(idx, field.name()[2::])
        self.updateOriginalLayer(layerA, outputLayer)

        #getting error flags
        if 'error' in ret.keys():
            errorLayer = processing.getObject(ret['error'])
            return self.getProcessingErrors(errorLayer)