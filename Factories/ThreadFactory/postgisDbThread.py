# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-03-29
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
from PyQt4.QtSql import QSqlQuery, QSqlDatabase

from qgis.core import QgsMessageLog

import os, codecs

from DsgTools.Factories.ThreadFactory.genericThread import GenericThread
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory

class PostgisDbMessages(QObject):
    def __init__(self, thread):
        super(PostgisDbMessages, self).__init__()

        self.thread = thread

    def getProblemMessage(self, command, query):
        return self.tr("Problem on database structure creation: ")+'SQL: '+command+'\n'+query.lastError().text()+'\n'

    def getProblemFeedbackMessage(self):
        return self.tr('Problem creating the database structure!\n Check the Log terminal for details.')

    def getUserCanceledFeedbackMessage(self):
        return self.tr('User canceled the database structure creation!')

    def getSuccessFeedbackMessage(self):
        return self.tr("Successful datatabase structure creation")

    @pyqtSlot()
    def progressCanceled(self):
        self.thread.stopped[0] = True

class PostgisDbThread(GenericThread):
    def __init__(self):
        """
        Constructor.
        """
        super(PostgisDbThread, self).__init__()

        self.factory = SqlGeneratorFactory()
        #setting the sql generator
        self.gen = self.factory.createSqlGenerator(False)

        self.messenger = PostgisDbMessages(self)

    def setParameters(self, db, version, epsg, stopped):
        '''
        Sets thread parameters
        '''
        self.db = db
        self.version = version
        self.epsg = epsg
        self.stopped = stopped

    def run(self):
        '''
        Runs the process
        '''
        # Processing ending
        (ret, msg) = self.createDatabaseStructure()
        self.signals.processingFinished.emit(ret, msg, self.getId())

    def createDatabaseStructure(self):
        '''
        Creates database structure according to the selected edgv version
        '''
        currentPath = os.path.dirname(__file__)
        currentPath = os.path.join(currentPath, '..', '..', 'DbTools', 'PostGISTool')
        if self.version == '2.1.3':
            edgvPath = os.path.join(currentPath, 'sqls', '213', 'edgv213.sql')
        elif self.version == '3.0':
            edgvPath = os.path.join(currentPath, 'sqls', '30', 'edgv30.sql')
        elif self.version == 'FTer_2a_Ed':
            edgvPath = os.path.join(currentPath, 'sqls', 'FTer_2a_Ed', 'edgvFter_2a_Ed.sql')
        else:
            pass
        return self.loadDatabaseStructure(edgvPath)

    def loadDatabaseStructure(self, edgvPath):
        '''
        Loads the database structure
        edgvPath: path to the databse sql
        '''
        file = codecs.open(edgvPath, encoding='utf-8', mode="r")
        sql = file.read()
        sql = sql.replace('[epsg]', str(self.epsg))
        file.close()
        commands = sql.split('#')

        # Progress bar steps calculated
        self.signals.rangeCalculated.emit(len(commands), self.getId())

        self.db.transaction()
        query = QSqlQuery(self.db)

        for command in commands:
            if not self.stopped[0]:
                if not query.exec_(command):
                    QgsMessageLog.logMessage(self.messenger.getProblemMessage(command, query), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                    self.db.rollback()
                    self.db.close()
                    self.dropDatabase(self.db)
                    return (0, self.messenger.getProblemFeedbackMessage())

                # Updating progress
                self.signals.stepProcessed.emit(self.getId())
            else:
                self.db.rollback()
                self.db.close()
                self.dropDatabase(self.db)                
                QgsMessageLog.logMessage(self.messenger.getUserCanceledFeedbackMessage(), "DSG Tools Plugin", QgsMessageLog.INFO)
                return (-1, self.messenger.getUserCanceledFeedbackMessage())

        self.db.commit()
        if self.version == '2.1.3':
            sql = 'ALTER DATABASE %s SET search_path = "$user", public, topology,\'cb\',\'complexos\',\'dominios\';' % self.db.databaseName()
        elif self.version == 'FTer_2a_Ed':
            sql = 'ALTER DATABASE %s SET search_path = "$user", public, topology,\'pe\',\'ge\',\'complexos\',\'dominios\';' % self.db.databaseName()
        
        if not query.exec_(sql):
            QgsMessageLog.logMessage(self.messenger.getProblemMessage(command, query), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return (0, self.messenger.getProblemFeedbackMessage())
        
        self.db.close()
        QgsMessageLog.logMessage(self.messenger.getSuccessFeedbackMessage(), "DSG Tools Plugin", QgsMessageLog.INFO)
        return (1, self.messenger.getSuccessFeedbackMessage())

    def dropDatabase(self,db):
        '''
        Drops the created database case a problem occurs during database creation
        db: QSqlDatabase to be dropped
        '''
        host = db.hostName()
        port = db.port()
        user = db.userName()
        password = db.password()
        database = 'postgres'
        pgDB = QSqlDatabase('QPSQL')
        pgDB.setHostName(host)
        pgDB.setPort(port)
        pgDB.setUserName(user)
        pgDB.setPassword(password)
        pgDB.setDatabaseName(database)
        if not pgDB.open():
            return False
        sql = self.gen.dropDatabase(db.databaseName())
        query = QSqlQuery(pgDB)
        return query.exec_(sql)