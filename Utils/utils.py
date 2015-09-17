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

import os
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory

class Utils:
    def __init__(self):
        self.factory = SqlGeneratorFactory()

    def __del__(self):
        pass

    def getQmlDir(self, db):
        currentPath = os.path.dirname(__file__)
        if qgis.core.QGis.QGIS_VERSION_INT >= 20600:
            qmlVersionPath = os.path.join(currentPath, '..', 'Qmls', 'qgis_26')
        else:
            qmlVersionPath = os.path.join(currentPath, '..', 'Qmls', 'qgis_22')

        version = self.getDatabaseVersion(db)
        if version == '3.0':
            qmlPath = os.path.join(qmlVersionPath, 'edgv_30')
        elif version == '2.1.3':
            qmlPath = os.path.join(qmlVersionPath, 'edgv_213')
        return qmlPath

    def findEPSG(self, db):
        gen = self.factory.createSqlGenerator(self.isSpatialiteDB(db))
        sql = gen.getSrid()
        query = QSqlQuery(sql, db)
        srids = []
        while query.next():
            srids.append(query.value(0))
        return srids[0]

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

    def getSpatialiteDatabase(self):
        db = None
        fd = QFileDialog()
        filename = fd.getOpenFileName(filter='*.sqlite')
        if filename:
            db = QSqlDatabase("QSQLITE")
            db.setDatabaseName(filename)
        return (filename, db)

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

    def getDatabaseVersion(self, db):
        gen = self.factory.createSqlGenerator(self.isSpatialiteDB(db))
        sqlVersion = gen.getEDGVVersion()
        queryVersion =  QSqlQuery(sqlVersion, db)
        version = '2.1.3'
        while queryVersion.next():
            version = queryVersion.value(0)
        return version

    def isSpatialiteDB(self, db):
        if db.driverName() == 'QPSQL':
            isSpatialite = False
        elif db.driverName() == 'QSQLITE':
            isSpatialite = True
        return isSpatialite
    
    def getServerConfiguration(self, name):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers/'+name)
        host = settings.value('host')
        port = settings.value('port')
        user = settings.value('username')
        password = settings.value('password')
        settings.endGroup()
        return (host, port, user, password)
    
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
    
    def storeConnection(self, server, database):
        (host, port, user, password) = self.getServerConfiguration(server)
        
        connection = server+'_'+database
        settings = QSettings()
        if not settings.contains('PostgreSQL/connections/'+connection+'/database'):
            settings.beginGroup('PostgreSQL/connections/'+connection)
            settings.setValue('database', database)
            settings.setValue('host', host)
            settings.setValue('port', port)
            settings.setValue('username', user)
            settings.setValue('password', password)
            settings.endGroup()
            return True
        return False
            