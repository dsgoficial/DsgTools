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
#General imports
from osgeo import ogr
from uuid import uuid4
import codecs, os, json, binascii

#DSG Tools imports
from DsgTools.Factories.DbFactory.dbFactory import DbFactory 
from DsgTools.CustomWidgets.progressWidget import ProgressWidget
from DsgTools.Utils.utils import Utils

#PyQt4 imports
from PyQt4.Qt import QObject

class PermissionManager(QObject):
    '''
    This class manages the permissions on dsgtools databases.
    '''
    def __init__(self, serverAbstractDb, dbDict, parentWidget = None):
        super(PermissionManager,self).__init__()
        self.parentWidget = parentWidget
        self.dbDict = dbDict
        self.serverAbstractDb = serverAbstractDb
        self.adminDb = self.instantiateAdminDb(serverAbstractDb)
        self.getRolesInformation()
        self.utils = Utils()
    
    def getRolesInformation(self):
        self.dbRolesDict = self.adminDb.getRolesDict()
        self.rolesDict = dict()
        for db in self.dbRolesDict.keys():
            for role in self.dbRolesDict[db]:
                profileName = role.split('_')[0:-5]
                if profileName not in self.rolesDict.keys():
                    self.rolesDict[profileName] = dict()
                if db not in self.rolesDict[profileName].keys():
                    self.rolesDict[profileName][db] = []
                self.rolesDict[profileName][db].append(role)
    
    def instantiateAdminDb(self, serverAbstractDb):
        '''
        Instantiates dsgtools_admindb in the same server as serverAbstractDb. 
        If dsgtools_admindb does not exists, instantiateAdminDb calls createAdminDb
        '''
        (host, port, user, password) = serverAbstractDb.getParamsFromConectedDb()
        adminDb = DbFactory().createDbFactory('QPSQL')
        if not serverAbstractDb.hasAdminDb():
            return self.createAdminDb(serverAbstractDb, adminDb, host, port, user, password)
        adminDb.connectDatabaseWithParameters(host, port, 'dsgtools_admindb', user, password)
        return adminDb
    
    def createAdminDb(self, serverAbstractDb, adminDb, host, port, user, password):
        '''
        Creates dsgtools_admindb
        '''
        serverAbstractDb.createAdminDb()
        adminDb.connectDatabaseWithParameters(host, port, 'dsgtools_admindb', user, password)
        sqlPath = adminDb.getCreationSqlPath('admin')
        adminDb.runSqlFromFile(sqlPath)
        return adminDb
    
    def getProfile(self, name, edgvVersion):
        '''
        Get profile from table public.
        '''
        profileDict = json.loads(self.adminDb.getRoleFromAdminDb(name, edgvVersion))
        if not profileDict:
            raise Exception(self.tr("Profile not found on dsgtools_admindb!"))
        return profileDict
    
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
    
    def grantPermission(self, dbName, permissionName, edgvVersion, userName):
        '''
        Grants permission on a db to a user using a profile.
        1. Gets profile from public.permission_profile;
        2. Checks if profile exists on db, if it does not, installs it;
        3. Grants profile to user on db.
        '''
        profileDict = self.getProfile(permissionName, edgvVersion)
        if not self.permissionIsInstalled(self.dbDict[dbName], dbName, permissionName):
            self.dbDict[dbName].createRole(permissionName, profileDict) #creates profile in db
            self.getRolesInformation() #done to refresh dicts due to new permission
        for role in self.rolesDict[permissionName][dbName]:
            self.dbDict[dbName].grantRole(userName, role)
    
    def permissionIsInstalled(self, abstractDb, dbName, permissionName):
        '''
        Checks if permission is already installed;
        Returns True if it is installed and False otherwise.
        '''
        if permissionName not in self.rolesDict.keys():
            return False
        if dbName not in self.rolesDict[permissionName].keys():
            return False
        return True

    
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
        1. Get roles with the same definition of permissionName and delete them.
        2. Delete permission profile from public.permission_profile on dsgtools_admindb;
        '''
        #first step, delete roles with the same definition of selected profile
        #
        pass
    
    def importProfile(self, fullFilePath):
        '''
        Function to import profile into dsgtools_admindb. It has the following steps:
        1. Reads inputJsonFilePath and parses it into a python dict;
        2. Validates inputPermissionDict;
        3. Tries to insert into database, if there is an error, abstractDb raises an error which is also raised by importProfile
        '''
        #getting profile name
        profileName = os.path.basename(fullFilePath).split('.')[0]
        #getting json
        inputJsonDict, inputJson = self.utils.readJsonFile(fullFilePath, returnFileAndDict = True)
        #error handling and json validation
        if inputJsonDict == dict():
            raise Exception(self.tr("Not valid DsgTools permission file!"))
        if not self.validateJsonProfile(inputJsonDict):
            raise Exception(self.tr("Not valid DsgTools permission file!"))
        edgvVersion = inputJsonDict.keys()[0].split('_')[-1]
        try:
            self.createPermissionProfile(profileName, edgvVersion, inputJson)
        except Exception as e:
            raise Exception(self.tr("Error importing profile {0}!\n").format(profileName)+str(e))
    
    def batchImportProfiles(self, profilesDir):
        '''
        1. Get all profiles in profilesDir;
        2. Import each using importProfile;
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
    
    def validateJsonProfile(self, inputJsonDict):
        '''
        1. Validates each key and value in inputJsonDict;
        2. If input is ok, returns True;
        3. If one piece of json is not valid, returns False.
        This validator does not validate the name of classes or names of categories. It only checks the format of dsgtools json profile.
        '''
        for key1 in inputJsonDict.keys():
            if not isinstance(inputJsonDict[key1], dict):
                return False
            if key1 not in ['database_2.1.3', 'database_FTer_2a_Ed']:
                return False
            for key2 in inputJsonDict[key1].keys():
                if not isinstance(inputJsonDict[key1][key2],dict):
                    return False
                for key3 in inputJsonDict[key1][key2].keys():
                    if not isinstance(inputJsonDict[key1][key2][key3],dict):
                        return False
                    for key4 in inputJsonDict[key1][key2][key3].keys():
                        if not isinstance(inputJsonDict[key1][key2][key3][key4],dict):
                            return False
                        for key5 in inputJsonDict[key1][key2][key3][key4].keys():
                            if key5 not in ["read", "write"]:
                                return False
                            if inputJsonDict[key1][key2][key3][key4][key5] not in ["0","1","2"]:
                                return False
        return True
