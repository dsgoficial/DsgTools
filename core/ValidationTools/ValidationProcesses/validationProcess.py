# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from builtins import str
from builtins import range
import binascii
from datetime import datetime
import json
# Qt imports
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.Qt import QObject

#QGIS imports
from qgis.core import Qgis, QgsVectorLayer, QgsCoordinateReferenceSystem, \
                      QgsGeometry, QgsFeature, QgsDataSourceUri, QgsFeatureRequest, \
                      QgsMessageLog, QgsExpression, QgsField, QgsWkbTypes, \
                      QgsTask, QgsProcessingAlgorithm

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
                       QgsFields)

class ValidationAlgorithm(QgsProcessingAlgorithm):
    """
    Processing algorithm with handy stuff for other algs.
    """
    def getIteratorAndFeatureCount(self, lyr, onlySelected = False):
        """
        Gets the iterator and feature count from lyr.
        """
        if onlySelected:
            total = 100.0 / lyr.selectedFeatureCount() if lyr.selectedFeatureCount() else 0
            iterator = lyr.getSelectedFeatures()
        else:
            total = 100.0 / lyr.featureCount() if lyr.featureCount() else 0
            iterator = lyr.getFeatures()
        return iterator, total
    
    def prepareFlagSink(self, parameters, source, wkbType, context):
        flagFields = self.getFlagFields()
        (self.flagSink, self.dest_id) = self.parameterAsSink(parameters, self.FLAGS,
                context, flagFields, wkbType, source.sourceCrs())
        if self.flagSink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.FLAGS))
    
    def getFlagFields(self):
        fields = QgsFields()
        fields.append(QgsField('reason',QVariant.String))
        return fields
    
    def flagFeature(self, flagGeom, flagText):
        """
        Creates and adds to flagSink a new flag with the reason.
        :param flagGeom: (QgsGeometry) geometry of the flag;
        :param flagText: (string) Text of the flag
        """
        newFeat = QgsFeature(self.getFlagFields())
        newFeat['reason'] = flagText
        newFeat.setGeometry(flagGeom)
        self.flagSink.addFeature(newFeat, QgsFeatureSink.FastInsert)

