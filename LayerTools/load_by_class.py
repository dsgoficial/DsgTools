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

import os

from PyQt4 import QtGui, uic, QtCore


import load_by_class_base
import sqlite3, os
from PyQt4.QtCore import QFileInfo,QSettings
from qgis.core import QgsCoordinateReferenceSystem,QgsDataSourceURI,QgsVectorLayer,QgsMapLayerRegistry
from qgis.gui import QgsGenericProjectionSelector,QgsMessageBar
import qgis as qgis
from PyQt4 import QtGui
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Factories', 'SqlFactory'))
from sqlGeneratorFactory import SqlGeneratorFactory

from PyQt4.QtSql import QSqlQueryModel, QSqlTableModel,QSqlDatabase,QSqlQuery


class LoadByClass(QtGui.QDialog, load_by_class_base.Ui_LoadByClass):
    def __init__(self, parent=None):
        """Constructor."""
#         super(QtGui.QDialog).__init__(parent)

        super(LoadByClass, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
#         self.connect(self.pushButtonOpenFile, QtCore.SIGNAL("clicked()"), self.loadSpatialite)
        self.filename = ""
        self.dbLoaded = False
        self.crsSet = False
        self.onlyWithElementsBool = False
        self.epsg = 0
        self.crs = ''
        self.classes = []
        self.selectedClasses = []
        self.setupUi(self)
        self.factory = SqlGeneratorFactory()
        self.gen = None
        #qmlPath will be set as /qml_qgis/qgis_22/edgv_213/, but in a further version, there will be an option to detect from db
        version = qgis.core.QGis.QGIS_VERSION_INT
        if version >= 20600:
            self.qmlPath = os.path.dirname(__file__)+'/qml_qgis/qgis_26/edgv_213/'
        else:
            self.qmlPath = os.path.dirname(__file__)+'/qml_qgis/qgis_22/edgv_213/'
        self.qmlPath.replace('\\','/')


        self.bar = QgsMessageBar()
        self.setLayout(QtGui.QGridLayout(self))
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.bar.setSizePolicy(sizePolicy)
        self.layout().addWidget(self.bar, 0,0,1,1)

        #Objects Connections
        QtCore.QObject.connect(self.pushButtonOpenFile, QtCore.SIGNAL(("clicked()")), self.loadSpatialite)
        QtCore.QObject.connect(self.fileLineEditLoadByClass, QtCore.SIGNAL(("textChanged(QString)")), self.listsCategories)
        QtCore.QObject.connect(self.pushButtonCancelLoadByClass, QtCore.SIGNAL(("clicked()")), self.cancel)
        QtCore.QObject.connect(self.checkBoxSelectAllLoadByClass, QtCore.SIGNAL(("stateChanged(int)")), self.selectAll)
        QtCore.QObject.connect(self.pushButtonOkLoadByClass, QtCore.SIGNAL(("clicked()")), self.okSelected)
        QtCore.QObject.connect(self.tabWidgetLoadByClass,QtCore.SIGNAL(("currentChanged(int)")), self.restoreInitialState)



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





    def loadSpatialite(self):
        fd = QtGui.QFileDialog()
        self.filename = fd.getOpenFileName(filter='*.sqlite')
        if self.filename <> "":
            self.dbLoaded = True
            self.fileLineEditLoadByClass.setText(self.filename)

    def updateBDField(self):
        if self.dbLoaded == True:
            self.fileLineEditLoadByClass.setText(self.filename)
        else:
            self.filename = ""
            self.fileLineEditLoadByClass.setText(self.filename)



    def setCRS(self):
        projSelector = QgsGenericProjectionSelector()
        projSelector.setMessage(theMessage='Select the Coordinate Reference System')
        projSelector.exec_()
        try:
            self.epsg = int(projSelector.selectedAuthId().split(':')[-1])
            self.crs = QgsCoordinateReferenceSystem(self.epsg, QgsCoordinateReferenceSystem.EpsgCrsId)
            if self.crs <> "":
                self.crsSet = True
                self.crsLineEditLoadByClassSpatialite.setText(self.crs.description())
        except:
            self.bar.pushMessage("", "Coordinate Reference System not set!", level=QgsMessageBar.WARNING)
            pass

    def countElements(self,lista):
        con = sqlite3.connect(self.filename)
        cursor = con.cursor()
        listaQuantidades = []
        for i in lista:
            cursor.execute("SELECT count() FROM "+i[0]+";")
            listaQuantidades.append(cursor.fetchall()[0][0])
        #check if connection was closed

        return listaQuantidades

    def getLayersWithElements(self):
        auxPoint = self.countElements(self.point)
        auxLine = self.countElements(self.line)
        auxArea = self.countElements(self.area)
        count = 0
        for i in auxPoint:
            if i > 0:
                self.pointLayersWithElements.append(self.point[count])
            count+=1
        count = 0
        for i in auxLine:
            if i > 0:
                self.lineLayersWithElements.append(self.line[count])
            count+=1
        count = 0

        for i in auxArea:
            if i > 0:
                self.areaLayersWithElements.append(self.area[count])
            count+=1


    def listsCategories(self):
        if self.tabWidgetLoadByClass.tabText(self.tabWidgetLoadByClass.currentIndex()) == "Spatialite":
            con = sqlite3.connect(self.filename)
            cursor = con.cursor()
            self.gen = self.factory.createSqlGenerator(True)
            sql = self.gen.getTablesFromDatabase()
            cursor.execute(sql)
            tableList = cursor.fetchall()

        for i in tableList:

            if (i[0].split("_")[-1] == "p"):
                self.classes.append(i[0])
            if (i[0].split("_")[-1] == "l"):
                self.classes.append(i[0])
            if (i[0].split("_")[-1] == "a"):
                self.classes.append(i[0])

        self.classes.sort() #sorts it into alphabetical order


        for i in self.classes:
            item = QtGui.QListWidgetItem(i)
            self.listWidgetClassesLoadByClass.addItem(item)
        try:
            self.epsg = self.findsEPSGSpatialite(cursor)

            if self.epsg == -1:
                self.bar.pushMessage("", "Coordinate Reference System not set or invalid!", level=QgsMessageBar.WARNING)
            else:
                self.crs = QgsCoordinateReferenceSystem(self.epsg, QgsCoordinateReferenceSystem.EpsgCrsId)
                self.crsLineEditLoadByClassSpatialite.setText(self.crs.description())
                self.crsLineEditLoadByClassSpatialite.setReadOnly(True)
                self.dbLoaded = True
        except:

            pass



    def findsEPSGSpatialite(self,cursor):
        self.gen = self.factory.createSqlGenerator(True)
        sql = self.gen.getSrid()
        cursor.execute(sql)
        list = cursor.fetchall()
        return list[0][0]

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



    def setQMLDir(self):
        fd = QtGui.QFileDialog()
        dir = fd.getExistingDirectory()
        return dir.replace('\\','/')+'/'

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


    def showText(self):
        print self.tabWidgetLoadByClass.tabText(self.tabWidgetLoadByClass.currentIndex())