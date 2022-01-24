import os, sys, copy
from PyQt5 import QtCore, uic, QtWidgets, QtGui
from .tableEditorWidget import TableEditorWidget

class TabEditorWidget( TableEditorWidget ):

    def __init__(
            self, 
            controller
        ):
        super( TabEditorWidget, self).__init__( controller=controller )
        self.tableWidget.setColumnHidden(0, True)

    def handleEditBtn(self, index):
        try:
            self.getController().openEditTabDialog(
                self.getRowData( index.row() ),
                self.updateTab
            )
        except Exception as e:
            self.showError('Erro', str(e))

    def handleDeleteBtn(self, index):
        try:
            deletedTabData = self.getRowData( index.row() )
            self.getController().deleteTabMenuEditor( deletedTabData['id'] )
            self.tableWidget.removeRow( index.row() )
        except Exception as e:
            self.showError('Erro', str(e))
       
    def addRow(self, 
            tabId, 
            tabName
        ):
        idx = self.getRowIndex( tabId )
        if idx < 0:
            idx = self.tableWidget.rowCount()
            self.tableWidget.insertRow(idx)
        self.tableWidget.setItem(idx, 0, self.createNotEditableItem( tabId ))
        self.tableWidget.setItem(idx, 1, self.createNotEditableItem(tabName))
        self.tableWidget.setCellWidget(idx, 2, self.createEditRowWidget(idx, 2) )
        
    def addRows(self, tabs):
        self.clearAllItems()
        for tab in tabs:  
            self.addRow(
                tab['id'], 
                tab['name']
            )
        self.adjustColumns()

    def getRowIndex(self, tabId):
        if not tabId:
            return -1
        for idx in range(self.tableWidget.rowCount()):
            if not (
                    tabId == self.tableWidget.model().index(idx, 0).data()
                ):
                continue
            return idx
        return -1

    def getRowData(self, rowIndex):
        return {
            'id': self.tableWidget.model().index(rowIndex, 0).data(),
            'name': self.tableWidget.model().index(rowIndex, 1).data()
        }

    def getColumnsIndexToSearch(self):
        return [1]

    def getUiPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '..',
            'uis', 
            "tabEditorWidget.ui"
        )

    @QtCore.pyqtSlot(bool)
    def on_addBtn_clicked(self):
        try:
            self.getController().openAddTabDialog( self.addTab )
        except Exception as e:
            self.showError('Erro', str(e))

    def addTab(self, data):
        if not data:
            return
        self.getController().addTabMenuEditor( data['id'], data['name'] )
        self.addRow( data['id'], data['name'] )

    def updateTab(self, data):
        if not data:
            return
        self.getController().updateTabMenuEditor( data['id'], data['name'] )
        self.addRow( data['id'], data['name'] )