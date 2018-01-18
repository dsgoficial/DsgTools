# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-01-18
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsMapLayerRegistry, QgsGeometry, QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, QgsFeature, QgsSpatialIndex
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.ValidationTools.ValidationProcesses.identifyDanglesProcess import IdentifyDanglesProcess
from collections import deque, OrderedDict
import processing, binascii

class LineOnLineOverlayProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Overlay Lines with Lines')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['l'], withElements=True, excludeValidation = True)
            # adjusting process parameters
            interfaceDictList = []
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDictList.append({self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType})
            self.parameters = {'Snap': 1.0, 'MinArea': 0.001, 'Classes': interfaceDictList, 'Only Selected':False}
            self.identifyDangles = IdentifyDanglesProcess(postgisDb, iface, instantiating = True)
            self.identifyDangles.parameters = self.parameters

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        self.startTimeCount()
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            lyrListKeys = self.parameters['Classes']
            if len(lyrListKeys) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            for lyrKey in lyrListKeys:
                # preparation
                cl = self.classesWithElemDict[lyrKey]
                lyr = self.loadLayerBeforeValidationProcess(cl)
                if self.parameters['Only Selected']:
                    featureDict = {i.id():i for i in lyr.selectedFeatures()}
                else:
                    featureDict = {i.id():i for i in lyr.getFeatures()}
                featureList = featureDict.values()
                spatialIdx = self.buildSpatialIndex(featureList)
                size = len(featureList)                   
                endVerticesDict = self.identifyDangles.buildInitialAndEndPointDict(featureList, cl['tableSchema'], cl['tableName'])
                pointList = self.identifyDangles.searchDanglesOnPointDict(endVerticesDict, cl['tableSchema'], cl['tableName'])
                extendedList = self.extendLines(featureDict, spatialIdx, pointList, endVerticesDict, self.parameters['Snap'])
                result = []
                
                # storing flags
                if len(result) > 0:
                    error = True
                    recordList = []
                    for tupple in result:
                        recordList.append((cl, tupple[0], self.tr('Overlay error.'), tupple[1], cl['geom']))
                    numberOfProblems = self.addFlag(recordList)
                    QgsMessageLog.logMessage(str(numberOfProblems) + self.tr(' feature(s) from {0}.{1}').format(cl['tableSchema'], cl['tableName']) + self.tr(' with overlay errors. Check flags.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                else:
                    QgsMessageLog.logMessage(self.tr('All features from {0}.{1} overlayed.').format(cl['tableSchema'], cl['tableName']), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                self.logLayerTime(cl['tableSchema'] + '.' + cl['tableName'])
            if error:
                self.setStatus(self.tr('There are overlay errors. Check log.'), 4) #Finished with errors
            else:
                self.setStatus(self.tr('Line on Line Overlay process complete.'), 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0
    
    def buildSpatialIndex(self, featureList):
        """
        Spatial Indexing for features
        """
        spatialIdx = QgsSpatialIndex()
        for feat in featureList:
            spatialIdx.insertFeature(feat)
        return spatialIdx
    
    def extendLines(self, featureDict, spatialIdx, pointList, endVerticesDict, d):
        """
        Extends lines that are close from other lines. 
        It has the following steps:
        1. Iterate over pointList to get the window search;
        2. For each point, get the id of the containing line, it will be the line to be prolonged;
        3. Get a buffer of radius d and its bounding box;
        4. Get on spatialIdx the candidates those whose bb intersects buffer bb, except the line to be prolonged;
        5. Assess if there is at least one line that intersect the buffer, if there is, the line must be prolonged.
        """
        #1. Iterate over pointList to get the window search
        for point in pointList:
            qgisPoint = QgsGeometry.fromPoint(point)
            #calculate buffer
            buffer = qgisPoint.buffer()
            bufferBB = buffer.boundingBox()
            #get the id of the candidate to be prolonged
            prolongId = endVerticesDict[point][0]
            #get the line to be prolonged from featId
            extendLineCandidate = featureDict[prolongId]
            for id in spatialIdx.intersects(bufferBB):
                if buffer.intersects(featureDict[id].geometry()) and \
                   (qgisPoint.distance(featureDict[id].geometry()) < 10**-9 or \
                   qgisPoint.intersects(featureDict[id].geometry())):
                   #if we have entered this if, we extend the line and break
                   #extend line
                   extendedLine = self.extendLine(extendLineCandidate.geom(), qgisPoint, d)
                   #update feat geom
                   extendLineCandidate.setGeom(extendedLine)
                   break
        return featureDict
    
    def extendLine(self, lineGeom, referencePoint, d):
        """
        1. Get the segment that must be extended;

        """
        pass
    