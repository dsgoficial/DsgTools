# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-30
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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

from .dbCreator import DbCreator
from DsgTools.core.dsgEnums import DsgEnums


class PostgisDbCreator(DbCreator):
    def __init__(self, createParam, parentWidget=None):
        super(self.__class__, self).__init__(createParam)
        self.parentWidget = parentWidget

    def instantiateNewDb(self, dbName):
        host = self.abstractDb.db.hostName()
        port = self.abstractDb.db.port()
        user = self.abstractDb.db.userName()
        password = self.abstractDb.db.password()
        newDb = self.dbFactory.createDbFactory(DsgEnums.DriverPostGIS)
        newDb.connectDatabaseWithParameters(host, port, dbName, user, password)
        return newDb

    def createEdgvDb(self, dbName, srid, version):
        """
        Creates an EDGV database straight from the creation sql shipped with
        the plugin, already at the requested srid.

        No template database is kept on the server: a template outlives the
        plugin version that built it, and a server holding an old one kept
        handing out the old model (issue #857).
        """
        self.abstractDb.createDatabase(dbName)
        newDb = self.instantiateNewDb(dbName)
        try:
            newDb.setStructureFromSql(version, int(srid))
        except Exception:
            # the structure is rolled back: do not leave an empty database
            # behind. Dropped as its owner, since dropDatabase() demands a
            # superuser and the creation may have failed for the lack of one.
            newDb.closeDatabase()
            try:
                self.abstractDb._execute_autocommit(
                    self.abstractDb.gen.dropDatabase(dbName)
                )
            except Exception:
                pass
            raise
        return newDb

    def createDb(self, dbName, srid, paramDict=dict(), parentWidget=None):
        """
        dbName: new database name
        srid: coordinate system of database
        paramDict = {
            'templateDb': existing database to be copied (batch creation),
            'isTemplateEdgv': True to create an EDGV database from its sql,
            'version': EDGV version, when isTemplateEdgv,
            'templateName': existing database to be copied, when not isTemplateEdgv
        }
        """
        # 0. if 'templateDb' in paramDict.keys: use createFromTemplate then end createDb
        if "templateDb" in list(paramDict.keys()):
            self.abstractDb.createDbFromTemplate(
                dbName, templateName=paramDict["templateDb"], parentWidget=parentWidget
            )
            return self.instantiateNewDb(dbName)
        if paramDict["isTemplateEdgv"]:
            return self.createEdgvDb(dbName, srid, paramDict["version"])
        # copy of an existing database chosen by the user
        self.abstractDb.createDbFromTemplate(
            dbName,
            templateName=paramDict["templateName"],
            parentWidget=parentWidget,
        )
        newDb = self.instantiateNewDb(dbName)
        newDb.updateDbSRID(srid, parentWidget=parentWidget)
        newDb.checkAndCreateStyleTable()
        return newDb
