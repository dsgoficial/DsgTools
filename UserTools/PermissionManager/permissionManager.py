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
    '''
    This class manages the permissions on dsgtools databases.
    '''
    def __init__(self, serverAbstractDb, parentWidget = None):
        super(PermissionManager,self).__init__()
        self.parentWidget = parentWidget
        self.serverAbstractDb = serverAbstractDb
        self.adminDb = self.instantiateAdminDb(serverAbstractDb)
    
    def instantiateAdminDb(self, serverAbstractDb):
        '''
        Instantiates dsgtools_admindb in the same server as serverAbstractDb. 
        If dsgtools_admindb does not exists, instantiateAdminDb calls createAdminDb
        '''
        (host, port, user, password) = serverAbstractDb.getParamsFromConectedDb()
        adminDb = DbFactory().createDbFactory('QPSQL')
        if not serverAbstractDb.hasAdminDb():
            return self.createAdminDb(serverAbstractDb, adminDb, host, port, user, password)
        return adminDb.connectDatabaseWithParameters(host, port, 'dsgtools_admindb', user, password)
    
    def createAdminDb(self, serverAbstractDb, adminDb, host, port, user, password):
        '''
        Creates dsgtools_admindb
        '''
        serverAbstractDb.createAdminDb()
        adminDb.connectDatabaseWithParameters(host, port, 'dsgtools_admindb', user, password)
        sqlPath = adminDb.getCreationSqlPath('admin')
        adminDb.runSqlFromFile(sqlPath)
        return adminDb

    def syncPermissionsWithAdminDb(self):
        '''
        Sync permissions with dsgtools_admindb.
        1- Gets roles from pg_roles
        2-  
        '''
        pass
    
    def getProfileByName(self, name):
        '''
        Get profile from table public.
        '''
        pass
    
    def updatePermission(self, roleName, newDefinition):
        '''
        Updates permission on all databases from server upon changes on permission definition. 
        '''
        pass
    
    def createPermissionProfile(self, permissionName, edgvVersion, jsonDict):
        '''
        Creates profile on dsgtools_admindb. 
        '''
        self.adminDb.insertIntoPermissionProfile(permissionName, edgvVersion, jsonDict)
    
    def updatePermissionProfile(self, permissionName, edgvVersion, newJsonDict):
        '''
        1. Updates public.permission_profile on dsgtools_admindb with the newJsonDict;
        2. Gets all roles from all databases that have the same permissionName;
        3. For each role, parse this role to detect the differences between oldJson and newJson;
        4. For each difference, grant or revoke the change;
        '''
        pass
    
    def deletePermission(self, permissionName, edgvVersion):
        '''
        1. Delete permission profile from public.permission_profile on dsgtools_admindb;
        2. Get roles with the same definition of permissionName and delete them.
        '''
        pass
    
    def importProfile(self, profileName, inputJsonFilePath):
        '''
        1. Reads inputJsonFilePath and parses it into a python dict;
        2. Validates inputPermissionDict;
        3. Checks if profile with profileName already exists;
        4. If it does not exist, import it into database;
        '''
        pass
    
    def batchImportProfiles(self, profilesDir):
        '''
        1. Get all profiles in profilesDir;
        2. Import each using importProfile
        '''
        pass

    def exportProfile(self, profileName, edgvversion, outputPath):
        '''
        1. Get profile from public.permission_profile;
        2. Export it to outputPath.
        '''
        pass
    
    def batchExportProfiles(self, outputDir):
        '''
        1. Get all profiles in public.permission_profile;
        2. Export each using exportProfile.
        '''
        pass