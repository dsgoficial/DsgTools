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

from DsgTools.Factories.DbCreatorFactory.dbCreator import DbCreator
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

class PostgisDbCreator(DbCreator):
    
    def __init__(self, createParam, version, parentWidget = None):
        super(self.__class__,self).__init__(createParam, version)
        self.parentWidget = parentWidget
    
    def instantiateNewDb(self, dbName):
        host = self.abstractDb.db.hostName()
        port = self.abstractDb.db.port()
        user = self.abstractDb.db.userName()
        password = self.abstractDb.db.password()
        newDb = self.dbFactory.createDbFactory('QPSQL')
        newDb.connectDatabaseWithParameters(host, port, dbName, user, password)
        return newDb
    
    def checkAndCreateTemplate(self):
        '''
        checks and create an edgv template
        '''
        hasTemplate = self.abstractDb.checkTemplate(self.version)
        if not hasTemplate:
            self.abstractDb.createTemplateDatabase(self.version)
            templateName = self.abstractDb.getTemplateName(self.version)
            templateDb = self.instantiateNewDb(templateName)
            templateDb.setStructureFromSql(self.version, 4674)
    
    def createDb(self, dbName, srid, paramDict = dict()):
        '''
        dbName: new database name
        srid: coordinate system of database
        paramDict = {'templateDb': database to be used as template. Default is edgv}
        '''
        #0. if 'templateDb' in paramDict.keys: use createFromTemplate then end createDb
        if 'templateDb' in paramDict.keys():
            self.abstractDb.createDbFromTemplate(dbName, self.version, templateName = paramDict['templateDb'])
            return self.instantiateNewDb(dbName)
        else:
            #1. test if edgv template is created
            #2. if edgv template is not created, create it
            self.checkAndCreateTemplate()
            #3. create db from template
            self.abstractDb.createDbFromTemplate(dbName, self.version)
            newDb = self.instantiateNewDb(dbName)
            newDb.updateDbSRID(srid)
            return newDb
