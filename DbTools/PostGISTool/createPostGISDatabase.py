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
"""# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import QSqlDatabase,QSqlQuery
from sqlGeneratorFactory import SqlGeneratorFactory

from qgis.core import QgsMessageLog

import sys, os, codecs

class CreatePostGISDatabase(QThread):
    def __init__(self, db, version, epsg):
        """Constructor.
        """
        QThread.__init__( self, QThread.currentThread() )

        self.db = db
        self.version = version
        self.epsg = epsg

        # QThread
        self.mutex = QMutex()
        self.stopMe = 0
        self.factory = SqlGeneratorFactory()
        #setting the sql generator
        self.gen = self.factory.createSqlGenerator(False)

    def run(self):
        # QThread
        self.mutex.lock()
        self.stopMe = 0
        self.mutex.unlock()

        # Processing ending
        self.emit( SIGNAL( "processingFinished(PyQt_PyObject)" ), self.createDatabaseStructure())

    def stop( self ):
        # Stopping the thread
        self.mutex.lock()
        self.stopMe = 1
        self.mutex.unlock()
        QThread.wait( self )

    def createDatabaseStructure(self):
        currentPath = os.path.dirname(__file__)
        if self.version == '2.1.3':
            edgvPath = os.path.join(currentPath, 'sqls', '213', 'edgv213.sql')
        elif self.version == '3.0':
            edgvPath = os.path.join(currentPath, 'sqls', '30', 'edgv30.sql')
        else:
            pass
        return self.loadDatabaseStructure(edgvPath)

    def loadDatabaseStructure(self, edgvPath):
        file = codecs.open(edgvPath, encoding='utf-8', mode="r")
        sql = file.read()
        sql = sql.replace('[epsg]', str(self.epsg))
        file.close()
        commands = sql.split('#')

        # Progress bar steps calculated
        self.emit( SIGNAL( "rangeCalculated( PyQt_PyObject )" ), len(commands))

        self.db.transaction()
        query = QSqlQuery(self.db)

        update = True
        for command in commands:
            if self.stopMe == 0:
                if not query.exec_(command):
                    QgsMessageLog.logMessage(self.tr("Problem on database structure creation: ")+'SQL: '+command+'\n'+query.lastError().text()+'\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                    self.db.rollback()
                    self.db.close()
                    return 0

                # Updating progress
                self.emit( SIGNAL( "queryProcessed()" ))
            else:
                self.db.rollback()
                self.db.close()
                QgsMessageLog.logMessage(self.tr("User canceled datatabase structure creation"), "DSG Tools Plugin", QgsMessageLog.INFO)
                return -1

        self.db.commit()
        print self.db.connectionName()
        sql = self.gen.allowConnections(self.db.connectionName())
        print sql
        query = QSqlQuery(sql,self.db)
        self.db.commit()
        self.db.close()
        QgsMessageLog.logMessage(self.tr("Successful datatabase structure creation"), "DSG Tools Plugin", QgsMessageLog.INFO)
        return 1
