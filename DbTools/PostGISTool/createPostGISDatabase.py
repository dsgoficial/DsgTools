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

import sys, os

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

    def run(self):
        # QThread
        self.mutex.lock()
        self.stopMe = 0
        self.mutex.unlock()
        
        self.createDatabaseStructure()

        # Processing ending
        self.emit( SIGNAL( "processingFinished()" ) )
    
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
        file = open(edgvPath, "r")
        sql = file.read()
        sql = sql.replace('[epsg]', str(self.epsg))
        file.close()
        commands = sql.split(';')

        # Progress bar steps calculated
        self.emit( SIGNAL( "rangeCalculated( PyQt_PyObject )" ), len(commands))
        
        self.db.transaction()
        query = QSqlQuery(self.db)
        for command in commands:
            if not query.exec_(command):
                print query.lastError().text()
                self.db.rollback()
                self.db.close()
                return False
            # Updating progress
            self.emit( SIGNAL( "queryProcessed()" ) )
        self.db.commit()
        self.db.close()
        return True
    