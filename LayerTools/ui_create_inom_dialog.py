# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools

                             -------------------
        begin                : 2014-09-19
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Felipe Ferrari
        email                : ferrari@dsg.eb.mil.br
         mod history          : 2014-12-17 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
         mod history          : 2014-03-31 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from qgis.core import *
from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtSql import QSqlDatabase,QSqlQuery
from PyQt4.QtGui import QMessageBox

import os
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_create_inom_dialog_base.ui'))

from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.LayerTools.map_index import UtmGrid
from DsgTools.Utils.utils import Utils

class CreateInomDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(CreateInomDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface
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

        self.setValidCharacters()

        self.setMask()

    def __del__(self):
        self.closeDatabase()

    @pyqtSlot()
    def on_okButton_clicked(self):
        if not self.dbLoaded:
            QMessageBox.warning(self, self.tr("Warning!"), self.tr('Please, select a database first.'))
            return

        if not self.validateMI():
            QMessageBox.warning(self, self.tr("Warning!"), self.tr('Map name index not valid!'))
            return
        frame = self.map_index.getQgsPolygonFrame(self.inomLineEdit.text())
        reprojected = self.reprojectFrame(frame)
        self.insertFrameIntoLayer(reprojected)
        self.done(1)

    def insertFrameIntoLayer(self,reprojected):
        self.utils = Utils()
        self.dbVersion = self.utils.getDatabaseVersion(self.db)
        self.qmlPath = self.utils.getQmlDir(self.db)

        layer = self.getFrameLayer()
        if not layer:
            return

        layer.startEditing()
        feat = QgsFeature()
        feat.setFields(layer.dataProvider().fields())
        feat.setGeometry(reprojected)
        feat.setAttribute(2, self.inomen)
        feat.setAttribute(3, self.scaleCombo.currentText())
        layer.addFeatures([feat], makeSelected=True)
        layer.commitChanges()

        bbox = reprojected.boundingBox()
        for feature in layer.getFeatures():
            bbox.combineExtentWith(feature.geometry().boundingBox())

        bbox = self.iface.mapCanvas().mapSettings().layerToMapCoordinates(layer, bbox)
        self.iface.mapCanvas().setExtent(bbox)
        self.iface.mapCanvas().refresh()

    def getFrameLayer(self):
        for lyr in self.iface.legendInterface().layers():
            if lyr.name() == 'public_aux_moldura_a' or lyr.name() == 'aux_moldura_a':
                dbname = self.getDBNameFromLayer(lyr)
                if self.isSpatialite and dbname == self.filename:
                    return lyr
                if not self.isSpatialite:
                    (database, host, port, user, password) = self.utils.getPostGISConnectionParameters(self.comboBoxPostgis.currentText())
                    if dbname == database:
                        return lyr

        if self.isSpatialite:
            return self.loadSpatialiteFrame()
        else:
            return self.loadPostGISFrame()

        return None

    def getDBNameFromLayer(self, lyr):
        dbname = None
        splitUri = lyr.dataProvider().dataSourceUri().split(' ')
        if len(splitUri) > 0:
            dbsplit = splitUri[0].split('=')
            if len(dbsplit) > 1 and dbsplit[0] == 'dbname':
                dbnameInString = dbsplit[1]
                dbnameSplit = dbnameInString.split('\'')
                if len(dbnameSplit) > 1:
                    dbname = dbnameSplit[1]
        return dbname

    def loadPostGISFrame(self):
        self.selectedClasses = ['public.aux_moldura_a']
        (database, host, port, user, password) = self.utils.getPostGISConnectionParameters(self.comboBoxPostgis.currentText())
        uri = QgsDataSourceURI()
        uri.setConnection(str(host),str(port), str(database), str(user), str(password))
        if len(self.selectedClasses)>0:
            try:
                geom_column = 'geom'
                for layer in self.selectedClasses:
                    split = layer.split('.')
                    schema = split[0]
                    layerName = split[1]
                    sql = self.gen.loadLayerFromDatabase(layer)
                    uri.setDataSource(schema, layerName, geom_column, sql,'id')
                    uri.disableSelectAtId(True)
                    return self.loadEDGVLayer(uri, layerName, 'postgres')
            except:
                self.bar.pushMessage(self.tr("Error!"), self.tr("Could not load the selected frame!"), level=QgsMessageBar.CRITICAL)
        else:
            self.bar.pushMessage(self.tr("Warning!"), self.tr("Please, select at least one class!"), level=QgsMessageBar.WARNING)

    def loadSpatialiteFrame(self):
        self.selectedClasses = ['public_aux_moldura_a']
        uri = QgsDataSourceURI()
        uri.setDatabase(self.filename)
        schema = ''
        geom_column = 'GEOMETRY'
        if len(self.selectedClasses)>0:
            for layer_name in self.selectedClasses:
                uri.setDataSource(schema, layer_name, geom_column)
                return self.loadEDGVLayer(uri, layer_name, 'spatialite')

    def loadEDGVLayer(self, uri, layer_name, provider):
        vlayer = QgsVectorLayer(uri.uri(), layer_name, provider)
        vlayer.setCrs(self.crs)
        QgsMapLayerRegistry.instance().addMapLayer(vlayer) #added due to api changes
        if self.isSpatialite and (self.dbVersion == '3.0' or self.dbVersion == '2.1.3'):
            lyr = '_'.join(layer_name.replace('\r','').split('_')[1::])
        else:
            lyr = layer_name.replace('\r','')
        vlayerQml = os.path.join(self.qmlPath, lyr+'.qml')
        vlayer.loadNamedStyle(vlayerQml,False)
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)
        if not vlayer.isValid():
            QgsMessageLog.logMessage(vlayer.error().summary(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return None
        return vlayer

    @pyqtSlot()
    def on_cancelButton_clicked(self):
        self.done(0)

    @pyqtSlot(int)
    def on_comboBoxPostgis_currentIndexChanged(self):
        if self.comboBoxPostgis.currentIndex() > 0:
            self.loadDatabase()

    @pyqtSlot(str)
    def on_miLineEdit_textChanged(self,s):
        if (s!=''):
            self.inomen=self.map_index.getINomenFromMI(str(s))
            self.inomLineEdit.setText(self.inomen)

    @pyqtSlot(str)
    def on_mirLineEdit_textChanged(self,s):
        if (s!=''):
            self.inomen=self.map_index.getINomenFromMIR(str(s))
            self.inomLineEdit.setText(self.inomen)

    def reprojectFrame(self, poly):
        crsSrc = QgsCoordinateReferenceSystem(self.crs.geographicCRSAuthId())
        coordinateTransformer = QgsCoordinateTransform(crsSrc, self.crs)
        polyline = poly.asMultiPolygon()[0][0]
        newPolyline = []
        for point in polyline:
            newPolyline.append(coordinateTransformer.transform(point))
        qgsPolygon = QgsGeometry.fromMultiPolygon([[newPolyline]])
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
        else:
            self.isSpatialite = False

        #getting the sql generator according to the database type
        self.gen = self.factory.createSqlGenerator(self.isSpatialite)
        self.comboBoxPostgis.setCurrentIndex(0)

    def setCRS(self):
        try:
            self.epsg = self.findEPSG()
            print self.epsg
            if self.epsg == -1:
                self.bar.pushMessage("", self.tr("Coordinate Reference System not set or invalid!"), level=QgsMessageBar.WARNING)
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
        try:
            if not self.db.open():
                print self.db.lastError().text()
            else:
                self.dbLoaded = True
                self.setCRS()
        except:
            pass

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
        self.comboBoxPostgis.addItem(self.tr("Select Database"))
        self.comboBoxPostgis.addItems(self.getPostGISConnections())

    def findEPSG(self):
        sql = self.gen.getSrid()
        query = QSqlQuery(sql, self.db)
        srids = []
        while query.next():
            srids.append(query.value(0))
        return srids[0]

    def setValidCharacters(self):
        self.chars = []

        chars = 'NS'
        self.chars.append(chars)
        chars = 'ABCDEFGHIJKLMNOPQRSTUVZ'
        self.chars.append(chars)
        chars = ['01','02','03','04','05','06','07','08','09','10',
                   '11','12','13','14','15','16','17','18','19','20',
                   '21','22','23','24','25','26','27','28','29','30',
                   '31','32','33','34','35','36','37','38','39','40',
                   '41','42','43','44','45','46','47','48','49','50',
                   '51','52','53','54','55','56','57','58','59','60']
        self.chars.append(chars)
        chars = 'VXYZ'
        self.chars.append(chars)
        chars = 'ABCD'
        self.chars.append(chars)
        chars = ['I','II','III','IV','V','VI']
        self.chars.append(chars)
        chars = '1234'
        self.chars.append(chars)
        chars = ['NO','NE','SO','SE']
        self.chars.append(chars)
        chars = 'ABCDEF'
        self.chars.append(chars)
        chars = ['I','II','III','IV']
        self.chars.append(chars)
        chars = '123456'
        self.chars.append(chars)
        chars = 'ABCD'
        self.chars.append(chars)

    def setMask(self):
        if self.scaleCombo.currentText() == '1000k':
            self.inomLineEdit.setInputMask('NN-NN')
        elif self.scaleCombo.currentText() == '500k':
            self.inomLineEdit.setInputMask('NN-NN-N')
        elif self.scaleCombo.currentText() == '250k':
            self.inomLineEdit.setInputMask('NN-NN-N-N')
        elif self.scaleCombo.currentText() == '100k':
            self.inomLineEdit.setInputMask('NN-NN-N-N-Nn')
        elif self.scaleCombo.currentText() == '50k':
            self.inomLineEdit.setInputMask('NN-NN-N-N-Nn-N')
        elif self.scaleCombo.currentText() == '25k':
            self.inomLineEdit.setInputMask('NN-NN-N-N-Nn-N-NN')
        elif self.scaleCombo.currentText() == '10k':
            self.inomLineEdit.setInputMask('NN-NN-N-N-Nn-N-NN-N')
        elif self.scaleCombo.currentText() == '5k':
            self.inomLineEdit.setInputMask('NN-NN-N-N-Nn-N-NN-N-Nn')
        elif self.scaleCombo.currentText() == '2k':
            self.inomLineEdit.setInputMask('NN-NN-N-N-Nn-N-NN-N-Nn-N')
        elif self.scaleCombo.currentText() == '1k':
            self.inomLineEdit.setInputMask('NN-NN-N-N-Nn-N-NN-N-Nn-N-N')

    def validateMI(self):
        mi = self.inomLineEdit.text()
        split = mi.split('-')
        for i in range(len(split)):
            word = str(split[i])
            if len(word) == 0:
                return False
            if i == 0:
                if word[0] not in self.chars[0]:
                    print word
                    return False
                if word[1] not in self.chars[1]:
                    print word
                    return False
            elif i == 1:
                if word not in self.chars[2]:
                    print word
                    return False
            elif i == 2:
                if word not in self.chars[3]:
                    print word
                    return False
            elif i == 3:
                if word not in self.chars[4]:
                    print word
                    return False
            elif i == 4:
                if word not in self.chars[5]:
                    print word
                    return False
            elif i == 5:
                if word not in self.chars[6]:
                    print word
                    return False
            elif i == 6:
                if word not in self.chars[7]:
                    print word
                    return False
            elif i == 7:
                if word not in self.chars[8]:
                    print word
                    return False
            elif i == 8:
                if word not in self.chars[9]:
                    print word
                    return False
            elif i == 9:
                if word not in self.chars[10]:
                    print word
                    return False
            elif i == 10:
                if word not in self.chars[11]:
                    print word
                    return False
        return True

    def disableAll(self):
        self.mirLineEdit.setEnabled(False)
        self.miLineEdit.setEnabled(False)
        self.inomLineEdit.setEnabled(False)

    @pyqtSlot(int)
    def on_scaleCombo_currentIndexChanged(self):
        self.setMask()

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