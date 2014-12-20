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
import load_by_category_dialog

from qgis.core import QgsCoordinateReferenceSystem,QgsDataSourceURI,QgsVectorLayer,QgsMapLayerRegistry,QgsMessageLog
from qgis.gui import QgsGenericProjectionSelector,QgsMessageBar
import qgis as qgis

from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import QFileInfo,QSettings,pyqtSlot, Qt
from PyQt4.QtSql import QSqlQueryModel, QSqlTableModel,QSqlDatabase,QSqlQuery

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Factories', 'SqlFactory'))
from sqlGeneratorFactory import SqlGeneratorFactory

class LoadByCategory(QtGui.QDialog, load_by_category_dialog.Ui_LoadByCategory):
    def __init__(self, parent=None):
        """Constructor."""
        super(LoadByCategory, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.filename = ""
        self.dbLoaded = False
        self.epsg = 0
        self.crs = None
        self.categories = []
        self.selectedClasses = []

        self.point = []
        self.line = []
        self.polygon = []
        self.pointWithElement = []
        self.lineWithElement = []
        self.polygonWithElement = []

        #Sql factory generator
        self.isSpatialite = True

        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.factory = SqlGeneratorFactory()
        self.gen = self.factory.createSqlGenerator(self.isSpatialite)

        self.parentTreeNode = None

        self.comboBoxPostgis.setCurrentIndex(0)
        self.checkBoxPoint.setCheckState(0)
        self.checkBoxLine.setCheckState(0)
        self.checkBoxPolygon.setCheckState(0)
        self.checkBoxAll.setCheckState(0)


        #qmlPath will be set as /qml_qgis/qgis_22/edgv_213/, but in a further version, there will be an option to detect from db
        version = qgis.core.QGis.QGIS_VERSION_INT
        currentPath = os.path.dirname(__file__)
        if version >= 20600:
            self.qmlVersionPath = os.path.join(currentPath, 'qml_qgis', 'qgis_26')
        else:
            self.qmlVersionPath = os.path.join(currentPath, 'qml_qgis', 'qgis_22')

        self.bar = QgsMessageBar()
        self.setLayout(QtGui.QGridLayout(self))
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.bar.setSizePolicy(sizePolicy)
        self.layout().addWidget(self.bar, 0,0,1,1)

        #Objects Connections
        QtCore.QObject.connect(self.pushButtonOpenFile, QtCore.SIGNAL(("clicked()")), self.loadDatabase)
        QtCore.QObject.connect(self.pushButtonCancel, QtCore.SIGNAL(("clicked()")), self.cancel)
        QtCore.QObject.connect(self.pushButtonOk, QtCore.SIGNAL(("clicked()")), self.okSelected)
        QtCore.QObject.connect(self.tabWidget,QtCore.SIGNAL(("currentChanged(int)")), self.restoreInitialState)
        QtCore.QObject.connect(self.pushButtonSelectAll, QtCore.SIGNAL(("clicked()")), self.selectAll)
        QtCore.QObject.connect(self.pushButtonDeselectAll, QtCore.SIGNAL(("clicked()")), self.deselectAll)
        QtCore.QObject.connect(self.pushButtonSelectOne, QtCore.SIGNAL(("clicked()")), self.selectOne)
        QtCore.QObject.connect(self.pushButtonDeselectOne, QtCore.SIGNAL(("clicked()")), self.deselectOne)
        QtCore.QObject.connect(self.checkBoxAll, QtCore.SIGNAL(("stateChanged(int)")), self.setAllGroup)

        self.db = None
        #populating the postgis combobox
        self.populatePostGISConnectionsCombo()
        self.dbVersion = '2.1.3'

    def __del__(self):
        self.closeDatabase()

    def closeDatabase(self):
        if self.db:
            self.db.close()
            self.db = None

    def restoreInitialState(self):
        self.filename = ""
        self.dbLoaded = False
        self.epsg = 0
        self.crs = None
        self.categories = []
        self.selectedClasses = []
        self.spatialiteFileEdit.setText(self.filename)
        self.postGISCrsEdit.setText('')
        self.postGISCrsEdit.setReadOnly(True)
        self.spatialiteCrsEdit.setText('')
        self.spatialiteCrsEdit.setReadOnly(True)
        self.listWidgetCategoryFrom.clear()
        self.listWidgetCategoryTo.clear()

        self.point = []
        self.line = []
        self.polygon = []
        self.pointWithElement = []
        self.lineWithElement = []
        self.polygonWithElement = []
        self.parentTreeNode = None

        #Setting the database type
        if self.tabWidget.currentIndex() == 0:
            self.isSpatialite = True
        else:
            self.isSpatialite = False

        #getting the sql generator according to the database type
        self.gen = self.factory.createSqlGenerator(self.isSpatialite)
        self.comboBoxPostgis.setCurrentIndex(0)
        self.checkBoxPoint.setCheckState(0)
        self.checkBoxLine.setCheckState(0)
        self.checkBoxPolygon.setCheckState(0)
        self.checkBoxAll.setCheckState(0)


        self.dbVersion = '2.1.3'


    def updateBDField(self):
        if self.dbLoaded == True:
            self.spatialiteFileEdit.setText(self.filename)
        else:
            self.filename = ""
            self.spatialiteFileEdit.setText(self.filename)

    def listCategoriesFromDatabase(self):
        self.listWidgetCategoryFrom.clear()
        self.listWidgetCategoryTo.clear()
        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)

        sqlVersion = self.gen.getEDGVVersion()
        queryVersion =  QSqlQuery(sqlVersion, self.db)
        queryVersion.next()
        if queryVersion is not None:
            self.dbVersion = queryVersion.value(0)
        else:
            self.dbVersion = '2.1.3'

        if self.dbVersion == '3.0':
            self.qmlPath = os.path.join(self.qmlVersionPath, 'edgv_30')
        else:
            self.qmlPath = os.path.join(self.qmlVersionPath, 'edgv_213')

        while query.next():
            if self.isSpatialite:
                tableName = query.value(0)
                layerName = tableName
                split = tableName.split('_')
                if len(split) < 2:
                    continue
                if self.dbVersion == '3.0':
                    schema = split[0]
                    category = split[1]
                    categoryName = schema+'.'+category
                else:
                    categoryName = split[0] #done this way to have back compatibility with spatialites already in production

            else:
                tableSchema = query.value(0)
                tableName = query.value(1)
                split = tableName.split('_')
                category = split[0]
                categoryName = tableSchema+'.'+category
                layerName = tableSchema+'.'+tableName

            if layerName.split("_")[-1] == "p":
                self.point.append(layerName)
            if layerName.split("_")[-1] == "l":
                self.line.append(layerName)
            if layerName.split("_")[-1] == "a":
                self.polygon.append(layerName)

            if tableName.split("_")[-1] == "p" or tableName.split("_")[-1] == "l" \
                or tableName.split("_")[-1] == "a":
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

    def setCRS(self):
        try:
            self.epsg = self.findEPSG()
            print self.epsg
            if self.epsg == -1:
                self.bar.pushMessage("", self.tr('DsgTools',"Coordinate Reference System not set or invalid!"), level=QgsMessageBar.WARNING)
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

    @pyqtSlot(int)
    def on_comboBoxPostgis_currentIndexChanged(self):
        if self.comboBoxPostgis.currentIndex() > 0:
            self.loadDatabase()

    def loadDatabase(self):
        self.closeDatabase()
        try:
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
                self.listCategoriesFromDatabase()
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

    def getSelectedItems(self):
        lista = self.classesListWidget.selectedItems()
        self.selectedClasses = []
        tam = len(lista)
        for i in range(tam):
            self.selectedClasses.append(lista[i].text())
        self.selectedClasses.sort()

    def okSelected(self):
        if self.checkBoxOnlyWithElements.isChecked():
            self.setLayersWithElements()
            ponto = self.pointWithElement
            linha = self.lineWithElement
            area = self.polygonWithElement
        else:
            ponto = self.point
            linha = self.line
            area = self.polygon

        if self.db and self.crs and len(self.listWidgetCategoryTo)>0:
            categoriasSelecionadas = []

            for i in range(self.listWidgetCategoryTo.__len__()):
                categoriasSelecionadas.append(self.listWidgetCategoryTo.item(i).text())

            try:

                if self.checkBoxPoint.isChecked():
                    self.loadLayers('p',categoriasSelecionadas,ponto)

                if self.checkBoxLine.isChecked():
                    self.loadLayers('l',categoriasSelecionadas,linha)

                if self.checkBoxPolygon.isChecked():
                    self.loadLayers('a',categoriasSelecionadas,area)

                if self.checkBoxPoint.isChecked()== False and self.checkBoxLine.isChecked() == False and self.checkBoxPolygon.isChecked() == False:
                    self.bar.pushMessage(self.tr('DsgTools',"WARNING!"), self.tr('DsgTools',"Please, select at least one type of layer!"), level=QgsMessageBar.WARNING)
                else:
                    self.restoreInitialState()
                    self.close()
            except:
                qgis.utils.iface.messageBar().pushMessage(self.tr('DsgTools',"CRITICAL!"), self.tr('DsgTools',"Problem loading the categories!"), level=QgsMessageBar.CRITICAL)
                pass

        else:
            if self.db and not self.crs:
                self.bar.pushMessage(self.tr('DsgTools',"CRITICAL!"), self.tr('DsgTools',"Could not determine the coordinate reference system!"), level=QgsMessageBar.CRITICAL)
            if not self.db and not self.crs:
                self.bar.pushMessage(self.tr('DsgTools',"CRITICAL!"), self.tr('DsgTools',"Database not loaded properly!"), level=QgsMessageBar.CRITICAL)
                self.bar.pushMessage(self.tr('DsgTools',"CRITICAL!"), self.tr('DsgTools',"Could not determine the coordinate reference system!"), level=QgsMessageBar.CRITICAL)
            if len(self.listWidgetCategoryTo)==0:
                self.bar.pushMessage(self.tr('DsgTools',"WARNING!"), self.tr('DsgTools',"Please, select at least one category!"), level=QgsMessageBar.WARNING)
            categoriasSelecionadas = []
            self.pointWithElement = []
            self.lineWithElement = []
            self.polygonWithElement = []

    def loadLayers(self, type, categories, layer_names):
        if self.isSpatialite:
            self.loadSpatialiteLayers(type, categories, layer_names)
        else:
            self.loadPostGISLayers(type, categories, layer_names)

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
            sql = self.gen.getElementCountFromLayer(layer)
            query = QSqlQuery(sql,self.db)
            query.next()
            number = query.value(0)
            if number > 0:
                print sql
                print number
            if not query.exec_(sql):
                QgsMessageLog.logMessage(self.tr('DsgTools',"Problem counting elements: ")+query.lastError().text(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            listaQuantidades.append([layer, number])
        return listaQuantidades

    def loadPostGISLayers(self, type, categories, layer_names):
        (database, host, port, user, password) = self.getPostGISConnectionParameters(self.comboBoxPostgis.currentText())
        uri = QgsDataSourceURI()
        uri.setConnection(str(host),str(port), str(database), str(user), str(password))
        geom_column = 'geom'
        if self.parentTreeNode is None:
            self.parentTreeNode = qgis.utils.iface.legendInterface (). addGroup (database, -1)

        if type == 'p':
            idGrupo = qgis.utils.iface.legendInterface (). addGroup ("Ponto", True,self.parentTreeNode)
            for categoria in categories:
                self.preparePostGISToLoad(uri, categoria, layer_names, idGrupo, geom_column)
        if type == 'l':
            idGrupo = qgis.utils.iface.legendInterface (). addGroup ("Linha", True,self.parentTreeNode)
            for categoria in categories:
                self.preparePostGISToLoad(uri, categoria, layer_names, idGrupo, geom_column)
        if type == 'a':
            idGrupo = qgis.utils.iface.legendInterface (). addGroup ("Area", True,self.parentTreeNode)
            for categoria in categories:
                self.preparePostGISToLoad(uri, categoria, layer_names, idGrupo, geom_column)

    def preparePostGISToLoad(self, uri, categoria, layer_names, idGrupo, geom_column):
        idSubgrupo = qgis.utils.iface.legendInterface().addGroup(categoria,True,idGrupo)
        for layer_name in layer_names:
            split = layer_name.split('_')
            category = split[0]
            schema = category.split('.')[0]
            name = layer_name.replace(schema+'.','')
            if category == categoria:
                sql = self.gen.loadLayerFromDatabase(layer_name)
                print schema,name,geom_column,sql
                uri.setDataSource(schema, name, geom_column, sql,'id')
                uri.disableSelectAtId(True)
                self.loadEDGVLayer(uri, name, schema, 'postgres', idSubgrupo)

    def prepareSpatialiteToLoad(self, uri, categoria, layer_names, idGrupo, geom_column):
        idSubgrupo = qgis.utils.iface.legendInterface().addGroup(categoria,True,idGrupo)
        for layer_name in layer_names:
            split = layer_name.split('_')
            category = split[0]+'.'+split[1]
            if category == categoria:
                print category,layer_name,geom_column
                uri.setDataSource('', layer_name, geom_column)
                self.loadEDGVLayer(uri, layer_name, '', 'spatialite', idSubgrupo)

    def loadSpatialiteLayers(self, type, categories, layer_names):
        uri = QgsDataSourceURI()
        uri.setDatabase(self.filename)
        geom_column = 'GEOMETRY'

        if self.parentTreeNode is None:
            self.parentTreeNode = qgis.utils.iface.legendInterface (). addGroup (self.filename.split('.sqlite')[0].split('/')[-1], -1)

        if type == 'p':
            idGrupo = qgis.utils.iface.legendInterface (). addGroup ("Ponto", True,self.parentTreeNode)
            for categoria in categories:
                self.prepareSpatialiteToLoad(uri, categoria, layer_names, idGrupo, geom_column)
        if type == 'l':
            idGrupo = qgis.utils.iface.legendInterface (). addGroup ("Linha", True,self.parentTreeNode)
            for categoria in categories:
                self.prepareSpatialiteToLoad(uri, categoria, layer_names, idGrupo, geom_column)
        if type == 'a':
            idGrupo = qgis.utils.iface.legendInterface (). addGroup ("Area", True,self.parentTreeNode)
            for categoria in categories:
                self.prepareSpatialiteToLoad(uri, categoria, layer_names, idGrupo, geom_column)

    def loadEDGVLayer(self, uri, layer_name, schema, provider, idSubgrupo):
        vlayer = QgsVectorLayer(uri.uri(), layer_name, provider)
        vlayer.setCrs(self.crs)
        QgsMapLayerRegistry.instance().addMapLayer(vlayer) #added due to api changes
        vlayerQml = os.path.join(self.qmlPath, layer_name.replace('\r','')+'.qml')
        vlayer.loadNamedStyle(vlayerQml,False)
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)
        qgis.utils.iface.legendInterface().moveLayer(vlayer, idSubgrupo)
        if not vlayer.isValid():
            print vlayer.error().summary()
