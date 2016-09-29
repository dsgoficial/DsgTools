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
from PyQt4.Qt import QObject

#QGIS imports
from qgis.core import QgsCoordinateReferenceSystem, QgsGeometry, QgsFeature, QgsDataSourceURI, QgsFeatureRequest, QgsMessageLog, QgsExpression

# DSGTools imports
from DsgTools.Factories.LayerLoaderFactory.layerLoaderFactory import LayerLoaderFactory

class ValidationProcess(QObject):
    def __init__(self, postgisDb, iface):
        '''
        Constructor
        '''
        super(ValidationProcess, self).__init__()
        self.abstractDb = postgisDb
        if self.getStatus() == None:
            self.setStatus('Instantianting process', 0)
        self.classesToBeDisplayedAfterProcess = []
        self.parameters = None
        self.iface = iface
        self.layerLoader = LayerLoaderFactory().makeLoader(self.iface, self.abstractDb)
        
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
        '''
        Gets the layer features considering the edit buffer in the case
        the layer is already in edition mode
        '''
        #return dict
        featureMap = dict()
        #getting edit buffer
        editBuffer = inputLyr.editBuffer()
        #black list for removed features
        blackList = []
        if editBuffer:
            blackList = editBuffer.deletedFeatureIds()
            #1 - changed
            changedMap = editBuffer.changedGeometries()
            for featid in changedMap.keys():
                newFeat = inputLyr.getFeatures(QgsFeatureRequest(featid)).next()
                newFeat.setGeometry(changedMap[featid])
                featureMap[featid] = newFeat
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
        '''
        Creates a temp table where all features plus the edit buffer features from a layer
        will be inserted
        '''
        try:
            self.abstractDb.createAndPopulateTempTableFromMap(tableName, layer)
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
    # def outputData(self, type, inputClass, dataDict):
    #     '''
    #     type: postgis or qgsvectorlayer
    #     inputClass: name of the class
    #     dataDict: dict with the keys update, delete or insert. for each type, there is a proper data, ie:
    #         postgis: dict like this:
    #                 {'UPDATE': {'id,geom': [[id value as int, geom value in wkb]]}}
    #         qgsvectorlayer: layer with geometry
    #     '''
    #     outputLayer = self.layerLoader.load([inputClass], uniqueLoad=True)[inputClass]
    #     if type == 'postgis':
    #         ret = self.outputPostgisData(outputLayer, dataDict)
    #     else:
    #         ret = self.outputVectorData(outputLayer, dataDict)
    #
    # def outputPostgisData(self, outputLayer, dataDict):
    #     '''
    #     Deals with postgis outputs.
    #     outputLayer: edgv layer previously loaded;
    #     dataDict: dict with the keys update, delete or insert. For each type
    #                 there is a key of names of the fields and values with a list of lists.
    #     '''
    #     outputLayer.startEditing()
    #     for type in dataDict.keys():
    #         if type == 'INSERT':
    #             self.insertFeaturesFromPostgis(outputLayer, dataDict[type])
    #         elif type == 'UPDATE':
    #             self.updateFeaturesFromPostgis(outputLayer, dataDict[type])
    #         elif type == 'DELETE':
    #             self.deleteFeaturesFromPostgis(outputLayer, dataDict[type])
    #
    # def makeFieldDict(self, outputLayer, attrList):
    #     '''
    #     Build the field dict where the name of an attribute points to its index
    #     '''
    #     #dict where the name of an attribute points to its index
    #     fieldDict = dict()
    #     for attr in attrList:
    #         fieldDict[attr] = outputLayer.fieldNameIndex(attr)
    #     return fieldDict
    #
    # def insertFeaturesFromPostgis(self, outputLayer, dataDict):
    #     '''
    #     Inserts features marked as new into the output layer
    #     outputLayer: edgv layer previously loaded;
    #     dataDict: Dict where there is a key of names of the fields and values with a list of lists.
    #     '''
    #     for attributes in dataDict.keys():
    #         attrList = attributes.split(',')
    #         #dict where the name of an attribute points to its index
    #         fieldDict = self.makeFieldDict(outputLayer, attrList)
    #         #features to be inserted
    #         featList = []
    #         for tuple in dataDict[attributes]:
    #             #creating new feature
    #             newFeat = QgsFeature(outputLayer.pendingFields())
    #             for i in range(len(attrList)):
    #                 if attrList[i] == 'geom':
    #                     wkbGeom = tuple[i]
    #                     geom = QgsGeometry()
    #                     geom.fromWkb(wkbGeom)
    #                     newFeat.setGeometry(geom)
    #                 else:
    #                     #everything else
    #                     newFeat.setAttribute(fieldDict[attrList[i]], tuple[i])
    #             featList.append(newFeat)
    #         outputLayer.addFeatures(featList)
    #
    # def updateFeaturesFromPostgis(self, outputLayer, dataDict):
    #     '''
    #     Updates features from the output layer
    #     outputLayer: edgv layer previously loaded;
    #     dataDict: Dict where there is a key of names of the fields and values with a list of lists.
    #     '''
    #     for attributes in dataDict.keys():
    #         attrList = attributes.split(',')
    #         #dict where the name of an attribute points to its index
    #         fieldDict = self.makeFieldDict(outputLayer, attrList)
    #         for tuple in dataDict[attributes]:
    #             for i in range(len(attrList)):
    #                 if attrList[i] == 'id':
    #                     id = tuple[i]
    #                 elif attrList[i] == 'geom':
    #                     wkbGeom = tuple[i]
    #                     geom = QgsGeometry()
    #                     geom.fromWkb(wkbGeom)
    #                     outputLayer.changeGeometry(int(id), geom)
    #                 else:
    #                     outputLayer.changeAttributeValue(int(id), fieldDict[attrList[i]], tuple[i])
    #
    # def deleteFeaturesFromPostgis(self, outputLayer, dataDict):
    #     '''
    #     Deletes features from output layer
    #     '''
    #     for attributes in dataDict.keys():
    #         for tuple in dataDict[attributes]:
    #             outputLayer.deleteFeature(tuple[0])
    
    def updateOriginalLayer(self, pgInputLayer, qgisOutputVector):
        '''
        Updates the original layer using the grass output layer
        pgInputLyr: postgis input layer
        grassOutputLyr: grass output layer
        '''
        provider = pgInputLayer.dataProvider()
        pgInputLayer.startEditing()
        addList = []
        idsToRemove = []
        #making the changes and inserts
        for feature in pgInputLayer.getFeatures():
            id = feature['id']
            outFeats = []
            #getting the output features with the specific id
            for gf in qgisOutputVector.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression("id=%d"%id))):
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
                    idx = newFeat.fieldNameIndex('id')
                    newFeat.setAttribute(idx, provider.defaultValue(idx))
                    addList.append(newFeat)
            #in the case we don't find features in the output we should mark them to be removed
            if len(outFeats) == 0:
                idsToRemove.append(id)
        #pushing the changes into the edit buffer
        pgInputLayer.addFeatures(addList, True)
        #removing features from the layer.
        pgInputLayer.deleteFeatures(idsToRemove)

    def getProcessingErrors(self, layer):
        '''
        Gets processing errors
        layer: error layer (QgsVectorLayer) output made by grass
        '''
        recordList = []
        for feature in layer.getFeatures():
            recordList.append((feature.id(), binascii.hexlify(feature.geometry().asWkb())))
        return recordList