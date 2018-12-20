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
        email                : borba.philipe@eb.mil.br
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
from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.error, urllib.parse
from xml.dom.minidom import parseString

from qgis.PyQt.QtCore import QSettings, QObject
from qgis.PyQt.QtWidgets import QMessageBox


class BDGExTools(QObject):
    def __init__(self,parent=None):
        """
        Constructor
        """
        super(BDGExTools, self).__init__()

        self.wmtsDict = dict()
        self.wmtsDict['MultiScale']='ctm250'
        self.wmtsDict['1:250k']='ctm250'
        self.wmtsDict['1:100k']='ctm100'
        self.wmtsDict['1:50k']='ctm50'
        self.wmtsDict['1:25k']='ctm25'
        self.wmtsDict['Landsat7']='landsat7'
        self.wmtsDict['RapidEye']='rapideye'
        pass

    def __del__(self):
        pass
    
    def setUrllibProxy(self, url):
        """
        Sets the proxy
        """
        (enabled, host, port, user, password, type, urlsList) = self.getProxyConfiguration()
        if enabled == 'false' or type != 'HttpProxy':
            return
        
        for address in urlsList:
            if address in url:
                proxy = urllib.request.ProxyHandler({})
                opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
                urllib.request.install_opener(opener)
                return

        proxyStr = 'http://'+user+':'+password+'@'+host+':'+port
        proxy = urllib.request.ProxyHandler({'http': proxyStr})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        return          

    def getProxyConfiguration(self):
        """
        Gets the proxy configuration from QSettings
        """
        settings = QSettings()
        settings.beginGroup('proxy')
        enabled = settings.value('proxyEnabled')
        host = settings.value('proxyHost')
        port = settings.value('proxyPort')
        user = settings.value('proxyUser')
        password = settings.value('proxyPassword')
        type = settings.value('proxyType')
        excludedUrls = settings.value('proxyExcludedUrls')
        try:
            urlsList = excludedUrls.split('|')
        except:
            urlsList = []
        settings.endGroup()
        return (enabled, host, port, user, password, type, urlsList)

    def getTileCache(self,layerName):
        """
        Makes the requisition to the tile cache service
        """
        url = "http://www.geoportal.eb.mil.br/mapcache?request=GetCapabilities"
        # set proxy
        self.setUrllibProxy(url)

        try:
            getCapa = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
            resp = urllib.request.urlopen(getCapa)
            response = resp.read()
        except urllib.error.URLError as e:
            QMessageBox.critical(None, self.tr("URL Error!"), '{0}\nReason: {1}'.format(e.args, e.reason))
            return None
        except urllib.error.HTTPError as e:
            QMessageBox.critical(None, self.tr("HTTP Error!"), '{0}\nReason: {1}'.format(e.code, e.msg))
            return None

        try:
            myDom=parseString(response)
        except:
            QMessageBox.critical(None, self.tr("Parse Error!"), self.tr('Invalid GetCapabilities response: \n{0}').format(response))
            return None

        qgsIndexDict = dict()
        count = 0

        for tileMap in myDom.getElementsByTagName("Layer"):
            qgsIndexDict[tileMap.getElementsByTagName("Name")[0].firstChild.nodeValue]=count
            count += 1

        tileMatrixSet = '{0}-wmsc-{1}'.format(self.wmtsDict[layerName],qgsIndexDict[self.wmtsDict[layerName]])
        return 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers={0}&styles=&url=http://www.geoportal.eb.mil.br/mapcache'.format(self.wmtsDict[layerName])
