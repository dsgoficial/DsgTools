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
"""
# Import the PyQt and QGIS libraries
from qgis.PyQt.Qt import QObject
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtSql import QSqlQuery, QSqlDatabase

from qgis.core import QgsMessageLog

import os, codecs

from .genericThread import GenericThread
from ..SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from ..DbFactory.dbFactory import DbFactory
from DsgTools.core.dsgEnums import DsgEnums


class PostgisDbMessages(QObject):
    def __init__(self, thread):
        """
        PostGIS database creation messages constructor
        :param thread:
        """
        super(PostgisDbMessages, self).__init__()

        self.thread = thread

    def getProblemMessage(self, command, query):
        """
        Returns database structure creation error message
        """
        return (
            self.tr("Problem on database structure creation: ")
            + "SQL: "
            + command
            + "\n"
            + query.lastError().text()
            + "\n"
        )

    def getProblemFeedbackMessage(self):
        """
        Returns database creation error message
        """
        return self.tr(
            "Problem creating the database structure!\n Check the Log terminal for details."
        )

    def getUserCanceledFeedbackMessage(self):
        """
        Returns user canceled error message
        """
        return self.tr("User canceled the database structure creation!")

    def getSuccessFeedbackMessage(self):
        """
        Returns successful creation message
        """
        return self.tr("Successful datatabase structure creation")

    @pyqtSlot()
    def progressCanceled(self):
        self.thread.stopped[0] = True


class PostgisDbThread(GenericThread):
    def __init__(self, parent=None):
        """
        Constructor.
        """
        super(PostgisDbThread, self).__init__()

        self.factory = SqlGeneratorFactory()
        # setting the sql generator
        self.gen = self.factory.createSqlGenerator(driver=DsgEnums.DriverPostGIS)
        self.messenger = PostgisDbMessages(self)
        self.dbFactory = DbFactory()
        self.parent = parent

    def setParameters(self, abstractDb, dbName, version, epsg, stopped):
        """
        Sets thread parameters
        """
        self.abstractDb = abstractDb  # database = postgis
        self.dbName = dbName
        self.db = None
        self.version = version
        self.epsg = epsg
        self.stopped = stopped

    def run(self):
        """
        Runs the process
        """
        # Processing ending
        (ret, msg) = self.createDatabaseStructure()
        self.signals.processingFinished.emit(ret, msg, self.getId())

    def connectToTemplate(self, setInnerDb=True):
        """
        Connects to the template database to speed up database creation
        :return:
        """
        database = self.abstractDb.getTemplateName(self.version)
        host = self.abstractDb.db.hostName()
        port = self.abstractDb.db.port()
        user = self.abstractDb.db.userName()
        password = self.abstractDb.db.password()
        template = self.dbFactory.createDbFactory(DsgEnums.DriverPostGIS)
        template.connectDatabaseWithParameters(host, port, database, user, password)
        template.checkAndOpenDb()
        if setInnerDb:
            self.db = template.db
        return template

    def createDatabaseStructure(self):
        """
        Creates database structure according to the selected edgv version
        """
        currentPath = os.path.dirname(__file__)
        currentPath = os.path.join(currentPath, "..", "..", "DbTools", "PostGISTool")
        if self.version == "2.1.3":
            edgvPath = os.path.join(currentPath, "sqls", "213", "edgv213.sql")
        elif self.version == "2.1.3 Pro":
            edgvPath = os.path.join(currentPath, "sqls", "213_Pro", "edgv213_pro.sql")
        elif self.version == "3.0":
            edgvPath = os.path.join(currentPath, "sqls", "3", "edgv3.sql")
        else:
            edgvPath = ""
        return self.loadDatabaseStructure(edgvPath)

    def loadDatabaseStructure(self, edgvPath):
        """
        Loads the database structure
        edgvPath: path to the databse sql
        """
        commands = []
        hasTemplate = self.abstractDb.checkTemplate(self.version)
        if hasTemplate:
            templateDb = self.connectToTemplate(setInnerDb=False)
            mustUpdateTemplate = templateDb.checkTemplateImplementationVersion()
            if mustUpdateTemplate:
                templateName = templateDb.db.databaseName()
                templateDb.__del__()
                self.abstractDb.dropDatabase(templateName, dropTemplate=True)
                hasTemplate = False
        if not hasTemplate:
            file = codecs.open(edgvPath, encoding="utf-8", mode="r")
            sql = file.read()
            sql = sql.replace("[epsg]", "4674")
            file.close()
            commands = [i for i in sql.split("#") if i != ""]
        # Progress bar steps calculated
        self.signals.rangeCalculated.emit(len(commands) + 4, self.getId())

        if not hasTemplate:
            try:
                self.abstractDb.createTemplateDatabase(self.version)
                self.signals.stepProcessed.emit(self.getId())
                self.connectToTemplate()
                self.signals.stepProcessed.emit(self.getId())
            except Exception as e:
                return (
                    0,
                    self.messenger.getProblemFeedbackMessage()
                    + "\n"
                    + ":".join(e.args),
                )
            self.db.open()
            self.db.transaction()
            query = QSqlQuery(self.db)

            for command in commands:
                if not self.stopped[0]:
                    if not query.exec_(command):
                        QgsMessageLog.logMessage(
                            self.messenger.getProblemMessage(command, query),
                            "DSGTools Plugin",
                            Qgis.Critical,
                        )
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
                    QgsMessageLog.logMessage(
                        self.messenger.getUserCanceledFeedbackMessage(),
                        "DSGTools Plugin",
                        Qgis.Info,
                    )
                    return (-1, self.messenger.getUserCanceledFeedbackMessage())

            self.db.commit()
            if self.version == "2.1.3":
                sql = (
                    "ALTER DATABASE %s SET search_path = \"$user\", public, topology,'cb','complexos','dominios';"
                    % self.db.databaseName()
                )
            elif self.version == "2.1.3 Pro":
                sql = (
                    "ALTER DATABASE %s SET search_path = \"$user\", public, topology,'edgv','dominios';"
                    % self.db.databaseName()
                )
            elif self.version == "FTer_2a_Ed":
                sql = (
                    "ALTER DATABASE %s SET search_path = \"$user\", public, topology,'pe','ge','complexos','dominios';"
                    % self.db.databaseName()
                )
            elif self.version == "3.0":
                sql = (
                    "ALTER DATABASE %s SET search_path = \"$user\", public, topology,'edgv','complexos','dominios';"
                    % self.db.databaseName()
                )

            if sql:
                if not query.exec_(sql):
                    QgsMessageLog.logMessage(
                        self.messenger.getProblemMessage(command, query),
                        "DSGTools Plugin",
                        Qgis.Critical,
                    )
                    return (0, self.messenger.getProblemFeedbackMessage())
            # this commit was missing, so alter database statement was not commited.
            self.db.commit()
            self.db.close()
            self.abstractDb.setDbAsTemplate(self.version)
        # creates from template
        if not self.stopped[0]:
            templateName = self.abstractDb.getTemplateName(self.version)
            self.abstractDb.createDbFromTemplate(
                self.dbName, templateName, parentWidget=self.parent
            )
            self.signals.stepProcessed.emit(self.getId())
            # 5. alter spatial structure
            createdDb = self.dbFactory.createDbFactory(DsgEnums.DriverPostGIS)
            createdDb.connectDatabaseWithParameters(
                self.abstractDb.db.hostName(),
                self.abstractDb.db.port(),
                self.dbName,
                self.abstractDb.db.userName(),
                self.abstractDb.db.password(),
            )
            errorTuple = createdDb.updateDbSRID(
                self.epsg, parentWidget=self.parent, threading=True
            )
            # if an error occur during the thread we should pass the message to the main thread
            if errorTuple:
                QgsMessageLog.logMessage(
                    self.messenger.getProblemMessage(errorTuple[0], errorTuple[1]),
                    "DSGTools Plugin",
                    Qgis.Critical,
                )
                return (0, self.messenger.getProblemFeedbackMessage())
            self.signals.stepProcessed.emit(self.getId())
        else:
            QgsMessageLog.logMessage(
                self.messenger.getUserCanceledFeedbackMessage(),
                "DSGTools Plugin",
                Qgis.Info,
            )
            return (-1, self.messenger.getUserCanceledFeedbackMessage())
        QgsMessageLog.logMessage(
            self.messenger.getSuccessFeedbackMessage(), "DSGTools Plugin", Qgis.Info
        )
        return (1, self.messenger.getSuccessFeedbackMessage())

    def dropDatabase(self, db):
        """
        Drops the created database case a problem occurs during database creation
        db: QSqlDatabase to be dropped
        """
        host = db.hostName()
        port = db.port()
        user = db.userName()
        password = db.password()
        database = "postgres"
        pgDB = QSqlDatabase("QPSQL")
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
