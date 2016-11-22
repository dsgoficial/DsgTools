# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-11-22
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
from DsgTools.Factories.DbFactory.dbFactory import DbFactory 
from osgeo import ogr
from uuid import uuid4
import codecs, os, json, binascii
import psycopg2
from DsgTools.CustomWidgets.progressWidget import ProgressWidget
from PyQt4.Qt import QObject

class PermissionManager(QObject):
    def __init__(self, serverAbstractDb, parentWidget = None):
        super(PermissionManager,self).__init__()
        self.parentWidget = parentWidget
        self.instantiateAdminDb(serverAbstractDb)
    
    def instantiateAdminDb(self, serverAbstractDb):
        '''
        Instantiates dsgtools_admindb in the same server as serverAbstractDb. 
        If dsgtools_admindb does not exists, instantiateAdminDb calls createAdminDb
        '''
        pass
    
    def createAdminDb(self, serverAbstractDb):
        '''
        Creates dsgtools_admindb
        '''
        serverAbstractDb.createAdminDb()
        (host, port, user, password) = serverAbstractDb.getParamsFromConectedDb()
        
        adminDb = DbFactory().createDbFactory('QPSQL')
        adminDb.connectDatabaseWithParameters(host, port, 'dsgtools_admindb', user, password)
        sqlPath = adminDb.getCreationSqlPath('admin')
        adminDb.runSqlFromFile(sqlPath)
        
        
                
        