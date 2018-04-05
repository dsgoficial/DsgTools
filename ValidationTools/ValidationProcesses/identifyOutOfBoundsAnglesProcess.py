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
from qgis.core import QgsMessageLog, QgsFeature, QgsGeometry, QgsVertexId, QGis
import math
from math import pi
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.CustomWidgets.progressWidget import ProgressWidget
from DsgTools.GeometricTools.DsgGeometryHandler import DsgGeometryHandler

class IdentifyOutOfBoundsAnglesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating = False, withElements = True):
        """
        Constructor
        """
        super(IdentifyOutOfBoundsAnglesProcess, self).__init__(postgisDb, iface, instantiating, withElements)
        self.processAlias = self.tr('Identify Out Of Bounds Angles')
        self.geometryHandler = DsgGeometryHandler(iface, parent = iface.mapCanvas())
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a', 'l'], withElements = withElements, excludeValidation = True)
            # adjusting process parameters
            interfaceDictList = []
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDictList.append({self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType})
            self.parameters = {'Angle': 10.0, 'Classes': interfaceDictList, 'Only Selected':False}
    
    def getOutOfBoundsAngleInPolygon(self, feat, geometry_column, part, angle, outOfBoundsList):
        for linearRing in part.asPolygon():
            linearRing = self.geometryHandler.getClockWiseList(linearRing)
            nVertex = len(linearRing)-1
            for i in xrange(nVertex):
                vertexAngle = (linearRing[i].azimuth(linearRing[(i-1)%nVertex]) - linearRing[i].azimuth(linearRing[(i+1)%nVertex]) + 360) % 360
                if vertexAngle % 360 < angle:
                    geomDict = {'angle':vertexAngle % 360  ,'feat_id':feat.id(), 'geometry_column': geometry_column, 'geom':QgsGeometry.fromPoint(linearRing[i])}
                    outOfBoundsList.append(geomDict)
                elif 360 - vertexAngle < angle:
                    geomDict = {'angle': (360 - vertexAngle)  ,'feat_id':feat.id(), 'geometry_column': geometry_column, 'geom':QgsGeometry.fromPoint(linearRing[i])}
                    outOfBoundsList.append(geomDict)
    
    def getOutOfBoundsAngleInLine(self, feat, geometry_column, part, angle, outOfBoundsList):
        line = part.asPolyline()
        nVertex = len(line)-1
        for i in xrange(1,nVertex):
            vertexAngle = (line[i].azimuth(line[(i-1)%nVertex]) - line[i].azimuth(line[(i+1)%nVertex]) + 360) % 360
            if vertexAngle % 360 < angle:
                geomDict = {'angle':vertexAngle % 360  ,'feat_id':feat.id(), 'geometry_column': geometry_column, 'geom':QgsGeometry.fromPoint(line[i])}
                outOfBoundsList.append(geomDict)
            elif 360 - vertexAngle < angle:
                geomDict = {'angle': (360 - vertexAngle)  ,'feat_id':feat.id(), 'geometry_column': geometry_column, 'geom':QgsGeometry.fromPoint(line[i])}
                outOfBoundsList.append(geomDict)
    
    def getOutOfBoundsAngle(self, feat, angle, geometry_column):
        outOfBoundsList = []
        geom = feat.geometry()
        for part in geom.asGeometryCollection():
            if part.type() == QGis.Polygon:
                self.getOutOfBoundsAngleInPolygon(feat, geometry_column, part, angle, outOfBoundsList)
            if part.type() == QGis.Line:
                self.getOutOfBoundsAngleInLine(feat, geometry_column, part, angle, outOfBoundsList)
            
        return outOfBoundsList
    
    def getOutOfBoundsAngleList(self, lyr, angle, geometry_column, onlySelected = False):
        featureList, size = self.getFeatures(lyr, onlySelected = onlySelected)
        outOfBoundsList = []
        for feat in featureList:
            outOfBoundsList += self.getOutOfBoundsAngle(feat, angle, geometry_column)
        return outOfBoundsList
    
    def buildAndRaiseOutOfBoundsFlag(self, tableSchema, tableName, flagLyr, geomDictList):
        """
        
        """
        featFlagList = []
        for geomDict in geomDictList:
            # reason = self.tr('Angle of {0} degrees is out of bound.').format(geomDict['angle'])
            reason = '{0}'.format(geomDict['angle'])
            newFlag = self.buildFlagFeature(flagLyr, self.processName, tableSchema, tableName, geomDict['feat_id'], geomDict['geometry_column'], geomDict['geom'], reason)
            featFlagList.append(newFlag)
        return self.raiseVectorFlags(flagLyr, featFlagList)


    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithElem = self.parameters['Classes']
            self.startTimeCount()
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            tol = self.parameters['Angle']
            error = False
            flagLyr = self.getFlagLyr(0)
            for key in classesWithElem:
                # preparation
                classAndGeom = self.classesWithElemDict[key]
                lyr = self.loadLayerBeforeValidationProcess(classAndGeom)
                # running the process
                localProgress = ProgressWidget(0, 1, self.tr('Running process on ')+classAndGeom['tableName'], parent=self.iface.mapCanvas())
                localProgress.step()
                result = self.getOutOfBoundsAngleList(lyr, tol, classAndGeom['geom'], onlySelected = self.parameters['Only Selected'])
                localProgress.step()
                
                # storing flags
                if len(result) > 0:
                    numberOfProblems = self.buildAndRaiseOutOfBoundsFlag(classAndGeom['tableSchema'], classAndGeom['tableName'], flagLyr, result)
                    QgsMessageLog.logMessage(str(numberOfProblems) + self.tr(' features from') + classAndGeom['tableName'] + self.tr(' have out of bounds angle(s). Check flags.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                else:
                    QgsMessageLog.logMessage(self.tr('There are no out of bounds angles on ') + classAndGeom['tableName'] + '.', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                self.logLayerTime(classAndGeom['tableSchema']+'.'+classAndGeom['tableName'])
            if error:
                self.setStatus(self.tr('There are features with angles out of bounds. Check log.'), 4) #Finished with errors
            else:
                self.setStatus(self.tr('There are no features with angles out of bounds.'), 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0