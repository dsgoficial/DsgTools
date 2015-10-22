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
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtCore import QSettings


class AbstractDb:
    def __init__(self,qtsqlDb,isSpatialite):
        self.db = qtsqlDb
        self.gen = SqlGeneratorFactory().createSqlGenerator(isSpatialite)
        self.dbVersion = self.getDatabaseVersion()
        self.ogrDb = None
    
    def getDatabaseVersion(self):
        sqlVersion = self.gen.getEDGVVersion()
        queryVersion =  QSqlQuery(sqlVersion, self.db)
        while queryVersion.next():
            version = queryVersion.value(0)
        return version
    
    def getType(self):
        return self.db.driverName()
    
    def setConnection(self):
        return None
    
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
        sql = self.gen.getSrid()
        query = QSqlQuery(sql, self.db)
        srids = []
        while query.next():
            srids.append(query.value(0))
        return srids[0]

    def listWithElementsFromDatabase(self, classList):
        classListWithNumber = self.countElements(classList, self.db)
        classesWithElements = dict()
        for cl in classListWithNumber:
            if cl[1]>0:
                classesWithElements[cl[0]]=cl[1]   
        return classesWithElements

    def getStructureDict(self, edgvVersion):
        return None

    def makeOgrConn(self):
        return None    

    def getNotNullDict(self):
        return None

    def getDomainDict(self):
        return None

    def getAggregationAttributes(self):
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