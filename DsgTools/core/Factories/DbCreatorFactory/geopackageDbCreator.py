# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-06-27
        git sha              : $Format:%H$
        copyright            : (C) 2019 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
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

from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.Factories.DbCreatorFactory.dbCreator import DbCreator
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget
from DsgTools.core.dsgEnums import DsgEnums

class GeopackageDbCreator(DbCreator):
    
    def __init__(self, createParam, parentWidget = None):
        super(GeopackageDbCreator,self).__init__(createParam)
        self.parentWidget = parentWidget
    
    def instantiateNewDb(self, dbPath):
        newDb = self.dbFactory.createDbFactory(DsgEnums.DriverGeopackage)
        newDb.connectDatabase(dbPath)
        return newDb
    
    def getTemplateLocation(self, version):
        if version == '2.1.3':
            return os.path.join(
                        os.path.dirname(__file__), '..', '..', '..', 'core',
                        'DbModels', 'Geopackage', '213', 'seed_edgv213.gpkg'
                    )
        elif version == '3.0':
            return os.path.join(
                        os.path.dirname(__file__), '..', '..', '..', 'core',
                        'DbModels', 'Geopackage', '3', 'seed_edgv3.gpkg'
                    )
        return ''
    
    def createDb(self, dbName, srid, paramDict = dict(), parentWidget = None):
        destination = os.path.join(self.outputDir,dbName+'.gpkg')
        if 'version' not in list(paramDict.keys()):
            raise Exception('Undefined database version')
        edgvPath = self.getTemplateLocation(paramDict['version'])
        f = open(edgvPath,'rb')
        g = open(destination,'wb')
        x = f.readlines()
        if parentWidget:
            progress = ProgressWidget(
                            1, len(x)+2,
                            self.tr('Creating Geopackage {0}... ').format(dbName),
                            parent=parentWidget
                        )
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
        cursor.execute("UPDATE gpkg_geometry_columns SET srs_id={srid}".format(srid=srid))
        con.commit()
        cursor.close()
        con.close()
