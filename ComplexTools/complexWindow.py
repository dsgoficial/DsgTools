# -*- coding: utf-8 -*-
import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QTreeWidgetItem, QMessageBox
from PyQt4.QtSql import QSqlQueryModel, QSqlTableModel,QSqlDatabase,QSqlQuery

from qgis.core import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'complexWindow_base.ui'))

from manageComplex import ManageComplexDialog
#from associateWithComplex import AssociateWithComplexDialog

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
        
        QObject.connect(self.dbButton, SIGNAL(("clicked()")), self.getDataSources)
        QObject.connect(self.dbCombo, SIGNAL("activated(int)"), self.updateComplexClass)
        QObject.connect(self.complexCombo, SIGNAL("activated(int)"), self.loadAssociatedFeatures)
        QObject.connect(self.iface, SIGNAL("newProjectCreated()"), self.clearDock)        
        
        self.db = None
        self.databases = None
        
    def __del__(self):
        if self.db:
            self.db.close()
            self.db = None        

    def clearDock(self):
        self.treeWidget.clear()
        self.dbCombo.clear()
        self.complexCombo.clear()
        
    def isSpatialiteDatabase(self, dbName):
        (dataSourceUri, credentials) = self.databases[dbName]
        if dataSourceUri.host() == "":
            return True
        return False
        
    def getUserCredentials(self, lyr):
        connInfo = QgsDataSourceURI( lyr.dataProvider().dataSourceUri() ).connectionInfo()
        (success, user, passwd ) = QgsCredentials.instance().get( connInfo, None, None )
        # Put the credentials back (for yourself and the provider), as QGIS removes it when you "get" it
        if success:
            QgsCredentials.instance().put( connInfo, user, passwd )   
            
        return (user, passwd)     
        
    def updateComplexClass(self):
        if self.db:
            self.db.close()
            self.db = None
            
        if self.dbCombo.currentIndex() == 0:
            return
            
        dbName = self.dbCombo.currentText()
        (dataSourceUri, credentials) = self.databases[dbName]
        #verifying the connection type
        if self.isSpatialiteDatabase(dbName):
            self.db = QSqlDatabase("QSQLITE")  
            self.db.setDatabaseName(dbName)
        else:
            self.db = QSqlDatabase("QPSQL")
            self.db.setDatabaseName(dbName)
            self.db.setHostName(dataSourceUri.host())
            self.db.setPort(int(dataSourceUri.port()))
            self.db.setUserName(credentials[0])
            self.db.setPassword(credentials[1])
        if not self.db.open():
            print self.db.lastError().text()
        
        self.populateComboBox()

    def populateComboBox(self):
        #getting all complex tables
        self.complexCombo.clear()
        self.complexCombo.addItem("select a complex class")
        
        dbName = self.dbCombo.currentText()
        (dataSourceUri, credentials) = self.databases[dbName]
        if self.isSpatialiteDatabase(dbName):
            #getting all complex tables
            query = QSqlQuery("SELECT name FROM sqlite_master WHERE type='table'", self.db)
            while query.next():
                name = query.value(0)
                if 'complexos_' in name:
                    self.complexCombo.addItem(query.value(0))
        else:
            #getting all complex tables
            query = QSqlQuery("select distinct table_name from information_schema.columns where table_schema = 'complexos'", self.db)
            while query.next():
                self.complexCombo.addItem(query.value(0))            
        
    def getDataSources(self):
        self.dbCombo.clear()
        self.dbCombo.addItem("select a database")
        
        if self.databases:
            self.databases.clear()
        
        #dictionary of names and datasourceUri
        self.databases = dict()
        self.layers = self.iface.mapCanvas().layers()
        for layer in self.layers:
            dataSourceUri = QgsDataSourceURI( layer.dataProvider().dataSourceUri() )
            dbName = dataSourceUri.database()
            if dbName not in self.databases:
                self.databases[dbName] = (dataSourceUri,self.getUserCredentials(layer))
                #populating the combo
                self.dbCombo.addItem(dbName)
    
    @pyqtSlot(bool)    
    def on_managePushButton_clicked(self):
        #opens a dialog to manage complexes
        if self.isSpatialiteDatabase(self.dbCombo.currentText()):
            self.dlg = ManageComplexDialog(self.iface, self.db, self.complexCombo.currentText())
        else:
            self.dlg = ManageComplexDialog(self.iface, self.db, 'complexos.'+self.complexCombo.currentText())
        #connectes a signal to update the tree widget when done
        QObject.connect(self.dlg, SIGNAL(("tableUpdated()")), self.loadAssociatedFeatures)
        result = self.dlg.exec_()
        if result:
            pass
    
    @pyqtSlot(bool)    
    def on_associatePushButton_clicked(self):
        self.associateFeatures()
        
    @pyqtSlot(bool)    
    def on_zoomButton_clicked(self):
        #case no item is selected we should warn the user
        if len(self.treeWidget.selectedItems()) == 0:
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", "Please, select an item to zoom.")
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
                    QMessageBox.warning(self.iface.mainWindow(), "Warning!", "The associated classes must be loaded in the table of contents.")
                    return

                for j in range(aggregated_item.childCount()):
                    id = aggregated_item.child(i).text(0)
                    freq = QgsFeatureRequest() 
                    freq.setFilterFid(int(id)) 
                    feature = layer.getFeatures( freq ).next()
                    bbox.unionRect(feature.geometry().boundingBox())
                
            self.iface.mapCanvas().setExtent(bbox)
            self.iface.mapCanvas().refresh()
        else:
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", "Select a complex.")
            return
        
    def getAdjustedComplexName(self, dbName, complex):
        if self.isSpatialiteDatabase(dbName):
            complex = '\''+complex.replace("complexos_","")+'\''
        else:
            complex = '\''+complex+'\''
        return complex
        
    @pyqtSlot(bool)    
    def on_disassociatePushButton_clicked(self):
        #case no item is selected we should warn the user
        if len(self.treeWidget.selectedItems()) == 0:
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", "Please, select an aggregated class or aggregated id.")
            return
            
        item = self.treeWidget.selectedItems()[0]
        #checking if the item is a complex (it should have depth = 2)
        if self.depth(item) == 3:
            aggregated_class = item.text(0)
            uuid = item.parent().text(1)
            complex = item.parent().parent().text(0)
            complex = self.getAdjustedComplexName(self.dbCombo.currentText(), complex)
            link_column = self.obtainLinkColumn(complex, aggregated_class)
            
            #getting the layer the needs to be updated
            aggregated_layer = None
            layers = self.iface.mapCanvas().layers()
            for layer in layers:
                if layer.name() == aggregated_class:
                    aggregated_layer = layer
                    break
                
            if not aggregated_layer:
                QMessageBox.warning(self.iface.mainWindow(), "Warning!", "The class you're trying to disassociate must loaded in the table of contents.")
                return
                
            for i in range(item.childCount()):
                #feature id that will be updated
                id = item.child(i).text(0)
                #field index that will be set to NULL
                fieldIndex = [i for i in range(len(layer.dataProvider().fields())) if layer.dataProvider().fields()[i].name() == link_column]  
                #attribute pair that will be changed
                attrs = {fieldIndex[0]:None}
                #actual update in the database
                from ctypes.wintypes import INT
                layer.dataProvider().changeAttributeValues({int(id):attrs})
        elif self.depth(item) == 4:
            aggregated_class = item.parent().text(0)
            uuid = item.parent().parent().text(1)
            complex = item.parent().parent().parent().text(0)
            complex = self.getAdjustedComplexName(self.dbCombo.currentText(), complex)
            link_column = self.obtainLinkColumn(complex, aggregated_class)

            #getting the layer the needs to be updated
            aggregated_layer = None
            layers = self.iface.mapCanvas().layers()
            for layer in layers:
                if layer.name() == aggregated_class:
                    aggregated_layer = layer
                    break    

            if not aggregated_layer:
                QMessageBox.warning(self.iface.mainWindow(), "Warning!", "The class you're trying to disassociate must loaded in the table of contents.")
                return

            #feature id that will be updated
            id = item.text(0)
            #field index that will be set to NULL
            fieldIndex = [i for i in range(len(layer.dataProvider().fields())) if layer.dataProvider().fields()[i].name() == link_column]  
            #attribute pair that will be changed
            attrs = {fieldIndex[0]:None}
            #actual update in the database
            layer.dataProvider().changeAttributeValues({int(id):attrs})
        else:
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", "Please, select an aggregated class or aggregated id.")
            return            
            
        self.loadAssociatedFeatures()
        
    def loadAssociatedFeatures(self):
        self.treeWidget.clear()
        
        if self.complexCombo.currentIndex() == 0:
            return
        
        complex = self.complexCombo.currentText()
        complex = self.getAdjustedComplexName(self.dbCombo.currentText(), complex)
            
        #query to get the possible links to the selected complex in the combobox
        sql = "SELECT complex_schema, complex, aggregated_schema, aggregated_class, column_name from complex_schema where complex = "+complex
        query = QSqlQuery(sql, self.db)
        print sql
        while query.next():
            #setting the variables
            complex_schema = query.value(0)
            complex = query.value(1)
            aggregated_schema = query.value(2)
            aggregated_class = query.value(3)
            column_name = query.value(4)
            
            #query to obtain the created complexes
            if self.isSpatialiteDatabase(self.dbCombo.currentText()):
                sql = "SELECT id, nome from "+complex_schema+"_"+complex
            else:
                sql = "SELECT id, nome from "+complex_schema+"."+complex

            complexQuery = QSqlQuery(sql, self.db)
            while complexQuery.next():
                complex_uuid = complexQuery.value(0)
                name = complexQuery.value(1)
                
                if not (complex_uuid and name):
                    continue
                #adding the information in the tree widget case there are no associated features
                if self.isSpatialiteDatabase(self.dbCombo.currentText()):
                    self.addAssociatedFeature(complex_schema+"_"+complex, name, complex_uuid, None, None)
                else:
                    self.addAssociatedFeature(complex, name, complex_uuid, None, None)
                
                #query to obtain the id of the associated feature
                if self.isSpatialiteDatabase(self.dbCombo.currentText()):
                    sql = "SELECT OGC_FID from "+aggregated_schema+"_"+aggregated_class+" where "+column_name+"="+'\''+complex_uuid+'\''
                else:
                    sql = "SELECT id from "+aggregated_schema+"."+aggregated_class+" where "+column_name+"="+'\''+complex_uuid+'\''

                associatedQuery = QSqlQuery(sql, self.db)
                
                while associatedQuery.next():
                    ogc_fid = associatedQuery.value(0)
                    #adding the information in the tree widget
                    if self.isSpatialiteDatabase(self.dbCombo.currentText()):
                        self.addAssociatedFeature(str(complex_schema+"_"+complex), str(name), complex_uuid, str(aggregated_schema+"_"+aggregated_class), ogc_fid)
                    else:
                        self.addAssociatedFeature(str(complex), str(name), complex_uuid, str(aggregated_class), ogc_fid)
                    
    def depth(self, item):
        #calculates the depth of the item
        depth = 0
        while item is not None:
            item = item.parent()
            depth += 1
        return depth

    def obtainLinkColumn(self, complexClass, aggregatedClass):
        #query to obtain the link column between the complex and the feature layer
        if self.isSpatialiteDatabase(self.dbCombo.currentText()):
            sql = "SELECT column_name from complex_schema where complex = "+complexClass+" and aggregated_class = "+'\''+aggregatedClass[3:]+'\''
        else:
            sql = "SELECT column_name from complex_schema where complex = "+complexClass+" and aggregated_class = "+'\''+aggregatedClass+'\''
            
        query = QSqlQuery(sql, self.db)
        column_name = ""
        while query.next():
            column_name = query.value(0)
        return column_name

    def associateFeatures(self):
        #case no item is selected we should warn the user
        if len(self.treeWidget.selectedItems()) == 0:
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", "Please, select a complex.")
            return
            
        item = self.treeWidget.selectedItems()[0]
        #checking if the item is a complex (it should have depth = 2)
        if self.depth(item) != 2:
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", "Please, select a complex.")
            return
        
        complex = self.complexCombo.currentText()
        #surrounding the name with ''
        complex = self.getAdjustedComplexName(self.dbCombo.currentText(), complex)

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
            column_name = self.obtainLinkColumn(complex, layer.name())
            
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
            message += "The following layers cannot be associated to complexes from "+self.complexCombo.currentText()+":\n"
            for text in forbiddenLayers:
                message += text+"\n"
            print message
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", message)

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
