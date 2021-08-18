# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-04-27
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
from qgis.PyQt.QtWidgets import QMessageBox, QApplication
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtCore import QSettings, pyqtSignal, pyqtSlot, QObject, Qt
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.Qt import QWidget, QObject

from qgis.core import QgsMapLayer, Qgis, QgsDataSourceUri, QgsMessageLog, QgsVectorLayer, QgsProcessingContext

from .....core.Factories.DbFactory.dbFactory import DbFactory
from .....core.Factories.LayerLoaderFactory.layerLoaderFactory import LayerLoaderFactory
from .....core.Utils.utils import Utils
from .....gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget
from DsgTools.core.dsgEnums import DsgEnums
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'styleManagerTool.ui'))

class StyleManagerTool(QWidget, FORM_CLASS): 
    def __init__(self, iface, parent = None):
        """
        Constructor
        """
        super(StyleManagerTool, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.splitter.hide()
        self.refreshDb()
        self.dbFactory = DbFactory()
        # self.applyPushButton.setEnabled(False)
        self.utils = Utils()
        self.algRunner = AlgRunner()
        
    @pyqtSlot(bool)
    def on_layerPushButton_toggled(self, toggled):
        """
        Shows/Hides the tool bar
        """
        if toggled:
            self.refreshDb()
            self.splitter.show()
        else:
            self.splitter.hide()
    
    @pyqtSlot(bool, name = 'on_refreshPushButton_clicked')
    def refreshDb(self):
        self.dbComboBox.clear()
        self.dbComboBox.addItem(self.tr('Select Database'))
        #populate database list
        for dbName in self.getDatabaseList():
            self.dbComboBox.addItem(dbName)

    @pyqtSlot(int, name = 'on_styleComboBox_currentIndexChanged')
    def enableApply(self):
        dbIdx = self.dbComboBox.currentIndex()
        stylesIdx = self.styleComboBox.currentIndex()
        if dbIdx > 0 and stylesIdx > 0:
            self.applyPushButton.setEnabled(True)
        else:
            self.applyPushButton.setEnabled(False)

    @pyqtSlot(bool)
    def on_applyPushButton_clicked(self):
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            dbName = self.dbComboBox.currentText()
            styleName = self.styleComboBox.currentText()
            lyrList = self.getLayers(dbName)
            abstractDb = self.getAbstractDb(dbName)
            dbVersion = abstractDb.getDatabaseVersion()
            stylesDict = abstractDb.getStyleDict(dbVersion)
            selectedStyle = stylesDict[styleName]
            if 'db:' in selectedStyle:
                self.algRunner.runApplStylesFromDatabaseToLayers(
                    inputList=lyrList,
                    context=QgsProcessingContext(),
                    styleName=selectedStyle.split(':')[-1]
                )
            else:
                stylePath = os.path.join(
                    abstractDb.getStyleDirectory(dbVersion),
                    selectedStyle
                )
                self.algRunner.runMatchAndApplyQmlStylesToLayer(
                    inputList=lyrList,
                    qmlFolder=stylePath,
                    context=QgsProcessingContext()
                )
            # localProgress = ProgressWidget(1, len(lyrList) - 1, self.tr('Loading style {0}').format(styleName), parent=self.iface.mapCanvas())
            # for lyr in lyrList:
            #     try:
            #         uri = QgsDataSourceUri(lyr.dataProvider().dataSourceUri())
            #         fullPath = self.getStyle(abstractDb, selectedStyle, lyr.name())
            #         if fullPath:
            #             lyr.loadNamedStyle(fullPath, True)
            #             # remove qml temporary file
            #             self.utils.deleteQml(fullPath)
            #             # clear fullPath variable
            #             del fullPath
            #     except:
            #         pass
            #     localProgress.step()
            # self.iface.mapCanvas().refreshAllLayers()
            QApplication.restoreOverrideCursor()
        except Exception as e:
            QgsMessageLog.logMessage(self.tr('Error setting style ') + styleName + ': ' +':'.join(e.args), "DSGTools Plugin", Qgis.Critical)
            QApplication.restoreOverrideCursor()

    
    def getLayers(self, dbName):
        lyrList = []
        for lyr in self.iface.mapCanvas().layers():
            if isinstance(lyr, QgsVectorLayer):
                candidateUri = QgsDataSourceUri(lyr.dataProvider().dataSourceUri())
                if (candidateUri.database() == dbName and lyr.providerType() in ['postgres', 'spatialite']) \
                    or (os.path.splitext(os.path.basename(candidateUri.uri().split('|')[0]))[0] == dbName and lyr.providerType() == 'ogr'):
                    lyrList.append(lyr)
        return lyrList
    
    def getDatabaseList(self):
        # dbList = list()
        dbSet = set()
        for lyr in self.iface.mapCanvas().layers():
            if isinstance(lyr, QgsVectorLayer):
                candidateUri = QgsDataSourceUri(lyr.dataProvider().dataSourceUri())
                dbName = candidateUri.database()
                # if dbName not in dbList and lyr.providerType() in ['postgres', 'spatialite']:
                if lyr.providerType() in ['postgres', 'spatialite']:
                    dbSet.add(dbName)
                elif lyr.providerType() == 'ogr':
                    dbName = os.path.splitext(os.path.basename(lyr.dataProvider().dataSourceUri().split('|')[0]))[0]
                    # if db not in dbList:
                    dbSet.add(dbName)
        return dbSet
    
    def loadStylesCombo(self, abstractDb):
        dbVersion = abstractDb.getDatabaseVersion()
        styleDict = abstractDb.getStyleDict(dbVersion)
        self.styleComboBox.clear()
        styleList = list(styleDict.keys())
        numberOfStyles = len(styleList)
        if numberOfStyles > 0:
            self.styleComboBox.addItem(self.tr('Select Style'))
            for i in range(numberOfStyles):
                self.styleComboBox.addItem(styleList[i])
        else:
            self.styleComboBox.addItem(self.tr('No available styles'))
    
    def getParametersFromLyr(self, dbName):
        for lyr in self.iface.mapCanvas().layers():
          if isinstance(lyr, QgsVectorLayer):
            candidateUri = QgsDataSourceUri(lyr.dataProvider().dataSourceUri())
            if candidateUri.database() == dbName or \
                    os.path.splitext(os.path.basename(candidateUri.uri().split('|')[0]))[0] == dbName:
                currLyr = lyr
                break
        dbParameters = dict()
        if currLyr.providerType() == 'postgres':
            dbParameters['host'] = candidateUri.host()
            dbParameters['port'] = candidateUri.port()
            dbParameters['user'] = candidateUri.username()
            dbParameters['password'] = candidateUri.password()
            return dbParameters, DsgEnums.DriverPostGIS
        elif currLyr.providerType() == 'spatialite':
            dbParameters['dbPath'] = candidateUri.database()
            return dbParameters, DsgEnums.DriverSpatiaLite
        elif currLyr.providerType() == 'ogr':
            # geopackage provider type is ogr
            dbParameters['dbPath'] = candidateUri.database()
            return dbParameters, DsgEnums.DriverGeopackage
        else:
            raise Exception(self.tr('Feature only implemented for PostGIS and Spatialite'))
    
    def getAbstractDb(self, dbName):
        dbParameters, driverName = self.getParametersFromLyr(dbName)
        abstractDb = self.dbFactory.createDbFactory(driverName)
        if 'host' in list(dbParameters.keys()):
            abstractDb.connectDatabaseWithParameters(dbParameters['host'], dbParameters['port'], dbName, dbParameters['user'], dbParameters['password'])
        else:
            abstractDb.connectDatabase(dbParameters['dbPath'])
        return abstractDb

    @pyqtSlot(int)
    def on_dbComboBox_currentIndexChanged(self, idx):
        self.enableApply()
        if self.sender().objectName() == 'dbComboBox':
            if idx <= 0:
                self.styleComboBox.clear()
                self.styleComboBox.addItem(self.tr('Select Style'))
                self.styleComboBox.setEnabled(False)
            elif idx > 0:
                self.styleComboBox.setEnabled(True)
                dbName = self.dbComboBox.currentText()
                abstractDb = self.getAbstractDb(dbName)
                self.loadStylesCombo(abstractDb)
