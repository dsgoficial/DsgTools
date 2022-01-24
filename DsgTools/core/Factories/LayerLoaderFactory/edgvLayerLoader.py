# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-07-16
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
import os

from qgis.core import (Qgis,
                       QgsField,
                       QgsWkbTypes,
                       QgsMessageLog,
                       QgsVectorLayer,
                       QgsDataSourceUri,
                       QgsVectorLayerJoinInfo)
from qgis.utils import iface
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.Qt import QObject
from qgis.PyQt.QtXml import QDomDocument

from DsgTools.core.Utils.utils import Utils

class EDGVLayerLoader(QObject):
    
    def __init__(self, iface, abstractDb, loadCentroids):
        """Constructor."""
        super(EDGVLayerLoader, self).__init__()
        
        self.abstractDb = abstractDb
        self.uri = QgsDataSourceUri() 
        self.iface = iface
        self.utils = Utils()
        self.logErrorDict = dict()
        self.errorLog = ''
        self.geomTypeDict = self.abstractDb.getGeomTypeDict(loadCentroids)
        self.geomDict = self.abstractDb.getGeomDict(self.geomTypeDict)
        self.correspondenceDict = {'POINT':'Point', 'MULTIPOINT':'Point', 'LINESTRING':'Line','MULTILINESTRING':'Line', 'POLYGON':'Area', 'MULTIPOLYGON':'Area'}
    
    def preLoadStep(self, inputList):
        if len(inputList) == 0:
            return [], False
        else:
            if isinstance(inputList[0], dict):
                lyrList = [i['tableName'] for i in inputList]
                return lyrList, True
            else:
                return inputList, False

    def load(self, inputList, useQml=False, uniqueLoad=False, useInheritance=False, stylePath=None, onlyWithElements=False, geomFilterList=[], isEdgv=True, customForm=False, loadEditingStructure=False, parent=None):
        return None
    
    def getStyle(self, stylePath, className):
        if 'db:' in stylePath['style']:
            return self.abstractDb.getStyle(stylePath['style'].split(':')[-1], className)
        else:
            return self.getStyleFromFile(stylePath['style'], className)
    
    def getStyleFromFile(self, stylePath, className):
        styleName = "{0}.qml".format(className)
        if styleName.lower() in [f.lower() for f in os.listdir(stylePath)]:
            qml = self.utils.parseStyle(os.path.join(stylePath, styleName))
            # dsgtools have the right to write on its own directory
            # a temporary file "temp.qml"
            tempPath = os.path.join(stylePath, "temp.qml")
            with open(tempPath, "w", encoding='utf-8') as f:
                f.writelines(qml)
                f.close()
            return tempPath
        else:
            return None
    
    def prepareLoad(self):
        dbName = self.abstractDb.getDatabaseName()
        groupList =  iface.legendInterface().groups()
        if dbName in groupList:
            return groupList.index(dbName)
        else:
            parentTreeNode = iface.legendInterface().addGroup(self.abstractDb.getDatabaseName(), -1)
            return parentTreeNode

    def createMeasureColumn(self, layer):
        if layer.geometryType() == QgsWkbTypes.PolygonGeometry:
            layer.addExpressionField('$area', QgsField(self.tr('area_otf'), QVariant.Double))
        elif layer.geometryType() == QgsWkbTypes.LineGeometry:
            layer.addExpressionField('$length', QgsField(self.tr('length_otf'), QVariant.Double))
        return layer
    
    def getDatabaseGroup(self, rootNode):
        dbName = self.abstractDb.getDatabaseName()
        return self.createGroup(dbName, rootNode)

    def getLyrDict(self, inputList, isEdgv = True):
        """
        Builds lyrDict in order to build loading tree
        lyrList: list of layers to be loaded
        isEdgv: optional parameter to indicate when db is not edgv. If db is not edgv, layers will be grouped by schema.
        """
        lyrDict = dict()
        if isinstance(inputList, list):
            if len(inputList) > 0:
                if isinstance(inputList[0],dict):
                    for elem in inputList:
                        if elem['geomType'] == 'GEOMETRY':
                            continue
                        if self.correspondenceDict[elem['geomType']] not in list(lyrDict.keys()):
                            lyrDict[self.correspondenceDict[elem['geomType']]] = dict()
                        if elem['cat'] not in list(lyrDict[self.correspondenceDict[elem['geomType']]].keys()):
                            lyrDict[self.correspondenceDict[elem['geomType']]][elem['cat']] = []
                        lyrDict[self.correspondenceDict[elem['geomType']]][elem['cat']].append(elem)
                else:
                    for type in list(self.geomTypeDict.keys()):
                        # some tables are only registered as GEOMETRY and should not be considered
                        if type == 'GEOMETRY':
                            continue
                        if self.correspondenceDict[type] not in list(lyrDict.keys()):
                            lyrDict[self.correspondenceDict[type]] = dict()
                        for lyr in self.geomTypeDict[type]:
                            if lyr in inputList:
                                if isEdgv:
                                    cat = lyr.split('_')[0]
                                else:
                                    cat = self.abstractDb.getTableSchemaFromDb(lyr)
                                if cat not in list(lyrDict[self.correspondenceDict[type]].keys()):
                                    lyrDict[self.correspondenceDict[type]][cat] = []
                                lyrDict[self.correspondenceDict[type]][cat].append(lyr)
                    for type in list(lyrDict.keys()):
                        if lyrDict[type] == dict():
                            lyrDict.pop(type)
        return lyrDict

    def prepareGroups(self, rootNode, lyrDict):
        aux = dict()
        groupDict = dict()
        groupNodeList = list(lyrDict.keys())
        groupNodeList.sort(reverse=True)
        for geomNodeName in groupNodeList:
            groupDict[geomNodeName] = dict()
            geomNode = self.createGroup(geomNodeName, rootNode)
            catList = list(lyrDict[geomNodeName].keys())
            catList.sort()
            for catNodeName in catList:
                groupDict[geomNodeName][catNodeName] = self.createGroup(catNodeName, geomNode)
        return groupDict
    
    def createGroup(self, groupName, rootNode):
        groupNode = rootNode.findGroup(groupName)
        if groupNode:
            return groupNode
        else:
            return rootNode.addGroup(groupName)
        
    def loadDomains(self, layerList, dbRootNode, edgvVersion):
        if edgvVersion not in ('FTer_2a_Ed', '3.0'):
            return dict()
        domLayerDict = dict()
        try:
            qmlDict = self.abstractDb.getQmlDict(layerList)
        except:
            return dict()
        domainNode = self.createGroup(self.tr("Domains"), dbRootNode)
        loadedDomainsDict = {} if not domainNode.findLayers() else {i.layer().name() : i.layer() for i in domainNode.findLayers()}
        for lyr in layerList:
            if lyr in qmlDict:
                for attr in qmlDict[lyr]:
                    domain = qmlDict[lyr][attr]
                    domLyr = self.getDomainLyr(domain, loadedDomainsDict, domainNode)
                    if lyr not in list(domLayerDict.keys()):
                        domLayerDict[lyr] = dict()
                    if attr not in list(domLayerDict[lyr].keys()):
                        domLayerDict[lyr][attr] = domLyr
        return domLayerDict
    
    def getDomainLyr(self, domain, loadedDomainsDict, domainNode):
        if domain in loadedDomainsDict:
            return loadedDomainsDict[domain]
        domainLyr = self.loadDomain(domain, domainNode)
        loadedDomainsDict[domain] = domainLyr
        return domainLyr
        

    def logError(self):
        msg = ''
        for lyr in self.logErrorDict:
            msg += self.tr('Error for lyr ')+ lyr + ': ' +self.logErrorDict[lyr] + '\n'
        self.errorLog += msg

    def setDataSource(self, schema, layer, geomColumn, sql, pkColumn='id'):
        self.uri.setDataSource(schema, layer, geomColumn, sql, pkColumn)
        if sql == '':
            self.uri.disableSelectAtId(False)
        else:
            self.uri.disableSelectAtId(True)

    def setDomainsAndRestrictionsWithQml(self, vlayer):
        qmldir = ''
        try:
            qmldir, qmlType = self.abstractDb.getQml(vlayer.name())
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSGTools Plugin", Qgis.Critical)
            return None
        if qmlType == 'db':
            tempPath = os.path.join(os.path.dirname(__file__), "temp.qml")
            with open(tempPath, "w", encoding='utf-8') as f:
                f.writelines(qmldir)
                f.close()
            vlayer.loadNamedStyle(tempPath, True)
            os.remove(tempPath)
        else:
            vlayerQml = os.path.join(qmldir, vlayer.name()+'.qml')
            #treat case of qml with multi
            vlayer.loadNamedStyle(vlayerQml, True)
        return vlayer
    
    def removeEmptyNodes(self, dbNode):
        for geomNode in dbNode.children():
            if not geomNode.findLayers():
                dbNode.removeChildNode(geomNode)
                continue
            for catNode in geomNode.children():
                if not catNode.findLayers():
                    geomNode.removeChildNode(catNode)
    
    def getParams(self, inputParam):
        if isinstance(inputParam, dict):
            lyrName = inputParam['lyrName']
            schema = inputParam['tableSchema']
            geomColumn = inputParam['geom']
            tableName = inputParam['tableName']
            srid =  self.geomDict['tablePerspective'][tableName]['srid']
        elif isinstance(inputParam, tuple):
            schema, tableName = inputParam
            lyrName = tableName
            geomColumn, srid = '', ''
        else:
            lyrName = inputParam
            tableName = self.geomDict['tablePerspective'][lyrName]['tableName']
            schema = self.geomDict['tablePerspective'][lyrName]['schema']
            geomColumn = self.geomDict['tablePerspective'][lyrName]['geometryColumn']
            srid =  self.geomDict['tablePerspective'][lyrName]['srid']
        return lyrName, schema, geomColumn, tableName, srid

    def getLayerByName(self, layer):
        """
        Return the layer layer from a given layer name.
        :param layer: (str) layer name.
        :return: (QgsVectorLayer) vector layer. 
        """
        try:
            # self.provider is added on children classes
            return QgsVectorLayer(self.uri.uri(), layer, self.provider)
        except:
            return None

    def getComplexLayerByName(self, layer):
        """
        Return the layer layer from a given layer name.
        :param layer: (str) layer name.
        :return: (QgsVectorLayer) vector layer. 
        """
        try:
            # self.provider is added on children classes]
            schema, table = self.abstractDb.getTableSchema(layer)
            return QgsVectorLayer(self.uri.uri(), table, self.provider)
        except:
            return None
    
    def buildJoin(self, originalLyr, originalLyrFieldName, joinnedLyr, joinLyrFieldName):
        """
        Builds a join bewteen lyr and joinnedLyr.
        :param originalLyr: QgsVectorLayer original layer;
        :param originalLyrFieldName: (str) name of the field;
        :param joinnedLyr: QgsVectorLayer lyr to be joinned to originalLayer;
        :param joinLyrFieldName: (str) name of the join field name (usually primary key of joinnedLyr)
        """
        joinObject = QgsVectorLayerJoinInfo()
        joinObject.setJoinFieldName(joinLyrFieldName)
        joinObject.setTargetFieldName(originalLyrFieldName)
        joinObject.setJoinLayer(joinnedLyr)
        joinObject.setJoinFieldNamesSubset()
        joinObject.upsertOnEdit(True) #set to enable edit on original lyr
        joinObject.setCascadedDelete(True)
        joinObject.setDynamicFormEnabled(True)
        joinObject.setEditable(True)
        joinObject.setUsingMemoryCache(True)
        originalLyr.addJoin(joinObject)