class ValidationProcess(QgsTask):
    def __init__(self, params, description = '', flags = QgsTask.CanCancel):
        """
        Constructor
        """
        super(ValidationProcess, self).__init__(description, flags)
        self.processCategory = None
        self.parameters = params
        self.processAlias = self.tr('Validation Process')
        self.totalTime = 0
        self.startTime = 0
        self.endTime = 0
        self.dbUserName = None
        self.logMsg = None
        self.processName = None

    def setDbUserName(self, userName):
        """
        Identifies the database username.
        """
        self.dbUserName = userName
    
    def getName(self):
        """
        Gets the process name
        """
        return str(self.__class__).split('.')[-1].replace('\'>', '')
    
    
    def preProcess(self):
        """
        Returns the name of the pre process that must run before, must be reimplemented in each process
        """
        return None
    
    def postProcess(self):
        """
        Returns the name of the post process that must run after, must be reimplemented in each process
        """        
        return None
            
    def removeFeatureFlags(self, layer, featureId):
        """
        Removes specific flags from process
        layer: Name of the layer that should be remove from the flags
        featureId: Feature id from layer name that must be removed
        """
        #REDO
        pass
    
    def finishedWithError(self):
        """
        Sets the finished with error status (status number 2)
        Clears the classes to be displayed
        """
        self.setStatus(self.tr('Process finished with errors.'), 2) #Failed status
        #drop temps
        try:
            classesWithElem = self.parameters['Classes']
            for cl in classesWithElem:
                tempName = cl.split(':')[0]+'_temp'
                self.abstractDb.dropTempTable(tempName)
        except:
            pass
        self.clearClassesToBeDisplayedAfterProcess()

    def getTableNameFromLayer(self, lyr):
        """
        Gets the layer name as present in the rules
        """
        uri = lyr.dataProvider().dataSourceUri()
        dsUri = QgsDataSourceUri(uri)
        name = '.'.join([dsUri.schema(), dsUri.table()])
        return name

    def mapInputLayer(self, inputLyr, selectedFeatures = False):
        """
        Gets the layer features considering the edit buffer in the case
        the layer is already in edition mode
        """
        #return dict
        featureMap = dict()
        #getting only selected features
        if selectedFeatures:
            for feat in inputLyr.selectedFeatures():
                featureMap[feat.id()] = feat
        #getting all features
        else:
            for feat in inputLyr.getFeatures():
                featureMap[feat.id()] = feat
        return featureMap

    def updateOriginalLayerV2(self, pgInputLayer, qgisOutputVector, featureList=None, featureTupleList=None, deleteFeatures = True):
        """
        Updates the original layer using the grass output layer
        pgInputLyr: postgis input layer
        qgisOutputVector: qgis output layer
        Speed up tips: http://nyalldawson.net/2016/10/speeding-up-your-pyqgis-scripts/
        1- Make pgIdList, by querying it with flag QgsFeatureRequest.NoGeometry
        2- Build output dict
        3- Perform operation
        """
        provider = pgInputLayer.dataProvider()
        # getting keyColumn because we want to be generic
        uri = QgsDataSourceUri(pgInputLayer.dataProvider().dataSourceUri())
        keyColumn = uri.keyColumn()
        # starting edition mode
        pgInputLayer.startEditing()
        pgInputLayer.beginEditCommand('Updating layer')
        addList = []
        idsToRemove = []
        inputDict = dict()
        #this is done to work generically with output layers that are implemented different from ours
        isMulti = QgsWkbTypes.isMultiType(int(pgInputLayer.wkbType())) #
        #making the changes and inserts
        #this request only takes ids to build inputDict
        request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
        for feature in pgInputLayer.getFeatures(request):
            inputDict[feature.id()] = dict()
            inputDict[feature.id()]['featList'] = []
            inputDict[feature.id()]['featWithoutGeom'] = feature
        if qgisOutputVector is not None:
            for feat in qgisOutputVector.dataProvider().getFeatures():
                if keyColumn == '':
                    featid = feat.id()
                else:
                    featid = feat[keyColumn]
                if featid in inputDict: #verificar quando keyColumn = ''
                    inputDict[featid]['featList'].append(feat)
        elif featureTupleList:
            for gfid, gf in featureTupleList:
                if gfid in inputDict and gf['classname'] == pgInputLayer.name():
                    inputDict[gfid]['featList'].append(gf)
        else:
            for feat in featureList:
                if keyColumn == '':
                    featid = feat.id()
                else:
                    featid = feat[keyColumn]
                if featid in inputDict:
                    inputDict[featid]['featList'].append(feat)
        #finally, do what must be done
        for id in inputDict:
            outFeats = inputDict[id]['featList']
            #starting to make changes
            for i in range(len(outFeats)):
                if i == 0:
                    #let's update this feature
                    newGeom = outFeats[i].geometry()
                    if newGeom is not None:
                        if isMulti:
                            newGeom.convertToMultiType()
                        pgInputLayer.changeGeometry(id, newGeom) #It is faster according to the api
                    else:
                        if id not in idsToRemove:
                            idsToRemove.append(id)
                else:
                    #for the rest, let's add them
                    newFeat = QgsFeature(inputDict[id]['featWithoutGeom'])
                    newGeom = outFeats[i].geometry()
                    if newGeom:
                        if isMulti and newGeom:
                            newGeom.convertToMultiType()
                        newFeat.setGeometry(newGeom)
                        if keyColumn != '':
                            idx = newFeat.fieldNameIndex(keyColumn)
                            newFeat.setAttribute(idx, provider.defaultValue(idx))
                        addList.append(newFeat)
                    else:
                        if id not in idsToRemove:
                            idsToRemove.append(id)
            #in the case we don't find features in the output we should mark them to be removed
            if len(outFeats) == 0 and deleteFeatures:
                idsToRemove.append(id)
        #pushing the changes into the edit buffer
        pgInputLayer.addFeatures(addList)
        #removing features from the layer.
        pgInputLayer.deleteFeatures(idsToRemove)
        pgInputLayer.endEditCommand()

    def getProcessingErrors(self, layer):
        """
        Gets processing errors
        layer: error layer (QgsVectorLayer) output made by grass
        """
        recordList = []
        for feature in layer.getFeatures():
            recordList.append((feature.id(), binascii.hexlify(feature.geometry().asWkb())))
        return recordList
    
    def prepareExecution(self, cl, geometryColumn='geom', selectedFeatures = False):
        """
        Prepare the process to be executed
        cl: table name
        """
        # loading layer prior to execution
        lyr = self.loadLayerBeforeValidationProcess(cl)
        # getting keyColumn because we want to be generic
        uri = QgsDataSourceUri(lyr.dataProvider().dataSourceUri())
        keyColumn = uri.keyColumn()
        #getting feature map including the edit buffer
        # featureMap = self.mapInputLayer(lyr, selectedFeatures = selectedFeatures)
        #getting table name with schema
        if isinstance(cl, dict):
            tableSchema = cl['tableSchema']
            tableName = cl['tableName']
            geometryColumn = cl['geom']
            fullTableName = '''{0}.{1}'''.format(cl['tableSchema'], cl['tableName'])
        else:
            fullTableName = cl
            tableSchema, tableName = cl.split('.')

        #setting temp table name
        processTableName = fullTableName+'_temp'
        # specific EPSG search
        parameters = {'tableSchema':tableSchema, 'tableName':tableName, 'geometryColumn':geometryColumn}
        srid = self.abstractDb.findEPSG(parameters=parameters)
        #creating temp table
        self.abstractDb.createTempTable(fullTableName, geometryColumn)
        self.populateTempTable(fullTableName, lyr, selectedFeatures = selectedFeatures)
        return processTableName, lyr, keyColumn
    
    def populateTempTable(self, fullTableName, inputLyr, selectedFeatures = False):
        iterator = inputLyr.selectedFeatures() if selectedFeatures else inputLyr.getFeatures()
        featList = []
        idx = len(inputLyr.fields())-1
        for feat in iterator:
            feat.deleteAttribute(idx)
            featList.append(feat)
        tempLyr = self.loadTempLayer(fullTableName + '_temp')
        self.addFeaturesToTempTable(tempLyr, featList)
    
    def addFeaturesToTempTable(self, tempLyr, featList):
        tempLyr.startEditing()
        tempLyr.beginEditCommand('Populating temp table')
        tempLyr.addFeatures(featList)
        tempLyr.endEditCommand()
        tempLyr.commitChanges()

    def loadTempLayer(self, tempLyrName):
        """
        Loads temp layer but does not load it into interface.
        """
        schema, tableName = tempLyrName.split('.')
        uri = self.layerLoader.uri
        uri.setDataSource(schema, tableName, 'geom', '', 'id')
        tempLyr = QgsVectorLayer(uri.uri(), tempLyrName, 'postgres')
        return tempLyr
        
    
    def postProcessSteps(self, processTableName, lyr):
        """
        Execute the final steps after the actual process
        """
        #getting the output as a QgsVectorLayer
        outputLayer = QgsVectorLayer(self.abstractDb.getURI(processTableName, True).uri(), processTableName, "postgres")
        #updating the original layer (lyr)
        self.updateOriginalLayerV2(lyr, outputLayer)
        #dropping the temp table as we don't need it anymore
        self.abstractDb.dropTempTable(processTableName)
    
    def getGeometryTypeText(self, geomtype):
        if geomtype == QgsWkbTypes.Point:
            return 'Point'
        elif geomtype == QgsWkbTypes.MultiPoint:
            return 'MultiPoint'
        elif geomtype == QgsWkbTypes.LineString:
            return 'Linestring'
        elif geomtype == QgsWkbTypes.MultiLineString:
            return 'MultiLinestring'
        elif geomtype == QgsWkbTypes.Polygon:
            return 'Polygon'
        elif geomtype == QgsWkbTypes.MultiPolygon:
            return 'MultiPolygon'
        else:
            raise Exception(self.tr('Operation not defined with provided geometry type!'))

    def createUnifiedLayer(self, layerList, attributeTupple = False, attributeBlackList = '', onlySelected = False):
        """
        Creates a unified layer from a list of layers
        """
        #getting srid from something like 'EPSG:31983'
        srid = layerList[0].crs().authid().split(':')[-1] #quem disse que tudo tem que ter mesmo srid? TODO: mudar isso
        # creating the layer
        geomtype = layerList[0].geometryType()
        for lyr in layerList:
            if lyr.geometryType() != geomtype:
                raise Exception(self.tr('Error! Different geometry primitives!'))

        coverage = self.iface.addVectorLayer("{0}?crs=epsg:{1}".format(self.getGeometryTypeText(geomtype),srid), "coverage", "memory")
        provider = coverage.dataProvider()
        coverage.startEditing()
        coverage.beginEditCommand('Creating coverage layer') #speedup

        #defining fields
        if not attributeTupple:
            fields = [QgsField('featid', QVariant.Int), QgsField('classname', QVariant.String)]
        else:
            fields = [QgsField('featid', QVariant.Int), QgsField('classname', QVariant.String), QgsField('tupple', QVariant.String), QgsField('blacklist', QVariant.String)]
        provider.addAttributes(fields)
        coverage.updateFields()

        totalCount = 0
        for layer in layerList:
            if onlySelected:
                totalCount += layer.selectedFeatureCount()
            else:
                totalCount += layer.featureCount()
        self.localProgress = ProgressWidget(1, totalCount - 1, self.tr('Building unified layers with  ') + ', '.join([i.name() for i in layerList])+'.', parent=self.iface.mapCanvas())
        featlist = []
        if attributeBlackList != '':
            bList = attributeBlackList.replace(' ','').split(',')
        else:
            bList = []
        for layer in layerList:
            # recording class name
            classname = layer.name()
            uri = QgsDataSourceUri(layer.dataProvider().dataSourceUri())
            keyColumn = uri.keyColumn()
            if onlySelected:
                featureList = layer.selectedFeatures()
            else:
                featureList = layer.getFeatures()
            for feature in featureList:
                newfeat = QgsFeature(coverage.fields())
                newfeat.setGeometry(feature.geometry())
                newfeat['featid'] = feature.id()
                newfeat['classname'] = classname
                if attributeTupple:
                    attributeList = []
                    attributes = [field.name() for field in feature.fields() if (field.type() != 6 and field.name() != keyColumn)]
                    attributes.sort()
                    for attribute in attributes:
                        if attribute not in bList:
                            attributeList.append(u'{0}'.format(feature[attribute])) #done due to encode problems
                    tup = ','.join(attributeList)
                    newfeat['tupple'] = tup
                featlist.append(newfeat)
                self.localProgress.step()
        
        #inserting new features into layer
        coverage.addFeatures(featlist)
        coverage.endEditCommand()
        coverage.commitChanges()
        return coverage

    def splitUnifiedLayer(self, outputLayer, layerList):
        """
        Updates all original layers making requests with the class name
        """
        for layer in layerList:
            classname = layer.name()
            tupplelist = [(feature['featid'], feature) for feature in outputLayer.getFeatures() if feature['classname'] == classname]
            self.updateOriginalLayerV2(layer, None, featureTupleList=tupplelist)

    def getGeometryColumnFromLayer(self, layer):
        uri = QgsDataSourceUri(layer.dataProvider().dataSourceUri())
        geomColumn = uri.geometryColumn()
        return geomColumn

    def startTimeCount(self):
        self.startTime = datetime.now()
        self.endTime = 0
    
    def endTimeCount(self, cummulative = True):
        self.endTime = datetime.now()
        elapsedTime = (self.endTime - self.startTime) if self.startTime != 0 else self.endTime
        if cummulative:
            if self.totalTime == 0:
                self.totalTime = elapsedTime
            else:
                self.totalTime += elapsedTime
        return elapsedTime

    def logLayerTime(self, lyr):
        time = self.endTimeCount()
        if self.startTime != 0 and self.endTime != 0:
            QgsMessageLog.logMessage(self.tr('Elapsed time for process {0} on layer {1}: {2}').format(self.processAlias, lyr, str(time)), "DSG Tools Plugin", Qgis.Critical)

    def logTotalTime(self):
        if self.startTime != 0 and self.endTime != 0 and self.totalTime != 0:
            QgsMessageLog.logMessage(self.tr('Elapsed time for process {0}: {1}').format(self.processAlias, str(self.totalTime)), "DSG Tools Plugin", Qgis.Critical)
    
    def jsonifyParameters(self, params):
        """
        Sets a dict type feature to a json structure in order to make it visually better
        both to expose on log and to save it on validation history table.
        parameter params: a dict type variable
        returns: a json structured text
        """
        return json.dumps(params, sort_keys=True, indent=4)

    def logProcess(self):
        """
        Returns information to user:
        -userName (get information from abstractDb.db.userName())
        -parameters (get parameters from parameter dict) ***
        -layersRun (the layers that were used)
        -flagNumber (number of flags)
        -elapsedTime
        """
        # logging username
        logMsg = ""
        if self.dbUserName:
            logMsg += self.tr("Database username: {0}").format(self.dbUserName)
        else:
            logMsg += self.tr("Unable to get database username.")
        # logging process parameters
        if self.parameters:
            parametersString = self.tr("\nParameters used on this execution of process {}\n").format(self.processAlias)
            parametersString += self.jsonifyParameters(self.parameters)
            logMsg += parametersString
        else:
            logMsg += self.tr("Unable to get database parameters for process {}.").format(self.processAlias)
        # logging #Flag
        logMsg += self.tr("\nNumber of flags raised by the process: {}").format(\
                        str(self.abstractDb.getNumberOfFlagsByProcess(self.processName)))
        # logging total time elapsed
        if self.totalTime:
            logMsg += self.tr("\nTotal elapsed time for process {0}: {1}\n").format(self.processAlias, self.totalTime)
        else:
            logMsg += self.tr("\nUnable to get total elapsed time.")
        self.logMsg = logMsg
        QgsMessageLog.logMessage(logMsg, "DSG Tools Plugin", Qgis.Critical)

    def raiseVectorFlags(self, flagLyr, featFlagList):
        flagLyr.startEditing()
        flagLyr.beginEditCommand('Raising flags') #speedup
        flagLyr.addFeatures(featFlagList)
        flagLyr.endEditCommand()
        flagLyr.commitChanges()
        return len(featFlagList)
    
    def buildFlagFeature(self, flagLyr, processName, tableSchema, tableName, feat_id, geometry_column, geom, reason):
        newFeat = QgsFeature(flagLyr.fields())
        newFeat['process_name'] = processName
        newFeat['layer'] = '{0}.{1}'.format(tableSchema, tableName)
        newFeat['feat_id'] = feat_id
        newFeat['reason'] = reason
        newFeat['geometry_column'] = geometry_column
        newFeat['user_fixed'] = False
        newFeat['dimension'] = geom.type()
        newFeat.setGeometry(geom)
        return newFeat
            
    def getFeatures(self, lyr, onlySelected = False, returnIterator = True, returnSize = True):
        if onlySelected:
            featureList = lyr.selectedFeatures()
            size = len(featureList)
        else:
            featureList = [i for i in lyr.getFeatures()] if not returnIterator else lyr.getFeatures()
            size = len(lyr.allFeatureIds())
        if returnIterator:
            return featureList, size
        else:
            return featureList