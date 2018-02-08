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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsMapLayerRegistry, QgsGeometry, QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, QgsFeature, QgsSpatialIndex, QgsPoint
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
            self.parameters = {'Snap': 1.0, 'MinArea': 0.001, 'Classes': interfaceDictList, 'Only Selected':False, 'Only First Order Lines':True}
            self.identifyDangles = IdentifyDanglesProcess(postgisDb, iface, instantiating = True)
            self.identifyDangles.parameters = self.parameters
    
    def preProcess(self):
        return [self.tr('Snap to Grid (adjust coordinates precision)'), self.tr('Identify Small Lines'), self.tr('Remove Small Lines')]

    def postProcess(self):
         return [self.tr('Clean Geometries'), self.tr('Identify Duplicated Geometries'), self.tr('Remove Duplicated Elements'), self.tr('Identify Small Lines'), self.tr('Remove Small Lines'), self.tr('Identify Small Lines')] #more than one post process (this is treated in validationManager)

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
                return 1
            for lyrKey in lyrListKeys:
                self.startTimeCount()
                # preparation
                cl = self.classesWithElemDict[lyrKey]
                lyr = self.loadLayerBeforeValidationProcess(cl)
                if self.parameters['Only Selected']:
                    featureDict = {i.id():i for i in lyr.selectedFeatures()}
                else:
                    featureDict = {i.id():i for i in lyr.getFeatures()}
                featureList = featureDict.values()
                if featureList == []:
                    self.setStatus(self.tr('Empty layer or empty selection!. Nothing to be done.'), 1) #Finished
                    QgsMessageLog.logMessage(self.tr('Layer {0} is empty or there are no selected features!. Nothing to be done.').format(lyr.name()), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                    continue
                spatialIdx = self.buildSpatialIndex(featureList)
                size = len(featureList)                   
                endVerticesDict = self.identifyDangles.buildInitialAndEndPointDict(featureList, cl['tableSchema'], cl['tableName'])
                pointList = self.identifyDangles.searchDanglesOnPointDict(endVerticesDict, cl['tableSchema'], cl['tableName'])
                filteredPointList = self.identifyDangles.filterPointListWithFilterLayer(pointList, lyr, self.parameters['Snap'], isRefLyr = True, ignoreNotSplit = False)
                extendedList = self.extendLines(featureDict, spatialIdx, filteredPointList, endVerticesDict, self.parameters['Snap'])
                lyr.beginEditCommand('Extending lines')
                for feat in extendedList:
                    lyr.updateFeature(feat)
                lyr.endEditCommand()
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
        updateDict = dict()
        for point in pointList:
            qgisPoint = QgsGeometry.fromPoint(point)
            #calculate buffer
            buffer = qgisPoint.buffer(d, -1)
            bufferBB = buffer.boundingBox()
            #get the id of the candidate to be prolonged
            prolongId = endVerticesDict[point][0]
            #get the line to be prolonged from featId
            extendLineCandidate = featureDict[prolongId]
            for id in spatialIdx.intersects(bufferBB):
                if buffer.intersects(featureDict[id].geometry()):
                   #if we have entered this if, we extend the line and break
                   #extended line. After trying to extend, we must check if the extended line intersects the current id,
                   #if it does, apply extension.
                   extendedLine = self.extendLine(extendLineCandidate.geometry(), qgisPoint, d)
                   #false positive case
                   if extendedLine != extendLineCandidate.geometry() and extendedLine.intersects(featureDict[id].geometry()):
                       #update feat geom
                       extendLineCandidate.setGeometry(extendedLine)
                       updateDict[extendLineCandidate.id()] = extendLineCandidate
                       break
        return updateDict.values()
    
    def extendLine(self, geom, referencePoint, d):
        """
        1. Get the segment that must be extended;
        2. Determine if the referencePoint (QgsPoint) is an End Point os a Start Point;
        3. Create a new segment
        """
        isMultipart = geom.isMultipart()
        segment = self.getSegment(geom, referencePoint)
        if segment == []:
            return geom
        if QgsGeometry.fromPoint(segment[1]).equals(referencePoint):
            extendedPoint = self.getExtendedPoint(segment[0], segment[1], d)
            newLine = QgsGeometry.fromPolyline([segment[1], extendedPoint])
        else:
            extendedPoint = self.getExtendedPoint(segment[1], segment[0], d)
            newLine = QgsGeometry.fromPolyline([segment[0], extendedPoint])
        if isMultipart:
            newLine.convertToMultiType()
        newGeom = geom.combine(newLine)
        newGeom.mergeLines()
        return newGeom
    
    def getSegment(self, geom, referencePoint):
        if geom.isMultipart():
            multiLine = geom.asMultiPolyline()
            for i in xrange(len(multiLine)):
                line = multiLine[i]
                lineSize = len(line)
                if line[0] == referencePoint.asPoint():
                    if lineSize == 2:
                        return line
                    else:
                        return line[0::2]
                if line[-1] == referencePoint.asPoint():
                    if lineSize == 2:
                        return line
                    else:
                        return line[-2:]
        else:
            line = geom.asPolyline()
            lineSize = len(line)
            if line[0] == referencePoint.asPoint():
                if lineSize == 2:
                    return line
                else:
                    return line[0::2]
            if line[-1] == referencePoint.asPoint():
                if lineSize == 2:
                    return line
                else:
                    return line[-2:]
        return []
    
    def getExtendedPoint(self, startPoint, endPoint, d):
        """
        End Point C:
        C = startPoint + (startPoint - endPoint) * d / (distance from start to end point)
        """
        dAB = startPoint.distance(endPoint)
        Xc = endPoint.x() + (endPoint.x() - startPoint.x()) * d / dAB
        Yc = endPoint.y() + (endPoint.y() - startPoint.y()) * d / dAB
        return QgsPoint(Xc, Yc)
    