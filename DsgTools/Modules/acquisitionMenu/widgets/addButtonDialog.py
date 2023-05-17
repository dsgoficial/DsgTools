import os, sys, copy
from PyQt5 import QtCore, uic, QtWidgets, QtGui
from DsgTools.Modules.utils.factories.utilsFactory import UtilsFactory
import uuid


class AddButtonDialog(QtWidgets.QDialog):
    def __init__(
        self, controller, messageFactory=UtilsFactory().createMessageFactory()
    ):
        super(AddButtonDialog, self).__init__()
        uic.loadUi(self.getUiPath(), self)
        self.controller = controller
        self.messageFactory = messageFactory
        self.uuid = None
        self.tabCombo = None
        self.layerCombo = None
        self.toolCombo = None
        self.attributeTable = None
        self.callback = None
        self.tabNames = []
        self.toolNames = []
        self.layerNames = []
        self.selectedBackgroundColor = ""
        self.selectedTextColor = ""
        self.previewBtn.setText("")
        self.nameLe.textEdited.connect(self.previewBtn.setText)

    def showError(self, title, message):
        errorMessageBox = self.messageFactory.createMessage("ErrorMessageBox")
        errorMessageBox.show(self, title, message)

    def showInfo(self, title, message):
        infoMessageBox = self.messageFactory.createMessage("InfoMessageBox")
        infoMessageBox.show(self, title, message)

    def getController(self):
        return self.controller

    def setSelectedBackgroundColor(self, selectedBackgroundColor):
        self.selectedBackgroundColor = selectedBackgroundColor

    def getSelectedBackgroundColor(self):
        return self.selectedBackgroundColor

    def setSelectedTextColor(self, selectedTextColor):
        self.selectedTextColor = selectedTextColor

    def getSelectedTextColor(self):
        return self.selectedTextColor

    def setAttributeTableWidget(self, attributeTableWidget):
        self.attributeTable = attributeTableWidget
        self.attributeLayout.addWidget(attributeTableWidget)

    def setTabComboWidget(self, tabComboWidget):
        self.tabCombo = tabComboWidget
        self.tabListLayout.addWidget(tabComboWidget)

    def setTabNames(self, tabNames):
        self.tabNames = tabNames
        self.tabCombo.loadItems([i["name"] for i in self.tabNames])

    def setToolComboWidget(self, toolComboWidget):
        self.toolCombo = toolComboWidget
        self.toolListLayout.addWidget(toolComboWidget)

    def setToolNames(self, toolNames):
        self.toolNames = toolNames
        self.toolCombo.clear()
        for toolName in self.toolNames:
            self.toolCombo.addItem(toolName, self.toolNames[toolName])

    def setLayerComboWidget(self, layerComboWidget):
        self.layerCombo = layerComboWidget
        self.layerCombo.currentIndexChanged.connect(self.loadLayerAttribures)
        self.layerListLayout.addWidget(layerComboWidget)

    def setLayerNames(self, layerNames):
        self.layerNames = layerNames
        self.layerCombo.loadItems(layerNames)

    def setUUID(self, uuid):
        self.uuid = uuid

    def getUUID(self):
        return self.uuid if self.uuid else str(uuid.uuid4())

    def showTopLevel(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def getUiPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "..",
            "uis",
            "addButtonDialog.ui",
        )

    def setData(self, buttonConfig):
        self.setUUID(buttonConfig["buttonId"])
        self.nameLe.setText(buttonConfig["buttonName"])
        self.tabCombo.setCurrentIndex(
            self.tabCombo.findText(buttonConfig["buttonTabName"])
        )
        self.toolCombo.setCurrentIndex(
            self.toolCombo.findData(buttonConfig["buttonAcquisitionTool"])
        )
        self.layerCombo.setCurrentIndex(
            self.layerCombo.findText(buttonConfig["buttonLayer"])
        )
        self.setSelectedBackgroundColor(buttonConfig["buttonBackgroundColor"])
        self.backgroundColorBtn.setStyleSheet(
            "QPushButton {background-color: rgb("
            + self.getSelectedBackgroundColor()
            + ")}"
        )
        self.setSelectedTextColor(buttonConfig["buttonTextColor"])
        self.textColorBtn.setStyleSheet(
            "QPushButton {background-color: rgb(" + self.getSelectedTextColor() + ")}"
        )
        self.attributeTable.setAttributesValues(buttonConfig["buttonAttributes"])
        self.keyWordsLe.setText(buttonConfig["buttonKeyWords"])
        self.tooltipLe.setText(buttonConfig["buttonTooltip"])
        self.suppressFormCkb.setChecked(buttonConfig["buttonSuppressForm"])
        self.suppressReclassificationFormCkb.setChecked(buttonConfig.get("buttonSuppressReclassificationForm", False))

        self.previewBtn.setText(buttonConfig["buttonName"])
        self.setColorPreviewButton(
            self.getSelectedTextColor(), self.getSelectedBackgroundColor()
        )

    def setColorPreviewButton(self, textColor, backgroundColor):
        self.previewBtn.setStyleSheet(
            """background-color: rgb({0}); color: rgb({1});""".format(
                backgroundColor, textColor
            )
        )

    def getData(self):
        if not self.validData():
            raise Exception("Dados inválidos!")
        return {
            "buttonId": self.getUUID(),
            "buttonName": self.nameLe.text(),
            "buttonBackgroundColor": self.getSelectedBackgroundColor(),
            "buttonTextColor": self.getSelectedTextColor(),
            "buttonTabName": self.tabCombo.itemText(self.tabCombo.currentIndex()),
            "buttonTabId": [
                i["id"]
                for i in self.tabNames
                if i["name"] == self.tabCombo.itemText(self.tabCombo.currentIndex())
            ][0],
            "buttonAcquisitionTool": self.toolCombo.itemData(
                self.toolCombo.currentIndex()
            ),
            "buttonLayer": self.layerCombo.itemText(self.layerCombo.currentIndex()),
            "buttonAttributes": self.attributeTable.getAttributes(),
            "buttonKeyWords": self.keyWordsLe.text(),
            "buttonTooltip": self.tooltipLe.text(),
            "buttonSuppressForm": self.suppressFormCkb.isChecked(),
            "buttonSuppressReclassificationForm": self.suppressReclassificationFormCkb.isChecked(),
        }

    def validData(self):
        self.tabCombo.setStyleSheet("")
        self.toolCombo.setStyleSheet("")
        self.layerCombo.setStyleSheet("")
        self.nameLe.setStyleSheet("")
        if not self.nameLe.text():
            self.nameLe.setStyleSheet("QLineEdit { border: 1px solid red; }")
            return False
        if not (self.tabCombo.currentText() in [i["name"] for i in self.tabNames]):
            self.tabCombo.setStyleSheet("QComboBox { border: 1px solid red; }")
            return False
        if not (self.toolCombo.currentText() in self.toolNames):
            self.toolCombo.setStyleSheet("QComboBox { border: 1px solid red; }")
            return False
        if not (self.layerCombo.currentText() in self.layerNames):
            self.layerCombo.setStyleSheet("QComboBox { border: 1px solid red; }")
            return False
        return True

    def loadLayerAttribures(self, index):
        attrConfig = self.getController().getAttributesConfigByLayerName(
            self.layerCombo.itemText(index)
        )
        self.attributeTable.loadAttributes(attrConfig)

    @QtCore.pyqtSlot(bool)
    def on_backgroundColorBtn_clicked(self):
        colorRgb = self.openColorDialog(self.getSelectedBackgroundColor())
        self.setSelectedBackgroundColor(colorRgb)
        self.backgroundColorBtn.setStyleSheet(
            "QPushButton {background-color: rgb(" + colorRgb + ")}"
        )
        self.setColorPreviewButton(
            self.getSelectedTextColor(), self.getSelectedBackgroundColor()
        )

    @QtCore.pyqtSlot(bool)
    def on_textColorBtn_clicked(self):
        colorRgb = self.openColorDialog(self.getSelectedTextColor())
        self.setSelectedTextColor(colorRgb)
        self.textColorBtn.setStyleSheet(
            "QPushButton {background-color: rgb(" + colorRgb + ")}"
        )
        self.setColorPreviewButton(
            self.getSelectedTextColor(), self.getSelectedBackgroundColor()
        )

    def openColorDialog(
        self,
        colorRgb,
    ):
        colorDlg = QtWidgets.QColorDialog()
        if colorRgb:
            r, g, b = colorRgb.split(",")
            colorDlg.setCurrentColor(QtGui.QColor(int(r), int(g), int(b)))
        if not colorDlg.exec():
            return
        r, g, b, _ = colorDlg.selectedColor().getRgb()
        return "{0},{1},{2}".format(r, g, b)

    def setCallback(self, callback):
        self.callback = callback

    def getCallback(self):
        return self.callback

    @QtCore.pyqtSlot(bool)
    def on_saveBtn_clicked(self):
        if not self.validData():
            self.showError("Aviso", "Dados inválidos")
            return
        self.accept()
        self.getCallback()(self.getData())

    @QtCore.pyqtSlot(bool)
    def on_cancelBtn_clicked(self):
        self.reject()
