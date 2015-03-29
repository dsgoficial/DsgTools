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

from genericThread import GenericThread

class PostgisDbThread(GenericThread):
    def __init__(self, db, version, epsg, stopped):
        """Constructor.
        """
        super(PostgisDbThread, self).__init__()

        self.db = db
        self.version = version
        self.epsg = epsg
        self.stopped = stopped

        self.factory = SqlGeneratorFactory()
        #setting the sql generator
        self.gen = self.factory.createSqlGenerator(False)

    def run(self):
        # Processing ending
        (ret, msg) = self.createDatabaseStructure()
        self.processingFinished.emit(ret, msg)

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
        self.rangeCalculated.emit(len(commands))

        self.db.transaction()
        query = QSqlQuery(self.db)

        update = True
        for command in commands:
            if not self.stopped[0]:
                if not query.exec_(command):
                    QgsMessageLog.logMessage(self.tr("Problem on database structure creation: ")+'SQL: '+command+'\n'+query.lastError().text()+'\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                    self.db.rollback()
                    self.db.close()
                    return (0,self.tr('Problem creating the database structure!\n Check the Log terminal for details.'))

                # Updating progress
                self.stepProcessed.emit()
            else:
                self.db.rollback()
                self.db.close()
                QgsMessageLog.logMessage(self.tr("User canceled datatabase structure creation"), "DSG Tools Plugin", QgsMessageLog.INFO)
                return (-1,self.tr('User canceled the database structure creation!'))

        self.db.commit()
        sql = self.gen.allowConnections(self.db.connectionName())
        query = QSqlQuery(sql,self.db)
        self.db.commit()
        self.db.close()
        QgsMessageLog.logMessage(self.tr("Successful datatabase structure creation"), "DSG Tools Plugin", QgsMessageLog.INFO)
        return (1,self.tr("Successful datatabase structure creation"))
