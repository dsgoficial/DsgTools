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
from builtins import range
from qgis.core import QgsMessageLog, QgsFeature, QgsGeometry, QgsVertexId, Qgis
from DsgTools.core.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess, ValidationAlgorithm
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler

from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsFeature,
                       QgsDataSourceUri,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsWkbTypes,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterNumber,
                       QgsWkbTypes)

class IdentifyOutOfBoundsAnglesAlgorithm(ValidationAlgorithm):
    FLAGS = 'FLAGS'
    INPUT = 'INPUT'
    SELECTED = 'SELECTED'
    TOLERANCE = 'TOLERANCE'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorLine, QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE,
                self.tr('Minimum angle'),
                minValue=0,
                defaultValue=10
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr('Flag layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        geometryHandler = GeometryHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        tol = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.Point, context)
        # Compute the number of steps to display within the progress bar and
        # get features from source
        featureList, total = self.getIteratorAndFeatureCount(inputLyr)           

        for current, feat in enumerate(featureList):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
            outOfBoundsList = geometryHandler.getOutOfBoundsAngle(feat, tol)
            if outOfBoundsList:
                for item in outOfBoundsList:
                    flagText = self.tr('Feature from layer {0} with id={1} has angle of value {2} degrees, which is lesser than the tolerance of {3} degrees.').format(inputLyr.name(), item['feat_id'], item['angle'], tol)
                    self.flagFeature(item['geom'], flagText)      
            # Update the progress bar
            feedback.setProgress(int(current * total))

        return {self.FLAGS: self.flagSink}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifyoutofboundsangles'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Out Of Bounds Angles')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Validation Tools')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Validation Tools'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return IdentifyOutOfBoundsAnglesAlgorithm()


class IdentifyOutOfBoundsAnglesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating = False, withElements = True):
        """
        Constructor
        """
        super(IdentifyOutOfBoundsAnglesProcess, self).__init__(postgisDb, iface, instantiating, withElements)
        self.processCategory = 'identification'
        self.processAlias = self.tr('Identify Out Of Bounds Angles')
        self.geometryHandler = GeometryHandler(iface, parent = iface.mapCanvas())
        
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
            for i in range(nVertex):
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
        for i in range(1,nVertex):
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
            if part.type() == Qgis.Polygon:
                self.getOutOfBoundsAngleInPolygon(feat, geometry_column, part, angle, outOfBoundsList)
            if part.type() == Qgis.Line:
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
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", Qgis.Critical)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithElem = self.parameters['Classes']
            self.startTimeCount()
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", Qgis.Critical)
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
                    QgsMessageLog.logMessage(str(numberOfProblems) + self.tr(' features from') + classAndGeom['tableName'] + self.tr(' have out of bounds angle(s). Check flags.'), "DSG Tools Plugin", Qgis.Critical)
                else:
                    QgsMessageLog.logMessage(self.tr('There are no out of bounds angles on ') + classAndGeom['tableName'] + '.', "DSG Tools Plugin", Qgis.Critical)
                self.logLayerTime(classAndGeom['tableSchema']+'.'+classAndGeom['tableName'])
            if error:
                self.setStatus(self.tr('There are features with angles out of bounds. Check log.'), 4) #Finished with errors
            else:
                self.setStatus(self.tr('There are no features with angles out of bounds.'), 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
            self.finishedWithError()
            return 0