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
from PyQt4.QtSql import QSqlDatabase,QSqlQuery

from qgis.core import QgsMessageLog

import sys, os, codecs

from DsgTools.Factories.ThreadFactory.genericThread import GenericThread

from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory

class PostgisDbMessages(QObject):
    def __init__(self, thread):
        super(PostgisDbMessages, self).__init__()

        self.thread = thread

    def getProblemMessage(self):
        return self.tr("Problem on database structure creation: ")+'SQL: '+command+'\n'+query.lastError().text()+'\n'

    def getProblemFeedbackMessage(self):
        self.tr('Problem creating the database structure!\n Check the Log terminal for details.')

    def getUserCanceledFeedbackMessage(self):
        return self.tr('User canceled the database structure creation!')

    def getSuccessFeedbackMessage(self):
        return self.tr("Successful datatabase structure creation")

    @pyqtSlot()
    def progressCanceled(self):
        self.thread.stopped[0] = True

class PostgisDbThread(GenericThread):
    def __init__(self):
        """Constructor.
        """
        super(PostgisDbThread, self).__init__()

        self.factory = SqlGeneratorFactory()
        #setting the sql generator
        self.gen = self.factory.createSqlGenerator(False)

        self.messenger = PostgisDbMessages(self)

    def setParameters(self, db, version, epsg, stopped):
        self.db = db
        self.version = version
        self.epsg = epsg
        self.stopped = stopped

    def run(self):
        # Processing ending
        (ret, msg) = self.createDatabaseStructure()
        self.signals.processingFinished.emit(ret, msg, self.getId())

    def createDatabaseStructure(self):
        currentPath = os.path.dirname(__file__)
        currentPath = os.path.join(currentPath, '..', '..', 'DbTools', 'PostGISTool')
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
        self.signals.rangeCalculated.emit(len(commands), self.getId())

        self.db.transaction()
        query = QSqlQuery(self.db)

        update = True
        for command in commands:
            if not self.stopped[0]:
                if not query.exec_(command):
                    QgsMessageLog.logMessage(self.messenger.getProblemMessage(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                    self.db.rollback()
                    self.db.close()
                    return (0, self.messenger.getProblemFeedbackMessage())

                # Updating progress
                self.signals.stepProcessed.emit(self.getId())
            else:
                self.db.rollback()
                self.db.close()
                QgsMessageLog.logMessage(self.messenger.getUserCanceledFeedbackMessage(), "DSG Tools Plugin", QgsMessageLog.INFO)
                return (-1, self.messenger.getUserCanceledFeedbackMessage())

        self.db.commit()
        sql = self.gen.allowConnections(self.db.connectionName())
        query = QSqlQuery(sql,self.db)
        self.db.commit()
        self.db.close()
        QgsMessageLog.logMessage(self.messenger.getSuccessFeedbackMessage(), "DSG Tools Plugin", QgsMessageLog.INFO)
        return (1, self.messenger.getSuccessFeedbackMessage())
