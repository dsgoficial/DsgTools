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
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory 
from DsgTools.core.ServerManagementTools.genericDbManager import GenericDbManager
from DsgTools.core.Utils.utils import Utils

#qgis.PyQt imports
from qgis.PyQt.Qt import QObject

class PermissionManager(GenericDbManager):
    '''
    This class manages the permissions on dsgtools databases.
    '''
    def __init__(self, serverAbstractDb, dbDict, edgvVersion, parentWidget = None):
        super(self.__class__,self).__init__(serverAbstractDb, dbDict, edgvVersion, parentWidget = None)
    
    def getRolesInformation(self):
        '''
        Builds two dicts:
        dbRolesDict = { 'dbname':[-list of roles-] }
        rolesDict = { 'profileName': { 'dbname' : [-list of roles with uuid on it-] } }
        '''
        dbRolesDict = self.adminDb.getRolesDict()
        rolesDict = dict()
        for db in list(dbRolesDict.keys()):
            for role in dbRolesDict[db]:
                profileName = '_'.join(role.split('_')[0:-5])
                if profileName not in list(rolesDict.keys()):
                    rolesDict[profileName] = dict()
                if db not in list(rolesDict[profileName].keys()):
                    rolesDict[profileName][db] = []
                rolesDict[profileName][db].append(role)
        return dbRolesDict, rolesDict
    
    def getDatabasePerspectiveDict(self):
        '''
        Gets a dict in the format: {dbName: {roleName :[-list of users-]}}
        The dbs are from dbDict 
        '''
        (dbRolesDict, rolesDict) = self.getRolesInformation()
        profiles = self.getSettings()
        grantedRoleDict = self.adminDb.getGrantedRolesDict()
        dbPerspectiveDict = dict()
        for dbName in self.dbDict:
            if dbName not in list(dbPerspectiveDict.keys()):
                dbPerspectiveDict[dbName] = dict()
            edgvVersion = self.dbDict[dbName].getDatabaseVersion()
            if edgvVersion in list(profiles.keys()):
                for profile in profiles[edgvVersion]:
                    if profile not in list(dbPerspectiveDict[dbName].keys()):
                        dbPerspectiveDict[dbName][profile] = []
                    if profile in list(rolesDict.keys()):
                        if dbName in list(rolesDict[profile].keys()):
                            for role in rolesDict[profile][dbName]:
                                if role in list(grantedRoleDict.keys()):
                                    for user in grantedRoleDict[role]:
                                        if user not in dbPerspectiveDict[dbName][profile]:
                                            dbPerspectiveDict[dbName][profile].append(user)
        return dbPerspectiveDict
    
    def getUserPerspectiveDict(self):
        '''
        Gets a dict in the format: {userName: {dbName : ['-list of roles']}
        '''
        dbPerspectiveDict = self.getDatabasePerspectiveDict()
        userPerspectiveDict = dict()
        userList = [i[0] for i in self.adminDb.getUsersFromServer()]
        for user in userList:
            userPerspectiveDict[user] = dict()
        
        for dbName in list(dbPerspectiveDict.keys()):
            for profile in dbPerspectiveDict[dbName]:
                for user in dbPerspectiveDict[dbName][profile]:
                    if dbName not in list(userPerspectiveDict[user].keys()):
                        userPerspectiveDict[user][dbName] = []
                    if profile not in userPerspectiveDict[user][dbName]:
                        userPerspectiveDict[user][dbName].append(profile)
        return userPerspectiveDict
    
    def grantPermission(self, dbName, permissionName, edgvVersion, userName):
        '''
        Grants permission on a db to a user using a profile.
        1. Gets profile from public.permission_profile;
        2. Checks if profile exists on db, if it does not, installs it;
        3. Grants profile to user on db.
        '''
        profileDict = self.getSetting(permissionName, edgvVersion)
        self.grantPermissionWithProfileDict(dbName, permissionName, userName, profileDict)
    
    def grantPermissionWithProfileDict(self, dbName, permissionName, userName, profileDict, updatePermission = False):
        '''
        Grants permission on a db using profileDict
        '''
        if updatePermission:
            role = self.dbDict[dbName].createRole(permissionName, profileDict, permissionManager = True)
            self.dbDict[dbName].grantRole(userName, role)
        else:
            if not self.isPermissionInstalled(self.dbDict[dbName], dbName, permissionName):
                self.dbDict[dbName].createRole(permissionName, profileDict) #creates profile in db
            (dbRolesDict, rolesDict) = self.getRolesInformation() #done to refresh dicts due to new permission 
            for role in rolesDict[permissionName][dbName]:
                self.dbDict[dbName].grantRole(userName, role)
    
    def revokePermission(self, dbName, permissionName, userName):
        '''
        Revokes permission on a db from permissionName.
        '''
        (dbRolesDict, rolesDict) = self.getRolesInformation()
        for realRoleName in rolesDict[permissionName][dbName]:
            try:
                self.dbDict[dbName].revokeRole(userName, realRoleName)
            except Exception as e:
                raise Exception(self.tr('Problem revoking role ') + permissionName + self.tr(' on database ') + dbName +':\n' + ':'.join(e.args))
    
    def isPermissionInstalled(self, abstractDb, dbName, permissionName):
        '''
        Checks if permission is already installed;
        Returns True if it is installed and False otherwise.
        '''
        (dbRolesDict, rolesDict) = self.getRolesInformation()
        if permissionName not in list(rolesDict.keys()):
            return False
        if dbName not in list(rolesDict[permissionName].keys()):
            return False
        return True
    
    def updateSetting(self, settingName, edgvVersion, newProfileDict):
        '''
        1. Gets all roles from all databases that have the same settingName;
        2. For each role, get users that are granted to them;
        3. Drop role, create a new one and grant it to previous users;
        4. Updates public.permission_profile on dsgtools_admindb with the newJsonDict.
        '''
        abstractDbsToRollBack = []
        try:
            abstractDbsToRollBack.append(self.adminDb)
            self.adminDb.db.transaction() #done to rollback in case of trouble
            (dbRolesDict, rolesDict) = self.getRolesInformation()
            grantedRoleDict = self.adminDb.getGrantedRolesDict()
            if settingName in list(rolesDict.keys()):
                for dbName in list(rolesDict[settingName].keys()):
                    for roleName in rolesDict[settingName][dbName]:
                        if dbName not in list(self.dbDict.keys()):
                            abstractDb = self.instantiateAbstractDb(dbName)
                        else:
                            abstractDb = self.dbDict[dbName]
                        #prepairs to rollback in case of exception
                        abstractDbsToRollBack.append(abstractDb)
                        abstractDb.db.transaction()
                        usersToBeGranted = []
                        if roleName in list(grantedRoleDict.keys()):
                            usersToBeGranted = grantedRoleDict[roleName]
                        abstractDb.dropRoleOnDatabase(roleName)
                        for userName in usersToBeGranted:
                            self.grantPermissionWithProfileDict(dbName, settingName, userName, newProfileDict, updatePermission = True)
            newjsonprofile = json.dumps(newProfileDict, sort_keys=True, indent=4)
            self.adminDb.updatePermissionProfile(settingName, edgvVersion, newjsonprofile)
            for abstractDb in abstractDbsToRollBack:
                abstractDb.db.commit()
        except Exception as e:
            for abstractDb in abstractDbsToRollBack:
                abstractDb.db.rollback()
            raise Exception(self.tr('Unable to update profile ') + settingName +': ' +':'.join(e.args))
    
    def deleteSetting(self, settingName, edgvVersion):
        '''
        1. Get roles with the same definition of permissionName and delete them.
        2. Delete permission profile from public.permission_profile on dsgtools_admindb;
        '''
        #first step, delete roles with the same definition of selected profile
        abstractDbsToRollBack = []
        try:
            abstractDbsToRollBack.append(self.adminDb)
            self.adminDb.db.transaction() #done to rollback in case of trouble
            (dbRolesDict, rolesDict) = self.getRolesInformation()
            if settingName in list(rolesDict.keys()):
                for dbName in list(rolesDict[settingName].keys()):
                    for roleName in rolesDict[settingName][dbName]:
                        if dbName not in list(self.dbDict.keys()):
                            abstractDb = self.instantiateAbstractDb(dbName)
                        else:
                            abstractDb = self.dbDict[dbName]
                        #prepairs to rollback in case of exception
                        abstractDbsToRollBack.append(abstractDb)
                        abstractDb.db.transaction()
                        abstractDb.dropRoleOnDatabase(roleName)
            #after deletion, delete permission profile from public.permission_profile
            self.adminDb.removeRecordFromPropertyTable('Permission',settingName, edgvVersion)
            for abstractDb in abstractDbsToRollBack:
                abstractDb.db.commit()
        except Exception as e:
            for abstractDb in abstractDbsToRollBack:
                abstractDb.db.rollback()
            raise Exception(self.tr('Problem deleting permission: ')+':'.join(e.args))
    
    def validateJsonProfile(self, inputJsonDict):
        '''
        1. Validates each key and value in inputJsonDict;
        2. If input is ok, returns True;
        3. If one piece of json is not valid, returns False.
        This validator does not validate the name of classes or names of categories. It only checks the format of dsgtools json profile.
        '''
        for key1 in list(inputJsonDict.keys()):
            if not isinstance(inputJsonDict[key1], dict):
                return False
            if key1 not in ['database_2.1.3', 'database_2.1.3_pro', 'database_3.0', 'database_FTer_2a_Ed','database_Non_EDGV']:
                return False
            for key2 in list(inputJsonDict[key1].keys()):
                if not isinstance(inputJsonDict[key1][key2],dict):
                    return False
                for key3 in list(inputJsonDict[key1][key2].keys()):
                    if not isinstance(inputJsonDict[key1][key2][key3],dict):
                        return False
                    for key4 in list(inputJsonDict[key1][key2][key3].keys()):
                        if not isinstance(inputJsonDict[key1][key2][key3][key4],dict):
                            return False
                        for key5 in list(inputJsonDict[key1][key2][key3][key4].keys()):
                            if key5 not in ["read", "write"]:
                                return False
                            if inputJsonDict[key1][key2][key3][key4][key5] not in ["0","1","2"]:
                                return False
        return True
