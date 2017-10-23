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
        email                : borba@dsg.eb.mil.br
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
import binascii
# Qt imports
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QVariant
from PyQt4.Qt import QObject

#QGIS imports
from qgis.core import QGis, QgsVectorLayer, QgsCoordinateReferenceSystem, QgsGeometry, QgsFeature, QgsDataSourceURI, QgsFeatureRequest, QgsMessageLog, QgsExpression, QgsField, QgsWKBTypes

# DSGTools imports
from DsgTools.Factories.LayerLoaderFactory.layerLoaderFactory import LayerLoaderFactory
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

class ValidationProcess(QObject):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(ValidationProcess, self).__init__()
        self.abstractDb = postgisDb
        if self.getStatus() == None:
            self.setStatus(self.tr('Instantianting process'), 0)
        self.classesToBeDisplayedAfterProcess = []
        self.parameters = None
        self.iface = iface
        self.layerLoader = LayerLoaderFactory().makeLoader(self.iface, self.abstractDb)
        self.processAlias = self.tr('Validation Process')
        self.instantiating = instantiating
        
    def setParameters(self, params):
        """
        Define the process parameteres
        """
        self.parameters = params

    def execute(self):
        """
        Abstract method. MUST be reimplemented.
        """
        pass
    
    def shouldBeRunAgain(self):
        """
        Defines if the method should run again later
        """
        return False
    
    def getName(self):
        """
        Gets the process name
        """
        return str(self.__class__).split('.')[-1].replace('\'>', '')
    
    def getProcessGroup(self):
        """
        Returns the process group
        """
        return 'Ungrouped'
    
    def getClassesToBeDisplayedAfterProcess(self):
        """
        Returns classes to be loaded to TOC after executing this process.
        """
        return self.classesToBeDisplayedAfterProcess
    
    def addClassesToBeDisplayedList(self,className):
        """
        Add a class into the class list that will be displayed after the process
        """
        if className not in self.classesToBeDisplayedAfterProcess:
            self.classesToBeDisplayedAfterProcess.append(className)
    
    def clearClassesToBeDisplayedAfterProcess(self):
        """
        Clears the class list to be displayed
        """
        self.classesToBeDisplayedAfterProcess = []
    
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
    
    def addFlag(self, flagTupleList):
        """
        Adds flags
        flagTUpleList: list of tuples to be added as flag
        """
        try:
            return self.abstractDb.insertFlags(flagTupleList, self.getName())
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred inserting flags! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            
    def removeFeatureFlags(self, layer, featureId):
        """
        Removes specific flags from process
        layer: Name of the layer that should be remove from the flags
        featureId: Feature id from layer name that must be removed
        """
        try:
            return self.abstractDb.removeFeatureFlags(layer, featureId, self.getName())
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
    def getStatus(self):
        """
        Gets the process status
        """
        try:
            return self.abstractDb.getValidationStatus(self.getName())
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
    def getStatusMessage(self):
        """
        Gets the status message text
        """
        try:
            return self.abstractDb.getValidationStatusText(self.getName())
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
    def setStatus(self, msg, status):
        """
        Sets the status message
        status: Status number
        msg: Status text message
        """
        try:
            self.abstractDb.setValidationProcessStatus(self.getName(), msg, status)
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
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
    
    def inputData(self):
        """
        Returns current active layers
        """
        return self.iface.mapCanvas().layers()

    def getTableNameFromLayer(self, lyr):
        """
        Gets the layer name as present in the rules
        """
        uri = lyr.dataProvider().dataSourceUri()
        dsUri = QgsDataSourceURI(uri)
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
    
    def updateOriginalLayer(self, pgInputLayer, qgisOutputVector, featureList=None, featureTupleList=None):
        """
        Updates the original layer using the grass output layer
        pgInputLyr: postgis input layer
        qgisOutputVector: qgis output layer
        Speed up tips: http://nyalldawson.net/2016/10/speeding-up-your-pyqgis-scripts/
        """
        provider = pgInputLayer.dataProvider()
        # getting keyColumn because we want to be generic
        uri = QgsDataSourceURI(pgInputLayer.dataProvider().dataSourceUri())
        keyColumn = uri.keyColumn()
        # starting edition mode
        pgInputLayer.startEditing()
        addList = []
        idsToRemove = []
        #making the changes and inserts
        for feature in pgInputLayer.getFeatures():
            id = feature.id()
            outFeats = []
            #getting the output features with the specific id
            if qgisOutputVector:
                for gf in qgisOutputVector.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression("{0}={1}".format(keyColumn, id)))):
                    outFeats.append(gf)
            elif featureTupleList:
                for gfid, gf in featureTupleList:
                    if gfid == id and gf['classname'] == pgInputLayer.name():
                        outFeats.append(gf)
            else:
                for gf in [gf for gf in featureList if gf.id() == id]:
                    outFeats.append(gf)
            #starting to make changes
            for i in range(len(outFeats)):
                if i == 0:
                    #let's update this feature
                    newGeom = outFeats[i].geometry()
                    newGeom.convertToMultiType()
                    feature.setGeometry(newGeom)
                    pgInputLayer.updateFeature(feature)
                else:
                    #for the rest, let's add them
                    newFeat = QgsFeature(feature)
                    newGeom = outFeats[i].geometry()
                    newGeom.convertToMultiType()
                    newFeat.setGeometry(newGeom)
                    idx = newFeat.fieldNameIndex(keyColumn)
                    newFeat.setAttribute(idx, provider.defaultValue(idx))
                    addList.append(newFeat)
            #in the case we don't find features in the output we should mark them to be removed
            if len(outFeats) == 0:
                idsToRemove.append(id)
        #pushing the changes into the edit buffer
        pgInputLayer.addFeatures(addList, True)
        #removing features from the layer.
        pgInputLayer.deleteFeatures(idsToRemove)

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
        uri = QgsDataSourceURI(pgInputLayer.dataProvider().dataSourceUri())
        keyColumn = uri.keyColumn()
        # starting edition mode
        pgInputLayer.startEditing()
        addList = []
        idsToRemove = []
        inputDict = dict()
        #this is done to work generically with output layers that are implemented different from ours
        isMulti = QgsWKBTypes.isMultiType(int(pgInputLayer.wkbType())) #
        #making the changes and inserts
        #this request only takes ids to build inputDict
        request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry).setSubsetOfAttributes([keyColumn], pgInputLayer.fields() )
        for feature in pgInputLayer.getFeatures(request):
            inputDict[feature.id()] = []
        inputDictKeys = inputDict.keys()
        if qgisOutputVector:
            for feat in qgisOutputVector.dataProvider().getFeatures():
                if feat.id() in inputDictKeys:
                    inputDict[feat.id()].append(feat)
        elif featureTupleList:
            for gfid, gf in featureTupleList:
                if gfid in inputDictKeys and gf['classname'] == pgInputLayer.name():
                    inputDict[gfid].append(gf)
        else:
            for feat in featureList:
                if feat.id() in inputDictKeys:
                    inputDict[feat.id()].append(feat)
        #finally, do what must be done
        for id in inputDictKeys:
            #starting to make changes
            for i in range(len(inputDict[id])):
                outFeats = inputDict[id]
                if i == 0:
                    #let's update this feature
                    newGeom = outFeats[i].geometry()
                    if isMulti:
                        newGeom.convertToMultiType()
                    feature.setGeometry(newGeom)
                    pgInputLayer.updateFeature(feature)
                else:
                    #for the rest, let's add them
                    newFeat = QgsFeature(feature)
                    newGeom = outFeats[i].geometry()
                    if isMulti:
                        newGeom.convertToMultiType()
                    newFeat.setGeometry(newGeom)
                    idx = newFeat.fieldNameIndex(keyColumn)
                    newFeat.setAttribute(idx, provider.defaultValue(idx))
                    addList.append(newFeat)
            #in the case we don't find features in the output we should mark them to be removed
            if len(outFeats) == 0 and deleteFeatures:
                idsToRemove.append(id)
        #pushing the changes into the edit buffer
        pgInputLayer.addFeatures(addList, True)
        #removing features from the layer.
        pgInputLayer.deleteFeatures(idsToRemove)

    def getProcessingErrors(self, layer):
        """
        Gets processing errors
        layer: error layer (QgsVectorLayer) output made by grass
        """
        recordList = []
        for feature in layer.getFeatures():
            recordList.append((feature.id(), binascii.hexlify(feature.geometry().asWkb())))
        return recordList
    
    def loadLayerBeforeValidationProcess(self, cl):
        """
        Loads all layers to QGIS' TOC prior the validation process
        """
        #creating vector layer
        if self.abstractDb.getDatabaseVersion() == 'Non_EDGV':
            isEdgv = False
        else:
            isEdgv = True
        if isinstance(cl, dict):
            lyr = self.layerLoader.load([cl], uniqueLoad=True, isEdgv=isEdgv)[cl['lyrName']]
        else:
            schema, layer_name = self.abstractDb.getTableSchema(cl)
            lyr = self.layerLoader.load([layer_name], uniqueLoad=True, isEdgv=isEdgv)[layer_name]
        return lyr
    
    def prepareExecution(self, cl, geometryColumn='geom', selectedFeatures = False):
        """
        Prepare the process to be executed
        cl: table name
        """
        # loading layer prior to execution
        lyr = self.loadLayerBeforeValidationProcess(cl)
        # getting keyColumn because we want to be generic
        uri = QgsDataSourceURI(lyr.dataProvider().dataSourceUri())
        keyColumn = uri.keyColumn()
        #getting feature map including the edit buffer
        featureMap = self.mapInputLayer(lyr, selectedFeatures = selectedFeatures)
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
        self.abstractDb.createAndPopulateTempTableFromMap(fullTableName, featureMap, geometryColumn, keyColumn, srid)
        return processTableName, lyr, keyColumn
    
    def postProcessSteps(self, processTableName, lyr):
        """
        Execute the final steps after the actual process
        """
        #getting the output as a QgsVectorLayer
        outputLayer = QgsVectorLayer(self.abstractDb.getURI(processTableName, True).uri(), processTableName, "postgres")
        #updating the original layer (lyr)
        self.updateOriginalLayer(lyr, outputLayer)
        #dropping the temp table as we don't need it anymore
        self.abstractDb.dropTempTable(processTableName)
    
    def getGeometryTypeText(self, geomtype):
        if geomtype == QGis.WKBPoint:
            return 'Point'
        elif geomtype == QGis.WKBMultiPoint:
            return 'MultiPoint'
        elif geomtype == QGis.WKBLineString:
            return 'Linestring'
        elif geomtype == QGis.WKBMultiLineString:
            return 'MultiLinestring'
        elif geomtype == QGis.WKBPolygon:
            return 'Polygon'
        elif geomtype == QGis.WKBMultiPolygon:
            return 'MultiPolygon'
        else:
            raise Exception(self.tr('Operation not defined with provided geometry type!'))

    def createUnifiedLayer(self, layerList, attributeTupple = False, attributeBlackList = ''):
        """
        Creates a unified layer from a list of layers
        """
        #getting srid from something like 'EPSG:31983'
        srid = layerList[0].crs().authid().split(':')[-1]
        # creating the layer
        geomtype = layerList[0].dataProvider().geometryType()
        for lyr in layerList:
            if lyr.dataProvider().geometryType() != geomtype:
                raise Exception(self.tr('Error! Different geometry primitives!'))

        coverage = self.iface.addVectorLayer("{0}?crs=epsg:{1}".format(self.getGeometryTypeText(geomtype),srid), "coverage", "memory")
        provider = coverage.dataProvider()
        coverage.startEditing()

        #defining fields
        if not attributeTupple:
            fields = [QgsField('featid', QVariant.Int), QgsField('classname', QVariant.String)]
        else:
            fields = [QgsField('featid', QVariant.Int), QgsField('classname', QVariant.String), QgsField('tupple', QVariant.String), QgsField('blacklist', QVariant.String)]
        provider.addAttributes(fields)
        coverage.updateFields()

        totalCount = 0
        for layer in layerList:
            totalCount += layer.pendingFeatureCount()
        self.localProgress = ProgressWidget(1, totalCount - 1, self.tr('Building unified layers with  ') + ', '.join([i.name() for i in layerList])+'.', parent=self.iface.mapCanvas())
        featlist = []
        if attributeBlackList != '':
            bList = attributeBlackList.replace(' ','').split(',')
        else:
            bList = []
        for layer in layerList:
            # recording class name
            classname = layer.name()
            uri = QgsDataSourceURI(layer.dataProvider().dataSourceUri())
            keyColumn = uri.keyColumn()
            for feature in layer.getFeatures():
                newfeat = QgsFeature(coverage.pendingFields())
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
        coverage.addFeatures(featlist, True)
        coverage.commitChanges()
        return coverage

    def splitUnifiedLayer(self, outputLayer, layerList):
        """
        Updates all original layers making requests with the class name
        """
        for layer in layerList:
            classname = layer.name()
            tupplelist = [(feature['featid'], feature) for feature in outputLayer.getFeatures()]
            self.updateOriginalLayer(layer, None, featureTupleList=tupplelist)

    def getGeometryColumnFromLayer(self, layer):
        uri = QgsDataSourceURI(layer.dataProvider().dataSourceUri())
        geomColumn = uri.geometryColumn()
        return geomColumn
