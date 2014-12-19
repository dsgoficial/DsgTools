# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                               
                             -------------------
        begin                : 2014-09-19
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Felipe Ferrari
        email                : ferrari@dsg.eb.mil.br
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
from qgis.core import QgsGeometry,QgsCoordinateReferenceSystem,QgsDataSourceURI,QgsVectorLayer,QgsMapLayerRegistry,QgsMessageLog,QgsCoordinateTransform

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtSql import QSqlQueryModel, QSqlTableModel,QSqlDatabase,QSqlQuery

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Factories', 'SqlFactory'))
from sqlGeneratorFactory import SqlGeneratorFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_create_inom_dialog_base.ui'))

from map_index import UtmGrid

class CreateInomDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(CreateInomDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        #Sql factory generator
        self.isSpatialite = True
        self.tabWidget.setCurrentIndex(0)
        self.factory = SqlGeneratorFactory()
        self.gen = self.factory.createSqlGenerator(self.isSpatialite)

        QObject.connect(self.tabWidget, SIGNAL(("currentChanged(int)")), self.restoreInitialState)
        QObject.connect(self.pushButtonOpenFile, SIGNAL(("clicked()")), self.loadDatabase)
        
        self.restoreInitialState()

        self.db = None
        #populating the postgis combobox
        self.populatePostGISConnectionsCombo()
        
        self.map_index = UtmGrid()
        
        self.disableAll()
        

    def __del__(self):
        self.closeDatabase()

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        frame = self.map_index.getQgsPolygonFrame(self.inomLineEdit.text())
        reprojected = self.reprojectFrame(frame)
        ewkt = '\''+reprojected.exportToWkt()+'\','+str(self.epsg)
        sql = self.gen.insertFrameIntoTable(ewkt)
        print sql
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            QgsMessageLog.logMessage("Problem creating the frame:"+query.lastError().text(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)

    @pyqtSlot(int)
    def on_comboBoxPostgis_currentIndexChanged(self):
        if self.comboBoxPostgis.currentIndex() > 0:
            self.loadDatabase()
            
    def reprojectFrame(self, poly):
        print self.crs.geographicCRSAuthId(),self.epsg
        crsSrc = QgsCoordinateReferenceSystem(self.crs.geographicCRSAuthId())
        coordinateTransformer = QgsCoordinateTransform(crsSrc, self.crs)
        polyline = poly.asPolygon()[0]
        newPolyline = []
        for point in polyline:
            newPolyline.append(coordinateTransformer.transform(point))
        qgsPolygon = QgsGeometry.fromPolygon([newPolyline])
        return qgsPolygon
           
    def closeDatabase(self):
        if self.db:
            self.db.close()
            self.db = None
            
    def restoreInitialState(self):
        self.filename = ""
        self.dbLoaded = False
        self.epsg = 0
        self.crs = None
        self.postGISCrsEdit.setText('')
        self.postGISCrsEdit.setReadOnly(True)
        self.spatialiteCrsEdit.setText('')
        self.spatialiteCrsEdit.setReadOnly(True)

        if self.tabWidget.currentIndex() == 0:
            self.isSpatialite = True
            self.frameLayer = 'aux_aux_moldura_a'
        else:
            self.isSpatialite = False
            self.frameLayer = 'aux.aux_moldura_a'

        #getting the sql generator according to the database type
        self.gen = self.factory.createSqlGenerator(self.isSpatialite)
        self.comboBoxPostgis.setCurrentIndex(0)

    def setCRS(self):
        try:
            self.epsg = self.findEPSG()
            print self.epsg
            if self.epsg == -1:
                self.bar.pushMessage("", "Coordinate Reference System not set or invalid!", level=QgsMessageBar.WARNING)
            else:
                self.crs = QgsCoordinateReferenceSystem(self.epsg, QgsCoordinateReferenceSystem.EpsgCrsId)
                if self.isSpatialite:
                    self.spatialiteCrsEdit.setText(self.crs.description())
                    self.spatialiteCrsEdit.setReadOnly(True)
                else:
                    self.postGISCrsEdit.setText(self.crs.description())
                    self.postGISCrsEdit.setReadOnly(True)
        except:
            pass
        
    def loadDatabase(self):
        self.closeDatabase()
        if self.isSpatialite:
            fd = QtGui.QFileDialog()
            self.filename = fd.getOpenFileName(filter='*.sqlite')
            if self.filename:
                self.spatialiteFileEdit.setText(self.filename)
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
            self.setCRS()
            
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
        

    def disableAll(self):
        self.mirLineEdit.setEnabled(False)
        self.miLineEdit.setEnabled(False)
        self.inomLineEdit.setEnabled(False)
        
    @pyqtSlot(bool)
    def on_mirRadioButton_toggled(self, toggled):
        if toggled:
            self.mirLineEdit.setEnabled(True)
        else:
            self.mirLineEdit.setEnabled(False)
            
    @pyqtSlot(bool)
    def on_miRadioButton_toggled(self, toggled):
        if toggled:
            self.miLineEdit.setEnabled(True)
        else:
            self.miLineEdit.setEnabled(False)
            
    @pyqtSlot(bool)
    def on_inomRadioButton_toggled(self, toggled):
        if toggled:
            self.inomLineEdit.setEnabled(True)
        else:
            self.inomLineEdit.setEnabled(False)