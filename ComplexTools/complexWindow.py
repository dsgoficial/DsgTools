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

#PyQt4 imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QTreeWidgetItem, QMessageBox
from PyQt4.QtSql import QSqlDatabase, QSqlQuery

#QGIS imports
from qgis.core import *

#DsgTools imports
from DsgTools.ComplexTools.manageComplex import ManageComplexDialog
from DsgTools.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.Factories.DbFactory.dbFactory import DbFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'complexWindow_base.ui'))

class ComplexWindow(QtGui.QDockWidget, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(ComplexWindow, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        #self.enderecoLine.setText('186.228.51.52')
        #self.portaLine.setText('2101'
        self.iface = iface
        
        self.dbButton.clicked.connect(self.getDataSources)
        self.dbCombo.activated.connect(self.updateComplexClass)
        self.complexCombo.activated.connect(self.loadAssociatedFeatures)
        self.iface.newProjectCreated.connect(self.clearDock)

        self.abstractDb = None
        self.databases = None
        self.abstractDbFactory = DbFactory()

    def __del__(self):
        self.renewDb
            
    def renewDb(self):
        if self.abstractDb:
            del self.abstractDb
            self.abstractDb = None

    def clearDock(self):
        self.treeWidget.clear()
        self.dbCombo.clear()
        self.complexCombo.clear()

    #verificar se é necessario
    def isSpatialiteDatabase(self, dbName):
        (dataSourceUri, credentials) = self.databases[dbName]
        if dataSourceUri.host() == "":
            return True
        return False

    def getUserCredentials(self, lyr):
        dataSourceUri = QgsDataSourceURI( lyr.dataProvider().dataSourceUri() )
        if dataSourceUri.host() == "":
            return (None, None)

        connInfo = dataSourceUri.connectionInfo()
        (success, user, passwd ) = QgsCredentials.instance().get( connInfo, None, None )
        # Put the credentials back (for yourself and the provider), as QGIS removes it when you "get" it
        if success:
            QgsCredentials.instance().put( connInfo, user, passwd )

        return (user, passwd)

    def updateComplexClass(self):
        self.renewDb()

        if self.dbCombo.currentIndex() == 0:
            return

        dbName = self.dbCombo.currentText()
        
        (dataSourceUri, credentials) = self.databases[dbName]
        #verifying the connection type
        if self.isSpatialiteDatabase(dbName):
            self.abstractDb = self.abstractDbFactory.createDbFactory('QSQLITE')
            self.abstractDb.connectDatabase(dataSourceUri.database())
        else:
            self.abstractDb = self.abstractDbFactory.createDbFactory('QPSQL')
            
            database = dbName
            host = dataSourceUri.host()
            port = int(dataSourceUri.port())
            user = credentials[0]
            password = credentials[1]
            
            self.abstractDb.connectDatabaseWithParameters(host,port,database,user,password)
        try:
            self.abstractDb.checkAndOpenDb()
            self.populateComboBox()
        except Exception as e:
            QMessageBox.critical(self.iface.mainWindow(), self.tr("Critical!"), e.args[0])

    def populateComboBox(self):
        #getting all complex tables
        self.complexCombo.clear()
        self.complexCombo.addItem(self.tr("select a complex class"))

        dbName = self.dbCombo.currentText()
        (dataSourceUri, credentials) = self.databases[dbName]
        
        complexClasses = self.abstractDb.listComplexClassesFromDatabase()
        self.complexCombo.addItems(complexClasses)

    def getDataSources(self):
        self.dbCombo.clear()
        self.dbCombo.addItem(self.tr("select a database"))

        if self.databases:
            self.databases.clear()

        #dictionary of names and datasourceUri
        self.databases = dict()
        self.layers = self.iface.mapCanvas().layers()
        for layer in self.layers:
            dataSourceUri = QgsDataSourceURI(layer.dataProvider().dataSourceUri())
            dbName = dataSourceUri.database()
            if dbName not in self.databases:
                self.databases[dbName] = (dataSourceUri,self.getUserCredentials(layer))
                #populating the combo
                self.dbCombo.addItem(dbName)

    @pyqtSlot(bool)
    def on_managePushButton_clicked(self):
        #opens a dialog to manage complexes
        dlg = ManageComplexDialog(self.iface, self.abstractDb, self.complexCombo.currentText())
        #connects a signal to update the tree widget when done
        QObject.connect(dlg, SIGNAL(("tableUpdated()")), self.loadAssociatedFeatures)
        #connects a signal to disassociate features from complex before removal
        QObject.connect(dlg, SIGNAL(("markedToRemove( PyQt_PyObject )")), self.disassociateFeatures)
        result = dlg.exec_()
        if result:
            pass

    @pyqtSlot(bool)
    def on_associatePushButton_clicked(self):
        self.associateFeatures()

    @pyqtSlot(bool)
    def on_zoomButton_clicked(self):
        #case no item is selected we should warn the user
        if len(self.treeWidget.selectedItems()) == 0:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Please, select an item to zoom."))
            return

        item = self.treeWidget.selectedItems()[0]
        #checking if the item is a complex (it should have depth = 2)
        if self.depth(item) == 2:
            bbox = QgsRectangle()
            for i in range(item.childCount()):
                aggregated_item = item.child(i)
                aggregated_class = aggregated_item.text(0)
                #getting the layer the needs to be updated
                aggregated_layer = None
                layers = self.iface.mapCanvas().layers()
                for layer in layers:
                    if layer.name() == aggregated_class:
                        aggregated_layer = layer
                        break

                if not aggregated_layer:
                    QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("The associated classes must be loaded in the table of contents."))
                    return

                for j in range(aggregated_item.childCount()):
                    id = aggregated_item.child(j).text(0)
                    freq = QgsFeatureRequest()
                    freq.setFilterFid(int(id))
                    feature = layer.getFeatures( freq ).next()
                    if j==0 and i == 0:
                        bbox=feature.geometry().boundingBox()
                    bbox.combineExtentWith(feature.geometry().boundingBox())

            self.iface.mapCanvas().setExtent(bbox)
            self.iface.mapCanvas().refresh()
        else:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Select a complex."))
            return

    def disassociateFeatures(self, toBeRemoved):
        for uuid in toBeRemoved:
            items = self.treeWidget.findItems(uuid, Qt.MatchRecursive, 1)
            if len(items) == 0:
                return
            complexItem = items[0]
            count = complexItem.childCount()
            for i in range(count):
                self.disassociateAggregatedClass(complexItem.child(i))

    def disassociateAggregatedClass(self, item):
        aggregated_class = item.text(0)
        uuid = item.parent().text(1)
        complex = item.parent().parent().text(0)
        link_column = self.abstractDb.obtainLinkColumn(complex, aggregated_class)

        #getting the layer the needs to be updated
        aggregated_layer = None
        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            if layer.name() == aggregated_class:
                aggregated_layer = layer
                break

        if not aggregated_layer:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("The class you're trying to disassociate must loaded in the table of contents."))
            return

        for i in range(item.childCount()):
            #feature id that will be updated
            id = item.child(i).text(0)
            self.updateLayerOnDisassociate(layer, aggregated_class, link_column, id)

    def disassociateAggregatedId(self, item):
        aggregated_class = item.parent().text(0)
        uuid = item.parent().parent().text(1)
        complex = item.parent().parent().parent().text(0)
        link_column = self.abstractDb.obtainLinkColumn(complex, aggregated_class)

        #getting the layer the needs to be updated
        aggregated_layer = None
        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            if layer.name() == aggregated_class:
                aggregated_layer = layer
                break

        if not aggregated_layer:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("The class you're trying to disassociate must loaded in the table of contents."))
            return

        #feature id that will be updated
        id = item.text(0)
        self.updateLayerOnDisassociate(layer, aggregated_class, link_column, id)

    def updateLayerOnDisassociate(self, layer, aggregated_class, link_column, id):
        if self.abstractDb.isComplexClass(aggregated_class):
            try:
                self.abstractDb.disassociateComplexFromComplex(aggregated_class, link_column, id)
            except Exception as e:
                QMessageBox.critical(self.iface.mainWindow(), self.tr("Critical!"), e.args[0])
        else:
            #field index that will be set to NULL
            fieldIndex = [i for i in range(len(layer.dataProvider().fields())) if layer.dataProvider().fields()[i].name() == link_column]
            #attribute pair that will be changed
            attrs = {fieldIndex[0]:None}
            #actual update in the database
            layer.dataProvider().changeAttributeValues({int(id):attrs})

    @pyqtSlot(bool)
    def on_disassociatePushButton_clicked(self):
        #case no item is selected we should warn the user
        if len(self.treeWidget.selectedItems()) == 0:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Please, select an aggregated class or aggregated id."))
            return

        item = self.treeWidget.selectedItems()[0]
        #checking if the item is a complex (it should have depth = 2)
        if self.depth(item) == 3:
            self.disassociateAggregatedClass(item)
        elif self.depth(item) == 4:
            self.disassociateAggregatedId(item)
        else:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Please, select an aggregated class or aggregated id."))
            return

        self.loadAssociatedFeatures()

    def loadAssociatedFeatures(self):
        self.treeWidget.clear()

        if self.complexCombo.currentIndex() == 0:
            return

        complex = self.complexCombo.currentText()
        
        associatedDict = self.abstractDb.loadAssociatedFeatures(complex)
        
        for name in associatedDict.keys():
            for complex_uuid in associatedDict[name].keys():
                self.addAssociatedFeature(str(complex), str(name), complex_uuid, None, None)
                for aggregated_class in associatedDict[name][complex_uuid]:
                    for ogc_fid in associatedDict[name][complex_uuid][aggregated_class]:
                        self.addAssociatedFeature(str(complex), str(name), complex_uuid, str(aggregated_class), ogc_fid)

    def depth(self, item):
        #calculates the depth of the item
        depth = 0
        while item is not None:
            item = item.parent()
            depth += 1
        return depth

    def associateFeatures(self):
        #case no item is selected we should warn the user
        if len(self.treeWidget.selectedItems()) == 0:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Please, select a complex."))
            return

        item = self.treeWidget.selectedItems()[0]
        #checking if the item is a complex (it should have depth = 2)
        if self.depth(item) != 2:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Please, select a complex."))
            return

        complex = self.complexCombo.currentText()

        #uuid to be adjust on the selected features
        uuid = item.text(1)

        #getting the selected features
        forbiddenLayers = []
        self.layers = self.iface.mapCanvas().layers()
        for layer in self.layers:
            #case no fetures selected we proceed to the next one
            selectedFeatures = layer.selectedFeatures()
            if len(selectedFeatures) == 0:
                continue

            #obtaining the link column
            column_name = self.abstractDb.obtainLinkColumn(complex, layer.name())

            #storing the names of the incompatible layers
            if column_name == "":
                forbiddenLayers.append(layer.name())
                continue

            for feature in selectedFeatures:
                fieldIndex = [i for i in range(len(layer.dataProvider().fields())) if layer.dataProvider().fields()[i].name() == column_name]
                #feature id that will be updated
                id = feature.id()
                #attribute pair that will be changed
                attrs = {fieldIndex[0]:uuid}
                #actual update in the database
                layer.dataProvider().changeAttributeValues({id:attrs})

        #show the message of incompatible classes to associate
        if len(forbiddenLayers) > 0:
            message = ""
            message += self.tr("The following layers cannot be associated to complexes from ")+self.complexCombo.currentText()+":\n"
            for text in forbiddenLayers:
                message += text+"\n"
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), message)

        #updating the tree widget
        self.loadAssociatedFeatures()

    def createTreeItem(self, parent, text, uuid = ""):
        count = parent.childCount()
        children = []
        #making a list of item names
        for i in range(count):
            child = parent.child(i)
            children.append(child.text(0))

        #checking if the text is already in the tree widget
        if text not in children:
            #case not it should be created
            item = QTreeWidgetItem(parent)
            item.setExpanded(True)
            item.setText(0,text)
            #adding the complex uuid to the tree widget
            if uuid != "":
                item.setText(1, str(uuid))
        else:
            #case already exists the correspondind item should be returned
            for i in range(count):
                child = parent.child(i)
                if child.text(0) == text:
                    item = child
        return item

    def addAssociatedFeature(self, className, complexName, complexId, associatedClass, associatedId):
        #get the corresponding top level item
        classNameItem = self.createTreeItem(self.treeWidget.invisibleRootItem(), className)
        #get the corresponding complex item
        complexNameItem = self.createTreeItem(classNameItem, complexName, complexId)
        if associatedClass and associatedId:
            #get the corresponding class item
            associatedClassItem = self.createTreeItem(complexNameItem, associatedClass)
            #creates the corresponding associated item
            self.createTreeItem(associatedClassItem, str(associatedId))

    def __test(self, x):
        if (x.parent() == None) :
            return True
        else:
            return False
