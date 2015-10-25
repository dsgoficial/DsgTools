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
from DsgTools.Factories.DbFactory.abstractDb import AbstractDb
from PyQt4.QtSql import QSqlQuery

class SpatialiteDb(AbstractDb):

    def __init__(self):
        super(SpatialiteDb,self).__init__()
        self.db = QSqlDatabase('QSQLITE')
    
    def connectDatabaseWithServerName(self,name):
        return None
    
    def listGeomClassesFromDatabase(self):
        self.checkAndOpenDb()
        classList = []
        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        while query.next():
            tableName = query.value(0).toString()
            layerName = tableName
            classList.append(layerName)
        return classList
    
    def listComplexClassesFromDatabase(self):
        self.checkAndOpenDb()
        classList = []
        gen = self.factory.createSqlGenerator(isSpatialite)
        sql = gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        while query.next():
                tableName = query.value(0).toString()
                layerName = tableName
                tableSchema = layerName.split('_')[0]
                classList.append(layerName)
        return classList    

    def storeConnection(self, server):
        return None
        
    def getServerConfiguration(self, name):
        return None

    def storeConnection(self, server):
        return None

    def getStructureDict(self):
        self.checkAndOpenDb()
        classDict = dict()
        sql = self.gen.getStructure(self.dbVersion)        
        query = QSqlQuery(sql, self.db)
        while query.next():
            className = query.value(0).toString()
            classSql = query.value(1).toString()
            if className not in classDict.keys():
                classDict[className]=dict()
            classSql = classSql.split(className)[1]
            sqlList = classSql.replace('(','').replace(')','').replace('\"','').replace('\'','').split(',')
            for s in sqlList:
                 fieldName = str(s.strip().split(' ')[0])
                 classDict[className][fieldName]=fieldName

        return classDict
    
    def makeOgrConn(self):
        constring = self.db.databaseName()
        return constring

    def buildOgrDatabase(self):
        con = self.makeOgrConn()
        self.ogrDb = ogr.Open(con,update=1)

    def getNotNullDict(self):
        return None

    def getDomainDict(self):
        return None

    def convertToPostgis(self, outputDb,type):
        return None
    
    def convertToSpatialite(self, outputDb,type):
        return None    

    def makeValidationSummary(self):
        return None

    def validateWithOutputDatabaseSchema(self,outputdb):
        return None
    
    def buildInvalidatedDict(self):
        return None
    
    def buildInvalidatedLog(self,invalidated):
        return None