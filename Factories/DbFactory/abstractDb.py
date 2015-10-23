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
from PyQt4.QtCore import QSettings
from PyQt4.Qt import QObject


class AbstractDb(QObject):
    
    def __init__(self):
        super(AbstractDb,self).__init__()
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
    
    def convertToPostgis(self, outputDb, invalidatedDict,type):
        return None
    
    def convertToSpatialite(self, outputDb):
        return None    
