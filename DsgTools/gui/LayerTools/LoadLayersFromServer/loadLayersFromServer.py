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
from builtins import range
import os
from os.path import expanduser

from qgis.core import QgsMessageLog, Qgis

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt, QSettings
from qgis.PyQt.QtWidgets import (
    QListWidgetItem,
    QMessageBox,
    QMenu,
    QApplication,
    QFileDialog,
    QProgressBar,
)
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery

# DSGTools imports
from ....core.Utils.utils import Utils
from ....core.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from ....core.Factories.DbFactory.dbFactory import DbFactory
from ....core.Factories.LayerLoaderFactory.layerLoaderFactory import LayerLoaderFactory
from ...CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "loadLayersFromServer.ui")
)


class LoadLayersFromServer(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.iface = iface
        self.utils = Utils()
        self.setupUi(self)
        self.layerFactory = LayerLoaderFactory()
        self.customServerConnectionWidget.postgisCustomSelector.setTitle(
            self.tr("Select Databases")
        )
        self.customServerConnectionWidget.spatialiteCustomSelector.setTitle(
            self.tr("Selected Spatialites")
        )
        # self.customServerConnectionWidget.gpkgCustomSelector.setTitle(self.tr('Selected Geopackages'))
        self.layersCustomSelector.setTitle(self.tr("Select layers to be loaded"))
        self.customServerConnectionWidget.dbDictChanged.connect(
            self.updateLayersFromDbs
        )
        self.customServerConnectionWidget.resetAll.connect(self.resetInterface)
        self.customServerConnectionWidget.styleChanged.connect(self.populateStyleCombo)
        self.headerList = [
            self.tr("Category"),
            self.tr("Layer Name"),
            self.tr("Geometry\nColumn"),
            self.tr("Geometry\nType"),
            self.tr("Layer\nType"),
        ]
        self.layersCustomSelector.setHeaders(self.headerList)
        self.customServerConnectionWidget.serverConnectionTab.currentChanged.connect(
            self.layersCustomSelector.setInitialState
        )
        self.lyrDict = dict()

    def resetInterface(self):
        """
        Sets the initial state again
        """
        self.layersCustomSelector.clearAll()
        self.styleComboBox.clear()
        # TODO: refresh optional parameters
        self.checkBoxOnlyWithElements.setCheckState(0)

    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Closes the dialog
        """
        self.close()

    def updateLayersFromDbs(self, type, dbList, showViews=False):
        """ """
        errorDict = dict()
        if type == "added":
            progress = ProgressWidget(
                1, len(dbList), self.tr("Reading selected databases... "), parent=self
            )
            progress.initBar()
            for dbName in dbList:
                try:
                    QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                    geomList = self.customServerConnectionWidget.selectedDbsDict[
                        dbName
                    ].getGeomColumnTupleList(showViews=showViews)
                    for tableSchema, tableName, geom, geomType, tableType in geomList:
                        if self.tr("Unknown model") in dbName:
                            lyrName = tableName
                            cat = tableSchema
                        else:
                            lyrName = "_".join(tableName.split("_")[1::])
                            if lyrName == "":
                                lyrName = tableName
                                cat = "layers"
                            else:
                                cat = tableName.split("_")[0]
                        key = ",".join([cat, lyrName, geom, geomType, tableType])
                        if key not in list(self.lyrDict.keys()):
                            self.lyrDict[key] = dict()
                        self.lyrDict[key][dbName] = {
                            "tableSchema": tableSchema,
                            "tableName": tableName,
                            "geom": geom,
                            "geomType": geomType,
                            "tableType": tableType,
                            "lyrName": lyrName,
                            "cat": cat,
                        }
                except Exception as e:
                    errorDict[dbName] = ":".join(e.args)
                    QApplication.restoreOverrideCursor()
                progress.step()
                QApplication.restoreOverrideCursor()

        elif type == "removed":
            for key in list(self.lyrDict.keys()):
                for db in list(self.lyrDict[key].keys()):
                    if db in dbList:
                        self.lyrDict[key].pop(db)
                if self.lyrDict[key] == dict():
                    self.lyrDict.pop(key)
        interfaceDictList = []
        for key in list(self.lyrDict.keys()):
            cat, lyrName, geom, geomType, tableType = key.split(",")
            interfaceDictList.append(
                {
                    self.tr("Category"): cat,
                    self.tr("Layer Name"): lyrName,
                    self.tr("Geometry\nColumn"): geom,
                    self.tr("Geometry\nType"): geomType,
                    self.tr("Layer\nType"): tableType,
                }
            )
        self.layersCustomSelector.setInitialState(interfaceDictList, unique=True)

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Loads the selected classes/categories
        """
        # 1- filter classes if categories is checked and build list.
        selectedKeys = self.layersCustomSelector.getSelectedNodes()
        if len(selectedKeys) == 0:
            QMessageBox.information(
                self,
                self.tr("Error!"),
                self.tr("Select at least one layer to be loaded!"),
            )
            return
        # 2- get parameters
        withElements = self.checkBoxOnlyWithElements.isChecked()
        selectedStyle = (
            None
            if self.styleComboBox.currentIndex() == 0
            else self.customServerConnectionWidget.stylesDict[
                self.styleComboBox.currentText()
            ]
        )
        uniqueLoad = self.uniqueLoadCheckBox.isChecked()
        # 3- Build factory dict
        dbList = list(self.customServerConnectionWidget.selectedDbsDict.keys())
        factoryDict = {
            dbName: self.layerFactory.makeLoader(
                iface=self.iface,
                abstractDb=self.customServerConnectionWidget.selectedDbsDict[dbName],
            )
            for dbName in dbList
        }
        # 4- load for each db
        exceptionDict = dict()
        progress = ProgressWidget(
            1,
            len(dbList),
            self.tr("Loading layers from selected databases... "),
            parent=self,
        )
        for dbName in factoryDict:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            try:
                selectedClasses = [
                    self.lyrDict[key][dbName]
                    for key in selectedKeys
                    if key in self.lyrDict and dbName in self.lyrDict[key]
                ]
                factoryDict[dbName].load(
                    selectedClasses,
                    uniqueLoad=uniqueLoad,
                    onlyWithElements=withElements,
                    stylePath=selectedStyle,
                    useInheritance=False,
                    customForm=False,
                    parent=self,
                )
                progress.step()
            except Exception as e:
                exceptionDict[dbName] = ":".join(e.args)
                self.iface.mapCanvas().freeze(False)  # done to speedup things
                QApplication.restoreOverrideCursor()
                progress.step()
            QApplication.restoreOverrideCursor()
            if factoryDict[dbName].errorLog != "":
                if dbName in list(exceptionDict.keys()):
                    exceptionDict[dbName] += "\n" + factoryDict[dbName].errorLog
                else:
                    exceptionDict[dbName] = factoryDict[dbName].errorLog
        QApplication.restoreOverrideCursor()
        self.logInternalError(exceptionDict)
        self.close()
    def logInternalError(self, exceptionDict):
        """
        Logs internal errors during the load process in QGIS' log
        """
        msg = ""
        errorDbList = list(exceptionDict.keys())
        if len(errorDbList) == 0:
            return msg
        msg += self.tr("\nDatabases with error:")
        msg += ", ".join(errorDbList)
        msg += self.tr("\nError messages for each database were output in qgis log.")
        for errorDb in errorDbList:
            QgsMessageLog.logMessage(
                self.tr("Error for database ")
                + errorDb
                + ": "
                + exceptionDict[errorDb],
                "DSGTools Plugin",
                Qgis.Critical,
            )
        return msg

    def populateStyleCombo(self, styleDict):
        """
        Loads styles saved in the database
        """
        self.styleComboBox.clear()
        if len(styleDict.keys()) == 0:
            self.styleComboBox.addItem(self.tr("No available styles"))
            return
        self.styleComboBox.addItem(self.tr("Select Style"))
        for i, style in enumerate(styleDict.keys()):
            self.styleComboBox.addItem(style)
