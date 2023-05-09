# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-30
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

# 5 Imports

from builtins import str
from builtins import range
from qgis.PyQt.QtCore import QSettings, pyqtSignal, QObject

# DsgTools imports
from ..DbFactory.dbFactory import DbFactory
from ..DbFactory.abstractDb import AbstractDb
from ....gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget


class DbCreator(QObject):
    def __init__(self, createParam, parentWidget=None):
        super(DbCreator, self).__init__()
        self.dbFactory = DbFactory()
        self.parentWidget = parentWidget
        if isinstance(createParam, str):
            self.outputDir = createParam
        if isinstance(createParam, AbstractDb):
            self.abstractDb = createParam
        self.scaleMIDict = {
            1: "100k",
            2: "50k",
            3: "25k",
            4: "10k",
            5: "5k",
            6: "2k",
            7: "1k",
        }

    def getType(self):
        # Abstract method.
        return None

    def createDb(self, dbName, srid, paramDict=dict(), parentWidget=None):
        # Abstract method.
        pass

    def buildDatabaseName(self, dbBaseName, prefix=None, sufix=None):
        attrNameList = []
        if prefix:
            attrNameList.append(prefix)
        attrNameList.append(dbBaseName)
        if sufix:
            attrNameList.append(sufix)
        return "_".join(attrNameList)

    def buildAutoIncrementingDbNameList(
        self, dbInitialBaseName, numberOfDatabases, prefix=None, sufix=None
    ):
        dbNameList = []
        for i in range(numberOfDatabases):
            dbBaseName = dbInitialBaseName + str(i + 1)
            dbNameList.append(self.buildDatabaseName(dbBaseName, prefix, sufix))
        return dbNameList

    def batchCreateDb(self, dbNameList, srid, paramDict=dict()):
        outputDbDict = dict()
        errorDict = dict()
        templateDb = None
        if self.parentWidget:
            progress = ProgressWidget(
                1,
                len(dbNameList),
                self.tr("Creating databases... "),
                parent=self.parentWidget,
            )
            progress.initBar()
        for dbName in dbNameList:
            try:
                if not templateDb:
                    newDb = self.createDb(
                        dbName,
                        srid,
                        paramDict=paramDict,
                        parentWidget=self.parentWidget,
                    )
                    templateDb = dbName
                else:
                    paramDict["templateDb"] = templateDb
                    newDb = self.createDb(
                        dbName, srid, paramDict, parentWidget=self.parentWidget
                    )
                outputDbDict[dbName] = newDb
            except Exception as e:
                if dbName not in list(errorDict.keys()):
                    errorDict[dbName] = ":".join(e.args)
                else:
                    errorDict[dbName] += "\n" + ":".join(e.args)
            if self.parentWidget:
                progress.step()
        return outputDbDict, errorDict

    def createDbWithAutoIncrementingName(
        self,
        dbInitialBaseName,
        srid,
        numberOfDatabases,
        prefix=None,
        sufix=None,
        paramDict=dict(),
    ):
        dbNameList = self.buildAutoIncrementingDbNameList(
            dbInitialBaseName, numberOfDatabases, prefix, sufix
        )
        return self.batchCreateDb(dbNameList, srid, paramDict)

    def createDbFromMIList(
        self, miList, srid, prefix=None, sufix=None, createFrame=False, paramDict=dict()
    ):
        outputDbDict = dict()
        errorDict = dict()
        templateDb = None
        if self.parentWidget:
            progress = ProgressWidget(
                1,
                2 * len(miList) + 1,
                self.tr("Creating databases... "),
                parent=self.parentWidget,
            )
            progress.initBar()
            progress.step()
        for mi in miList:
            dbName = self.buildDatabaseName(mi, prefix, sufix)
            try:
                if not templateDb:
                    newDb = self.createDb(
                        dbName, srid, paramDict, parentWidget=self.parentWidget
                    )
                    templateDb = dbName
                else:
                    paramDict["templateDb"] = templateDb
                    newDb = self.createDb(
                        dbName, srid, paramDict, parentWidget=self.parentWidget
                    )
                outputDbDict[dbName] = newDb
            except Exception as e:
                if dbName not in list(errorDict.keys()):
                    errorDict[dbName] = ":".join(e.args)
                else:
                    errorDict[dbName] += "\n" + ":".join(e.args)
            if self.parentWidget:
                progress.step()
        if createFrame:
            for dbName in list(outputDbDict.keys()):
                try:
                    scale = self.scaleMIDict[len(mi.split("-"))]
                    mi = [i for i in miList if i in dbName][0]
                    outputDbDict[dbName].createFrame(
                        "mi", scale, mi, paramDict=paramDict
                    )
                except Exception as e:
                    if dbName not in list(errorDict.keys()):
                        errorDict[dbName] = ":".join(e.args)
                    else:
                        errorDict[dbName] += "\n" + ":".join(e.args)
                if self.parentWidget:
                    progress.step()
        return outputDbDict, errorDict
