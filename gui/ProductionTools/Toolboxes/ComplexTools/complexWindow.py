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
from builtins import str
from builtins import range
import os

#PyQt5 imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, QObject, Qt
from qgis.PyQt.QtWidgets import QTreeWidgetItem, QMessageBox
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery

#QGIS imports
from qgis.core import QgsDataSourceUri, QgsCredentials, QgsMessageLog, QgsRectangle, QgsFeatureRequest, QgsMapLayer

#DsgTools imports
from DsgTools.gui.ProductionTools.Toolboxes.ComplexTools.manageComplex import ManageComplexDialog
from DsgTools.core.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.dsgEnums import DsgEnums

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'complexWindow_base.ui'))

class ComplexWindow(QtWidgets.QDockWidget, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(ComplexWindow, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface
        
        self.dbButton.clicked.connect(self.getDataSources)
        self.dbCombo.activated.connect(self.updateComplexClass)
        self.complexCombo.activated.connect(self.loadAssociatedFeatures)
        self.iface.newProjectCreated.connect(self.clearDock)

        self.abstractDb = None
        self.databases = None
        self.abstractDbFactory = DbFactory()
    
    def addTool(self, manager, callback, parentMenu, iconBasePath, parentStackButton):
        icon_path = iconBasePath + 'complex.png'
        text = self.tr('Build Complex Structures')
        action = manager.add_action(
            icon_path,
            text=text,
            callback=callback,
            add_to_menu=False,
            add_to_toolbar=False,
            parentMenu = parentMenu,
            parentButton = parentStackButton
            )

    def __del__(self):
        """
        Destructor
        """
        self.renewDb
            
    def renewDb(self):
        """
        Deletes the current abstractDb
        """
        if self.abstractDb:
            del self.abstractDb
            self.abstractDb = None

    def clearDock(self):
        """
        Clears the complex dock widget
        """
        self.treeWidget.clear()
        self.dbCombo.clear()
        self.complexCombo.clear()

    #verificar se é necessario
    def isSpatialiteDatabase(self, dbName):
        """
        Checks if the database in use is a spatialite database
        """
        (dataSourceUri, credentials) = self.databases[dbName]
        if dataSourceUri.host() == "":
            return True
        return False

    def getUserCredentials(self, lyr):
        """
        Gets user credentials to acess the database
        """
        dataSourceUri = QgsDataSourceUri(lyr.dataProvider().dataSourceUri())
        if dataSourceUri.host() == '':
            return (None, None)

        if dataSourceUri.password() != '':
            return (dataSourceUri.username(), dataSourceUri.password())

        connInfo = dataSourceUri.connectionInfo()
        (success, user, passwd ) = QgsCredentials.instance().get(connInfo, dataSourceUri.username(), None)
        # Put the credentials back (for yourself and the provider), as QGIS removes it when you "get" it
        if success:
            QgsCredentials.instance().put(connInfo, user, passwd)
        else:
            return (None, None)

        return (user, passwd)

    def updateComplexClass(self):
        """
        Updates the complex classes in the complex combo box
        """
        self.renewDb()

        if self.dbCombo.currentIndex() == 0:
            return

        dbName = self.dbCombo.currentText()
        
        (dataSourceUri, credentials) = self.databases[dbName]
        #verifying the connection type
        if self.isSpatialiteDatabase(dbName):
            self.abstractDb = self.abstractDbFactory.createDbFactory(DsgEnums.DriverSpatiaLite)
            self.abstractDb.connectDatabase(dataSourceUri.database())
        else:
            self.abstractDb = self.abstractDbFactory.createDbFactory(DsgEnums.DriverPostGIS)
            
            database = dbName
            host = dataSourceUri.host()
            port = int(dataSourceUri.port())
            user = credentials[0]
            password = credentials[1]
            
            self.abstractDb.connectDatabaseWithParameters(host, port, database, user, password)
        try:
            self.abstractDb.checkAndOpenDb()
            self.populateComboBox()
        except Exception as e:
            QMessageBox.critical(self.iface.mainWindow(), self.tr("Critical!"), ':'.join(e.args))

    def populateComboBox(self):
        """
        Fills the complex combo box with complex classes
        """
        #getting all complex tables
        self.complexCombo.clear()
        self.complexCombo.addItem(self.tr("select a complex class"))

        complexClasses = []
        try:
            complexClasses = self.abstractDb.listComplexClassesFromDatabase()
        except Exception as e:
            QMessageBox.critical(self.iface.mainWindow(), self.tr("Critical!"), ':'.join(e.args))
            QgsMessageLog.logMessage(e.args[0], 'DSG Tools Plugin', Qgis.Critical)

        self.complexCombo.addItems(complexClasses)

    def getDataSources(self):
        """
        Obtains the available databases from the layers loaded in the TOC
        """
        self.dbCombo.clear()
        self.dbCombo.addItem(self.tr("select a database"))

        if self.databases:
            self.databases.clear()

        #dictionary of names and datasourceUri
        self.databases = dict()
        self.layers = self.iface.mapCanvas().layers()
        for layer in self.layers:
            dataSourceUri = QgsDataSourceUri(layer.dataProvider().dataSourceUri())
            dbName = dataSourceUri.database()
            if dbName not in list(self.databases.keys()):
                self.databases[dbName] = (dataSourceUri, self.getUserCredentials(layer))
                #populating the combo
                self.dbCombo.addItem(dbName)

    @pyqtSlot(bool)
    def on_managePushButton_clicked(self):
        """
        Opens the dialog to manage complex features
        """
        #opens a dialog to manage complexes
        if not self.abstractDb:
            QMessageBox.critical(self.iface.mainWindow(), self.tr("Critical!"), self.tr('Select a database before managing a complex!'))
            return
        dlg = ManageComplexDialog(self.iface, self.abstractDb, self.complexCombo.currentText())
        #connects a signal to update the tree widget when done
        dlg.tableUpdated.connect(self.loadAssociatedFeatures)
        #connects a signal to disassociate features from complex before removal
        dlg.markedToRemove.connect(self.disassociateFeatures)
        result = dlg.exec_()
        if result:
            pass

    @pyqtSlot(bool)
    def on_associatePushButton_clicked(self):
        """
        Slot used to associate features to a complex
        """
        self.associateFeatures()

    @pyqtSlot(bool)
    def on_zoomButton_clicked(self):
        """
        Slot used to zoom the mapcanvas to the features associated to a complex
        """
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
                    feature = next(layer.getFeatures( freq ))
                    if j==0 and i == 0:
                        bbox=feature.geometry().boundingBox()
                    bbox.combineExtentWith(feature.geometry().boundingBox())

            self.iface.mapCanvas().setExtent(bbox)
            self.iface.mapCanvas().refresh()
        else:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Select a complex."))
            return

    def disassociateFeatures(self, toBeRemoved):
        """
        Disassociates features from a complex
        toBeremoved: uuid of the complex that will have all its associated features disassociated
        """
        for uuid in toBeRemoved:
            items = self.treeWidget.findItems(uuid, Qt.MatchRecursive, 1)
            if len(items) == 0:
                return
            complexItem = items[0]
            count = complexItem.childCount()
            for i in range(count):
                self.disassociateAggregatedClass(complexItem.child(i))

    def disassociateAggregatedClass(self, item):
        """
        Disassociates a particular class from a complex
        item: aggregated class to be disassociated
        """
        aggregated_class = item.text(0)
        uuid = item.parent().text(1)
        complex = item.parent().parent().text(0)

        link_column = ''
        try:
            link_column = self.abstractDb.obtainLinkColumn(complex, aggregated_class)
        except Exception as e:
            QMessageBox.critical(self.iface.mainWindow(), self.tr('Critical'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), 'DSG Tools Plugin', Qgis.Critical)

        #getting the layer the needs to be updated
        aggregated_layer = None
        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            #in case of spatialite databases when a complex class is added as a layer it's name has 'complexos_'
            if layer.name() == aggregated_class or layer.name() == 'complexos_'+aggregated_class:
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
        """
        Disassociates a particular feature from a complex
        item: aggregated feature to be disassociated
        """        
        aggregated_class = item.parent().text(0)
        uuid = item.parent().parent().text(1)
        complex = item.parent().parent().parent().text(0)

        link_column = ''
        try:
            link_column = self.abstractDb.obtainLinkColumn(complex, aggregated_class)
        except Exception as e:
            QMessageBox.critical(self.iface.mainWindow(), self.tr('Critical'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), 'DSG Tools Plugin', Qgis.Critical)

        #getting the layer the needs to be updated
        aggregated_layer = None
        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            #in case of spatialite databases when a complex class is added as a layer it's name has 'complexos_'
            if layer.name() == aggregated_class or layer.name() == 'complexos_'+aggregated_class:
                aggregated_layer = layer
                break

        if not aggregated_layer:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("The class you're trying to disassociate must loaded in the table of contents."))
            return

        #feature id that will be updated
        id = item.text(0)
        self.updateLayerOnDisassociate(layer, aggregated_class, link_column, id)

    def updateLayerOnDisassociate(self, layer, aggregated_class, link_column, id):
        """
        Updates the layer upon disassociation from complex
        layer: layer that will be afected
        aggregated_class: aggregated class
        link_column: link column between complex and class
        id: feature id
        """
        try:
            if self.abstractDb.isComplexClass(aggregated_class):
                    self.abstractDb.disassociateComplexFromComplex(aggregated_class, link_column, id)
            else:
                #field index that will be set to NULL
                fieldIndex = [i for i in range(len(layer.dataProvider().fields())) if layer.dataProvider().fields()[i].name() == link_column]
                #attribute pair that will be changed
                attrs = {fieldIndex[0]:None}
                #actual update in the database
                layer.dataProvider().changeAttributeValues({int(id):attrs})
        except Exception as e:
            QMessageBox.critical(self.iface.mainWindow(), self.tr("Critical!"), e.args[0])
            QgsMessageLog.logMessage(':'.join(e.args), 'DSG Tools Plugin', Qgis.Critical)

    @pyqtSlot(bool)
    def on_disassociatePushButton_clicked(self):
        """
        Starts the disassociation process.
        It will firts check the depth of the item that need to be disassociated and them call the correct method to to the job.
        It can be a particular class or a particular feature
        """
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
        """
        Loads all features associated to a complex
        """
        self.treeWidget.clear()

        if self.complexCombo.currentIndex() == 0:
            return

        complex = self.complexCombo.currentText()

        associatedDict = dict()
        try:
            associatedDict = self.abstractDb.loadAssociatedFeatures(complex)
        except Exception as e:
            QMessageBox.critical(self.iface.mainWindow(), self.tr('Critical'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), 'DSG Tools Plugin', Qgis.Critical)
            
        for name in list(associatedDict.keys()):
            for complex_uuid in list(associatedDict[name].keys()):
                self.addAssociatedFeature(complex, name, complex_uuid, None, None)
                for aggregated_class in associatedDict[name][complex_uuid]:
                    for ogc_fid in associatedDict[name][complex_uuid][aggregated_class]:
                        self.addAssociatedFeature(complex, name, complex_uuid, aggregated_class, ogc_fid)

    def depth(self, item):
        """
        Calculates the item deth in the tree
        """
        #calculates the depth of the item
        depth = 0
        while item is not None:
            item = item.parent()
            depth += 1
        return depth

    def associateFeatures(self):
        """
        Associates all features selected in the map canvas to a complex.
        """
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
            if layer.type() != QgsMapLayer.VectorLayer:
                continue
            #case no fetures selected we proceed to the next one
            selectedFeatures = layer.selectedFeatures()
            if len(selectedFeatures) == 0:
                continue

            #obtaining the link column
            column_name = ''
            try:
                column_name = self.abstractDb.obtainLinkColumn(complex, layer.name())
            except Exception as e:
                QMessageBox.critical(self.iface.mainWindow(), self.tr('Critical'), self.tr('A problem occurred! Check log for details.'))
                QgsMessageLog.logMessage(':'.join(e.args), 'DSG Tools Plugin', Qgis.Critical)

            #storing the names of the incompatible layers
            if column_name == '':
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
        """
        Creates tree items
        parent: parent item
        text: item text
        uuid: complex uuid
        """
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
        """
        Adds a feature to a complex
        className: class name
        complexName: complex name
        complexId: complex uuid
        associatedClass: associated class
        associatedId: associated id
        """
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
