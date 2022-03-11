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

from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.error, urllib.parse
from xml.dom.minidom import parseString, Element

from qgis.core import Qgis
from qgis.PyQt.QtCore import QSettings, QObject
from qgis.PyQt.QtWidgets import QMessageBox

from DsgTools.core.Utils.utils import MessageRaiser

class BDGExRequestHandler(QObject):
    def __init__(self,parent=None):
        """
        Constructor
        """
        super(BDGExRequestHandler, self).__init__()
        self.availableServicesDict = {
            'mapcache' : {
                'url' : 'https://bdgex.eb.mil.br/mapcache',
                'services' : {
                    'WMS' : dict()
                }
            },
            'mapindex' : {
                'url' : 'https://bdgex.eb.mil.br/cgi-bin/mapaindice',
                'services': {
                    'WMS' : dict(),
                    'WFS' : dict()
                }
            },
            'auxlayers' : {
                'url' : 'https://bdgex.eb.mil.br/cgi-bin/geoportal',
                'services' : {
                    'WMS' : dict(),
                    'WFS' : dict()
                }
            }
        }

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
        excludedUrls = list()
        if settings.value('proxyExcludedUrls'):
            excludedUrls = settings.value('proxyExcludedUrls')
        if settings.value('noProxyUrls'):
            excludedUrls += settings.value('noProxyUrls')
        # try:
        #     urlsList = excludedUrls.split('|')
        # except:
        #     urlsList = []
        settings.endGroup()
        return (enabled, host, port, user, password, type, excludedUrls)

    def get_url_string(self, service, layerList, serviceType):
        """
        Returns QGIS url service string.
        """
        if service not in self.availableServicesDict:
            raise Exception('Service {service} not available'.format(service=service))
        if serviceType not in self.availableServicesDict[service]['services']:
            raise Exception(
                'Invalid request {service_type} for service {service}'.format(
                    service=service,
                    service_type=serviceType
                    )
                )
        url = self.availableServicesDict[service]['url']
        if not self.availableServicesDict[service]['services'][serviceType]:
            self.availableServicesDict[service]['services'][serviceType] = self.getCapabilitiesDict(service, url, service_type=serviceType)
        layers = self.availableServicesDict[service]['services'][serviceType]
        if layers is not None:
            layer = layers.get(layerList[0], None) \
                or layers.get("ms:{0}".format(layerList[0]), None)
            if layer:
                return self.getRequestString(
                    layerList,
                    url,
                    layer,
                    serviceType
                )

    def getCapabilitiesDict(self, service, url, service_type=None):
        service_type = service_type or 'WMS'
        capabilities_url = "{url}?service={service_type}&request=GetCapabilities".format(
            url=self.availableServicesDict[service]['url'],
            service_type=service_type
        )
        myDom = self.requestGetCapabilitiesXML(capabilities_url)
        if not myDom:
            return {}
        if service_type == 'WMS':
            return self.parseCapabilitiesXML(myDom)
        elif service_type == 'WFS':
            return self.parse_wfs_capabilities(myDom)
        else:
            return {}

    def requestGetCapabilitiesXML(self, url):
        """
        Gets url capabilities
        """
        self.setUrllibProxy(url)
        getCapa = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
        try:
            resp = urllib.request.urlopen(getCapa)
        except Exception as e:
            title = self.tr("BDGEx layers (DSGTools)")
            msg = self.tr("Unable to provide requested layer. Please check "
                          "your network settings (proxy and exceptions too, if"
                          " necessary).")
            MessageRaiser().raiseIfaceMessage(title, msg, Qgis.Warning, 5)
            return ""
        response = resp.read()
        try:
            myDom = parseString(response)
        except:
            raise Exception('Parse Error')
        return myDom
    
    def parseCapabilitiesXML(self, capabilitiesDom):
        """
        Parses GetCapabilities to get info.
        Return dictionary has the format:
        {
            'layer_name' : {
                'Name' : "layer name",
                'SRS' : "layer srs",
                'Title' : "layer title",
                'Abstract' : "layer abstract",
                'Format' : "layer image format"
            }
        }
        """
        jsonDict = dict()
        for node in capabilitiesDom.getElementsByTagName("Layer")[1::]:
            newItem = {}
            for tag in node.childNodes:
                if isinstance(tag, Element):
                    tagName = tag.tagName
                    if tag.childNodes:
                        newItem[tagName] = tag.childNodes[0].nodeValue
            jsonDict[newItem['Name']] = newItem
        #parse to add format to jsonDict
        for tile in capabilitiesDom.getElementsByTagName("TileSet"):
            itemName = tile.getElementsByTagName('Layers')[0].childNodes[0].nodeValue
            imgFormat = tile.getElementsByTagName('Format')[0].childNodes[0].nodeValue
            jsonDict[itemName]['Format'] = imgFormat
        for key, dictItem in jsonDict.items():
            if 'Format' not in dictItem:
                jsonDict[key]['Format'] = 'image/png'
            if 'SRS' not in dictItem:
                jsonDict[key]['SRS'] = 'EPSG:4326'
        return jsonDict
    
    def parse_wfs_capabilities(self, capabilitiesDom):
        jsonDict = dict()
        for node in capabilitiesDom.getElementsByTagName('FeatureType'):
            newItem = dict()
            name = node.getElementsByTagName('Name')[0].childNodes[0].nodeValue
            crsNode = node.getElementsByTagName('DefaultSRS') or node.getElementsByTagName('DefaultCRS')
            epsg = crsNode[0].childNodes[0].nodeValue
            newItem = {
                'Name' : name,
                'SRS' : 'EPSG:{code}'.format(code=epsg.split('::')[-1])
            }
            jsonDict[name] = newItem
        return jsonDict


    def getRequestString(self, layerList, url, infoDict, serviceType):
        """
        Makes the requisition to the tile cache service
        """
        if layerList == []:
            raise Exception('Invalid name request')
        elif len(layerList) > 1:
            # ctmList = [i for i in capabilitiesDict.keys() if 'ctm' in i]
            # ctmList.sort(key = lambda x : int(x.replace('ctm','')))
            layer_tag = 'layers='+'&layers='.join(layerList)
            styles_tag = '&'.join(['styles']*len(layerList))
        else:
            layer_tag = 'layers={layer_name}'.format(layer_name=layerList[0])
            styles_tag = 'styles'
        if serviceType == 'WMS':
            requestString = "crs={epsg}&dpiMode=7&featureCount=10&format={img_format}&{layer_tag}&{styles_tag}&url={url}".format(
                epsg=infoDict['SRS'],
                img_format=infoDict['Format'],
                layer_tag=layer_tag,
                styles_tag=styles_tag,
                url=url
            )
        elif serviceType == 'WFS':
            requestString = """pagingEnabled='true' restrictToRequestBBOX='1' srsname='{epsg}' typename='{layer_name}' url='{url}' version='auto' table="" sql=""".format(
                epsg=infoDict['SRS'],
                layer_name=infoDict['Name'],
                url=url
            )
        else:
            requestString == ''
        return requestString