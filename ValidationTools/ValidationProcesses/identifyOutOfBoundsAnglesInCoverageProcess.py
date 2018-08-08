# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-06-08
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
from qgis.core import QgsMessageLog, QgsFeature, QgsGeometry, QgsVertexId, QGis, QgsMapLayerRegistry
import math, processing
from math import pi
from itertools import combinations
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.CustomWidgets.progressWidget import ProgressWidget
from DsgTools.GeometricTools.DsgGeometryHandler import DsgGeometryHandler

class IdentifyOutOfBoundsAnglesInCoverageProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(IdentifyOutOfBoundsAnglesInCoverageProcess,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Identify Out Of Bounds Angles in Coverage')
        self.geometryHandler = DsgGeometryHandler(iface, parent = iface.mapCanvas())
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a', 'l'], withElements=True, excludeValidation = True)
            # adjusting process parameters
            interfaceDictList = []
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDictList.append({self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType})
            self.parameters = {'Angle': 10.0, 'Classes': interfaceDictList}
    
    def preProcess(self):
        """
        Gets the process that should be execute before this one
        """
        return self.tr('Identify Out Of Bounds Angles')
    
    def getLineEdges(self, coverageLyr):
        extent = coverageLyr.extent()
        (xmin, xmax, ymin, ymax) = extent.xMinimum(), extent.xMaximum(), extent.yMinimum(), extent.yMaximum()
        extent = '{0},{1},{2},{3}'.format(xmin, xmax, ymin, ymax)
        grass_output =processing.runalg('grass7:v.clean.advanced', coverageLyr,'break,rmdupl',-1, extent, -1, 0.0001, None, None)
        if not grass_output:
            raise Exception(self.tr('Problem executing grass7:v.clean.advanced. Check your installed libs.\n'))
        return processing.getObject(grass_output['output'])
    
    def getSegmentDict(self, lineLyr):
        segmentDict = dict()
        geomList = []
        for feat in lineLyr.getFeatures():
            geom = feat.geometry()
            if geom not in geomList:
                geomList.append(geom)
                lineList = geom.asPolyline()
                if lineList[0] not in segmentDict:
                    segmentDict[lineList[0]] = []
                segmentDict[lineList[0]].append(QgsGeometry.fromPolyline([lineList[0], lineList[1]]))
                if lineList[-1] not in segmentDict:
                    segmentDict[lineList[-1]] = []
                segmentDict[lineList[-1]].append(QgsGeometry.fromPolyline([lineList[-1], lineList[-2]]))
        return segmentDict
    
    def getAngleBetweenSegments(self, part):
        line = part.asPolyline()
        vertexAngle = (line[1].azimuth(line[0]) - line[1].azimuth(line[2]) + 360)
        vertexAngle = math.fmod(vertexAngle, 360)
        if vertexAngle > 180:
            vertexAngle = 360 - vertexAngle
        return vertexAngle

    def getOutOfBountsAngleInSegmentList(self, segmentList, angle):
        for line1, line2 in combinations(segmentList, 2):
            geom = line1.combine(line2)
            part = geom.mergeLines()
            if len(part.asPolyline()) > 2:
                vertexAngle = self.getAngleBetweenSegments(part)
                if vertexAngle < angle:
                    return vertexAngle
        return None
    
    def getOutOfBoundsAngleList(self, coverageLines, angle):
        lineLyr = self.getLineEdges(coverageLines)
        segmentDict = self.getSegmentDict(lineLyr)
        errorList = []
        for point, segmentList in segmentDict.iteritems():
            if len(segmentList) > 1:
                vertexAngle = self.getOutOfBountsAngleInSegmentList(segmentList, angle)
                if vertexAngle:
                    errorList.append((vertexAngle, point))
        return errorList

    def buildAndRaiseOutOfBoundsFlag(self, flagLyr, geomTupleList):
        """
        
        """
        featFlagList = []
        for angle, point in geomTupleList:
            # reason = self.tr('Angle of {0} degrees is out of bound.').format(geomDict['angle'])
            reason = self.tr('Angle out of bounds ({0:.2f} deg)').format(angle)
            newFlag = self.buildFlagFeature(flagLyr, self.processName, 'validation', 'coverage', -1, 'geom', QgsGeometry.fromPoint(point), reason)
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
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            self.startTimeCount()
            tol = self.parameters['Angle']
            error = False
            flagLyr = self.getFlagLyr(0)
            classlist = []
            for key in classesWithElem:
                # preparation
                classAndGeom = self.classesWithElemDict[key]
                lyr = self.loadLayerBeforeValidationProcess(classAndGeom)
                classlist.append(lyr)
            coverage = self.createUnifiedLineLayer(classlist)
            result = self.getOutOfBoundsAngleList(coverage, tol)
            try:
                QgsMapLayerRegistry.instance().removeMapLayer(coverage.id())
            except:
                QgsMessageLog.logMessage(self.tr('Error while trying to remove coverage layer.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            # storing flags
            if len(result) > 0:
                error = True
                numberOfProblems = self.buildAndRaiseOutOfBoundsFlag(flagLyr, result)
                QgsMessageLog.logMessage(self.tr('{0} angles between coverage features have out of bounds angle(s). Check flags.').format(numberOfProblems), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            else:
                QgsMessageLog.logMessage(self.tr('There are no out of bounds angles between features from coverage.') , "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            if error:
                self.setStatus(self.tr('Error while checking angles. Check log.'), 4) #Finished with errors
            else:
                self.setStatus(self.tr('There are no features with angles out of bounds.'), 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0