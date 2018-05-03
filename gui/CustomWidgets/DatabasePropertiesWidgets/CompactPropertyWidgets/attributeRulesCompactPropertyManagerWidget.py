# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-02-24
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
from DsgTools.core.ServerManagementTools.attributeRulesManager import AttributeRulesManager
from DsgTools.gui.CustomWidgets.DatabasePropertiesWidgets.CompactPropertyWidgets.genericCompactPropertyManagerWidget import GenericCompactPropertyManagerWidget
from DsgTools.gui.ProductionTools.Toolboxes.ValidationToolbox.attributeRulesEditor import AttributeRulesEditor
from DsgTools.core.Utils.utils import Utils
from DsgTools.core.dsgEnums import DsgEnums

from qgis.core import QgsMessageLog
import json

class AttributeRulesCompactPropertyManagerWidget(GenericCompactPropertyManagerWidget):
    def __init__(self, manager = None, parent = None):
        """
        Constructor
        """
        super(AttributeRulesCompactPropertyManagerWidget, self).__init__(parent = parent)
    
    def populateConfigInterface(self, templateDb, jsonDict = None):
        '''
        Must be reimplemented in each child
        '''
        dlg = AttributeRulesEditor(templateDb, parameterDict = jsonDict)
        if dlg.exec_():
            return dlg.getParameterDict()
        else:
            return None
    
    def instantiateManagerObject(self, abstractDb, dbDict, edgvVersion):
        return AttributeRulesManager(abstractDb, dbDict, edgvVersion)