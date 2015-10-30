# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-10-21
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import os
from osgeo import ogr
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from PyQt4.QtSql import QSqlQuery, QSqlDatabase
from PyQt4.QtCore import QSettings, SIGNAL, pyqtSignal, QObject
from DsgTools.Utils.utils import Utils

class DbSignals(QObject):
        updateLog = pyqtSignal(str)
        clearLog = pyqtSignal()

class AbstractDb(QObject):

    
    def __init__(self):
        super(AbstractDb,self).__init__()
        self.conversionTypeDict = dict({'QPSQL':'postgis','QSQLITE':'spatialite'})
        self.utils = Utils()
        self.signals = DbSignals()
        pass
    
    def __del__(self):
        if self.db.isOpen():
            self.db.close()
            self.db = None
    
    def checkAndOpenDb(self):
        if not self.db.isOpen():
            if not self.db.open():
                raise Exception(self.tr('Error when openning datatabase.\n')+self.db.lastError().text())

    def connectDatabase(self,conn=None):
        return None
    
    def connectDatabaseWithParameters(self,host,port,database,user,password):
        return None

    def connectDatabaseWithQSettings(self,name):
        return None

    def connectDatabaseWithGui(self):
        return None
    
    def getDatabaseVersion(self):
        return None
    
    def getType(self):
        return self.db.driverName()
    
    def listGeomClassesFromDatabase(self):
        return None

    def listComplexClassesFromDatabase(self):
        return None    

    def getConnectionFromQSettings(self, conName):
        return None

    def storeConnection(self, server):
        return None
        
    def getServerConfiguration(self, name):
        return None

    def countElements(self, layers):
        self.checkAndOpenDb()
        listaQuantidades = []
        for layer in layers:
            sql = self.gen.getElementCountFromLayer(layer)
            query = QSqlQuery(sql,self.db)
            query.next()
            number = query.value(0)
            if not query.exec_(sql):
                QgsMessageLog.logMessage(self.tr("Problem counting elements: ")+query.lastError().text(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            listaQuantidades.append([layer, number])
        return listaQuantidades     

    def findEPSG(self):
        self.checkAndOpenDb()    
        sql = self.gen.getSrid()
        query = QSqlQuery(sql, self.db)
        srids = []
        while query.next():
            srids.append(query.value(0))
        return srids[0]


    def listWithElementsFromDatabase(self, classList):
        self.checkAndOpenDb()
        classListWithNumber = self.countElements(classList)
        classesWithElements = dict()
        for cl in classListWithNumber:
            if cl[1]>0:
                classesWithElements[cl[0]]=cl[1]   
        return classesWithElements

    def listClassesWithElementsFromDatabase(self):
        geomClassList = self.listGeomClassesFromDatabase()
        complexClassList = self.listComplexClassesFromDatabase()
        classList = []
        for g in geomClassList:
            classList.append(g)
        for c in complexClassList:
            classList.append(c)
        classList.sort()
        return self.listWithElementsFromDatabase(classList)

    def getStructureDict(self):
        return None

    def makeOgrConn(self):
        return None    

    def getNotNullDict(self):
        return None

    def getDomainDict(self):
        return None

    def getAggregationAttributes(self):
        self.checkAndOpenDb()       
        columns = []
        sql = self.gen.getAggregationColumn()
        query = QSqlQuery(sql, self.db)
        while query.next():
            value = query.value(0)
            columns.append(value)
        return columns

    def buildOgrDatabase(self):
        return None

    def getOgrDatabase(self):
        if self.ogrDb != None:
            self.buildOgrDatabase()
            return self.ogrDb

    def buildFieldMap(self):
        self.checkAndOpenDb()
        fieldMap = self.getStructureDict()
        return fieldMap

    def validateWithOutputDatabaseSchema(self,outputdb):
        return None
    
    def convertDatabase(self,outputAbstractDb,type):
        self.signals.clearLog.emit()
        if outputAbstractDb.db.driverName() == 'QPSQL':
            return self.convertToPostgis(outputAbstractDb,type)
        if outputAbstractDb.db.driverName() == 'QSQLITE':
            return self.convertToSpatialite(outputAbstractDb,type)
        return None
    
    def convertToPostgis(self, outputAbstractDb,type):
        return None
    
    def convertToSpatialite(self, outputAbstractDb,type):
        return None 

    def buildInvalidatedDict(self):
        return None
    
    def makeValidationSummary(self,invalidated):
        hasErrors = False
        for key in invalidatedDataDict.keys():
            if len(invalidatedDataDict[key].keys()) > 0:
                hasErrors = True
        if hasErrors:
            self.signals.updateLog.emit('\n'+'{:-^60}'.format(self.tr('Validation Problems Summary')))
            for key in invalidatedDataDict.keys():
                
                if key == 'nullLine' and len(invalidatedDataDict[key].keys())>0:
                    self.signals.updateLog.emit(self.tr('\n\nClasses with null lines:\n'))
                    self.signals.updateLog.emit('\n\n'+'{:<50}'.format(self.tr('Class'))+self.tr('Elements\n\n'))
                    for cl in invalidatedDataDict[key].keys():
                        self.signals.updateLog.emit('{:<50}'.format(cl)+str(invalidatedDataDict[key][cl])+'\n')

                if key == 'nullPk' and len(invalidatedDataDict[key].keys())>0:
                    self.signals.updateLog.emit(self.tr('\n\nClasses with null primary keys:\n'))
                    self.signals.updateLog.emit('\n\n'+'{:<50}'.format(self.tr('Class'))+self.tr('Elements\n\n'))
                    for cl in invalidatedDataDict[key].keys():
                        self.signals.updateLog.emit('{:<50}'.format(cl)+str(invalidatedDataDict[key][cl])+'\n')

                if key == 'notInDomain' and len(invalidatedDataDict[key].keys())>0:
                    self.signals.updateLog.emit(self.tr('\n\nFeatures with attributes not in domain:\n\n'))
                    for cl in invalidatedDataDict[key].keys():
                        self.signals.updateLog.emit(self.tr('\nClass: ')+cl+'\n')
                        for id in invalidatedDataDict[key][cl].keys():
                            attrCommaList = '(id,'+','.join(invalidatedDataDict[key][cl][id].keys())+') = '
                            at = invalidatedDataDict[key][cl][id].keys()
                            valueList = '('+str(id)
                            for i in range(len(at)):
                                valueList += ','+str(invalidatedDataDict[key][cl][id][at[i]])
                            valueList += ')\n'
                            self.signals.updateLog.emit(attrCommaList+valueList)

                if key == 'nullAttribute' and len(invalidatedDataDict[key].keys())>0:
                    self.signals.updateLog.emit(self.tr('\n\nFeatures with null attributes in a not null field:\n\n'))
                    for cl in invalidatedDataDict[key].keys():
                        self.signals.updateLog.emit(self.tr('Class: ')+cl+'\n')
                        for id in invalidatedDataDict[key][cl].keys():
                            attrCommaList = '(id,'+','.join(invalidatedDataDict[key][cl][id].keys())+') = '
                            valueList = '('+str(id)
                            for attr in invalidatedDataDict[key][cl][id].keys():
                                valueList += ','+str(invalidatedDataDict[key][cl][id][attr])
                            valueList += ')\n'
                            self.signals.updateLog.emit(attrCommaList+valueList)
        return hasErrors
    
    def translateOGRLayerNameToOutputFormat(self,lyr,outputAbstractDb):
        return None
    
    def getTableSchema(self,lyr):
        return None
            
    def buildReadSummary(self,inputOgrDb,outputAbstractDb,classList):
        self.signals.clearLog.emit() #Clears log
        inputType = self.conversionTypeDict[self.db.driverName()]
        outputType = self.conversionTypeDict[outputAbstractDb.db.driverName()]
        self.signals.updateLog.emit(self.tr('Conversion type: ')+inputType+'2'+outputType+'\n')
        self.signals.updateLog.emit(self.tr('\nInput database: ')+self.db.databaseName()+'\n')
        self.signals.updateLog.emit(self.tr('\nOutput database: ')+outputAbstractDb.db.databaseName()+'\n')
        self.signals.updateLog.emit('\n'+'{:-^60}'.format(self.tr('Read Summary')))
        self.signals.updateLog.emit('\n\n'+'{:<50}'.format(self.tr('Class'))+self.tr('Elements\n\n'))
        for cl in classList:
            self.signals.updateLog.emit('{:<50}'.format(cl)+str(inputOgrDb.GetLayerByName(str(cl)).GetFeatureCount())+'\n')
        return None
    
    def makeTranslationMap(self, layerName, layer, outLayer, fieldMapper):
        layerFieldMapper=fieldMapper[layerName]
        layerDef = layer.GetLayerDefn()
        outLayerDef = outLayer.GetLayerDefn()
        panMap = []        
        for i in range(layerDef.GetFieldCount()):
            featureDef = layerDef.GetFieldDefn(i)
            fieldName = featureDef.GetName()
            if fieldName in layerFieldMapper.keys():
                name = layerFieldMapper[fieldName]
                fieldId = outLayerDef.GetFieldIndex(name)
                panMap.append(fieldId) 
            else:
                panMap.append(-1)
        return panMap
    
    def translateLayer(self, inputLayer, inputLayerName, outputLayer, outputFileName, layerPanMap, defaults={}, translateValues={}):
        inputLayer.ResetReading()
        initialCount = outputLayer.GetFeatureCount()
        count = 0
        for feat in inputLayer:
            newFeat=ogr.Feature(outputLayer.GetLayerDefn())
            newFeat.SetFromWithMap(feat,True,layerPanMap)
            outputLayer.CreateFeature(newFeat)
            count += 1
        return (count, outputLayer.GetFeatureCount()-initialCount)
    
    def translateDS(self, inputDS, outputDS, fieldMap, inputLayerList): 
        self.signals.updateLog.emit('\n'+'{:-^60}'.format(self.tr('Write Summary')))
        self.signals.updateLog.emit('\n\n'+'{:<50}'.format(self.tr('Class'))+self.tr('Elements\n\n'))
        status = False
        for inputLyr in inputLayerList:
            schema = self.getTableSchema(inputLyr)
            attr = fieldMap[inputLyr].keys()
            attrList = []
            for a in attr:
                if schema == 'complexos':
                    attrList.append(a)
                elif a not in ['id']:
                    attrList.append(a)
            sql = self.gen.getFeaturesWithSQL(inputLyr,attrList) #order elements here
            inputOgrLayer = inputDS.ExecuteSQL(sql.encode('utf-8'))
            outputFileName = self.translateOGRLayerNameToOutputFormat(inputLyr,outputDS)
            outputLayer=outputDS.GetLayerByName(outputFileName)
            #order conversion here
            layerPanMap=self.makeTranslationMap(inputLyr, inputOgrLayer,outputLayer, fieldMap)
            (iter,diff)=self.translateLayer(inputOgrLayer, inputLyr, outputLayer, outputFileName, layerPanMap)
            if iter == diff:
                status = True
            else:
                status = False
            self.signals.updateLog.emit('{:<50}'.format(str(outputFileName))+str(diff)+','+str(iter)+'\n')
        outputDS.Destroy()
        return status