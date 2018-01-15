# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-09-29
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
                               (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : luizclaudio.andrade@eb.mil.br
                               borba.philipe@eb.mil.br
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
from qgis.core import QgsMessageLog, QgsGeometry, QgsFeatureRequest, QgsExpression, QgsFeature, QgsSpatialIndex, QGis, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsField

from PyQt4.QtCore import QVariant

from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.ValidationTools.ValidationProcesses.unbuildEarthCoveragePolygonsProcess import UnbuildEarthCoveragePolygonsProcess
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

from collections import deque, OrderedDict

import binascii

from collections import OrderedDict
class IdentifyDanglesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Identify Dangles')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a', 'l'], withElements=True, excludeValidation = True)
            # adjusting process parameters
            interfaceDict = dict()
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDict[key] = {self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType}
            # getting tables with elements
            self.linesWithElement = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['l'], withElements=True, excludeValidation = True)
            # adjusting process parameters
            interfaceLineDict = dict()
            for key in self.linesWithElement:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceLineDict[key] = {self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType}
            self.opTypeDict = OrderedDict([(self.tr('Consider dangle on unsegmented lines'),0), (self.tr('Ignore dangle on unsegmented lines'),1)])
            self.parameters = {'Only Selected':False, 'Search Radius':1.0, 'Layer and Filter Layers': OrderedDict({'referenceDictList':interfaceLineDict, 'layersDictList':interfaceDict}), 'Identification Type':deque(self.opTypeDict.keys())}
            self.unbuildProc = UnbuildEarthCoveragePolygonsProcess(postgisDb, iface, instantiating = True)
            self.unbuildProc.parameters = {'Snap': -1.0, 'MinArea': 0.001} #no snap and no small area
    
    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        self.startTimeCount()
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            refKey = self.parameters['Layer and Filter Layers'][0]
            classesWithElemKeys = self.parameters['Layer and Filter Layers'][1]
            if len(classesWithElemKeys) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1

            if not refKey:
                self.setStatus(self.tr('One layer must be selected! Stopping.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('One layer must be selected! Stopping.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            recordList = []
            # preparation
            refcl = self.classesWithElemDict[refKey]
            localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for {0}.{1}').format(refcl['tableSchema'], refcl['tableName']), parent=self.iface.mapCanvas())
            localProgress.step()
            reflyr = self.loadLayerBeforeValidationProcess(refcl)
            localProgress.step()

            #build seach dict
            endVerticesDict = self.buildInitialAndEndPointDict(reflyr, refcl['tableSchema'], refcl['tableName'])
            #search for dangles candidates
            pointList = self.searchDanglesOnPointDict(endVerticesDict, refcl['tableSchema'], refcl['tableName'])
            #build filter layer
            filterLayer = self.buildFilterLayer(reflyr)
            #filter pointList with filterLayer
            filteredPointList = self.filterPointListWithFilterLayer(pointList, filterLayer, self.parameters['Search Radius'])
            #build flag list with filtered points
            recordList = self.buildFlagList(filteredPointList, endVerticesDict, refcl['tableSchema'], refcl['tableName'], refcl['geom'])

            self.logLayerTime(refcl['tableSchema']+'.'+refcl['tableName'])

            if len(recordList) > 0:
                numberOfProblems = self.addFlag(recordList)
                msg = self.tr('{0} features have dangles. Check flags.').format(numberOfProblems)
                self.setStatus(msg, 4) #Finished with flags
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            else:
                msg = self.tr('There are no dangles.')
                self.setStatus(msg, 1) #Finished
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0            
    
    def buildInitialAndEndPointDict(self, lyr, tableSchema, tableName):
        """
        Calculates initial point and end point from each line from lyr.
        """
        if self.parameters['Only Selected']:
            featureList = lyr.selectedFeatures()
            size = len(featureList)
        else:
            featureList = lyr.getFeatures()
            size = len(lyr.allFeatureIds())
        localProgress = ProgressWidget(1, size, self.tr('Building search structure for {0}.{1}').format(tableSchema,tableName), parent=self.iface.mapCanvas())
        # start and end points dict
        endVerticesDict = {}
        # iterating over features to store start and end points
        for feat in featureList:
            geom = feat.geometry()
            if geom.isMultipart():
                multiLine = geom.asMultiPolyline()
                for j in xrange(len(multiLine)):
                    line = multiLine[j]
                    startPoint = line[0]
                    endPoint = line[len(line) - 1]
                    # storing start point in the dict
                    if startPoint not in endVerticesDict.keys():
                        endVerticesDict[startPoint] = []
                    endVerticesDict[startPoint].append(feat.id())
                    # storing end point in the dict
                    if endPoint not in endVerticesDict.keys():
                        endVerticesDict[endPoint] = []
                    endVerticesDict[endPoint].append(feat.id())
            else:
                line = geom.asPolyline()
                startPoint = line[0]
                endPoint = line[len(line) - 1]
                # storing start point in the dict
                if startPoint not in endVerticesDict.keys():
                    endVerticesDict[startPoint] = []
                endVerticesDict[startPoint].append(feat.id())
                # storing end point in the dict
                if endPoint not in endVerticesDict.keys():
                    endVerticesDict[endPoint] = []
                endVerticesDict[endPoint].append(feat.id())
            localProgress.step()
        return endVerticesDict
    
    def searchDanglesOnPointDict(self, endVerticesDict, tableSchema, tableName):
        """
        Counts the number of points on each endVerticesDict's key and returns a list of QgsPoint built from key candidate.
        """
        pointList = []
        # actual search for dangles
        localProgress = ProgressWidget(1, len(endVerticesDict.keys()), self.tr('Searching dangles on {0}.{1}').format(tableSchema, tableName), parent=self.iface.mapCanvas())
        for point in endVerticesDict.keys():
            # this means we only have one occurrence of point, therefore it is a dangle
            if len(endVerticesDict[point]) > 1:
                localProgress.step()
                continue
            pointList.append(point)
            localProgress.step()
        return pointList

    def getCoordinateTransformer(self, inputLyr, outputLyr):
        """
        Makes coordinate transformer
        """
        crsSrc = QgsCoordinateReferenceSystem(inputLyr.crs().authid())
        mapLayerCrs = outputLyr.crs()
        coordinateTransformer = QgsCoordinateTransform(mapLayerCrs, crsSrc)
        return coordinateTransformer

    def addFeaturesToFilterLayer(self, filterLyr, lyr):
        """
        Get all features from lyr and add it to filterLyr
        """
        #gets coordinate transformer
        coordinateTransformer = self.getCoordinateTransformer(filterLyr, lyr)
        #gets lyr features and stores only geometry into filterLyr
        featList = []
        for feat in lyr.getFeatures():
            newfeat = QgsFeature(filterLyr.pendingFields())
            newfeat['featid'] = feat.id()
            geom = feat.geometry()
            if not geom:
                continue
            geom.transform(coordinateTransformer)
            geom.convertToMultiType()
            newfeat.setGeometry(geom)
            featList.append(newfeat)
        filterLyr.addFeatures(featList, True)

    def buildFilterLayer(self, refLyr):
        """
        Buils one layer of filter lines.
        Build unified layer is not used because we do not care for attributes here, only geometry.
        refLyr elements are also added.
        """
        srid = refLyr.crs().authid().split(':')[-1]
        filterLyr = self.iface.addVectorLayer("{0}?crs=epsg:{1}".format(self.getGeometryTypeText(QGis.WKBMultiLineString),srid), "filterLyr", "memory")
        provider = filterLyr.dataProvider()
        filterLayersWithElemKeys = self.parameters['Layer and Filter Layers'][1]
        filterLyr.startEditing()
        filterLyr.beginEditCommand('Creating filter layer') #speedup
        fields = [QgsField('featid', QVariant.Int)]
        provider.addAttributes(fields)
        filterLyr.updateFields()
        for key in filterLayersWithElemKeys:
            clDict = self.classesWithElemDict[key]
            #loads lyr
            inputLyr = self.loadLayerBeforeValidationProcess(clDict)
            if inputLyr.geometryType() == QGis.Polygon:
                #uses makeBoundaries method from unbuildEarthCoveragePolygonsProcess to get candidate lines layer
                lyr = self.unbuildProc.makeBoundaries(inputLyr)
            else:
                lyr = inputLyr
            self.addFeaturesToFilterLayer(filterLyr, lyr)
        filterLyr.endEditCommand()
        filterLyr.commitChanges()
        return filterLyr

    def filterPointListWithFilterLayer(self, pointList, filterLayer, searchRadius):
        """
        Builds buffer areas from each point and evaluates the intersecting lines. If there are more than two intersections, it is a dangle.
        """
        spatialIdx, allFeatureDict = self.buildSpatialIndexAndIdDict(filterLayer)
        notDangleIndexList = []
        for i in range(len(pointList)):
            candidateCount = 0
            qgisPoint = QgsGeometry.fromPoint(pointList[i])
            #search radius to narrow down candidates
            buffer = qgisPoint.buffer(searchRadius, -1)
            bufferBB = buffer.boundingBox()
            #gets candidates from spatial index
            candidateIds = spatialIdx.intersects(bufferBB)
            #if there is only one feat in candidateIds, that means that it is not a dangle
            candidateNumber = len(candidateIds)
            for id in candidateIds:
                if qgisPoint.distance(allFeatureDict[id].geometry()) < 10**-9: #float problem, tried with intersects and touches and did not get results
                    notDangleIndexList.append(i)
                    break
        filteredDangleList = []
        for i in range(len(pointList)):
            if i not in notDangleIndexList:
                filteredDangleList.append(pointList[i])
        return filteredDangleList

    def filterPseudoDangles(self, pointList, filterLayer, searchRadius):
        spatialIdx, allFeatureDict = self.buildSpatialIndexAndIdDict(filterLayer)
        notDangleIndexList = []

    
    def buildSpatialIndexAndIdDict(self, inputLyr):
        """
        creates a spatial index for the centroid layer
        """
        spatialIdx = QgsSpatialIndex()
        idDict = {}
        for feat in inputLyr.getFeatures():
            spatialIdx.insertFeature(feat)
            idDict[feat.id()] = feat
        return spatialIdx, idDict

    def buildFlagList(self, pointList, endVerticesDict, tableSchema, tableName, geometryColumn):
        """
        Builds record list from pointList to raise flags.
        """
        recordList = []
        for point in pointList:
            geometry = binascii.hexlify(QgsGeometry.fromPoint(point).asWkb())
            featid = endVerticesDict[point][0]
            recordList.append(('{0}.{1}'.format(tableSchema, tableName), featid, self.tr('Dangle on {0}.{1}').format(tableSchema, tableName), geometry, geometryColumn))
        return recordList