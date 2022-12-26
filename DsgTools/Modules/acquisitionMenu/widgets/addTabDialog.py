import os, sys, copy
from PyQt5 import QtCore, uic, QtWidgets, QtGui
import uuid


class AddTabDialog(QtWidgets.QDialog):
    def __init__(self, controller):
        super(AddTabDialog, self).__init__()
        uic.loadUi(self.getUiPath(), self)
        self.controller = controller
        self.uuid = None
        self.callback = None

    def getController(self):
        return self.controller

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
            os.path.abspath(os.path.dirname(__file__)), "..", "uis", "addTabDialog.ui"
        )

    def setData(self, tab):
        self.setUUID(tab["id"])
        self.tabNameLe.setText(tab["name"])

    def getData(self):
        return {"id": self.getUUID(), "name": self.tabNameLe.text()}

    def setCallback(self, callback):
        self.callback = callback

    def getCallback(self):
        return self.callback

    @QtCore.pyqtSlot(bool)
    def on_saveBtn_clicked(self):
        self.accept()
        self.getCallback()(self.getData())

    @QtCore.pyqtSlot(bool)
    def on_cancelBtn_clicked(self):
        self.reject()
