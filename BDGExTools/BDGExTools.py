# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-04-11
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Philipe Borba - Cartographic Engineer @ Brazilian Army
                                           Maurício de Paulo - Cartographic Engineer @ Brazilian Army
        email                : borba@dsg.eb.mil.br
                               mauricio@dsg.eb.mil.br
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
# Import the PyQt and QGIS libraries
import urllib
from xml.dom.minidom import parse, parseString
import sys, os


class BDGExTools:
    def __init__(self,parent=None):
        self.wmtsDict = dict()
        self.wmtsDict['1:250k']='ctm250'
        self.wmtsDict['1:100k']='ctm100'
        self.wmtsDict['1:50k']='ctm50'
        self.wmtsDict['1:25k']='ctm25'
        self.wmtsDict['Landsat7']='landsat7'
        pass

    def __del__(self):
        pass
    
    def getTileCache(self,layerName):
        getCapa=urllib.urlopen("http://www.geoportal.eb.mil.br/tiles?request=GetCapabilities")
        myDom=parse(getCapa)
        qgsIndexDict = dict()
        count = 0
        for tileMap in myDom.getElementsByTagName("TileMap"):
            qgsIndexDict[tileMap.getAttribute("title")]=count
            count += 1
        tileMatrixSet = self.wmtsDict[layerName]+'-wmsc-'+str(qgsIndexDict[self.wmtsDict[layerName]])
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/gif&layers='+self.wmtsDict[layerName]+'&styles=&tileMatrixSet='+tileMatrixSet+'&url=http://www.geoportal.eb.mil.br/tiles?service=WMTS'
        return urlWithParams
