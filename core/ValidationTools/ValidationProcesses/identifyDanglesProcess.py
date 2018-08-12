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
from builtins import range
from qgis.core import QgsMessageLog, QgsGeometry, QgsFeatureRequest, QgsExpression, \
                      QgsFeature, QgsSpatialIndex, Qgis, QgsCoordinateReferenceSystem, \
                      QgsCoordinateTransform, QgsField, QgsFeatureIterator, QgsProject, \
                      Qgis, QgsWkbTypes

from qgis.PyQt.QtCore import QVariant

from DsgTools.core.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess

from collections import deque, OrderedDict

from DsgTools.core.ValidationTools.ValidationProcesses.validationProcess import ValidationAlgorithm, ValidationProcess
from DsgTools.core.GeometricTools.layerHandler import LayerHandler

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
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber)

class IdentifyDanglesAlgorithm(ValidationAlgorithm):
    INPUT = 'INPUT'
    SELECTED = 'SELECTED'
    TOLERANCE = 'TOLERANCE'
    LINEFILTERLAYERS = 'LINEFILTERLAYERS'
    POLYGONFILTERLAYERS = 'POLYGONFILTERLAYERS'
    TYPE = 'TYPE'
    IGNOREINNER = 'IGNOREINNER'
    FLAGS = 'FLAGS'
    

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorLine ]
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
                self.tr('Search radius'),
                minValue=0,
                defaultValue=2
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.LINEFILTERLAYERS,
                self.tr('Linestring Filter Layers'),
                QgsProcessing.TypeVectorLine,
                optional = True
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.LINEFILTERLAYERS,
                self.tr('Polygon Filter Layers'),
                QgsProcessing.TypeVectorPolygon,
                optional = True
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.TYPE,
                self.tr('Identification Type'),
                self.tr('Ignore dangle on unsegmented lines'),
                defaultValue = False
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNOREINNER,
                self.tr('Ignore search radius on inner layer search'),
                defaultValue = False
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

        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        searchRadius = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        lineFilterLyrList = self.parameterAsLayerList(parameters, self.LINEFILTERLAYERS, context)
        polygonFilterLyrList = self.parameterAsLayerList(parameters, self.POLYGONFILTERLAYERS, context)
        ignoreNotSplit = self.parameterAsBool(parameters, self.TYPE, context)
        ignoreInner = self.parameterAsBool(parameters, self.IGNOREINNER, context)
        self.prepareFlagSink(parameters, inputLyr, inputLyr.wkbType(), context)

        # Compute the number of steps to display within the progress bar and
        # get features from source
        featureList, total = self.getIteratorAndFeatureCount(inputLyr)
        endVerticesDict = self.buildInitialAndEndPointDict(featureList, feedback, progressDelta=25)
        #search for dangles candidates
        pointList = self.searchDanglesOnPointDict(endVerticesDict, feedback, progressDelta=25)
        #build filter layer
        filterLayer = self.buildFilterLayer(lineLyrList, polygonLyrList, context, feedback, onlySelected=onlySelected)
        #filter pointList with filterLayer
        delta = 20 if not ignoreInner else 40
        filteredPointList = self.filterPointListWithFilterLayer(pointList, filterLayer, searchRadius, feedback, progressDelta = delta)
        #filter with own layer
        if not ignoreInner: #True when looking for dangles on contour lines
            filteredPointList = self.filterPointListWithFilterLayer(filteredPointList, reflyr, searchRadius, isRefLyr = True, ignoreNotSplit = ignoreNotSplit, progressDelta=20)
        #build flag list with filtered points
        if filteredPointList:
            currentValue = feedback.progress()
            currentTotal = 10/len(filteredPointList)
            for current, point in enumerate(filteredPointList):
                if feedback.isCanceled():
                    break
                self.flagFeature(QgsGeometry.fromPoint(point), self.tr('Dangle on {0}').format(inputLyr.name()))
                feedback.setProgress(currentValue + int(current*currentTotal))      
        feedback.setProgress(100)
        return {self.FLAGS: self.flagSink}

    def buildInitialAndEndPointDict(self, featureList, feedback, progressDelta = 100):
        """
        Calculates initial point and end point from each line from lyr.
        """
        # start and end points dict
        currentProgress = feedback.progress()
        endVerticesDict = dict()
        localTotal = progressDelta/len(featureList)
        # iterating over features to store start and end points
        for current, feat in enumerate(featureList):
            if feedback.isCanceled():
                break
            geom = feat.geometry()
            lineList = geom.asMultiPolyline() if geom.isMultipart() else [geom.asPolyline()]
            for line in lineList:
                self.addFeatToDict(endVerticesDict, line, feat.id())
            feedback.setProgress(currentProgress + int(localTotal*current))
        return endVerticesDict

    def addFeatToDict(self, endVerticesDict, line, featid):
        self.addPointToDict(line[0], endVerticesDict, featid)
        self.addPointToDict(line[len(line) - 1], endVerticesDict, featid)
    
    def addPointToDict(self, point, pointDict, featid):
        if point not in pointDict:
            pointDict[point] = []
        pointDict[point].append(featid)
    
    def searchDanglesOnPointDict(self, endVerticesDict, feedback, progressDelta = 100):
        """
        Counts the number of points on each endVerticesDict's key and returns a list of QgsPoint built from key candidate.
        """
        pointList = []
        currentProgress = feedback.progress()
        localTotal = progressDelta/len(featureList)
        # actual search for dangles
        for current, point in enumerate(endVerticesDict):
            if feedback.isCanceled():
                break
            # this means we only have one occurrence of point, therefore it is a dangle
            if len(endVerticesDict[point]) <= 1:
                pointList.append(point)
            feedback.setProgress(currentProgress + int(localTotal*current))
        return pointList

    def buildFilterLayer(self, lineLyrList, polygonLyrList, context, feedback, onlySelected = False):
        """
        Buils one layer of filter lines.
        Build unified layer is not used because we do not care for attributes here, only geometry.
        refLyr elements are also added.
        """
        layerHandler = LayerHandler()
        lineLyrs = lineLyrList
        for polygonLyr in polygonLyrList:
            if feedback.isCanceled():
                break
            lineLyrs += self.makeBoundaries(polygonLyr, context, feedback)
        unifiedLinesLyr = layerHandler.createAndPopulateUnifiedVectorLayer(lineLyrs, QgsWkbTypes.MultiLinestring, onlySelected = onlySelected)
        filterLyr = self.cleanLayer(unifiedLinesLyr, [0,6], context)
        return filterLyr
    
    def makeBoundaries(self, lyr, context, feedback):
        parameters = {
            'INPUT' : lyr,
            'OUTPUT' : 'memory:'
        }
        output = processing.run("native:boundary", parameters, context = context, feedback = feedback)
        return output['OUTPUT']

    def cleanLayer(self, inputLyr, toolList, context, typeList=[0,1,2,3,4,5,6]): 
        #TODO write one class that runs all processing stuff (model that tomorrow)
        output = QgsProcessingUtils.generateTempFilename('output.shp')
        error = QgsProcessingUtils.generateTempFilename('error.shp')
        parameters = {
            'input':inputLyr,
            'type':typeList,
            'tool':toolList,
            'threshold':'-1', 
            '-b':False, 
            '-c':True, 
            'output' : output, 
            'error': error, 
            'GRASS_REGION_PARAMETER':None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_VECTOR_DSCO':'',
            'GRASS_VECTOR_LCO':''
            }
        x = processing.run('grass7:v.clean', parameters, context = context)
        lyr = QgsProcessingUtils.mapLayerFromString(x['output'], context)
        return lyr

    def filterPointListWithFilterLayer(self, pointList, filterLayer, searchRadius, feedback, progressDelta = 100, isRefLyr = False, ignoreNotSplit = False):
        """
        Builds buffer areas from each point and evaluates the intersecting lines. If there are more than two intersections, it is a dangle.
        """
        currentProgress = feedback.progress()
        localTotal = progressDelta/len(pointList)
        spatialIdx, allFeatureDict = self.buildSpatialIndexAndIdDict(filterLayer)
        notDangleList = []
        for current, point in enumerate(pointList):
            if feedback.isCanceled():
                break
            candidateCount = 0
            qgisPoint = QgsGeometry.fromPoint(point)
            #search radius to narrow down candidates
            buffer = qgisPoint.buffer(searchRadius, -1)
            bufferBB = buffer.boundingBox()
            #gets candidates from spatial index
            candidateIds = spatialIdx.intersects(bufferBB)
            #if there is only one feat in candidateIds, that means that it is not a dangle
            bufferCount = len([id for id in candidateIds if buffer.intersects(allFeatureDict[id].geometry())])
            for id in candidateIds:
                if not isRefLyr:
                    if buffer.intersects(allFeatureDict[id].geometry()) and \
                    qgisPoint.distance(allFeatureDict[id].geometry()) < 10**-9: #float problem, tried with intersects and touches and did not get results
                        notDangleIndexList.append(point)
                        break
                else:
                    if ignoreNotSplit:
                        if buffer.intersects(allFeatureDict[id].geometry()) and \
                        (qgisPoint.distance(allFeatureDict[id].geometry()) < 10**-9 or \
                        qgisPoint.intersects(allFeatureDict[id].geometry())): #float problem, tried with intersects and touches and did not get results
                            candidateCount += 1
                    else:
                        if buffer.intersects(allFeatureDict[id].geometry()) and \
                        (qgisPoint.touches(allFeatureDict[id].geometry())): #float problem, tried with intersects and touches and did not get results
                            candidateCount += 1
                    if candidateCount == bufferCount:
                        notDangleIndexList.append(point)
            feedback.setProgress(currentProgress + localTotal*current)
        filteredDangleList = [point for point in pointList if point not in notDangleList]
        return filteredDangleList
    
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

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifydangles'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Dangles')

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
        return IdentifyDuplicatedGeometriesAlgorithm()

class IdentifyDanglesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating = False, withElements = True):
        """
        Constructor
        """
        super(IdentifyDanglesProcess, self).__init__(postgisDb, iface, instantiating, withElements)
        self.processCategory = 'identification'
        self.processAlias = self.tr('Identify Dangles')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a', 'l'], withElements = withElements, excludeValidation = True)
            # adjusting process parameters
            interfaceDict = dict()
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDict[key] = {self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType}
            # getting tables with elements
            self.linesWithElement = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['l'], withElements = withElements, excludeValidation = True)
            # adjusting process parameters
            interfaceLineDict = dict()
            for key in self.linesWithElement:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceLineDict[key] = {self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType}
            self.opTypeDict = OrderedDict([(self.tr('Consider dangle on unsegmented lines'),0), (self.tr('Ignore dangle on unsegmented lines'),1)])
            self.parameters = {'Only Selected':False, 'Ignore search radius on inner layer search':False, 'Search Radius':1.0, 'Layer and Filter Layers': OrderedDict({'referenceDictList':interfaceLineDict, 'layersDictList':interfaceDict}), 'Identification Type':deque(list(self.opTypeDict.keys()))}
            self.unbuildProc = UnbuildEarthCoveragePolygonsProcess(postgisDb, iface, instantiating = True)
            self.unbuildProc.parameters = {'Snap': -1.0, 'MinArea': 0.001} #no snap and no small area
    
    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", Qgis.Critical)
        self.startTimeCount()
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            refKey = self.parameters['Layer and Filter Layers'][0]
            classesWithElemKeys = self.parameters['Layer and Filter Layers'][1]
            if len(classesWithElemKeys) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", Qgis.Critical)
                return 1

            if not refKey:
                self.setStatus(self.tr('One layer must be selected! Stopping.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('One layer must be selected! Stopping.'), "DSG Tools Plugin", Qgis.Critical)
                return 1
            recordList = []
            # preparation
            refcl = self.classesWithElemDict[refKey]
            localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for {0}.{1}').format(refcl['tableSchema'], refcl['tableName']), parent=self.iface.mapCanvas())
            localProgress.step()
            reflyr = self.loadLayerBeforeValidationProcess(refcl)
            localProgress.step()

            idType = self.opTypeDict[self.parameters['Identification Type']]
            if idType == 0: #'Consider dangle on unsegmented lines'
                ignoreNotSplit = False
            else:
                ignoreNotSplit = True

            #build seach dict
            endVerticesDict = self.buildInitialAndEndPointDict(reflyr, refcl['tableSchema'], refcl['tableName'])
            #search for dangles candidates
            pointList = self.searchDanglesOnPointDict(endVerticesDict, refcl['tableSchema'], refcl['tableName'])
            #build filter layer
            filterLayer = self.buildFilterLayer(reflyr)
            #filter pointList with filterLayer
            filteredPointList = self.filterPointListWithFilterLayer(pointList, filterLayer, self.parameters['Search Radius'])
            #filter with own layer
            if not self.parameters['Ignore search radius on inner layer search']: #True when looking for dangles on contour lines
                filteredPointList = self.filterPointListWithFilterLayer(filteredPointList, reflyr, self.parameters['Search Radius'], isRefLyr = True, ignoreNotSplit = ignoreNotSplit)
            #build flag list with filtered points
            recordList = self.buildFlagList(filteredPointList, endVerticesDict, refcl['tableSchema'], refcl['tableName'], refcl['geom'])

            self.logLayerTime(refcl['tableSchema']+'.'+refcl['tableName'])

            try:
                QgsProject.instance().removeMapLayer(filterLayer.id())
            except:
                QgsMessageLog.logMessage(self.tr('Error while trying to remove filter layer.'), "DSG Tools Plugin", Qgis.Critical)

            if len(recordList) > 0:
                numberOfProblems = self.addFlag(recordList)
                msg = self.tr('{0} features have dangles. Check flags.').format(numberOfProblems)
                self.setStatus(msg, 4) #Finished with flags
            else:
                msg = self.tr('There are no dangles.')
                self.setStatus(msg, 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
            self.finishedWithError()
            return 0            
    
    def buildInitialAndEndPointDict(self, lyr, tableSchema, tableName):
        """
        Calculates initial point and end point from each line from lyr.
        """
        if isinstance(lyr, list):
            featureList = lyr
            size = len(featureList)
        else:
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
                for j in range(len(multiLine)):
                    line = multiLine[j]
                    startPoint = line[0]
                    endPoint = line[len(line) - 1]
                    # storing start point in the dict
                    if startPoint not in list(endVerticesDict.keys()):
                        endVerticesDict[startPoint] = []
                    endVerticesDict[startPoint].append(feat.id())
                    # storing end point in the dict
                    if endPoint not in list(endVerticesDict.keys()):
                        endVerticesDict[endPoint] = []
                    endVerticesDict[endPoint].append(feat.id())
            else:
                line = geom.asPolyline()
                startPoint = line[0]
                endPoint = line[len(line) - 1]
                # storing start point in the dict
                if startPoint not in list(endVerticesDict.keys()):
                    endVerticesDict[startPoint] = []
                endVerticesDict[startPoint].append(feat.id())
                # storing end point in the dict
                if endPoint not in list(endVerticesDict.keys()):
                    endVerticesDict[endPoint] = []
                endVerticesDict[endPoint].append(feat.id())
            localProgress.step()
        return endVerticesDict
    
    def searchDanglesOnPointDict(self, endVerticesDict, tableSchema, tableName):
        """
        Counts the number of points on each endVerticesDict's key and returns a list of QgsPoint built from key candidate.
        """
        pointList = []
        idList = []
        # actual search for dangles
        localProgress = ProgressWidget(1, len(list(endVerticesDict.keys())), self.tr('Searching dangles on {0}.{1}').format(tableSchema, tableName), parent=self.iface.mapCanvas())
        for point in list(endVerticesDict.keys()):
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
            newfeat = QgsFeature(filterLyr.fields())
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
        filterLyr = self.iface.addVectorLayer("{0}?crs=epsg:{1}".format('MultiLinestring',srid), "filterLyr", "memory")
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
            if inputLyr.geometryType() == QgsWkbTypes.Polygon:
                #uses makeBoundaries method from unbuildEarthCoveragePolygonsProcess to get candidate lines layer
                lyr = self.unbuildProc.makeBoundaries(inputLyr)
            else:
                lyr = inputLyr
            self.addFeaturesToFilterLayer(filterLyr, lyr)
        filterLyr.endEditCommand()
        filterLyr.commitChanges()
        return filterLyr

    def filterPointListWithFilterLayer(self, pointList, filterLayer, searchRadius, isRefLyr = False, ignoreNotSplit = False):
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
            bufferCount = len([id for id in candidateIds if buffer.intersects(allFeatureDict[id].geometry())])
            for id in candidateIds:
                if not isRefLyr:
                    if buffer.intersects(allFeatureDict[id].geometry()) and \
                    qgisPoint.distance(allFeatureDict[id].geometry()) < 10**-9: #float problem, tried with intersects and touches and did not get results
                        notDangleIndexList.append(i)
                        break
                else:
                    if ignoreNotSplit:
                        if buffer.intersects(allFeatureDict[id].geometry()) and \
                        (qgisPoint.distance(allFeatureDict[id].geometry()) < 10**-9 or \
                        qgisPoint.intersects(allFeatureDict[id].geometry())): #float problem, tried with intersects and touches and did not get results
                            candidateCount += 1
                    else:
                        if buffer.intersects(allFeatureDict[id].geometry()) and \
                        (qgisPoint.touches(allFeatureDict[id].geometry())): #float problem, tried with intersects and touches and did not get results
                            candidateCount += 1
                    if candidateCount == bufferCount:
                        notDangleIndexList.append(i)
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