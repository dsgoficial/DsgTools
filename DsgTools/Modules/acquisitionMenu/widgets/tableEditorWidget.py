import os, sys, copy
from PyQt5 import QtCore, uic, QtWidgets, QtGui
from DsgTools.Modules.utils.factories.utilsFactory import UtilsFactory

class TableEditorWidget( QtWidgets.QWidget ):

    def __init__(
            self, 
            controller,
            messageFactory=UtilsFactory().createMessageFactory()
        ):
        super( TableEditorWidget, self).__init__()
        uic.loadUi( self.getUiPath(), self )
        self.controller = controller
        self.messageFactory = messageFactory
        self.tableWidget.horizontalHeader().sortIndicatorOrder()
        self.tableWidget.setSortingEnabled(True)
        
    def getController(self):
        return self.controller

    def createTableToolButton(self, tooltip, iconPath ):
        button = QtWidgets.QPushButton('', self.tableWidget)
        button.setToolTip( tooltip )
        button.setIcon(QtGui.QIcon( iconPath ))
        button.setFixedSize(QtCore.QSize(30, 30))
        button.setIconSize(QtCore.QSize(20, 20))
        return button

    def getSelectedRowData(self):
        rowsData = []
        for item in self.tableWidget.selectionModel().selectedRows():
            rowsData.append( self.getRowData(item.row()) )
        return rowsData

    def getAllTableData(self):
        rowsData = []
        for idx in range(self.tableWidget.rowCount()):
            rowsData.append( self.getRowData(idx) )
        return rowsData

    def validateValue(self, value):
        if value is None:
            return ''
        return str(value)

    def createNotEditableItem(self, value):
        item = QtWidgets.QTableWidgetItem(self.validateValue(value))
        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        return item
    
    def createEditableItem(self, value):
        item = QtWidgets.QTableWidgetItem(self.validateValue(value))
        return item

    def searchRows(self, text):
        for idx in range(self.tableWidget.rowCount()):
            if text and not self.hasTextOnRow(idx, text):
                self.tableWidget.setRowHidden(idx, True)
            else:
                self.tableWidget.setRowHidden(idx, False)                

    def showError(self, title, message):
        errorMessageBox = self.messageFactory.createMessage('ErrorMessageBox')
        errorMessageBox.show(self, title, message)

    def showInfo(self, title, message):
        infoMessageBox = self.messageFactory.createMessage('InfoMessageBox')
        infoMessageBox.show(self, title, message)

    def clearAllItems(self):
        self.tableWidget.setRowCount(0)
    
    def adjustColumns(self):
        self.tableWidget.resizeColumnsToContents()

    def adjustRows(self):
        self.tableWidget.resizeRowsToContents()

    def removeSelected(self):
        while self.tableWidget.selectionModel().selectedRows() :
            self.tableWidget.removeRow(self.tableWidget.selectionModel().selectedRows()[0].row())

    def hasTextOnRow(self, rowIdx, text):
        for colIdx in self.getColumnsIndexToSearch():
            cellText = self.tableWidget.model().index(rowIdx, colIdx).data()
            if cellText and text.lower() in cellText.lower():
                return True
        return False

    def createEditRowWidget(self, row, col):
        wd = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wd)
        index = QtCore.QPersistentModelIndex(self.tableWidget.model().index(row, col))

        editBtn = self.createTableToolButton( 'Editar', self.getEditIconPath() )
        editBtn.clicked.connect(
            lambda *args, index=index: self.handleEditBtn(index)
        )
        layout.addWidget(editBtn)

        deleteBtn = self.createTableToolButton( 'Excluir', self.getDeleteIconPath() )
        deleteBtn.clicked.connect(
            lambda *args, index=index: self.handleDeleteBtn(index)
        )
        layout.addWidget(deleteBtn)

        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setContentsMargins(0,0,0,0)
        return wd

    def getEditIconPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '..',
            'icons', 
            "edit.png"
        )

    def getDeleteIconPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '..',
            'icons', 
            "delete.png"
        )

    @QtCore.pyqtSlot(str)
    def on_searchLe_textEdited(self, text):
        self.searchRows(text)
