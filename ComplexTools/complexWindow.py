# -*- coding: utf-8 -*-
import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QTreeWidgetItem
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
        self.dlg = AssociateWithComplexDialog(self.iface, self.db, self.complexCombo.currentText())
        result = self.dlg.exec_()
        if result:
            pass
        
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
                         
    def showComplexTree(self):
        self.treeWidget.clear()
        table = self.complexCombo.currentText()
        query = QSqlQuery("SELECT id, nome from "+table, self.db)
        while query.next():
            id = query.value(0)
            name = query.value(1)
            self.addComplex(str(table), str(name), id)
    
    def createTreeItem(self, parent, text):
        count = parent.childCount()
        children = []
        for i in range(count):
            child = parent.child(i)
            children.append(child.text(0))
        
        if text not in children:
            item = QTreeWidgetItem(parent)
            item.setText(0,text)
        else:
            for i in range(count):
                child = parent.child(i)
                if child.text(0) == text:
                    item = child
        return item
    
    def addAssociatedFeature(self, className, complexName, complexId, associatedClass, associatedId):        
        classNameItem = self.createTreeItem(self.treeWidget.invisibleRootItem(), className)        
        complexNameItem = self.createTreeItem(classNameItem, complexName)
        if associatedClass and associatedId:
            associatedClassItem = self.createTreeItem(complexNameItem, associatedClass)
            self.createTreeItem(associatedClassItem, str(associatedId))

    def __test(self, x):
        if (x.parent() == None) :
            return True
        else:
            return False
