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

import os
import json
import re
import requests
from xml.dom.minidom import parse, parseString

from qgis.utils import iface
from qgis.core import Qgis, QgsMessageLog, QgsExpression
from qgis.gui import QgsGui
from qgis.PyQt.QtCore import QObject, QSettings, QVariant
from qgis.PyQt.QtWidgets import QAction, QToolBar, QMessageBox, QTreeWidgetItem
from qgis.PyQt.QtGui import QColor


class Utils(object):
    def mergeDict(self, dictionary1, dictionary2):
        """
        Merges two dictionaries
        """
        output = dict()
        if type(dictionary1) != dict or type(dictionary2) != dict:
            return dictionary2
        for item, value in dictionary1.items():
            if item in dictionary2:
                if isinstance(dictionary2[item], dict):
                    output[item] = self.mergeDict(value, dictionary2.pop(item))
                else:
                    if type(value) == list:
                        if item not in list(output.keys()):
                            output[item] = []
                        for i in value:
                            if i not in output[item]:
                                output[item].append(i)
                        output[item].extend(
                            self.mergeDict(value, dictionary2.pop(item))
                        )
                    else:
                        output[item] = self.mergeDict(value, dictionary2.pop(item))
            else:
                if type(value) == list:
                    if item not in list(output.keys()):
                        output[item] = []
                    for i in value:
                        if i not in output[item]:
                            output[item].append(i)
                else:
                    output[item] = value
        for item, value in dictionary2.items():
            if type(value) == list:
                if item not in list(output.keys()):
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
            if keyList[0] not in list(inputDict.keys()):
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
            if keyList[0] not in list(inputDict.keys()):
                if len(list(inputDict.values())) == 0:
                    inputDict[keyList[0]] = dict()
            inputDict[keyList[0]] = self.buildOneNestedDict(
                inputDict[keyList[0]], keyList[1::], value
            )
            return inputDict

    def buildNestedDict(self, inputDict, keyList, value):
        """
        Builds a nested dict
        """
        if len(list(inputDict.keys())) > 0:
            tempDict = self.buildOneNestedDict(dict(), keyList, value)
            return self.mergeDict(inputDict, tempDict)
        else:
            return self.buildOneNestedDict(inputDict, keyList, value)

    def readJsonFile(self, filename, returnFileAndDict=False):
        """
        Reads a json file and makes a dictionary
        """
        try:
            file = open(filename, "r")
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
        if ".qml" in qml:
            doc = parse(qml)
        else:
            try:
                doc = parseString(qml)
            except:
                doc = parseString(qml.encode("utf-8"))
        forbiddenList = doc.getElementsByTagName("edittypes")
        if len(forbiddenList) > 0:
            forbiddenNode = forbiddenList[0]
            qgisNode = doc.getElementsByTagName("qgis")[0]
            qgisNode.removeChild(forbiddenNode)
        return doc.toxml().replace('<?xml version="1.0" encoding="utf-8"?>', "")

    def parseMultiQml(self, qmlPath, lyrList):
        """
        dict in the form {'lyrName': {'attributeName':'domainTableName'}}
        """
        refDict = dict()
        for lyr in lyrList:
            try:
                qml = os.path.join(qmlPath, lyr + ".qml")
                doc = parse(qml)
                refDict[lyr] = dict()
                for node in doc.getElementsByTagName("edittype"):
                    if node.getAttribute("widgetv2type") in (
                        "ValueMap",
                        "ValueRelation",
                    ):
                        attrName = node.getAttribute("name")
                        refDict[lyr][attrName] = node.getElementsByTagName(
                            "widgetv2config"
                        )[0].getAttribute("Layer")
            except:
                pass
        return refDict

    def parseMultiFromDb(self, qmlRecordDict, lyrList):
        """
        dict in the form {'lyrName': {'attributeName':'domainTableName'}}
        """
        refDict = dict()
        for lyr in lyrList:
            try:
                qml = qmlRecordDict[lyr]
                try:
                    doc = parseString(qml)
                except:
                    doc = parseString(qml.encode("utf-8"))
                refDict[lyr] = dict()
                for node in doc.getElementsByTagName("edittype"):
                    if node.getAttribute("widgetv2type") == "ValueRelation":
                        attrName = node.getAttribute("name")
                        refDict[lyr][attrName] = node.getElementsByTagName(
                            "widgetv2config"
                        )[0].getAttribute("Layer")
            except:
                pass
        return refDict

    def getRecursiveInheritance(self, parent, resultList, inhDict):
        if parent not in resultList:
            resultList.append(parent)
        if parent in list(inhDict.keys()):
            for child in inhDict[parent]:
                self.getRecursiveInheritance(child, resultList, inhDict)

    def getRecursiveInheritanceTreeDict(self, parent, resultDict, inhDict):
        if parent not in list(resultDict.keys()):
            resultDict[parent] = dict()
        if parent in list(inhDict.keys()):
            for child in inhDict[parent]:
                self.getRecursiveInheritanceTreeDict(child, resultDict[parent], inhDict)

    def find_all_paths(self, graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
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
        for key in list(inputDict.keys()):
            if key not in itemList:
                itemList.append(key)
            self.getAllItemsInDict(inputDict[key], itemList)

    def createWidgetItem(self, parent, text, column=None):
        item = QTreeWidgetItem(parent)
        if isinstance(text, list) and column == None:
            for i in range(len(text)):
                item.setText(i, text[i])
            return item
        else:
            item.setText(column, text)
            return item

    def createTreeWidgetFromDict(self, parentNode, inputDict, treeWidget, column):
        for key in list(inputDict.keys()):
            item = self.createWidgetItem(parentNode, key, column)
            self.createTreeWidgetFromDict(item, inputDict[key], treeWidget, column)

    def getTreeBranchFromNode(self, startNode, inputDict):
        if "root" not in list(inputDict.keys()):
            graph = {"root": inputDict}
        else:
            graph = inputDict
        path = self.find_all_paths(graph, "root", startNode)[0]
        for node in path:
            graph = graph[node]
        return {startNode: graph}

    def getNodeLineage(self, node, inputDict):
        return self.find_all_paths(inputDict, "root", node)[0][1::]

    def instantiateJsonDict(self, jsonDict):
        if isinstance(jsonDict, dict):
            return jsonDict
        else:
            return json.loads(jsonDict)

    def deleteQml(self, tempQml):
        """
        Deletes a file from a given dir, if it's a QML file.
        """
        try:
            if tempQml[-4:].lower() == ".qml":
                try:
                    os.remove(tempQml)
                except:
                    pass
                return True
            else:
                return False
        except:
            return False

    def get_proxy_config(self):
        """Get proxy config from QSettings and builds proxy parameters
        :return: dictionary of transfer protocols mapped to addresses, also authentication if set in QSettings
        :rtype: (dict, requests.auth.HTTPProxyAuth) or (dict, None)
        """
        enabled, host, port, user, password = self.get_proxy_from_qsettings()

        proxy_dict = {}
        if enabled and host:
            port_str = str(port) if port else ""
            for protocol in ["http", "https", "ftp"]:
                proxy_dict[protocol] = "{}://{}:{}".format(protocol, host, port_str)

        auth = (
            requests.auth.HTTPProxyAuth(user, password)
            if enabled and user and password
            else None
        )

        return proxy_dict, auth

    @staticmethod
    def get_proxy_from_qsettings():
        """Gets the proxy configuration from QSettings
        :return: Proxy settings: flag specifying if proxy is enabled, host, port, user and password
        :rtype: tuple(str)
        """
        settings = QSettings()
        settings.beginGroup("proxy")
        enabled = (
            str(settings.value("proxyEnabled")).lower() == "true"
        )  # to be compatible with QGIS 2 and 3
        # proxy_type = settings.value("proxyType")
        host = settings.value("proxyHost")
        port = settings.value("proxyPort")
        user = settings.value("proxyUser")
        password = settings.value("proxyPassword")
        settings.endGroup()
        return enabled, host, port, user, password

    def qgisMapTools(self):
        """
        A list of QGIS map tools.
        :return: (dict) a map from map tool name to its action.
        """
        tools = dict()
        for m in dir(iface):
            if m.lower().startswith("action"):
                action = getattr(iface, m)()
                name = action.text().replace("&", "")
                tools[name] = action
        return tools

    def dsgToolsMapTools(self):
        """
        A list of DSGTools map tools.
        :return: (dict) a map from map tool name to its action.
        """
        tools = dict()
        for toolbar in iface.mainWindow().findChildren(QToolBar):
            if toolbar.objectName().lower() == "dsgtools":
                for o in toolbar.children():
                    if hasattr(o, "actions"):
                        for a in o.actions():
                            tools[a.text().replace("&", "")] = a
                break
        return tools

    def allQgisActions(self):
        """
        Reads all registered actions on QGIS GUI.
        :return: (dict) a map from action name to its action object.
        """
        sm = QgsGui.shortcutsManager()
        actions = dict()
        for item in sm.listAll():
            if isinstance(item, QAction):
                # remove the mnemonic shortcuts added by Qt (which might remove
                # actual characters)
                actions[item.text().replace("&", "")] = item
        return actions

    def fieldIsBool(self, field):
        """
        Checks if a field is filled with a bool type data.
        :param field: (QgsField) field to be checked.
        :return: (bool) if data is boolean.
        """
        return field.type() == QVariant.Bool

    def fieldIsFloat(self, field):
        """
        Checks if a field is filled with any float type data.
        :param field: (QgsField) field to be checked.
        :return: (bool) if data is float.
        """
        floatTypes = [QVariant.Double]
        return field.type() in floatTypes

    def fieldIsInt(self, field):
        """
        Checks if a field is filled with any int type data.
        :param field: (QgsField) field to be checked.
        :return: (bool) if data is a whole number.
        """
        intTypes = [QVariant.Int, QVariant.UInt, QVariant.LongLong, QVariant.ULongLong]
        return field.type() in intTypes

    def fieldIsNumeric(self, field):
        """
        Checks if a field is filled with any numeric type data.
        :param field: (QgsField) field to be checked.
        :return: (bool) if data is numeric.
        """
        return field.isNumeric()

    def fieldIsNullable(self, field):
        """
        Checks if a field may be left empty (does not have the "not null"
        constraint).
        :param field: (QgsField) field to be checked.
        :return: (bool) if field is nullable.
        """
        # constraints are 2^n, where n is its "index" on the list of existing
        # ones. Currently there are 3 constraints: not null, unique and
        # expression constraint, hence values are 1, 2, 4. 0 is the null
        # constraint and "constraints" are identified by the sum of them.
        return (int(field.constraints().constraints()) % 2) == 0


class MessageRaiser(QObject):
    """
    Raises messages to QGIS interface, global log and message boxes.
    """

    def raiseIfaceMessage(self, title, msg, level=None, duration=None):
        """
        Raises messages to the user on a message box on the main QGIS window.
        :param title: (str) text that will be displayed in bold, first on bar.
        :param msg: (str) message to be displayed.
        :param level: (int) level code (warning, critical, etc).
        :param duration: (int) time in seconds message will be displayed.
        """
        level = Qgis.Info if level is None else level
        duration = 3 if duration is None else duration
        iface.messageBar().pushMessage(title, msg, level=level, duration=duration)

    def logMessage(self, msg, level=None):
        """
        Display a log message on QGIS log.
        :param msg: (str) message to be displayed.
        :param level: (int) level code (warning, critical, etc).
        """
        level = Qgis.Info if level is None else level
        QgsMessageLog.logMessage(msg, "DSGTools Plugin", level)

    def confirmAction(self, parent, msg, title=None, showNo=True):
        """
        Raises a message box that asks for user confirmation.
        :param parent: (QWidget) any QWidget that will hold "possession" of mb.
        :param msg: (str) message requesting for confirmation to be shown.
        :param showNo: (bool) whether No button should be exposed.
        :return: (bool) whether action was confirmed.
        """
        title = title or self.tr("Confirm action")
        if showNo:
            return (
                QMessageBox.question(
                    parent, title, msg, QMessageBox.Yes | QMessageBox.No
                )
                == QMessageBox.Yes
            )
        else:
            return (
                QMessageBox.question(parent, title, msg, QMessageBox.Ok)
                == QMessageBox.Ok
            )


class ValidateImportedDataMethods:
    """
    Docstring.
    """

    def __init__(self) -> None:
        pass

    def validateQColor(self, colorToEvaluate):
        """
        This method receives a string and evaluate if its an valid QColor.
        """

        colorStrWithoutSpaces = re.sub(r"\s", "", str(colorToEvaluate))

        hexColor = re.search(r"^#[0-9a-fA-F]{3,6}$", colorStrWithoutSpaces)
        listColor = re.search(r"\d{1,3},\d{1,3},\d{1,3}", colorStrWithoutSpaces)

        if hexColor is not None:
            if QColor(hexColor[0]).isValid():
                return True
        elif listColor is not None:
            color = listColor[0].split(",")
            rgb = QColor(int(color[0]), int(color[1]), int(color[2]))
            if rgb.isValid():
                return True
        return False

    def validatePythonTypes(self, value, pythonType):
        if pythonType.lower() == "string":
            if isinstance(value, str):
                return True
        elif pythonType.lower() == "list":
            if isinstance(value, list):
                return True
        return False

    def validateLengthOfDataTypes(self, data, dataLength):

        if isinstance(data, (list, tuple, dict, str)):
            if len(data) == dataLength:
                return True
        return False

    def validateQgsExpressions(self, qgsExpression):

        exp = QgsExpression(qgsExpression)

        if exp.isValid():
            if exp.isField():
                return False
            return True
        return False

    def showLoadingMsg(self, lyrList=None, msgType=None):
        """
        Shows a message box to user if successfully loaded data or not.
        If not, shows to user a list of not loaded layers and allows user
        to choice between ignore and continue or cancel the importation.
        :param lyrList: (list) a list of not loaded layers.
        :param msgType: (str) type of message box - warning or information.
        :return: (signal) value returned from the clicked button.
        """
        msg = QMessageBox()
        msg.setWindowTitle("Invalid Rules Information")

        if lyrList and msgType == "invalid":
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Some rules has invalid itens!")
            msg.setInformativeText(
                "If you ignore, the invalid rules may not be loaded."
            )

            textLyrList = sorted(set(lyrList))
            formatedLyrList = ["{}" for item in textLyrList]
            msgString = ",".join(formatedLyrList).replace(",", "\n")
            formatedMsgString = (
                "The following rules are not valid:\n" + msgString.format(*textLyrList)
            )

            msg.setDetailedText(formatedMsgString)
            msg.setStandardButtons(QMessageBox.Ignore | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setText("Successfully loaded rules!")

        choice = msg.exec_()
        return choice
