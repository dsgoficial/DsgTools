import os, sys, copy
from PyQt5 import QtCore, uic, QtWidgets, QtGui
import json
from DsgTools.Modules.utils.factories.utilsFactory import UtilsFactory


class MenuDock(QtWidgets.QDockWidget):
    def __init__(
        self, controller, messageFactory=None
    ):
        super(MenuDock, self).__init__()
        uic.loadUi(self.getUiPath(), self)
        self.controller = controller
        self.menuWidget = None
        self.currentMenu = None
        self.currentButton = None
        self.messageFactory = messageFactory if messageFactory is not None else UtilsFactory().createMessageFactory()
        self.menusCb.currentIndexChanged.connect(self.setCurrentMenu)

    def showError(self, title, message):
        errorMessageBox = self.messageFactory.createMessage("ErrorMessageBox")
        errorMessageBox.show(self, title, message)

    def showInfo(self, title, message):
        infoMessageBox = self.messageFactory.createMessage("InfoMessageBox")
        infoMessageBox.show(self, title, message)

    def getController(self):
        return self.controller

    def getUiPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", "uis", "menuDock.ui"
        )

    def loadMenus(self, menuConfigs):
        self.menusCb.clear()
        for menuConfig in menuConfigs:
            self.menusCb.addItem(menuConfig["menuName"], menuConfig)

    def setCurrentMenu(self, menuIndex):
        self.currentMenu = self.menusCb.itemData(menuIndex)
        self.getMenuWidget().load(self.currentMenu, self.setCurrentButton)

    def setMenuWidget(self, menuWidget):
        self.menuWidget = menuWidget
        self.menuLayout.addWidget(self.menuWidget)

    def getMenuWidget(self):
        return self.menuWidget

    def setCurrentButton(self, buttonConfig):
        try:
            if self.reclassifyCkb.isChecked():
               self.getController().validLayersToReclassification(buttonConfig)

            currentButton = self.getCurrentButtonConfig()
            if currentButton:
                self.getController().deactiveMenuButton(currentButton)
            self.setCurrentButtonConfig(buttonConfig)
            self.getController().activeMenuButton(buttonConfig)
            if not self.reclassifyCkb.isChecked():
                return
            self.getController().openReclassifyDialog(buttonConfig, self.reclassify)
        except Exception as e:
            self.showError("Erro", str(e))

    def getCurrentButtonConfig(self):
        return self.currentButton

    def setCurrentButtonConfig(self, buttonConfig):
        self.currentButton = buttonConfig

    @QtCore.pyqtSlot(str)
    def on_searchButtonLe_textEdited(self, text):
        self.getMenuWidget().searchButtons(text)

    def reclassify(self, reclassifyData):
        if not reclassifyData:
            return
        self.getController().reclassify(self.getCurrentButtonConfig(), reclassifyData)
