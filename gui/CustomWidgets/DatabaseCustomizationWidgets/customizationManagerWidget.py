# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-02-08
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os

# Qt imports
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, Qt, pyqtSignal
from qgis.PyQt.QtWidgets import QMessageBox, QApplication, QFileDialog
from qgis.PyQt.QtGui import QCursor

#DsgTools imports
from DsgTools.core.ServerManagementTools.customizationManager import CustomizationManager
from DsgTools.gui.CustomWidgets.DatabasePropertiesWidgets.BasicPropertyWidgets.genericParameterSetter import GenericParameterSetter
from DsgTools.gui.Misc.PostgisCustomization.createDatabaseCustomization import CreateDatabaseCustomization
from DsgTools.gui.CustomWidgets.DatabasePropertiesWidgets.BasicPropertyWidgets.genericManagerWidget import GenericManagerWidget
from DsgTools.core.Utils.utils import Utils
from DsgTools.core.dsgEnums import DsgEnums

from qgis.core import QgsMessageLog
import json

class CustomizationManagerWidget(GenericManagerWidget):
    def __init__(self, manager = None, parent = None):
        """
        Constructor
        """
        super(CustomizationManagerWidget, self).__init__(genericDbManager = manager, parent = parent)

    def setParameters(self, serverAbstractDb, edgvVersion, dbsDict = {}):
        if serverAbstractDb:
            self.setComponentsEnabled(True)
            self.serverAbstractDb = serverAbstractDb
            self.genericDbManager = CustomizationManager(serverAbstractDb, dbsDict, edgvVersion)
            self.refresh()
        else:
            self.setComponentsEnabled(False)

    @pyqtSlot(bool)
    def on_createPushButton_clicked(self):
        '''
        Slot that opens the create profile dialog
        '''
        paramDlg = GenericParameterSetter()
        if not paramDlg.exec_():
            return
        templateDb, propertyName, edgvVersion = paramDlg.getParameters()
        if edgvVersion == self.tr('Select EDGV Version'):
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Enter a EDGV Version'))
            return
        if propertyName == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Enter an Earth Coverage Name!'))
            return
        if propertyName in list(self.genericDbManager.getPropertyPerspectiveDict(viewType = DsgEnums.Property).keys()):
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Earth Coverage Name already exists!'))
            return
        dlg = CreateDatabaseCustomization(propertyName, templateDb, edgvVersion, self.genericDbManager)
        dlg.exec_()
    
    @pyqtSlot(bool)
    def on_deleteCustomizationPushButton_clicked(self):
        #TODO: Reimplement
        customizationName = self.customizationListWidget.currentItem().text()
        edgvVersion = self.versionSelectionComboBox.currentText()
        if QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to delete customization ')+customizationName+'?', QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.genericDbManager.deleteCustomization(customizationName, edgvVersion)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Customization ') + customizationName + self.tr(' successfully deleted.'))
            self.refreshProfileList()
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem deleting customization: ') + ':'.join(e.args))