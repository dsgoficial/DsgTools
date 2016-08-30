# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-26
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import os, sqlite3
from os.path import expanduser

from DsgTools.Factories.DbCreatorFactory.DbCreator import DbCreator

class SpatialiteDbCreator(DbCreator):
    
    def __init__(self, createParam, version):
        super(self.__class__,self).__init__(version)
        if isinstance(createParam, str):
            self.outputDir = createParam
        self.edgvPath = self.getTemplateLocation(self.version)
    
    def getTemplateLocation(self, version):
        currentPath = os.path.dirname(__file__)
        if version == '2.1.3':
            edgvPath = os.path.join(currentPath,'template', '213', 'seed_edgv213.sqlite')
        elif version == 'FTer_2a_Ed':
            edgvPath = os.path.join(currentPath, 'template', 'FTer_2a_Ed', 'seed_edgvfter_2a_ed.sqlite')
        return edgvPath
    
    def createDb(self, dbName, srid, paramDict = dict()):
        destination = os.path.join(self.outputDir,dbName+'.sqlite')
        f = open(self.edgvPath,'rb')
        g = open(destination,'wb')
        x = f.readline()
        while x:
            g.write(x)
            x = f.readline()
        g.close()
        self.defineSrid(destination, srid)
        
    
    def defineSrid(self, destination, srid):
        con = sqlite3.connect(destination)
        cursor = con.cursor()
        srid_sql = (srid,)
        cursor.execute("UPDATE geometry_columns SET srid=?",srid_sql)
        con.commit()
        con.close()