import os, sys, copy
from PyQt5 import QtCore, uic, QtWidgets, QtGui
from DsgTools.Modules.utils.factories.utilsFactory import UtilsFactory


class AttributeTableWidget(QtWidgets.QWidget):
    def __init__(
        self, controller, messageFactory=None
    ):
        super(AttributeTableWidget, self).__init__()
        uic.loadUi(self.getUiPath(), self)
        self.controller = controller
        self.messageFactory = messageFactory if messageFactory is not None else UtilsFactory().createMessageFactory()
        self.tableWidget.horizontalHeader().sortIndicatorOrder()
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setColumnHidden(0, True)

    def getController(self):
        return self.controller

    def getUiPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "..",
            "uis",
            "attributeTableWidget.ui",
        )

    def getSelectedRowData(self):
        rowsData = []
        for item in self.tableWidget.selectionModel().selectedRows():
            rowsData.append(self.getRowData(item.row()))
        return rowsData

    def validateValue(self, value):
        if value is None:
            return ""
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
        errorMessageBox = self.messageFactory.createMessage("ErrorMessageBox")
        errorMessageBox.show(self, title, message)

    def showInfo(self, title, message):
        infoMessageBox = self.messageFactory.createMessage("InfoMessageBox")
        infoMessageBox.show(self, title, message)

    def clearAllItems(self):
        self.tableWidget.setRowCount(0)

    def adjustColumns(self):
        self.tableWidget.resizeColumnsToContents()

    def adjustRows(self):
        self.tableWidget.resizeRowsToContents()

    def removeSelected(self):
        while self.tableWidget.selectionModel().selectedRows():
            self.tableWidget.removeRow(
                self.tableWidget.selectionModel().selectedRows()[0].row()
            )

    def hasTextOnRow(self, rowIdx, text):
        for colIdx in self.getColumnsIndexToSearch():
            cellText = self.tableWidget.model().index(rowIdx, colIdx).data()
            if cellText and text.lower() in cellText.lower():
                return True
        return False

    def getColumnsIndexToSearch(self):
        return [1]

    def createLineEdit(self):
        wd = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wd)
        lineEdit = QtWidgets.QLineEdit(self.tableWidget)
        layout.addWidget(lineEdit)
        return wd

    def createComboBox(self, values):
        data = {"IGNORAR": None}
        data.update(values)
        wd = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wd)
        comboBox = self.getController().getFilterComboBoxWidget()
        comboBox.loadItems(data)
        layout.addWidget(comboBox)
        return wd

    @QtCore.pyqtSlot(str)
    def on_searchLe_textEdited(self, text):
        self.searchRows(text)

    def loadAttributes(self, attributesConfig):
        self.clearAllItems()
        for attributeName in attributesConfig:
            if "map" in attributesConfig[attributeName]:
                widget = self.createComboBox(
                    self.formatMapValues(attributesConfig[attributeName]["map"])
                )
            else:
                widget = self.createLineEdit()
            self.addRow(None, attributeName, widget)
        self.adjustColumns()
        self.adjustRows()

    def formatMapValues(self, mapValues):
        if not (type(mapValues) is list):
            return mapValues
        newMapValues = {}
        for field in mapValues:
            newMapValues.update(field)
        return newMapValues

    def setAttributesValues(self, attributesValues):
        attributeNames = [key for key in attributesValues]
        for rowIndex in range(self.tableWidget.rowCount()):
            attributeName = self.tableWidget.model().index(rowIndex, 1).data()
            if not (attributeName in attributeNames):
                continue
            attributeValue = attributesValues[attributeName]
            widget = (
                self.tableWidget.cellWidget(rowIndex, 2).layout().itemAt(0).widget()
            )
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.setText(attributeValue)
            else:
                widget.setCurrentIndex(widget.findText(attributeValue))

    def getAttributes(self):
        attributes = {}
        for row in self.getAllTableData():
            attributes[row["attribute"]] = row["value"]
        return attributes

    def addRow(self, attributeId, attributeName, widget):
        idx = self.getRowIndex(attributeId)
        if idx < 0:
            idx = self.tableWidget.rowCount()
            self.tableWidget.insertRow(idx)
        self.tableWidget.setItem(idx, 0, self.createNotEditableItem(attributeId))
        self.tableWidget.setItem(idx, 1, self.createNotEditableItem(attributeName))
        self.tableWidget.setCellWidget(idx, 2, widget)

    def getRowIndex(self, tabId):
        if not tabId:
            return -1
        for idx in range(self.tableWidget.rowCount()):
            if not (tabId == self.tableWidget.model().index(idx, 0).data()):
                continue
            return idx
        return -1

    def getAllTableData(self):
        rowsData = []
        for idx in range(self.tableWidget.rowCount()):
            rowsData.append(self.getRowData(idx))
        return rowsData

    def getRowData(self, rowIndex):
        widget = self.tableWidget.cellWidget(rowIndex, 2).layout().itemAt(0).widget()
        value = (
            widget.text()
            if isinstance(widget, QtWidgets.QLineEdit)
            else widget.itemText(widget.currentIndex())
        )
        return {
            "attribute": self.tableWidget.model().index(rowIndex, 1).data(),
            "value": value,
        }
