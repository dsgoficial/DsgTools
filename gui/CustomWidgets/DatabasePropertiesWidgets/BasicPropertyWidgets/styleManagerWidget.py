# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-05-17
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from DsgTools.core.ServerManagementTools.styleManager import StyleManager
from DsgTools.gui.CustomWidgets.DatabasePropertiesWidgets.BasicPropertyWidgets.genericParameterSetter import GenericParameterSetter
from DsgTools.gui.CustomWidgets.DatabasePropertiesWidgets.BasicPropertyWidgets.genericManagerWidget import GenericManagerWidget
from DsgTools.core.Utils.utils import Utils
from DsgTools.core.dsgEnums import DsgEnums

from qgis.core import QgsMessageLog
import json

class StyleManagerWidget(GenericManagerWidget):
    def __init__(self, manager = None, parent = None):
        """
        Constructor
        """
        super(self.__class__, self).__init__(genericDbManager = manager, parent = parent)

    def setParameters(self, serverAbstractDb, edgvVersion, dbsDict = {}):
        if serverAbstractDb:
            self.setComponentsEnabled(True)
            self.serverAbstractDb = serverAbstractDb
            self.genericDbManager = StyleManager(serverAbstractDb, dbsDict, edgvVersion)
            self.refresh()
        else:
            self.setComponentsEnabled(False)

    @pyqtSlot(bool)
    def on_createPushButton_clicked(self):
        """
        Slot that opens the create profile dialog
        """
        #TODO
        pass        
    
    def populateConfigInterface(self, templateDb, jsonDict = None):
        '''
        Must be reimplemented in each child
        '''
        #TODO
        pass
    
    def getUpdateSelectedSettingHeader(self):
        header = self.tr('Update Style configuration complete. \n')
        operation = self.tr('style configuration')
        return header, operation

    def getUninstallSelectedSettingHeader(self):
        header = self.tr('Uninstall Style configuration complete. \n')
        operation = self.tr('style configuration')
        return header, operation

    def getApplyHeader(self):
        header = self.tr('Install Style configuration complete. \n')
        operation = self.tr('style configurations')
        return header, operation
    
    def getDeleteHeader(self):
        header = self.tr('Delete Style configuration complete. \n')
        operation = self.tr('style configurations')
        return header, operation
    
    def getUninstallFromSelected(self):
        header = self.tr('Uninstall Style configuration complete. \n')
        operation = self.tr('style configurations')
        return header, operation