#! -*- coding: utf-8 -*-
from PyQt5 import QtCore, uic, QtWidgets, QtGui
import os, sys


class ReclassifyDialog(QtWidgets.QDialog):

    success = QtCore.pyqtSignal(dict)

    def __init__(self, controller):
        super(ReclassifyDialog, self).__init__()
        uic.loadUi(self.getUiPath(), self)
        self.controller = controller
        self.attributeTable = None
        self.callback = None
        self.layersCheckbox = []
        self.layers = []

    def getUiPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "..",
            "uis",
            "reclassifyDialog.ui",
        )

    def getController(self):
        return self.controller

    def setAttributeTableWidget(self, attributeTableWidget):
        self.attributeTable = attributeTableWidget
        self.attributeLayout.addWidget(attributeTableWidget)

    def getAttributeTableWidget(self):
        return self.attributeTable

    def loadLayersStatus(self, layers):
        self.layers = layers
        for l in layers:
            checkBox = self.addLayerCheckBox(l)
            checkBox.setChecked(True)
            self.layersCheckbox.append(checkBox)

    def loadAttributes(self, attributesConfig):
        self.getAttributeTableWidget().loadAttributes(attributesConfig)

    def setAttributesValues(self, attributesValues):
        self.getAttributeTableWidget().setAttributesValues(attributesValues)

    def addLayerCheckBox(self, layer):
        checkBox = QtWidgets.QCheckBox(
            "Camada : {0} >>> Quantidade de selecionados : {1}".format(
                layer.name(), layer.selectedFeatureCount()
            )
        )
        checkBox.layerId = layer.id()
        self.layersFrame.layout().addWidget(checkBox)
        return checkBox

    def getSelectedLayers(self):
        selectedLayerIds = []
        for checkBox in self.layersCheckbox:
            if not checkBox.isChecked():
                continue
            selectedLayerIds.append(checkBox.layerId)
        return [l for l in self.layers if l.id() in selectedLayerIds]

    def getData(self):
        return {
            "layers": self.getSelectedLayers(),
            "attributes": self.getAttributeTableWidget().getAttributes(),
        }

    def showTopLevel(self):
        return self.exec_() == QtWidgets.QDialog.Accepted

    @QtCore.pyqtSlot(bool)
    def on_saveBtn_clicked(self):
        if not self.getSelectedLayers():
            self.reject()
        else:
            self.accept()
            self.success.emit(self.getData())

    @QtCore.pyqtSlot(bool)
    def on_cancelBtn_clicked(self):
        self.reject()
