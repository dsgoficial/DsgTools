import os, sys, copy
from PyQt5 import QtCore, uic, QtWidgets, QtGui
from .tableEditorWidget import TableEditorWidget
import json


class ButtonEditorWidget(TableEditorWidget):
    def __init__(self, controller):
        super(ButtonEditorWidget, self).__init__(controller=controller)
        self.tableWidget.setColumnHidden(0, True)
        self.tableWidget.setColumnHidden(1, True)
        self.tableWidget.setColumnHidden(3, True)

    def createEditRowWidget(self, row, col):
        wd = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wd)
        index = QtCore.QPersistentModelIndex(self.tableWidget.model().index(row, col))

        editBtn = self.createTableToolButton("Editar", self.getEditIconPath())
        editBtn.clicked.connect(lambda *args, index=index: self.handleEditBtn(index))
        layout.addWidget(editBtn)

        deleteBtn = self.createTableToolButton("Excluir", self.getDeleteIconPath())
        deleteBtn.clicked.connect(
            lambda *args, index=index: self.handleDeleteBtn(index)
        )
        layout.addWidget(deleteBtn)

        cloneBtn = self.createTableToolButton("Clonar", self.getCloneIconPath())
        cloneBtn.clicked.connect(lambda *args, index=index: self.handleCloneBtn(index))
        layout.addWidget(cloneBtn)

        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        return wd

    def getCloneIconPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", "icons", "clone.png"
        )

    def handleEditBtn(self, index):
        self.showEditButton(self.getRowData(index.row()))

    def handleDeleteBtn(self, index):
        try:
            deletedButtonData = self.getRowData(index.row())
            self.getController().deleteButtonMenuEditor(deletedButtonData)
            self.tableWidget.removeRow(index.row())
        except Exception as e:
            self.showError("Erro", str(e))

    def handleCloneBtn(self, index):
        self.getController().openCloneButtonDialog(
            self.getRowData(index.row()), self.addButton
        )

    def showEditButton(self, buttonConfig):
        try:
            self.getController().openEditButtonDialog(
                buttonConfig,
                lambda data, oldData=buttonConfig, callback=self.showEditButton: self.updateButton(
                    data, oldData, callback
                ),
            )
        except Exception as e:
            self.showError("Erro", str(e))

    def addRow(self, buttonId, buttonTab, buttonName, buttonConfig):
        idx = self.getRowIndex(buttonId)
        if idx < 0:
            idx = self.tableWidget.rowCount()
            self.tableWidget.insertRow(idx)
        self.tableWidget.setItem(idx, 0, self.createNotEditableItem(buttonId))
        self.tableWidget.setItem(idx, 1, self.createNotEditableItem(buttonTab))
        self.tableWidget.setItem(idx, 2, self.createNotEditableItem(buttonName))
        self.tableWidget.setItem(
            idx, 3, self.createNotEditableItem(json.dumps(buttonConfig))
        )
        self.tableWidget.setCellWidget(idx, 4, self.createEditRowWidget(idx, 4))
        self.adjustRows()

    def addRows(self, tabs):
        self.clearAllItems()
        for tab in tabs:
            self.addRow(tab["id"], tab["name"])
        self.adjustColumns()

    def getRowIndex(self, buttonId):
        if not buttonId:
            return -1
        for idx in range(self.tableWidget.rowCount()):
            if not (buttonId == self.tableWidget.model().index(idx, 0).data()):
                continue
            return idx
        return -1

    def getRowData(self, rowIndex):
        return json.loads(self.tableWidget.model().index(rowIndex, 3).data())

    def getColumnsIndexToSearch(self):
        return [1]

    def getUiPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "..",
            "uis",
            "buttonEditorWidget.ui",
        )

    @QtCore.pyqtSlot(bool)
    def on_addBtn_clicked(self):
        try:
            self.getController().openAddButtonDialog(self.addButton)
        except Exception as e:
            self.showError("Erro", str(e))

    def addButton(self, data):
        if not data:
            return
        self.getController().addButtonMenuEditor(data, self.showEditButton)
        self.addRow(data["buttonId"], data["buttonTabName"], data["buttonName"], data)

    def updateButton(self, newData, oldData, callback):
        if not newData:
            return
        self.getController().updateButtonMenuEditor(newData, oldData, callback)
        self.addRow(
            newData["buttonId"],
            newData["buttonTabName"],
            newData["buttonName"],
            newData,
        )
