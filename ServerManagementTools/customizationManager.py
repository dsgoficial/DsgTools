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

class CustomizationManager(QObject):
    '''
    This class manages the customizations on dsgtools databases.
    '''
    def __init__(self, serverAbstractDb, parentWidget = None):
        super(CustomizationManager,self).__init__()
        self.parentWidget = parentWidget
        self.serverAbstractDb = serverAbstractDb
        self.adminDb = self.instantiateAdminDb(serverAbstractDb)
        self.utils = Utils()
    
    def instantiateAbstractDb(self, name):
        '''
        Instantiates an abstractDb.
        '''
        (host, port, user, password) = self.serverAbstractDb.getParamsFromConectedDb()
        abstractDb = DbFactory().createDbFactory('QPSQL')
        abstractDb.connectDatabaseWithParameters(host, port, name, user, password)
        return abstractDb
    
    def getCustomizations(self):
        '''
        Gets all customizations from public.customizations
        '''
        return self.adminDb.getAllCustomizationsFromAdminDb()
    
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
    
    def getCustomization(self, name, edgvVersion):
        '''
        Get profile from table public.customizations
        '''
        customDict = json.loads(self.adminDb.getCustomizationFromAdminDb(name, edgvVersion))
        if not customDict:
            raise Exception(self.tr("Customization not found on dsgtools_admindb!"))
        return customDict
    
    def createCustomization(self, customizationName, edgvVersion, jsonDict):
        '''
        Creates customization on dsgtools_admindb.
        '''
        self.adminDb.insertIntoCustomizations(customizationName, jsonDict, edgvVersion)
    
    def updateCustomization(self, customizationName, edgvVersion, newCustomizationDict):
        '''
        Updates customization on dsgtools_admindb.
        '''
        self.adminDb.updateCustomization(customizationName, edgvVersion, newCustomizationDict)
    
    def deleteCustomization(self, customizationName, edgvVersion):
        '''
        Delete customization from public.customizations on dsgtools_admindb;
        '''
        self.adminDb.deletePermissionProfile(customizationName, edgvVersion)
    
    def importCustomization(self, fullFilePath):
        '''
        Function to import profile into dsgtools_admindb. It has the following steps:
        '''
        #getting profile name
        profileName = os.path.basename(fullFilePath).split('.')[0]
        #getting json
        inputJsonDict, inputJson = self.utils.readJsonFile(fullFilePath, returnFileAndDict = True)
        #error handling and json validation
        if inputJsonDict == dict():
            raise Exception(self.tr("Not valid DsgTools customization file!"))
        if not self.validateJsonProfile(inputJsonDict):
            raise Exception(self.tr("Not valid DsgTools customization file!"))
        edgvVersion = inputJsonDict.keys()[0].split('_')[-1]
        try:
            self.createCustomization(profileName, edgvVersion, inputJson)
        except Exception as e:
            raise Exception(self.tr("Error importing profile {0}!\n").format(profileName)+e.args[0])
    
    def batchImportCustomization(self, customizationsDir):
        '''
        1. Get all profiles in profilesDir;
        2. Import each using importProfile;
        '''
        importList = []
        for customization in os.walk(customizationsDir).next()[2]:
            if '.json' in os.path.basename(customization):
                importList.append(os.path.join(customizationsDir,customization))
        for customizationFile in importList:
            self.importCustomization(customizationFile)

    def exportCustomization(self, profileName, edgvVersion, outputPath):
        '''
        1. Get profile from public.customizations;
        2. Export it to outputPath.
        '''
        jsonDict = self.getCustomization(profileName, edgvVersion)
        outputFile = os.path.join(outputPath,profileName+'.json')
        with open(outputFile, 'w') as outfile:
            json.dump(jsonDict, outfile, sort_keys=True, indent=4)
    
    def batchExportProfiles(self, outputDir):
        '''
        1. Get all profiles in public.permission_profile;
        2. Export each using exportProfile.
        '''
        customizationDict = self.getCustomizations()
        for edgvVersion in customizationDict.keys():
            outputPath = os.path.join(outputDir,edgvVersion)
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)
            for customizationName in customizationDict[edgvVersion]:
                self.exportCustomization(customizationName, edgvVersion, outputPath)
    
    def validateJsonProfile(self, inputJsonDict):
        '''
        1. Validates each key and value in inputJsonDict;
        2. If input is ok, returns True;
        3. If one piece of json is not valid, returns False.
        This validator does not validate the name of classes or names of categories. It only checks the format of dsgtools json profile.
        '''
        #TODO
        return True
