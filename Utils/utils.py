# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import QSqlDatabase,QSqlQuery

import qgis as qgis
from qgis.gui import QgsMessageBar
from qgis.core import QgsMessageLog

import os
from osgeo import ogr
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory

class Utils:
    def __init__(self):
        self.factory = SqlGeneratorFactory()

    def __del__(self):
        pass
    
    def mergeDict(self,dictionary1, dictionary2):
        output = dict()
        if type(dictionary1) <> dict or type(dictionary2) <> dict:
            return dictionary2
        for item, value in dictionary1.iteritems():
            if dictionary2.has_key(item):
                if isinstance(dictionary2[item], dict):
                    output[item] = self.mergeDict(value, dictionary2.pop(item))
                else:
                    if type(value) == list:
                        if item not in output.keys():
                            output[item] = []
                        for i in value:
                            if i not in output[item]:
                                output[item].append(i)
                        output[item].extend(self.mergeDict(value, dictionary2.pop(item)))
                    else:
                        output[item] = self.mergeDict(value, dictionary2.pop(item))
            else:
                if type(value) == list:
                    if item not in output.keys():
                        output[item]=[]
                    for i in value:
                        if i not in output[item]:
                            output[item].append(i)
                else:
                    output[item] = value
        for item, value in dictionary2.iteritems():
            if type(value) == list:
                if item not in output.keys():
                    output[item]=[]
                for i in value:
                    if i not in output[item]:
                        output[item].append(i)
            else:
                output[item] = value
        return output
    
    def buildOneNestedDict(self,inputDict,keyList,value):
        if len(keyList) == 1:
            if keyList[0] not in inputDict.keys():
                inputDict[keyList[0]] = dict()
            if type(value) == list:
                inputDict[keyList[0]]=[]
                for i in value:
                    if i not in inputDict[keyList[0]]:
                        inputDict[keyList[0]].append(i)
            else:
                inputDict[keyList[0]]=value
            return inputDict
        else:
            if keyList[0] not in inputDict.keys():
                if len(inputDict.values()) == 0:
                    inputDict[keyList[0]] = dict()
            inputDict[keyList[0]] = self.buildOneNestedDict(inputDict[keyList[0]],keyList[1::],value)
            return inputDict
    
    def buildNestedDict(self,inputDict,keyList,value):
        if len(inputDict.keys())>0:
            tempDict = self.buildOneNestedDict(dict(),keyList,value)
            return self.mergeDict(inputDict, tempDict)
        else:
            return self.buildOneNestedDict(inputDict,keyList,value)

    def getPostGISConnectionParameters(self, name):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/connections/'+name)
        database = settings.value('database')
        host = settings.value('host')
        port = settings.value('port')
        user = settings.value('username')
        password = settings.value('password')
        settings.endGroup()
        return (database, host, port, user, password)

    def getPostGISConnections(self):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/connections')
        currentConnections = settings.childGroups()
        settings.endGroup()
        return currentConnections
    
    def getPostGISDatabase(self, postGISConnection):
        (database, host, port, user, password) = self.getPostGISConnectionParameters(postGISConnection)
        return self.getPostGISDatabaseWithParams(database, host, port, user, password)
    
    def getPostGISDatabaseWithParams(self, database, host, port, user, password):
        db = None
        db = QSqlDatabase("QPSQL")
        db.setDatabaseName(database)
        db.setHostName(host)
        db.setPort(int(port))
        db.setUserName(user)
        db.setPassword(password)
        return db

    def isSpatialiteDB(self, db):
        if db.driverName() == 'QPSQL':
            isSpatialite = False
        elif db.driverName() == 'QSQLITE':
            isSpatialite = True
        return isSpatialite
    
    #TODO: Reimplement in server_tools
    def browseServer(self,dbList,host,port,user,password):
        gen = self.factory.createSqlGenerator(False)
        edvgDbList = []
        for database in dbList:
            db = self.getPostGISDatabaseWithParams(database,host,port,user,password)
            if not db.open():
                qgis.utils.iface.messageBar().pushMessage('DB :'+database+'| msg: '+db.lastError().databaseText(), level=QgsMessageBar.CRITICAL)

            query = QSqlQuery(db)
            if query.exec_(gen.getEDGVVersion()):
                while query.next():
                    version = query.value(0)
                    if version:
                        edvgDbList.append((database,version))
        return edvgDbList
    
    #TODO: Reimplement in server_tools    
    def getDbsFromServer(self,name):
        gen = self.factory.createSqlGenerator(False)
        
        (host, port, user, password) = self.getServerConfiguration(name)
        database = 'postgres'
        
        db = self.getPostGISDatabaseWithParams(database,host,port,user,password)
        if not db.open():
            QgsMessageLog.logMessage(db.lastError().text(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        
        query = QSqlQuery(gen.getDatabasesFromServer(),db)
        dbList = []
        while query.next():
            dbList.append(query.value(0))
        return self.browseServer(dbList,host,port,user,password)
