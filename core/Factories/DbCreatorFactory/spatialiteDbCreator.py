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

import os, sqlite3
from os.path import expanduser

from ..DbFactory.dbFactory import DbFactory
from DsgTools.core.Factories.DbCreatorFactory.dbCreator import DbCreator
from ....gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget
from DsgTools.core.dsgEnums import DsgEnums

class SpatialiteDbCreator(DbCreator):
    
    def __init__(self, createParam, parentWidget = None):
        super(self.__class__,self).__init__(createParam)
        self.parentWidget = parentWidget
    
    def instantiateNewDb(self, dbPath):
        newDb = self.dbFactory.createDbFactory(DsgEnums.DriverSpatiaLite)
        newDb.connectDatabase(dbPath)
        return newDb
    
    def getTemplateLocation(self, version):
        currentPath = os.path.dirname(__file__)
        if version == '2.1.3':
            edgvPath = os.path.join(currentPath,'..','..','..','core','DbModels','SpatiaLite', '213', 'seed_edgv213.sqlite')
        elif version == '3.0':
            edgvPath = os.path.join(currentPath,'..','..','..','core','DbModels','SpatiaLite', '3', 'seed_edgv3.sqlite')
        return edgvPath
    
    def createDb(self, dbName, srid, paramDict = dict(), parentWidget = None):
        destination = os.path.join(self.outputDir,dbName+'.sqlite')
        if 'version' not in list(paramDict.keys()):
            raise Exception('Undefined database version')
        edgvPath = self.getTemplateLocation(paramDict['version'])
        f = open(edgvPath,'rb')
        g = open(destination,'wb')
        x = f.readlines()
        if parentWidget:
            progress = ProgressWidget(1,len(x)+2,self.tr('Creating Spatialite {0}... ').format(dbName), parent = parentWidget)
            progress.initBar()
        for i in x:
            g.write(i)
            if parentWidget:
                progress.step()
        g.close()
        f.close()
        #TODO: put defineSrid into AbstractDb
        self.defineSrid(destination, srid)
        if parentWidget:
            progress.step()
        newDb = self.instantiateNewDb(destination)
        if parentWidget:
            progress.step()
        return newDb
    
    def defineSrid(self, destination, srid):
        con = sqlite3.connect(destination)
        cursor = con.cursor()
        srid_sql = (srid,)
        cursor.execute("UPDATE geometry_columns SET srid=?",srid_sql)
        con.commit()
        con.close()