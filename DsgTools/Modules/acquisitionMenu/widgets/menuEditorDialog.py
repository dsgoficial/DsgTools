import os, sys, copy
from PyQt5 import QtCore, uic, QtWidgets, QtGui
import json
from DsgTools.Modules.utils.factories.utilsFactory import UtilsFactory

class MenuEditorDialog( QtWidgets.QDialog ):

    def __init__(
            self, 
            controller,
            messageFactory=UtilsFactory().createMessageFactory()
        ):
        super(MenuEditorDialog, self).__init__()
        uic.loadUi( self.getUiPath(), self )
        self.controller = controller
        self.messageFactory = messageFactory

    def showError(self, title, message):
        errorMessageBox = self.messageFactory.createMessage('ErrorMessageBox')
        errorMessageBox.show(self, title, message)

    def showInfo(self, title, message):
        infoMessageBox = self.messageFactory.createMessage('InfoMessageBox')
        infoMessageBox.show(self, title, message)

    def getController(self):
        return self.controller

    def clearLayout(self, layout):
        for idx in list(range(layout.count())):
            item = layout.takeAt( idx )
            widget = item.widget()
            if widget:
                widget.deleteLater()
            layout = item.layout()
            if layout:
                self.clearLayout( layout )
            del item

    def setMenuWidget(self, menuWidget):
        self.menuWidget = menuWidget
        self.menuLayout.addWidget( self.menuWidget )  

    def setTabEditorWidget(self, tabEditorWidget):
        self.tabEditorWidget = tabEditorWidget
        self.tabLayout.addWidget( self.tabEditorWidget )

    def setButtonEditorWidget(self, buttonEditorWidget):
        self.buttonEditorWidget = buttonEditorWidget
        self.buttonLayout.addWidget( self.buttonEditorWidget ) 

    def getUiPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '..',
            'uis', 
            "menuEditorDialog.ui"
        )

    def showTopLevel(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def addPreviewTab(self, tabId, tabName):
        self.menuWidget.addTabContainer( tabId, tabName )

    def updatePreviewTab(self, tabId, tabName):
        self.menuWidget.updateTabContainer( tabId, tabName )

    def deletePreviewTab(self, tabId):
        self.menuWidget.deleteTabContainer( tabId )

    def getPreviewTabNames(self):
        return self.menuWidget.getTabContainerNames()

    def addButtonPreviewMenu(self, buttonConfig, callback):
        self.menuWidget.addButton( buttonConfig, callback)

    def updateButtonPreviewMenu(self, newButtonConfig, oldButtonConfig, callback):
        self.menuWidget.updateButton( newButtonConfig, oldButtonConfig, callback)

    def deleteButtonPreviewMenu(self, buttonConfig):
        self.menuWidget.deleteButton( buttonConfig )

    @QtCore.pyqtSlot(bool)
    def on_importMenuBtn_clicked(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                   '',
                                                   "Desktop",
                                                  '*.json')
        if not filePath[0]:
            return
        with open( filePath[0], 'r') as f:
            menuConfig = json.load( f )
        menuName = menuConfig["menuName"]
        self.menuNameLe.setText( menuName )
        self.menuWidget.setMenuName( menuName )
        for tabData in menuConfig["setup"]:
            self.tabEditorWidget.addRow( tabData['tabId'], tabData['tabName'] )
            self.menuWidget.addTabContainer( tabData['tabId'], tabData['tabName'] )
            for buttonData in tabData['tabButtons']:
                self.buttonEditorWidget.addRow( buttonData['buttonId'], buttonData['buttonTabName'], buttonData['buttonName'], buttonData )
                self.menuWidget.addButton( buttonData, self.buttonEditorWidget.showEditButton )

    @QtCore.pyqtSlot(bool)
    def on_exportMenuBtn_clicked(self):
        menuName = self.menuNameLe.text()
        if not menuName:
            self.showError('Erro', 'Informe o nome do menu!')
            return
        filePath = QtWidgets.QFileDialog.getSaveFileName(
            self, 
            '',
            "{0}.json".format( menuName ),
            '*.json'
        )
        if not filePath[0]:
            return
        self.menuWidget.setMenuName( menuName )
        with open( filePath[0], 'w') as f:
            json.dump( self.menuWidget.dump(), f )

    @QtCore.pyqtSlot(bool)
    def on_createMenuBtn_clicked(self):
        menuName = self.menuNameLe.text()
        if not menuName:
            self.showError('Erro', 'Informe o nome do menu!')
            return
        self.menuWidget.setMenuName( menuName )
        self.getController().createMenuDock( [ self.menuWidget.dump() ] )

    @QtCore.pyqtSlot(bool)
    def on_deleteMenuBtn_clicked(self):
        self.menuWidget.setMenuName( "" )
        self.menuWidget.clean()
        self.tabEditorWidget.clearAllItems()
        self.buttonEditorWidget.clearAllItems()