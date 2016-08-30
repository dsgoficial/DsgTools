# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-10-21
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba@dsg.eb.mil.br
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

#PyQt4 Imports

from PyQt4.QtCore import QSettings, SIGNAL, pyqtSignal, QObject

#DsgTools imports
from DsgTools.Factories.DbFactory.dbFactory import DbFactory



class DbCreator(QObject):
    def __init__(self, version):
        super(self.__class__,self).__init__()
        self.version = version
        self.dbFactory = DbFactory()
        self.log = ''
        self.scaleMIDict = {1:'100k',2:'50k',3:'25k',4:'10k',5:'5k',6:'2k',7:'1k'}
    
    def getType(self):
        #Abstract method.
        return None
    
    def buildDatabaseName(self, dbBaseName, prefix = None, sufix = None):
        attrNameList = []
        if prefix:
            attrNameList.append(prefix)
        attrNameList.append(dbBaseName)
        if sufix:
            attrNameList.append(sufix)
        return '_'.join(attrNameList)
    
    def buildAutoIncrementingDbNameList(self, dbInitialBaseName, numberOfDatabases, prefix = None, sufix = None):
        dbNameList = []
        for i in range(numberOfDatabases):
            dbBaseName = dbInitialBaseName+str(i)
            dbNameList.append(self.buildDatabaseName(dbBaseName, prefix, sufix))
        return dbNameList
    
    def createDb(self, dbName, srid, paramDict  = dict()):
        #Abstract method.
        pass
    
    def batchCreateDb(self, dbNameList, srid, paramDict  = dict()):
        outputDbDict = dict()
        errorDict = dict()
        templateDb = None
        for dbName in dbNameList:
            try:
                if not templateDb: 
                    newDb = self.createDb(dbName, srid, paramDict)
                    templateDb = dbName
                else:
                    paramDict['templateDb'] = templateDb
                    newDb = self.createDb(dbName, srid, paramDict)
                outputDbDict[dbName] = newDb
            except Exception as e:
                if dbName not in errorDict.keys():
                    errorDict[dbName] = str(e.args[0])
                else:
                    errorDict[dbName] += '\n' + str(e.args[0])
        return outputDbDict, errorDict
    
    def createDbWithAutoIncrementingName(self, dbInitialBaseName, srid, numberOfDatabases, prefix = None, sufix = None, paramDict = dict()):
        dbNameList = self.buildAutoIncrementingDbNameList(dbInitialBaseName, numberOfDatabases, prefix, sufix)
        return self.batchCreateDb(dbNameList, srid, paramDict)
    
    def createDbFromMIList(self, miList, prefix = None, sufix = None, paramDict = dict(), createFrame = False):
        outputDbDict = dict()
        errorDict = dict()
        templateDb = None
        for mi in miList:
            dbName = self.buildDatabaseName(mi, prefix, sufix)
            try:
                if not templateDb: 
                    newDb = self.createDb(dbName, srid, paramDict)
                    templateDb = dbName
                else:
                    paramDict['templateDb'] = templateDb
                    newDb = self.createDb(dbName, srid, paramDict)
                if createFrame:
                    scale = self.scaleMIDict[len(mi.split('-'))]
                    newDb.createFrame('mi',scale,mi)
                outputDbDict[mi] = newDb
            except Exception as e:
                if dbName not in errorDict.keys():
                    errorDict[dbName] = str(e.args[0])
                else:
                    errorDict[dbName] += '\n' + str(e.args[0])
        return outputDbDict, errorDict