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
            if 'Complexo' in name:
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
        QObject.connect(self.dlg, SIGNAL(("tableUpdated(PyQt_PyObject)")), self.updateComplexTree)
        result = self.dlg.exec_()
        if result:
            pass
    
    @pyqtSlot(bool)    
    def on_associatePushButton_clicked(self):
        self.dlg = AssociateWithComplexDialog(self.iface, self.db, self.complexCombo.currentText())
        result = self.dlg.exec_()
        if result:
            pass
        
    def updateComplexTree(self, table):
        self.treeWidget.clear()
        for i in range(len(table)):
            row = table[i]
            className = row[0]
            complexName = row[1]
            complexId = row[2]
            self.addComplex(str(className), str(complexName), complexId)
    
    #Function for add a class of a complex
    #className: string of the name of the class
    def addClass(self, className):
        if type(className) is not str:
            return
        sl = [className] #string list that will be appended 
        treeItem = QTreeWidgetItem(sl)
        self.treeWidget.addTopLevelItem(treeItem)
        return treeItem
        
    #Function for add a complex of a specific class
    #className: string of the name of the class
    #complexName: string of the name of complex
    #complexId: string of the id of complex
    def addComplex(self, className, complexName, complexId):
        if (type(className) is not str) or (type(complexName) is not str):
            return
        items = self.treeWidget.findItems(className, Qt.MatchExactly)
        items = [x for x in items if self.__test(x)] #remove lines that aren't a Top Level
            
        if len(items) == 0:
            item = self.addClass(className)
        else:
            item = items[0]
        sl = [complexName, str(complexId)]
        treeItem = QTreeWidgetItem(sl)
        item.addChild(treeItem)
        return treeItem
    
    def __test(self, x):
        if (x.parent() == None) :
            return True
        else:
            return False
    
 
