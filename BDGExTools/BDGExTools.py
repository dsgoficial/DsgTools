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
       mod history          : 2015-04-12 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
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
import urllib2
from xml.dom.minidom import parse

from PyQt4.QtCore import QSettings, QObject
from PyQt4.QtGui import QMessageBox


class BDGExTools(QObject):
    def __init__(self,parent=None):
        super(BDGExTools, self).__init__()

        self.wmtsDict = dict()
        self.wmtsDict['1:250k']='ctm250'
        self.wmtsDict['1:100k']='ctm100'
        self.wmtsDict['1:50k']='ctm50'
        self.wmtsDict['1:25k']='ctm25'
        self.wmtsDict['Landsat7']='landsat7'
        pass

    def __del__(self):
        pass
    
    def setUrllibProxy(self):
        (enabled, host, port, user, password, type) = self.getProxyConfiguration()
        if enabled == 'false' or type != 'HttpProxy':
            return

        proxyStr = 'http://'+user+':'+password+'@'+host+':'+port
        proxy = urllib2.ProxyHandler({'http': proxyStr})
        opener = urllib2.build_opener(proxy, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

    def getProxyConfiguration(self):
        settings = QSettings()
        settings.beginGroup('proxy')
        enabled = settings.value('proxyEnable')
        host = settings.value('proxyHost')
        port = settings.value('proxyPort')
        user = settings.value('proxyUser')
        password = settings.value('proxyPassword')
        type = settings.value('proxyType')
        settings.endGroup()
        return (enabled, host, port, user, password, type)

    def getTileCache(self,layerName):
        # set proxy
        self.setUrllibProxy()

        try:
            getCapa = urllib2.urlopen("http://www.geoportal.eb.mil.br/tiles?request=GetCapabilities")
            response = getCapa.read()
        except urllib2.URLError, e:
            QMessageBox.critical(None, self.tr("URL Error!"), str(e.args) + '\nReason: '+str(e.reason))
            return None
        except urllib2.HTTPError, e:
            QMessageBox.critical(None, self.tr("HTTP Error!"), str(e.code) + '\nReason: '+str(e.msg))
            return None

        try:
            myDom=parse(getCapa)
        except:
            QMessageBox.critical(None, self.tr("Parse Error!"), self.tr('Invalid GetCapabilities response:')+'\n'+str(response))
            return None

        qgsIndexDict = dict()
        count = 0

        for tileMap in myDom.getElementsByTagName("TileMap"):
            qgsIndexDict[tileMap.getAttribute("title")]=count
            count += 1

        tileMatrixSet = self.wmtsDict[layerName]+'-wmsc-'+str(qgsIndexDict[self.wmtsDict[layerName]])
        return 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/gif&layers='+self.wmtsDict[layerName]+'&styles=&tileMatrixSet='+tileMatrixSet+'&url=http://www.geoportal.eb.mil.br/tiles?service=WMTS'
