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
from associateWithComplex import AssociateWithComplexDialog

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
        
        QObject.connect(self.dbButton, SIGNAL(("clicked()")), self.getDataSources)
        QObject.connect(self.dbCombo, SIGNAL("activated(int)"), self.updateComplexClass)
        QObject.connect(self.complexCombo, SIGNAL("activated(int)"), self.loadAssociatedFeatures)
        
        self.iface = iface
        
        self.db = None
        self.databases = None
        
    def __del__(self):
        if self.db:
            self.db.close()
            self.db = None        
        
    def updateComplexClass(self):
        if self.db:
            self.db.close()
            self.db = None
            
        dbName = self.dbCombo.currentText()
        dataSourceUri = self.databases[dbName]
        if ".sqlite" in dbName:
            self.db = QSqlDatabase("QSQLITE")  
            self.db.setDatabaseName(dbName)
        else:
            self.db = QSqlDatabase("QPSQL")
            self.db.setDatabaseName(dbName)
            self.db.setHostName(dataSourceUri.host())
            self.db.setPort(int(dataSourceUri.port()))
            self.db.setUserName(dataSourceUri.username())
            self.db.setPassword(dataSourceUri.password())
        self.db.open()
        
        self.populateComboBox()

    def populateComboBox(self):
        #getting all complex tables
        self.complexCombo.clear()
        
        query = QSqlQuery("SELECT name FROM sqlite_master WHERE type='table'", self.db)
        while query.next():
            name = query.value(0)
            if 'complexos_' in name:
                self.complexCombo.addItem(query.value(0))
        
    def getDataSources(self):
        if self.databases:
            self.databases.clear()
            
        self.databases = dict()
        self.layers = self.iface.mapCanvas().layers()
        for layer in self.layers:
            dataSourceUri = QgsDataSourceURI( layer.dataProvider().dataSourceUri() )
            dbName = dataSourceUri.database()
            if dbName not in self.databases:
                self.databases[dbName] = dataSourceUri
                self.dbCombo.addItem(dbName)
    
    @pyqtSlot(bool)    
    def on_managePushButton_clicked(self):
        self.dlg = ManageComplexDialog(self.iface, self.db, self.complexCombo.currentText())
        QObject.connect(self.dlg, SIGNAL(("tableUpdated()")), self.loadAssociatedFeatures)
        result = self.dlg.exec_()
        if result:
            pass
    
    @pyqtSlot(bool)    
    def on_associatePushButton_clicked(self):
        self.associateFeatures()
        
    def loadAssociatedFeatures(self):
        self.treeWidget.clear()
        complex = self.complexCombo.currentText()
        complex = '\''+complex.replace("complexos_","")+'\''
        sql = "SELECT complex_schema, complex, aggregated_schema, aggregated_class, column_name from complex_metadata where complex = "+complex
        query = QSqlQuery(sql, self.db)
        while query.next():
            complex_schema = query.value(0)
            complex = query.value(1)
            aggregated_schema = query.value(2)
            aggregated_class = query.value(3)
            column_name = query.value(4)            
            sql = "SELECT id, nome from "+complex_schema+"_"+complex
            complexQuery = QSqlQuery(sql, self.db)
            while complexQuery.next():
                complex_uuid = complexQuery.value(0)
                name = complexQuery.value(1)
                self.addAssociatedFeature(complex_schema+"_"+complex, name, complex_uuid, None, None)
                
                sql = "SELECT OGC_FID from "+aggregated_schema+"_"+aggregated_class+" where "+column_name+"="+complex_uuid
                associatedQuery = QSqlQuery(sql, self.db)
                while associatedQuery.next():
                    ogc_fid = associatedQuery.value(0)
                    self.addAssociatedFeature(str(complex_schema+"_"+complex), str(name), complex_uuid, str(aggregated_schema+"_"+aggregated_class), ogc_fid)
                    
    def depth(self, item):
        depth = 0
        while item is not None:
            item = item.parent()
            depth += 1
        return depth
                         
    def associateFeatures(self):
        root = self.treeWidget.invisibleRootItem()
        if len(self.treeWidget.selectedItems()) == 0:
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", "Please, select a complex.")
            return
            
        item = self.treeWidget.selectedItems()[0]
        father = item.parent()
        grandFather = father.parent()
        if self.depth(item) != 2:
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", "Please, select a complex.")
            return
        
        complex = self.complexCombo.currentText()
        complex = '\''+complex.replace("complexos_","")+'\''

        #uuid to be adjust on the selected features
        uuid = item.text(1)
        
        #getting the selected features
        forbiddenLayers = []
        self.layers = self.iface.mapCanvas().layers()
        for layer in self.layers:
            selectedFeatures = layer.selectedFeatures()
            if len(selectedFeatures) == 0:
                continue
            
            sql = "SELECT column_name from complex_metadata where complex = "+complex+" and aggregated_class = "+'\''+layer.name()[3:]+'\''
            query = QSqlQuery(sql, self.db)
            column_name = ""
            while query.next():
                column_name = query.value(0)

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
                                            
        if len(forbiddenLayers) > 0:
            message = ""
            message += "The following layers cannot be associated to complexes from "+self.complexCombo.currentText()+":\n"
            for text in forbiddenLayers:
                message += text+"\n"
            print message
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", message)

        self.loadAssociatedFeatures()

    def createTreeItem(self, parent, text, uuid = -1):
        count = parent.childCount()
        children = []
        for i in range(count):
            child = parent.child(i)
            children.append(child.text(0))
        
        if text not in children:
            item = QTreeWidgetItem(parent)
            item.setText(0,text)
            if uuid != -1:
                item.setText(1, str(uuid))
        else:
            for i in range(count):
                child = parent.child(i)
                if child.text(0) == text:
                    item = child
        return item
    
    def addAssociatedFeature(self, className, complexName, complexId, associatedClass, associatedId):        
        classNameItem = self.createTreeItem(self.treeWidget.invisibleRootItem(), className)        
        complexNameItem = self.createTreeItem(classNameItem, complexName, complexId)
        if associatedClass and associatedId:
            associatedClassItem = self.createTreeItem(complexNameItem, associatedClass)
            self.createTreeItem(associatedClassItem, str(associatedId))

    def __test(self, x):
        if (x.parent() == None) :
            return True
        else:
            return False
