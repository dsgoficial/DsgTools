# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
import json
import os
from xml.dom.minidom import parse, parseString
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4 import QtGui

class Utils:

    def mergeDict(self, dictionary1, dictionary2):
        """
        Merges two dictionaries
        """
        output = dict()
        if type(dictionary1) <> dict or type(dictionary2) <> dict:
            return dictionary2
        for item, value in dictionary1.iteritems():
            if dictionary2.has_key(item):
                if isinstance(dictionary2[item], dict):
                    output[item] = self.mergeDict(value, dictionary2.pop(item))
                else:
                    if type(value) == list:
                        if item not in output.keys():
                            output[item] = []
                        for i in value:
                            if i not in output[item]:
                                output[item].append(i)
                        output[item].extend(self.mergeDict(
                            value, dictionary2.pop(item)))
                    else:
                        output[item] = self.mergeDict(
                            value, dictionary2.pop(item))
            else:
                if type(value) == list:
                    if item not in output.keys():
                        output[item] = []
                    for i in value:
                        if i not in output[item]:
                            output[item].append(i)
                else:
                    output[item] = value
        for item, value in dictionary2.iteritems():
            if type(value) == list:
                if item not in output.keys():
                    output[item] = []
                for i in value:
                    if i not in output[item]:
                        output[item].append(i)
            else:
                output[item] = value
        return output

    def buildOneNestedDict(self, inputDict, keyList, value):
        """
        Builds a nested dictionary for a specific key
        """
        if len(keyList) == 1:
            if keyList[0] not in inputDict.keys():
                inputDict[keyList[0]] = dict()
            if type(value) == list:
                inputDict[keyList[0]] = []
                for i in value:
                    if i not in inputDict[keyList[0]]:
                        inputDict[keyList[0]].append(i)
            else:
                inputDict[keyList[0]] = value
            return inputDict
        else:
            if keyList[0] not in inputDict.keys():
                if len(inputDict.values()) == 0:
                    inputDict[keyList[0]] = dict()
            inputDict[keyList[0]] = self.buildOneNestedDict(
                inputDict[keyList[0]], keyList[1::], value)
            return inputDict

    def buildNestedDict(self, inputDict, keyList, value):
        """
        Builds a nested dict
        """
        if len(inputDict.keys()) > 0:
            tempDict = self.buildOneNestedDict(dict(), keyList, value)
            return self.mergeDict(inputDict, tempDict)
        else:
            return self.buildOneNestedDict(inputDict, keyList, value)

    def readJsonFile(self, filename, returnFileAndDict=False):
        """
        Reads a json file and makes a dictionary
        """
        try:
            file = open(filename, 'r')
            data = file.read()
            fileDict = json.loads(data)
            file.close()
            if returnFileAndDict:
                return fileDict, data
            else:
                return fileDict
        except:
            return dict()

    def parseStyle(self, qml):
        qml = qml.replace("''", "'")
        if '.qml' in qml:
            doc = parse(qml)
        else:
            doc = parseString(qml)
        forbiddenList = doc.getElementsByTagName('edittypes')
        if len(forbiddenList) > 0:
            forbiddenNode = forbiddenList[0]
            qgisNode = doc.getElementsByTagName('qgis')[0]
            qgisNode.removeChild(forbiddenNode)
        return doc.toxml().replace('<?xml version="1.0" encoding="utf-8"?>', '')

    def parseMultiQml(self, qmlPath, lyrList):
        """
        dict in the form {'lyrName': {'attributeName':'domainTableName'}}
        """
        refDict = dict()
        for lyr in lyrList:
            try:
                qml = os.path.join(qmlPath, lyr + '.qml')
                doc = parse(qml)
                refDict[lyr] = dict()
                for node in doc.getElementsByTagName('edittype'):
                    if node.getAttribute('widgetv2type') == 'ValueRelation':
                        attrName = node.getAttribute('name')
                        refDict[lyr][attrName] = node.getElementsByTagName(
                            'widgetv2config')[0].getAttribute('Layer')
            except:
                pass
        return refDict

    def getRecursiveInheritance(self, parent, resultList, inhDict):
        if parent not in resultList:
            resultList.append(parent)
        if parent in inhDict.keys():
            for child in inhDict[parent]:
                self.getRecursiveInheritance(child, resultList, inhDict)

    def getRecursiveInheritanceTreeDict(self, parent, resultDict, inhDict):
        if parent not in resultDict.keys():
            resultDict[parent] = dict()
        if parent in inhDict.keys():
            for child in inhDict[parent]:
                self.getRecursiveInheritanceTreeDict(
                    child, resultDict[parent], inhDict)

    def find_all_paths(self, graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_key(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = self.find_all_paths(graph[start], node, end, path)
                for newpath in newpaths:
                    if newpath not in paths:
                        paths.append(newpath)
        return paths

    def getAllItemsInDict(self, inputDict, itemList):
        for key in inputDict.keys():
            if key not in itemList:
                itemList.append(key)
            self.getAllItemsInDict(inputDict[key], itemList)

    def createWidgetItem(self, parent, text, column = None):
        item = QtGui.QTreeWidgetItem(parent)
        if isinstance(text,list) and column == None:
            for i in range(len(text)):
                item.setText(text[i],i)
                return item
        else:
            item.setText(column, text)
            return item

    def createTreeWidgetFromDict(self, parentNode, inputDict, treeWidget, column):
        for key in inputDict.keys():
            item = self.createWidgetItem(parentNode, key, column)
            self.createTreeWidgetFromDict(
                item, inputDict[key], treeWidget, column)
    
    def getTreeBranchFromNode(self, startNode, inputDict):
        if 'root' not in inputDict.keys():
            graph = {'root':inputDict}
        else:
            graph = inputDict
        path = self.find_all_paths(graph, 'root', startNode)[0]
        for node in path:
            graph = graph[node]
        return {startNode:graph}
    
    def getNodeLineage(self, node, inputDict):
        return self.find_all_paths(inputDict, 'root', node)[0][1::]

    def instantiateJsonDict(self, jsonDict):
        if isinstance(jsonDict, dict):
            return jsonDict
        else:
            return json.loads(jsonDict)
