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
from builtins import map, range, str

# QGIS imports
from qgis.core import (Qgis, QgsCoordinateReferenceSystem, QgsDataSourceUri,
                       QgsEditorWidgetSetup, QgsMessageLog, QgsProject,
                       QgsVectorLayer)
# Qt imports
from qgis.PyQt import QtCore, QtGui, uic
from qgis.PyQt.Qt import QObject
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.utils import iface

from ....core.LayerTools.CustomFormTools.customFormGenerator import \
    CustomFormGenerator
from ....core.LayerTools.CustomFormTools.customInitCodeGenerator import \
    CustomInitCodeGenerator
from ....gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import \
    ProgressWidget
#DsgTools imports
from .edgvLayerLoader import EDGVLayerLoader


class PostGISLayerLoader(EDGVLayerLoader):
    def __init__(self, iface, abstractDb, loadCentroids):
        """Constructor."""
        super(self.__class__, self).__init__(iface, abstractDb, loadCentroids)
        
        self.provider = 'postgres'
        self.setDatabaseConnection()
        self.buildUri()
        self.customFormGenerator = CustomFormGenerator()
        self.customInitCodeGenerator = CustomInitCodeGenerator()

    def checkLoaded(self, name):
        """
        Checks if the layers is already loaded in the QGIS' TOC
        :param name:
        :param loadedLayers:
        :return:
        """
        loaded = None
        for ll in self.iface.mapCanvas().layers():
            if ll.name() == name:
                candidateUri = QgsDataSourceUri(ll.dataProvider().dataSourceUri())
                if self.host == candidateUri.host() and self.database == candidateUri.database() and self.port == int(candidateUri.port()):
                    return ll
        return loaded
    
    def setDatabaseConnection(self):
        """
        Sets database connection parameters
        :return:
        """
        self.host = self.abstractDb.db.hostName()
        self.port = self.abstractDb.db.port()
        self.database = self.abstractDb.db.databaseName()
        self.user = self.abstractDb.db.userName()
        self.password = self.abstractDb.db.password()
    
    def buildUri(self):
        """
        Builds the database uri
        :return:
        """
        self.uri.setConnection(str(self.host),str(self.port), str(self.database), str(self.user), str(self.password))
    
    def filterLayerList(self, layerList, useInheritance, onlyWithElements, geomFilterList):
        """
        Filters the layers to be loaded
        :param layerList: list of layers
        :param useInheritance: should use inheritance
        :param onlyWithElements: should only load non empty layers?
        :param geomFilterList: geometry filter
        :return:
        """
        filterList = []
        lyrsWithElements = self.abstractDb.getLayersWithElementsV2(
            layerList,
            useInheritance=useInheritance
        ) if onlyWithElements else layerList
        if len(geomFilterList) > 0:
            finalSet = set()
            for key in self.correspondenceDict:
                finalSet = finalSet.union(
                    {
                        lyr for lyr in lyrsWithElements if self.correspondenceDict[key] in geomFilterList \
                            and key in self.geomTypeDict and lyr in self.geomTypeDict[key] 
                    }
                )
            finalList = list(finalSet)
        else:
            finalList = lyrsWithElements
        if finalList and isinstance(finalList[0], dict):
            finalList = [i['tableName'] for i in finalList]
        return finalList

    def load(self, inputList, useQml=False, uniqueLoad=False, useInheritance=False, stylePath=None, onlyWithElements=False, geomFilterList=[], customForm=False, loadEditingStructure=False, parent=None):
        """
        1. Get loaded layers
        2. Filter layers;
        3. Load domains;
        4. Get Aux Dicts;
        5. Build Groups;
        6. Load Layers;
        """
        self.iface.mapCanvas().freeze() #done to speedup things
        layerList, isDictList = self.preLoadStep(inputList)
        #2. Filter Layers:
        filteredLayerList = self.filterLayerList(inputList, useInheritance, onlyWithElements, geomFilterList)
        filteredDictList = [i for i in inputList if i['tableName'] in filteredLayerList] if isDictList else filteredLayerList
        edgvVersion = self.abstractDb.getDatabaseVersion()
        isEdgv = not edgvVersion == "Non_EDGV"
        rootNode = QgsProject.instance().layerTreeRoot()
        dbNode = self.getDatabaseGroup(rootNode)
        #3. Load Domains
        domLayerDict = self.loadDomains(filteredLayerList, dbNode, edgvVersion)
        #4. Get Aux dicts
        domainDict = self.abstractDb.getDbDomainDict(self.geomDict)
        constraintDict = self.abstractDb.getCheckConstraintDict()
        multiColumnsDict = self.abstractDb.getMultiColumnsDict()
        notNullDict = self.abstractDb.getNotNullDictV2()
        lyrDict = self.getLyrDict(filteredDictList, isEdgv=isEdgv)
        editingDict = self.abstractDb.getEditingDict() if loadEditingStructure else None
        if customForm:
            self.filterDict = self.abstractDb.getFilterDict()
            self.rulesDict = dict()
        
        #5. Build Groups
        groupDict = self.prepareGroups(dbNode, lyrDict)
        #6. load layers
        loadedDict = dict()
        if parent:
            primNumber = 0
            for prim in list(lyrDict.keys()):
                for cat in list(lyrDict[prim].keys()):
                    for lyr in lyrDict[prim][cat]:
                        primNumber += 1
            localProgress = ProgressWidget(1, primNumber-1, self.tr('Loading layers... '), parent=parent)
        for prim in list(lyrDict.keys()):
            for cat in list(lyrDict[prim].keys()):
                for lyr in lyrDict[prim][cat]:
                    try:
                        vlayer = self.loadLayer(
                            lyr,
                            parentNode=groupDict[prim][cat],
                            useInheritance=False,
                            useQml=useQml,
                            uniqueLoad=uniqueLoad,
                            stylePath=stylePath,
                            domainDict=domainDict,
                            multiColumnsDict=multiColumnsDict,
                            domLayerDict=domLayerDict,
                            edgvVersion=edgvVersion,
                            editingDict=editingDict,
                            customForm = customForm
                        )
                        if vlayer is None:
                            continue
                        key = lyr['lyrName'] if isinstance(lyr, dict) else lyr
                        loadedDict[key]=vlayer
                    except Exception as e:
                        key = lyr['lyrName'] if isinstance(lyr, dict) else lyr
                        self.logErrorDict[key] = self.tr('Error for layer ')+key+': '+':'.join(e.args)
                        self.logError()
                    if parent:
                        localProgress.step()
        self.removeEmptyNodes(dbNode)
        self.iface.mapCanvas().freeze(False) #done to speedup things
        return loadedDict

    def loadLayer(self, inputParam, parentNode, useInheritance, useQml, uniqueLoad, stylePath, domainDict, multiColumnsDict, domLayerDict, edgvVersion, geomColumn = None, isView = False, editingDict=None, customForm = False):
        """
        Loads a layer
        :param lyrName: Layer name
        :param idSubgrupo: sub group id
        :param uniqueLoad: boolean to mark if the layer should only be loaded once
        :param stylePath: path to the styles used
        :param domLayerDict: domain dictionary
        :return:
        """
        lyrName, schema, geomColumn, tableName, srid = self.getParams(inputParam)
        lyr = self.checkLoaded(tableName)
        if uniqueLoad and lyr is not None:
            return lyr
        self.setDataSource(
            schema=schema,
            layer=tableName,
            geomColumn=geomColumn,
            sql='',
            pkColumn=self.abstractDb.getPrimaryKeyColumn(f'''"{schema}"."{tableName}"''')
        )

        vlayer = QgsVectorLayer(self.uri.uri(), tableName, self.provider)
        QgsProject.instance().addMapLayer(vlayer, addToLegend = False)
        crs = QgsCoordinateReferenceSystem(int(srid), QgsCoordinateReferenceSystem.EpsgCrsId)
        if vlayer is None:
            return vlayer
        if not vlayer.isValid():
            QgsMessageLog.logMessage(vlayer.error().summary(), "DSGTools Plugin", Qgis.Critical)
        vlayer.setCrs(crs)
        vlayer = self.setDomainsAndRestrictionsWithQml(vlayer) if useQml \
            else self.setDomainsAndRestrictions(
                lyr=vlayer,
                lyrName=tableName,
                domainDict=domainDict,
                multiColumnsDict=multiColumnsDict,
                domLayerDict=domLayerDict
            )
        if stylePath is not None:
            fullPath = self.getStyle(stylePath, tableName)
            if fullPath:
                vlayer.loadNamedStyle(fullPath, True)
                # remove qml temporary file
                self.utils.deleteQml(fullPath)
                # clear fullPath variable
                del fullPath
        vlayer = self.createMeasureColumn(vlayer)
        parentNode.addLayer(vlayer)
        return vlayer
    
    def loadEditLayer(self, schema, tableName):
        """
        Parses database to check which is the referenced edit layer and loads it
        :param schema: original table schema
        :param tableName: original table name
        returns editLyr, joinLyrFieldName
        """
        editLyrSchema, editLyrTableName, pkName, joinLyrFieldName = self.abstractDb.getEditTable(schema, tableName)
        uri = """dbname='{database}' host={host} port={port} user='{user}' password='{password}' key={primary_key} table=\"{schema}\".\"{table}\" sql=""".format(
                database=self.database,
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                primary_key=pkName,
                schema=editLyrSchema,
                table=editLyrTableName
            )
    
    def loadDomain(self, domainTableName, domainGroup):
        """
        Loads layer domains
        :param domainTableName:
        :param domainGroup:
        :return:
        """
        #TODO: Avaliar se o table = deve ser diferente
        uri = "dbname='%s' host=%s port=%s user='%s' password='%s' key=code table=\"dominios\".\"%s\" sql=" % (self.database, self.host, self.port, self.user, self.password, domainTableName)
        domLayer = QgsVectorLayer(uri, domainTableName, self.provider)
        domainGroup.addLayer(domLayer)
        return domLayer

    def getStyleFromDb(self, edgvVersion, className):
        """
        Gets the style for this layer in the database
        :param edgvVersion:
        :param className:
        :return:
        """
        return self.abstractDb.getLyrStyle(edgvVersion, className)

    def setDomainsAndRestrictions(self, lyr, lyrName, domainDict, multiColumnsDict, domLayerDict):
        """
        Adjusts the domain restriction to all attributes in the layer
        :param lyr:
        :param lyrName:
        :param domainDict:
        :param multiColumnsDict:
        :param domLayerDict:
        :return:
        """
        lyrAttributes = [i for i in lyr.fields()]
        pkIdxList = lyr.primaryKeyAttributes()
        for i in range(len(lyrAttributes)):
            attrName = lyrAttributes[i].name()
            if attrName == 'id' or 'id_' in lyrAttributes[i].name() or i in pkIdxList:
                lyr.editFormConfig().setReadOnly(i,True)
            else:
                if lyrName in domainDict.keys():
                    if attrName in list(domainDict[lyrName]['columns'].keys()):
                        refTable = domainDict[lyrName]['columns'][attrName]['references']
                        refPk = domainDict[lyrName]['columns'][attrName]['refPk']
                        otherKey = domainDict[lyrName]['columns'][attrName]['otherKey']
                        valueDict = domainDict[lyrName]['columns'][attrName]['values']
                        isMulti = self.checkMulti(lyrName, attrName, multiColumnsDict)
                        if isMulti:
                            #make filter
                            if 'constraintList' in list(domainDict[lyrName]['columns'][attrName].keys()):
                                #make editDict
                                if lyrName in domLayerDict:
                                    if attrName in domLayerDict[lyrName]:
                                        filter = '{0} in ({1})'.format(refPk,','.join(map(str,domainDict[lyrName]['columns'][attrName]['constraintList'])))
                                        allowNull = domainDict[lyrName]['columns'][attrName]['nullable']
                                        dom = domLayerDict[lyrName][attrName]
                                        editDict = {'Layer':dom.id(),'Key':refPk,'Value':otherKey,'AllowMulti':True,'AllowNull':allowNull,'FilterExpression':filter}
                                        widgetSetup = QgsEditorWidgetSetup('ValueRelation', editDict)
                                        lyr.setEditorWidgetSetup(i, widgetSetup)
                        else:
                            #filter value dict
                            constraintList = domainDict[lyrName]['columns'][attrName]['constraintList']
                            valueRelationDict = dict()
                            for key in list(valueDict.keys()):
                                if len(constraintList) > 0: 
                                    if key in constraintList:
                                        valueRelationDict[valueDict[key]] = str(key)
                                else:
                                    valueRelationDict[valueDict[key]] = str(key)
                            widgetSetup = QgsEditorWidgetSetup('ValueMap',{'map':valueRelationDict})
                            lyr.setEditorWidgetSetup(i, widgetSetup)
        return lyr

    def checkMulti(self, tableName, attrName, multiColumnsDict):
        """
        Checks if an attribute is a value relation
        :param tableName:
        :param attrName:
        :param multiColumnsDict:
        :return:
        """
        if tableName in list(multiColumnsDict.keys()):
            if attrName in multiColumnsDict[tableName]:
                return True
        return False
    
    def checkNotNull(self, lyrName, notNullDict):
        """
        Checks not null attributes
        :param lyrName:
        :param notNullDict:
        :return:
        """
        allowNull = True
        if lyrName in list(notNullDict.keys()):
            if attrName in notNullDict[lyrName]['attributes']:
                allowNull = False
        return allowNull

    def getPathUiForm(self, dbName, layerName):
        #alterar
        pathUiForm =  os.path.join(
            os.path.dirname(__file__), '..', '..', 'LayerTools', 'CustomFormTools',
            'formsCustom' ,
            '{0}_{1}.ui'.format(dbName, layerName)
        )
        return pathUiForm

    def newUiForm(self, pathUiForm):
        formFile = open(pathUiForm, "wb")
        return formFile
    
    def loadFormCustom(self, lyr):
        pathUiForm = self.getPathUiForm(self.database, lyr.name())
        formFile = self.newUiForm(pathUiForm)
        #inserir flag do filtro
        withFilter = lyr.name() in self.filterDict
        self.customFormGenerator.create(formFile, lyr, withFilter=withFilter)
        lyr.editFormConfig().setInitCodeSource(2)
        lyr.editFormConfig().setLayout(2)
        lyr.editFormConfig().setUiForm(pathUiForm)
        initCode = self.createCustomInitCode(lyr)
        if initCode:
            lyr.editFormConfig().setInitFunction("formOpen")
            lyr.editFormConfig().setInitCode(initCode)
        return lyr

    def getRulesSelected(self, lyr):
        rules = []
        # currentlayerName = lyr.name()
        # if  self.getRules():
        #     allRules = self.getRules().getRulesToForm() 
        #     selectedRuleOnOrder = { allRules["order_rules"][k.encode("utf-8")] : k.encode("utf-8")  for k in data['selectedRulesType']}
        #     for order in reversed(sorted(selectedRuleOnOrder)):
        #         ruleName = selectedRuleOnOrder[order]
        #         for lyrName in  allRules[ruleName]:
        #             if  currentlayerName == lyrName:
        #                 rules.append(allRules[ruleName][currentlayerName])
        #     return rules
        return {}

    def createCustomInitCode(self, lyr):

        rules = self.getRulesSelected(lyr)
        # dbData = data['userData']['dbJson'][data['dbAlias']]
        # layerData = dbData[data['nameGeom']][data['nameCatLayer']][data['layerName']]
        if lyr.name() in list(self.filterDict.keys()):
            initCode = self.customInitCodeGenerator.getInitCodeWithFilter(self.filterDict[lyr.name()], rules) #layerData['filter'] é o resultado da query select * from dominios.<nome do dominio do atributo com filtro>
            return initCode
        else:
            initCode = self.customInitCodeGenerator.getInitCodeNotFilter(rules)
            return initCode

    def getLayerByName(self, layer):
        """
        Return the layer layer from a given layer name.
        :param layer: (str) layer name.
        :return: (QgsVectorLayer) vector layer. 
        """
        # parent class reimplementation
        table = layer.split('.')[1]
        return self.loadQgsVectorLayer(table)
    
    def loadQgsVectorLayer(self, inputParam, uniqueLoad=False, addToCanvas=False, nonSpatial=False):
        """
        Returns a QgsVectorLayer using the parameters from inputParam.
        If uniqueLoad=True, checks if layer is already loaded and if it is,
        returns it.
        """
        lyrName, schema, geomColumn, tableName, srid = self.getParams(inputParam=inputParam)
        lyr = self.checkLoaded(tableName)
        if uniqueLoad and lyr is not None:
            return lyr
        pkColumn = self.abstractDb.getPrimaryKeyColumn(
            "{table_schema}.{table_name}".format(
                table_schema=schema,
                table_name=tableName
            )
        )
        if nonSpatial:
            uri = """dbname='{dbname}' host={host} port={port} user='{user}' password='{password}' key={pk} checkPrimaryKeyUnicity='0' table="{table_schema}"."{table_name}" sql=""".format(
                dbname=self.database,
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                pk=pkColumn,
                table_schema=schema,
                table_name=tableName
            )
        else:
            self.setDataSource(schema, tableName, geomColumn, '', pkColumn=pkColumn)
            uri = self.uri.uri()
        lyr = QgsVectorLayer(uri, tableName, self.provider)
        QgsProject.instance().addMapLayer(lyr, addToLegend=addToCanvas)
        return lyr

    
    def loadLayersInsideProcessing(self, inputParamList, uniqueLoad=False, addToCanvas=True, nonSpatial=False, feedback=None):
        """
        Loads layer inside qgis using processing. If uniqueLoad=True, only loads
        if it is not loaded.
        """
        outputLayers = []
        progressStep = 100/len(inputParamList) if len(inputParamList) else 0
        for current, inputParam in enumerate(inputParamList):
            if feedback is not None and feedback.isCanceled():
                break
            lyr = self.loadQgsVectorLayer(
                inputParam=inputParam,
                uniqueLoad=uniqueLoad,
                addToCanvas=addToCanvas,
                nonSpatial=nonSpatial
            )
            outputLayers.append(lyr)
            if feedback is not None:
                feedback.setProgress(current*progressStep)
        return outputLayers
