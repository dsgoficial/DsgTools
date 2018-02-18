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
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt4.QtGui import QMessageBox, QApplication, QCursor, QFileDialog

#DsgTools imports
from DsgTools.ServerManagementTools.fieldToolBoxConfigManager import FieldToolBoxConfigManager
from DsgTools.CustomWidgets.genericParameterSetter import GenericParameterSetter
from DsgTools.CustomWidgets.genericManagerWidget import GenericManagerWidget
from DsgTools.CustomWidgets.genericCompactPropertyManagerWidget import GenericCompactPropertyManagerWidget
from DsgTools.ProductionTools.FieldToolBox.field_setup import FieldSetup
from DsgTools.Utils.utils import Utils
from DsgTools.dsgEnums import DsgEnums

from qgis.core import QgsMessageLog
import json

class AttributeRulesCompactPropertyManagerWidget(GenericCompactPropertyManagerWidget):
    def __init__(self, manager = None, parent = None):
        """
        Constructor
        """
        super(AttributeRulesCompactPropertyManagerWidget, self).__init__(genericDbManager = manager, parent = parent)