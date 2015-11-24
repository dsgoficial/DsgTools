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
        mod history          : 2014-12-17 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
                               2014-12-19 by Philipe Borba- Cartographic Engineer @ Brazilian Army
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

#QGIS imports
from qgis.core import QgsCoordinateReferenceSystem,QgsDataSourceURI,QgsVectorLayer,QgsMapLayerRegistry,QgsMessageLog
from qgis.gui import QgsMessageBar
import qgis as qgis

#PyQt imports
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import  Qt
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtGui import QApplication, QCursor

#DsgTools imports
from DsgTools.Factories.LayerFactory.layerFactory import LayerFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'load_by_category_dialog.ui'))

class LoadByCategory(QtGui.QDialog, FORM_CLASS):
    def __init__(self, codeList, parent=None):
        """Constructor."""
        super(LoadByCategory, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.categories = []
        self.selectedClasses = []
 
        self.point = []
        self.line = []
        self.polygon = []
        self.pointWithElement = []
        self.lineWithElement = []
        self.polygonWithElement = []
 
        self.parentTreeNode = None
 
        self.checkBoxPoint.setCheckState(0)
        self.checkBoxLine.setCheckState(0)
        self.checkBoxPolygon.setCheckState(0)
        self.checkBoxAll.setCheckState(0)
 
        self.bar = QgsMessageBar()
        self.setLayout(QtGui.QGridLayout(self))
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.bar.setSizePolicy(sizePolicy)
        self.layout().addWidget(self.bar, 0,0,1,1)
 
        #Objects Connections
        QtCore.QObject.connect(self.widget, QtCore.SIGNAL(("connectionChanged()")), self.listCategoriesFromDatabase)
        QtCore.QObject.connect(self.widget, QtCore.SIGNAL(("problemOccurred()")), self.pushMessage)
        
        QtCore.QObject.connect(self.pushButtonCancel, QtCore.SIGNAL(("clicked()")), self.cancel)
        QtCore.QObject.connect(self.pushButtonOk, QtCore.SIGNAL(("clicked()")), self.okSelected)
        QtCore.QObject.connect(self.pushButtonSelectAll, QtCore.SIGNAL(("clicked()")), self.selectAll)
        QtCore.QObject.connect(self.pushButtonDeselectAll, QtCore.SIGNAL(("clicked()")), self.deselectAll)
        QtCore.QObject.connect(self.pushButtonSelectOne, QtCore.SIGNAL(("clicked()")), self.selectOne)
        QtCore.QObject.connect(self.pushButtonDeselectOne, QtCore.SIGNAL(("clicked()")), self.deselectOne)
        QtCore.QObject.connect(self.checkBoxAll, QtCore.SIGNAL(("stateChanged(int)")), self.setAllGroup)
        
        self.codeList = codeList
        self.layerFactory = LayerFactory()
 
    def restoreInitialState(self):
        self.categories = []
        self.selectedClasses = []
        self.listWidgetCategoryFrom.clear()
        self.listWidgetCategoryTo.clear()

        self.point = []
        self.line = []
        self.polygon = []
        self.pointWithElement = []
        self.lineWithElement = []
        self.polygonWithElement = []
        self.parentTreeNode = None

        self.checkBoxPoint.setCheckState(0)
        self.checkBoxLine.setCheckState(0)
        self.checkBoxPolygon.setCheckState(0)
        self.checkBoxAll.setCheckState(0)

    def listCategoriesFromDatabase(self):
        self.listWidgetCategoryFrom.clear()
        self.listWidgetCategoryTo.clear()

        self.dbVersion = self.widget.getDBVersion()
        self.qmlPath = self.widget.getQmlPath()
        classes = self.widget.abstractDb.listGeomClassesFromDatabase()
        for table in classes:
            schema, layerName = self.widget.abstractDb.getTableSchema(table)
            category = layerName.split('_')[0]
            categoryName = schema+'.'+category
            if layerName.split("_")[-1] == "p":
                self.point.append(table)
            if layerName.split("_")[-1] == "l":
                self.line.append(table)
            if layerName.split("_")[-1] == "a":
                self.polygon.append(table)

            self.insertIntoListView(categoryName)
        self.listWidgetCategoryFrom.sortItems()
        self.setCRS()

    def insertIntoListView(self, item_name):
        found = self.listWidgetCategoryFrom.findItems(item_name, Qt.MatchExactly)
        if len(found) == 0:
            item = QtGui.QListWidgetItem(item_name)
            self.listWidgetCategoryFrom.addItem(item)

    def selectAll(self):
        tam = self.listWidgetCategoryFrom.__len__()
        for i in range(tam+1,1,-1):
            item = self.listWidgetCategoryFrom.takeItem(i-2)
            self.listWidgetCategoryTo.addItem(item)
        self.listWidgetCategoryTo.sortItems()

    def deselectAll(self):
        tam = self.listWidgetCategoryTo.__len__()
        for i in range(tam+1,1,-1):
            item = self.listWidgetCategoryTo.takeItem(i-2)
            self.listWidgetCategoryFrom.addItem(item)
        self.listWidgetCategoryFrom.sortItems()

    def selectOne(self):
        listedItems = self.listWidgetCategoryFrom.selectedItems()
        for i in listedItems:
            item = self.listWidgetCategoryFrom.takeItem(self.listWidgetCategoryFrom.row(i))
            self.listWidgetCategoryTo.addItem(item)
        self.listWidgetCategoryTo.sortItems()

    def deselectOne(self):
        listedItems = self.listWidgetCategoryTo.selectedItems()
        for i in listedItems:
            item = self.listWidgetCategoryTo.takeItem(self.listWidgetCategoryTo.row(i))
            self.listWidgetCategoryFrom.addItem(item)
        self.listWidgetCategoryFrom.sortItems()


    def setAllGroup(self):
        if self.checkBoxAll.isChecked():
            self.checkBoxPoint.setCheckState(2)
            self.checkBoxLine.setCheckState(2)
            self.checkBoxPolygon.setCheckState(2)
        else:
            self.checkBoxPoint.setCheckState(0)
            self.checkBoxLine.setCheckState(0)
            self.checkBoxPolygon.setCheckState(0)
            
    def pushMessage(self, msg):
        self.bar.pushMessage("", self.tr("Coordinate Reference System not set or invalid!"), level=QgsMessageBar.WARNING)

    def setCRS(self):
        try:
            self.epsg = self.utils.findEPSG(self.db)
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

    def cancel(self):
        self.restoreInitialState()
        self.close()

    def getSelectedItems(self):
        lista = self.classesListWidget.selectedItems()
        self.selectedClasses = []
        tam = len(lista)
        for i in range(tam):
            self.selectedClasses.append(lista[i].text())
        self.selectedClasses.sort()

    def okSelected(self):
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
    
            if self.checkBoxOnlyWithElements.isChecked():
                self.setLayersWithElements()
                ponto = self.pointWithElement
                linha = self.lineWithElement
                area = self.polygonWithElement
            else:
                ponto = self.point
                linha = self.line
                area = self.polygon
    
            if len(self.listWidgetCategoryTo)>0:
                categoriasSelecionadas = []
                for i in range(self.listWidgetCategoryTo.__len__()):
                    categoriasSelecionadas.append(self.listWidgetCategoryTo.item(i).text())
    
                if self.checkBoxPoint.isChecked():
                    self.loadLayers('p', categoriasSelecionadas, ponto)
                if self.checkBoxLine.isChecked():
                    self.loadLayers('l', categoriasSelecionadas, linha)
                if self.checkBoxPolygon.isChecked():
                    self.loadLayers('a', categoriasSelecionadas, area)
                if self.checkBoxPoint.isChecked()== False and self.checkBoxLine.isChecked() == False and self.checkBoxPolygon.isChecked() == False:
                    self.bar.pushMessage(self.tr("WARNING!"), self.tr("Please, select at least one type of layer!"), level=QgsMessageBar.WARNING)
                else:
                    self.restoreInitialState()
                    self.close()
            else:
                if self.widget.db and not self.widget.crs:
                    self.bar.pushMessage(self.tr("CRITICAL!"), self.tr("Could not determine the coordinate reference system!"), level=QgsMessageBar.CRITICAL)
                if not self.widget.db and not self.widget.crs:
                    self.bar.pushMessage(self.tr("CRITICAL!"), self.tr("Database not loaded properly!"), level=QgsMessageBar.CRITICAL)
                    self.bar.pushMessage(self.tr("CRITICAL!"), self.tr("Could not determine the coordinate reference system!"), level=QgsMessageBar.CRITICAL)
                if len(self.listWidgetCategoryTo)==0:
                    self.bar.pushMessage(self.tr("WARNING!"), self.tr("Please, select at least one category!"), level=QgsMessageBar.WARNING)
                categoriasSelecionadas = []
                self.pointWithElement = []
                self.lineWithElement = []
                self.polygonWithElement = []
    
            QApplication.restoreOverrideCursor()
        except:
            QApplication.restoreOverrideCursor()

    def setLayersWithElements(self):
        self.pointWithElement = []
        self.lineWithElement = []
        self.polygonWithElement = []

        pontoAux = self.countElements(self.point)
        linhaAux = self.countElements(self.line)
        areaAux = self.countElements(self.polygon)

        for i in pontoAux:
            if i[1] > 0:
                self.pointWithElement.append(i[0])

        for i in linhaAux:
            if i[1] > 0:
                self.lineWithElement.append(i[0])

        for i in areaAux:
            if i[1] > 0:
                self.polygonWithElement.append(i[0])

    def countElements(self, layers):
        listaQuantidades = []
        for layer in layers:
            sql = self.widget.gen.getElementCountFromLayer(layer)
            query = QSqlQuery(sql,self.widget.db)
            query.next()
            number = query.value(0)
            if not query.exec_(sql):
                QgsMessageLog.logMessage(self.tr("Problem counting elements: ")+query.lastError().text(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            listaQuantidades.append([layer, number])
        return listaQuantidades

    def loadLayers(self, type, categories, table_names):
        if self.parentTreeNode is None:
            self.parentTreeNode = qgis.utils.iface.legendInterface (). addGroup (self.widget.abstractDb.getDatabaseName(), -1)

        if type == 'p':
            idGrupo = qgis.utils.iface.legendInterface (). addGroup (self.tr('Point'), True,self.parentTreeNode)
            for category in categories:
                self.prepareLayer(category, table_names, idGrupo)
        if type == 'l':
            idGrupo = qgis.utils.iface.legendInterface (). addGroup (self.tr('Line'), True,self.parentTreeNode)
            for category in categories:
                self.prepareLayer(category, table_names, idGrupo)
        if type == 'a':
            idGrupo = qgis.utils.iface.legendInterface (). addGroup (self.tr('Area'), True,self.parentTreeNode)
            for category in categories:
                self.prepareLayer(category, table_names, idGrupo)
                
    def prepareLayer(self, category, table_names, idGrupo):
        idSubgrupo = qgis.utils.iface.legendInterface().addGroup(category, True, idGrupo)
        table_names.sort(reverse=True)
        for table_name in table_names:
            schema, layerName = self.widget.abstractDb.getTableSchema(table_name)
            if category.split('.')[1] == layerName.split('_')[0]:
                edgvLayer = self.layerFactory.makeLayer(self.widget.abstractDb, self.codeList, table_name)
                edgvLayer.load(self.widget.crs, idSubgrupo)