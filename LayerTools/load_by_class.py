# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LoadByClass
                                 A QGIS plugin
 Load database classes.
                             -------------------
        begin                : 2014-06-17
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba@dsg.eb.mil.br
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
import load_by_class_base
import sqlite3, os

from qgis.core import QgsCoordinateReferenceSystem,QgsDataSourceURI,QgsVectorLayer,QgsMapLayerRegistry
from qgis.gui import QgsGenericProjectionSelector,QgsMessageBar
import qgis as qgis

from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import QFileInfo,QSettings

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Factories', 'SqlFactory'))
from sqlGeneratorFactory import SqlGeneratorFactory

from PyQt4.QtSql import QSqlQueryModel, QSqlTableModel,QSqlDatabase,QSqlQuery

class LoadByClass(QtGui.QDialog, load_by_class_base.Ui_LoadByClass):
    def __init__(self, parent=None):
        """Constructor."""
        super(LoadByClass, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.filename = ""
        self.dbLoaded = False
        self.crsSet = False
        self.onlyWithElementsBool = False
        self.epsg = 0
        self.crs = ''
        self.classes = []
        self.selectedClasses = []

        #Sql factory generator
        self.isSpatialite = True

        self.setupUi(self)
        self.tabWidgetLoadByClass.setCurrentIndex(0)
        self.factory = SqlGeneratorFactory()
        self.gen = self.factory.createSqlGenerator(self.isSpatialite)

        #qmlPath will be set as /qml_qgis/qgis_22/edgv_213/, but in a further version, there will be an option to detect from db
        version = qgis.core.QGis.QGIS_VERSION_INT
        currentPath = os.path.dirname(__file__)
        if version >= 20600:
            self.qmlPath = os.path.join(currentPath, 'qml_qgis', 'qgis_26', 'edgv_213')
        else:
            self.qmlPath = os.path.join(currentPath, 'qml_qgis', 'qgis_22', 'edgv_213')

        self.bar = QgsMessageBar()
        self.setLayout(QtGui.QGridLayout(self))
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.bar.setSizePolicy(sizePolicy)
        self.layout().addWidget(self.bar, 0,0,1,1)

        #Objects Connections
        QtCore.QObject.connect(self.pushButtonOpenFile, QtCore.SIGNAL(("clicked()")), self.loadDatabase)
#         QtCore.QObject.connect(self.comboBoxPostgis, QtCore.SIGNAL(("currentIndexChanged(int)")), self.loadDatabase)
#         QtCore.QObject.connect(self.fileLineEditLoadByClass, QtCore.SIGNAL(("textChanged(QString)")), self.listClassesFromDatabase)
        QtCore.QObject.connect(self.pushButtonCancelLoadByClass, QtCore.SIGNAL(("clicked()")), self.cancel)
        QtCore.QObject.connect(self.checkBoxSelectAllLoadByClass, QtCore.SIGNAL(("stateChanged(int)")), self.selectAll)
        QtCore.QObject.connect(self.pushButtonOkLoadByClass, QtCore.SIGNAL(("clicked()")), self.okSelected)
        QtCore.QObject.connect(self.tabWidgetLoadByClass,QtCore.SIGNAL(("currentChanged(int)")), self.restoreInitialState)

        self.db = None
        #populating the postgis combobox
        self.populatePostGISConnectionsCombo()
        
    def __del__(self):
        self.closeDatabase()
        
    def closeDatabase(self):
        if self.db:
            self.db.close()
            self.db = None

    def restoreInitialState(self):
        self.filename = ""
        self.dbLoaded = False
        self.crsSet = False
        self.onlyWithElementsBool = False
        self.epsg = 0
        self.crs = ''
        self.classes = []
        self.selectedClasses = []
        self.fileLineEditLoadByClass.setText(self.filename)
        self.crsLineEditLoadByClassSpatialite.setText(self.crs)
        self.crsLineEditLoadByClassSpatialite.setReadOnly(False)

        tam = self.listWidgetClassesLoadByClass.__len__()
        for i in range(tam+1,1,-1):
            item = self.listWidgetClassesLoadByClass.takeItem(i-2)

        self.checkBoxSelectAllLoadByClass.setCheckState(0)
        #Setting the database type
        if self.tabWidgetLoadByClass.currentIndex() == 0:
            self.isSpatialite = True
        else:
            self.isSpatialite = False
        #getting the sql generator according to the database type
        self.gen = self.factory.createSqlGenerator(self.isSpatialite)
        self.comboBoxPostgis.setCurrentIndex(0)

    def updateBDField(self):
        if self.dbLoaded == True:
            self.fileLineEditLoadByClass.setText(self.filename)
        else:
            self.filename = ""
            self.fileLineEditLoadByClass.setText(self.filename)

    def listClassesFromDatabase(self):
        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        while query.next():
            tableName = query.value(0)
            if tableName.split("_")[-1] == "p" or tableName.split("_")[-1] == "l" \
                or tableName.split("_")[-1] == "a": 
                item = QtGui.QListWidgetItem(tableName)
                self.listWidgetClassesLoadByClass.addItem(item)
        self.listWidgetClassesLoadByClass.sortItems()
        self.setCRS()

    def setCRS(self):
        try:
            self.epsg = self.findEPSG()
            print self.epsg
            if self.epsg == -1:
                self.bar.pushMessage("", "Coordinate Reference System not set or invalid!", level=QgsMessageBar.WARNING)
            else:
                self.crs = QgsCoordinateReferenceSystem(self.epsg, QgsCoordinateReferenceSystem.EpsgCrsId)
                if self.isSpatialite:
                    self.crsLineEditLoadByClassSpatialite.setText(self.crs.description())
                    self.crsLineEditLoadByClassSpatialite.setReadOnly(True)
                else:
                    self.coordSysLineEditCarregaClassePostgis.setText(self.crs.description())
                    self.coordSysLineEditCarregaClassePostgis.setReadOnly(True)
        except:
            pass        

    def on_comboBoxPostgis_currentIndexChanged(self):
        if self.comboBoxPostgis.currentIndex() > 0:
            self.loadDatabase()

    def loadDatabase(self):
        if self.isSpatialite:
            fd = QtGui.QFileDialog()
            self.filename = fd.getOpenFileName(filter='*.sqlite')
            if self.filename:
                self.fileLineEditLoadByClass.setText(self.filename)
                self.db = QSqlDatabase("QSQLITE")
                self.db.setDatabaseName(self.filename)
        else:
            self.db = QSqlDatabase("QPSQL")
            (database, host, port, user, password) = self.getPostGISConnectionParameters(self.comboBoxPostgis.currentText())
            self.db.setDatabaseName(database)
            self.db.setHostName(host)
            self.db.setPort(int(port))
            self.db.setUserName(user)
            self.db.setPassword(password)
        if not self.db.open():
            print self.db.lastError().text()
        else:
            self.dbLoaded = True
            self.listClassesFromDatabase()

    def getPostGISConnectionParameters(self, name):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/connections/'+name)
        database = settings.value('database')
        host = settings.value('host')
        port = settings.value('port')
        user = settings.value('username')
        password = settings.value('password')
        settings.endGroup()
        return (database, host, port, user, password)

    def getPostGISConnections(self):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/connections')
        currentConnections = settings.childGroups()
        settings.endGroup()
        return currentConnections

    def populatePostGISConnectionsCombo(self):
        self.comboBoxPostgis.clear()
        self.comboBoxPostgis.addItem("Select Database")
        self.comboBoxPostgis.addItems(self.getPostGISConnections())

    def findEPSG(self):
        sql = self.gen.getSrid()
        query = QSqlQuery(sql, self.db)
        srids = []
        while query.next():
            srids.append(query.value(0))
        return srids[0]

    def cancel(self):
        self.restoreInitialState()
        self.close()

    def selectAll(self):
        if self.checkBoxSelectAllLoadByClass.isChecked():
            tam = self.listWidgetClassesLoadByClass.__len__()
            for i in range(tam+1):
                item = self.listWidgetClassesLoadByClass.item(i-1)
                self.listWidgetClassesLoadByClass.setItemSelected(item,2)

        else:
            tam = self.listWidgetClassesLoadByClass.__len__()
            for i in range(tam+1):
                item = self.listWidgetClassesLoadByClass.item(i-1)
                self.listWidgetClassesLoadByClass.setItemSelected(item,0)

    def getSelectedItems(self):
        lista = self.listWidgetClassesLoadByClass.selectedItems()
        self.selectedClasses = []
        tam = len(lista)
        for i in range(tam):
            self.selectedClasses.append(lista[i].text())
        self.selectedClasses.sort()
        #self.classes

    def okSelected(self):
        if isSpatialite:
            loadSpatialiteLayers()
        else:
            pass

    def loadSpatialiteLayers(self):
        f = self.filename
        xmlfilepath = self.qmlPath
        coordSys = self.crs
        self.getSelectedItems()
        uri = QgsDataSourceURI()
        uri.setDatabase(f)
        schema = ''
        geom_column = 'GEOMETRY'
        if len(self.selectedClasses)>0:
            try:
                for i in self.selectedClasses:
                    self.loadEDGVLayer(uri, i, schema, geom_column, coordSys, xmlfilepath)
                self.restoreInitialState()
                self.close()
            except:
                self.bar.pushMessage("Error!", "Parameters not properly set!", level=QgsMessageBar.CRITICAL)
        else:
            self.bar.pushMessage("Error!", "Parameters not properly set!", level=QgsMessageBar.CRITICAL)

    def loadEDGVLayer(self,uri, nome_camada,schema,geom_column, coordSys,xmlfilepath):
        uri.setDataSource(schema, nome_camada, geom_column)
        display_name = nome_camada
        vlayer = QgsVectorLayer(uri.uri(), display_name, 'spatialite')
        vlayer.setCrs(coordSys)
        QgsMapLayerRegistry.instance().addMapLayer(vlayer) #added due to api changes
        vlayer.loadNamedStyle(xmlfilepath+nome_camada.replace('\r','')+'.qml',False)
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)
