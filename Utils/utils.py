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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import QSqlDatabase,QSqlQuery

from qgis.core import *
from qgis.gui import *
import qgis as qgis

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Factories', 'SqlFactory'))
from sqlGeneratorFactory import SqlGeneratorFactory

class Utils:
    def __init__(self):
        self.factory = SqlGeneratorFactory()
    
    def __del__(self):
        pass
    
    def getQmlDir(self):
        currentPath = os.path.dirname(__file__)
        if qgis.core.QGis.QGIS_VERSION_INT >= 20600:
            qmlVersionPath = os.path.join(currentPath, '..', 'Qmls', 'qgis_26')
        else:
            qmlVersionPath = os.path.join(currentPath, '..', 'Qmls', 'qgis_22')
        return qmlVersionPath      

    def findEPSG(self, isSpatialite):
        gen = self.factory.createSqlGenerator(isSpatialite)
        sql = self.gen.getSrid()
        query = QSqlQuery(sql, self.db)
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
        fd = QtGui.QFileDialog()
        filename = fd.getOpenFileName(filter='*.sqlite')
        if filename:
            db = QSqlDatabase("QSQLITE")
            db.setDatabaseName(filename)
        return (filename, db)
    
    def getPostGISDatabase(self, postGISConnection):
        db = None
        db = QSqlDatabase("QPSQL")
        (database, host, port, user, password) = self.getPostGISConnectionParameters(postGISConnection)
        db.setDatabaseName(database)
        db.setHostName(host)
        db.setPort(int(port))
        db.setUserName(user)
        db.setPassword(password)
        return db
    
    def getDatabaseVersion(self, isSpatialite):
        gen = self.factory.createSqlGenerator(isSpatialite)
        sqlVersion = gen.getEDGVVersion()
        queryVersion =  QSqlQuery(sqlVersion, self.db)
        queryVersion.next()
        if queryVersion is not None:
            version = queryVersion.value(0)
        else:
            version = '2.1.3'
        return version
        