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
# Qt imports
from qgis.core import QgsMessageLog
from PyQt4.QtGui import QMessageBox
from PyQt4.Qt import QObject

#QGIS imports
from qgis.core import QgsCoordinateReferenceSystem, QgsGeometry, QgsFeature, QgsDataSourceURI, QgsFeatureRequest

# DSGTools imports
from DsgTools.Factories.LayerFactory.layerFactory import LayerFactory


class ValidationProcess(QObject):
    def __init__(self, postgisDb, codelist, iface):
        '''
        Constructor
        '''
        super(ValidationProcess, self).__init__()
        self.abstractDb = postgisDb
        if self.getStatus() == None:
            self.setStatus('Instantianting process', 0)
        self.classesToBeDisplayedAfterProcess = []
        self.parameters = None
        self.codeList = codelist
        self.iface = iface
        self.layerFactory = LayerFactory() 
        
    def setParameters(self, params):
        '''
        Define the process parameteres
        '''
        self.parameters = params

    def execute(self):
        '''
        Abstract method. MUST be reimplemented.
        '''
        pass
    
    def shouldBeRunAgain(self):
        '''
        Defines if the method should run again later
        '''
        return False
    
    def getName(self):
        '''
        Gets the process name
        '''
        return str(self.__class__).split('.')[-1].replace('\'>', '')
    
    def getProcessGroup(self):
        '''
        Returns the process group
        '''
        return 'Ungrouped'
    
    def getClassesToBeDisplayedAfterProcess(self):
        '''
        Returns classes to be loaded to TOC after executing this process.
        '''
        return self.classesToBeDisplayedAfterProcess
    
    def addClassesToBeDisplayedList(self,className):
        '''
        Add a class into the class list that will be displayed after the process
        '''
        if className not in self.classesToBeDisplayedAfterProcess:
            self.classesToBeDisplayedAfterProcess.append(className)
    
    def clearClassesToBeDisplayedAfterProcess(self):
        '''
        Clears the class list to be displayed
        '''
        self.classesToBeDisplayedAfterProcess = []
    
    def preProcess(self):
        '''
        Returns the name of the pre process that must run before, must be reimplemented in each process
        '''
        return None
    
    def postProcess(self):
        '''
        Returns the name of the post process that must run after, must be reimplemented in each process
        '''        
        return None
    
    def addFlag(self, flagTupleList):
        '''
        Adds flags
        flagTUpleList: list of tuples to be added as flag
        '''
        try:
            return self.abstractDb.insertFlags(flagTupleList, self.getName())
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            
    def removeFeatureFlags(self, layer, featureId):
        '''
        Removes specific flags from process
        layer: Name of the layer that should be remove from the flags
        featureId: Feature id from layer name that must be removed
        '''
        try:
            return self.abstractDb.removeFeatureFlags(layer, featureId, self.getName())
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
    def getStatus(self):
        '''
        Gets the process status
        '''
        try:
            return self.abstractDb.getValidationStatus(self.getName())
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
    def getStatusMessage(self):
        '''
        Gets the status message text
        '''
        try:
            return self.abstractDb.getValidationStatusText(self.getName())
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
    def setStatus(self, msg, status):
        '''
        Sets the status message
        status: Status number
        msg: Status text message
        '''
        try:
            self.abstractDb.setValidationProcessStatus(self.getName(), msg, status)
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
    def finishedWithError(self):
        '''
        Sets the finished with error status (status number 2)
        Clears the classes to be displayed
        '''
        self.setStatus('Process finished with errors.', 2) #Failed status
        self.clearClassesToBeDisplayedAfterProcess()
    
    def inputData(self):
        '''
        Returns current active layers
        '''
        return self.iface.mapCanvas().layers()

    def getTableNameFromLayer(self, lyr):
        '''
        Gets the layer name as present in the rules
        '''
        uri = lyr.dataProvider().dataSourceUri()
        dsUri = QgsDataSourceURI(uri)
        name = '.'.join([dsUri.schema(), dsUri.table()])
        return name

    def mapInputLayer(self, inputLyr):
        featureMap = dict()
        editBuffer = inputLyr.editBuffer()
        blackList = []
        if editBuffer:
            blackList = editBuffer.deletedFeatureIds()
            #1 - changed
            changedMap = editBuffer.changedGeometries()
            for featid in changedMap.keys():
                newFeat = inputLyr.getFeatures(QgsFeatureRequest(featid)).next()
                newFeat.setGeometry(changedMap[featid])
                featureMap[featid]= newFeat
            #2 - old
            for feat in inputLyr.getFeatures():
                featid = feat.id()
                if featid not in featureMap.keys() and featid not in blackList:
                    featureMap[featid] = feat
            #3 -added
            for feat in editBuffer.addedFeatures().values():
                featureMap[featid] = feat
        else:
            #2 - just the old
            for feat in inputLyr.getFeatures():
                featid = feat.id()
                if featid not in featureMap.keys() and featid not in blackList:
                    featureMap[featid] = feat            
        return featureMap
    
    def prepareWorkingStructure(self, tableName, layer):
        try:
            self.abstractDb.createAndPopulateTempTableFromMap(tableName, layer)
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
    def outputData(self, type, inputClass, dataDict):
        '''
        type: postgis or qgsvectorlayer
        inputClass: name of the class
        dataDict: dict with the keys update, delete or insert. for each type, there is a proper data, ie:
            postgis: tuple of (id,geom)
            qgsvectorlayer: layer with geometry 
        '''
        edgvLayer = self.layerFactory.makeLayer(self.abstractDb, self.codeList, inputClass)
        dbName = edgvLayer.prepareLoad()
        epsg = self.abstractDb.findEPSG()
        crs = QgsCoordinateReferenceSystem(epsg, QgsCoordinateReferenceSystem.EpsgCrsId)
        outputLayer = edgvLayer.load(crs, dbName, uniqueLoad = True)
        if type == 'postgis':
            ret = self.outputPostgisData(outputLayer, inputClass, dataDict)
        else:
            ret = self.outputVectorData(outputLayer, inputClass,dataDict)
        
    def outputPostgisData(self, outputLayer, inputClass, dataDict):
        '''
        outputLayer: edgv layer previously loaded;
        inputClass: name of the class;
        dataDict: dict with the keys update, delete or insert. for each type, there is a key of names of the fields and values with a list of tupples.
        '''
        outputLayer.startEditing()
        for type in dataDict.keys():
            if type == 'INSERT':
                self.insertFeaturesFromPostgis(outputLayer, type, dataDict)
            elif type == 'UPDATE':
                self.updateFeaturesFromPostgis(outputLayer, type, dataDict)
            elif type == 'DELETE':
                self.deleteFeaturesFromPostgis(outputLayer, type, dataDict)

    def insertFeaturesFromPostgis(self, outputLayer, type, dataDict):
        for attributes in dataDict[type].keys():
            attrList = attributes.split(',')
            fieldDict = dict()
            for attr in attrList:
                fieldDict[attr] = outputLayer.fieldNameIndex(attr)
            featList = []
            for tuple in dataDict[type][attributes]:
                newFeat = QgsFeature(outputLayer.pendingFields())
                insertDict = dict()
                for i in range(len(attrList)):
                    if attrList[i] == 'id':
                        pass
                    elif attrList[i] == 'geom':
                        wkbGeom = tuple[i]
                        geom = QgsGeometry()
                        geom.fromWkb(wkbGeom)
                        newFeat.setGeometry(geom)
                    else:
                        newFeat.setAttribute(fieldDict[attrList[i]],tuple[i])
                featList.append(newFeat)
            outputLayer.addFeatures(featList)

    def updateFeaturesFromPostgis(self, outputLayer, type, dataDict):
        for attributes in dataDict[type].keys():
            attrList = attributes.split(',')
            fieldDict = dict()
            for attr in attrList:
                fieldDict[attr] = outputLayer.fieldNameIndex(attr)
            featList = []
            for tuple in dataDict[type][attributes]:
                insertDict = dict()
                for i in range(len(attrList)):
                    if attrList[i] == 'id':
                        id = tuple[i]
                    elif attrList[i] == 'geom':
                        wkbGeom = tuple[i]
                        geom = QgsGeometry()
                        geom.fromWkb(wkbGeom)
                for i in range(len(attrList)):
                    if attrList[i] not in ['id', 'geom']:
                        outputLayer.changeAttributeValue(int(id), fieldDict[attrList[i]], tuple[i])
                    elif attrList[i] == 'geom':
                        outputLayer.changeGeometry(int(id), geom)
    
    def deleteFeaturesFromPostgis(self, outputLayer, type, dataDict):
        for attributes in dataDict[type].keys():
            attrList = attributes.split(',')
            fieldDict = dict()
            for attr in attrList:
                fieldDict[attr] = outputLayer.fieldNameIndex(attr)
            featList = []
            for tuple in dataDict[type][attributes]:
                outputLayer.deleteFeature(tuple[0])
    
    def outputVectorData(self, outputLayer, inputClass, dataDict):
        '''
        outputLayer: edgv layer previously loaded;
        inputClass: name of the class;
        dataDict: dict with the keys UPDATE, DELETE or INSERT. For each type, there is a list of features to be output.
        '''
        outputLayer.startEditing()
        for type in dataDict.keys():
            if type == 'INSERT':
                self.insertFeatures(outputLayer, type, dataDict)
            elif type == 'UPDATE':
                self.updateFeatures(outputLayer, type, dataDict)
            elif type == 'DELETE':
                self.deleteFeatures(outputLayer, type, dataDict)

    def insertFeatures(self, outputLayer, type, dataDict):
        #TODO
        featureList = dataDict[type]
        pass

    def updateFeatures(self, outputLayer, type, dataDict):
        #TODO
        featureList = dataDict[type]
        pass

    def deleteFeatures(self, outputLayer, type, dataDict):
        #TODO
        featureList = dataDict[type]
        pass
    