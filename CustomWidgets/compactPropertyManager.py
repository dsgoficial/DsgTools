# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-02-16
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt4.QtGui import QMessageBox, QApplication, QCursor, QFileDialog, QMenu, QHeaderView

#DsgTools imports
from DsgTools.CustomWidgets.listSelector import ListSelector
from DsgTools.Utils.utils import Utils
from DsgTools.dsgEnums import DsgEnums

from qgis.core import QgsMessageLog
import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'compactPropertyManager.ui'))

class CompactPropertyManager(QtGui.QWidget, FORM_CLASS):
    Add, Remove, Import, Export, Update = range(5)
    def __init__(self, genericDbManager = None, parent = None):
        """
        Constructor
        """
        super(CompactPropertyManager, self).__init__(parent)
        self.setupUi(self)
        self.changeTooltips('')
        self.genericDbManager = genericDbManager
    
    def changeTooltips(self, propertyName):
        """
        Changes all buttons' tooltips according to propertyName
        """
        self.createPropertyPushButton.setToolTip(self.tr('Add {0}').format(propertyName))
        self.removePropertyPushButton.setToolTip(self.tr('Remove {0}').format(propertyName))
        self.importPropertyPushButton.setToolTip(self.tr('Import {0}').format(propertyName))
        self.exportPropertyPushButton.setToolTip(self.tr('Export {0}').format(propertyName))
        self.updatePropertyPushButton.setToolTip(self.tr('Update {0}').format(propertyName))
    
    def enableButtons(self, enabled):
        """
        Enables or disables all buttons according to boolean enabled
        """
        self.createPropertyPushButton.setEnabled(enabled)
        self.removePropertyPushButton.setEnabled(enabled)
        self.importPropertyPushButton.setEnabled(enabled)
        self.exportPropertyPushButton.setEnabled(enabled)
        self.updatePropertyPushButton.setEnabled(enabled)