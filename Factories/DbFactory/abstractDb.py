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
from PyQt4.QtCore import QSettings, SIGNAL, pyqtSignal
from PyQt4.Qt import QObject
from apt.auth import update


class AbstractDb(QObject):
    updateLog = pyqtSignal(str)
    clearLog = pyqtSignal()
    
    def __init__(self):
        super(AbstractDb,self).__init__()
        self.conversionTypeDict = dict({'QPSQL':'postgis','QSQLITE':'spatialite'})
        pass
    
    def __del__(self):
        if self.db.isOpen():
            self.db.close()
            self.db = None
    
    def checkAndOpenDb(self):
        if not self.db.isOpen():
            if not self.db.open():
                raise Exception(self.tr('Error when openning datatabase.\n')+self.db.lastError().text())

    def connectDatabaseWithServerName(self,name):
        return None
    
    def getDatabaseVersion(self):
        self.checkAndOpenDb()
        sqlVersion = self.gen.getEDGVVersion()
        queryVersion =  QSqlQuery(sqlVersion, self.db)
        while queryVersion.next():
            version = queryVersion.value(0)
        return version
    
    def getType(self):
        return self.db.driverName()
    
    def listGeomClassesFromDatabase(self):
        return None

    def listComplexClassesFromDatabase(self):
        return None    
        
    def storeConnection(self, server):
        return None
        
    def getServerConfiguration(self, name):
        return None

    def storeConnection(self, server):
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
        classListWithNumber = self.countElements(classList, self.db)
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
    
    def convertDatabase(self,outputdb,type):
        if outputdb.driverName() == 'QPSQL':
            return self.convertToPostgis(outputdb,type)
        if outputdb.driverName() == 'QSQLITE':
            return self.convertToSpatialite(outputdb,type)
        return None
    
    def convertToPostgis(self, outputDb,type):
        return None
    
    def convertToSpatialite(self, outputDb,type):
        return None 

    def buildInvalidatedDict(self):
        return None
    
    def makeValidationSummary(self,invalidated):
        hasErrors = False
        for key in invalidatedDataDict.keys():
            if len(invalidatedDataDict[key].keys()) > 0:
                hasErrors = True
        if hasErrors:
            updateLog.emit('\n'+'{:-^60}'.format(self.tr('Validation Problems Summary')))
            for key in invalidatedDataDict.keys():
                
                if key == 'nullLine' and len(invalidatedDataDict[key].keys())>0:
                    updateLog.emit(self.tr('\n\nClasses with null lines:\n'))
                    updateLog.emit('\n\n'+'{:<50}'.format(self.tr('Class'))+self.tr('Elements\n\n'))
                    for cl in invalidatedDataDict[key].keys():
                        updateLog.emit('{:<50}'.format(cl)+str(invalidatedDataDict[key][cl])+'\n')

                if key == 'nullPk' and len(invalidatedDataDict[key].keys())>0:
                    updateLog.emit(self.tr('\n\nClasses with null primary keys:\n'))
                    updateLog.emit('\n\n'+'{:<50}'.format(self.tr('Class'))+self.tr('Elements\n\n'))
                    for cl in invalidatedDataDict[key].keys():
                        updateLog.emit('{:<50}'.format(cl)+str(invalidatedDataDict[key][cl])+'\n')

                if key == 'notInDomain' and len(invalidatedDataDict[key].keys())>0:
                    updateLog.emit(self.tr('\n\nFeatures with attributes not in domain:\n\n'))
                    for cl in invalidatedDataDict[key].keys():
                        updateLog.emit(self.tr('\nClass: ')+cl+'\n')
                        for id in invalidatedDataDict[key][cl].keys():
                            attrCommaList = '(id,'+','.join(invalidatedDataDict[key][cl][id].keys())+') = '
                            at = invalidatedDataDict[key][cl][id].keys()
                            valueList = '('+str(id)
                            for i in range(len(at)):
                                valueList += ','+str(invalidatedDataDict[key][cl][id][at[i]])
                            valueList += ')\n'
                            updateLog.emit(attrCommaList+valueList)

                if key == 'nullAttribute' and len(invalidatedDataDict[key].keys())>0:
                    updateLog.emit(self.tr('\n\nFeatures with null attributes in a not null field:\n\n'))
                    for cl in invalidatedDataDict[key].keys():
                        updateLog.emit(self.tr('Class: ')+cl+'\n')
                        for id in invalidatedDataDict[key][cl].keys():
                            attrCommaList = '(id,'+','.join(invalidatedDataDict[key][cl][id].keys())+') = '
                            valueList = '('+str(id)
                            for attr in invalidatedDataDict[key][cl][id].keys():
                                valueList += ','+str(invalidatedDataDict[key][cl][id][attr])
                            valueList += ')\n'
                            updateLog.emit(attrCommaList+valueList)
        return hasErrors
    
    def buildReadSummary(self,output,classDict):
        clearLog.emit() #Clears log
        inputType = self.conversionTypeDict[self.driverName()]
        outputType = self.conversionTypeDict[output.drivername()]
        updateLog.emit(self.tr('Conversion type: ')+inputType+'2'+outputType+'\n')
        updateLog.emit(self.tr('\nInput database: ')+self.databaseName()+'\n')
        updateLog.emit(self.tr('\nOutput database: ')+output.databaseName()+'\n')
        updateLog.emit('\n'+'{:-^60}'.format(self.tr('Read Summary')))
        updateLog.emit('\n\n'+'{:<50}'.format(self.tr('Class'))+self.tr('Elements\n\n'))
        classes = classesDict.keys()
        classes.sort()
        clStr = ''
        for i in classes:
            updateLog.emit('{:<50}'.format(i)+str(classesDict[i])+'\n')
        return None