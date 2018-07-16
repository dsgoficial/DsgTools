# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-07-16
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
from __future__ import print_function
import os
from qgis.core import QgsMessageLog, Qgis, QgsTask, QgsApplication
from DsgTools.gui.ProductionTools.Toolboxes.ValidationToolbox.processParametersDialog import ProcessParametersDialog

from qgis.PyQt.QtCore import Qt
from qgis.PyQt import QtGui
from qgis.PyQt.QtWidgets import QMessageBox, QApplication, QMenu
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.Qt import QObject

class ParameterFetcher(QObject):
    def __init__(self):
        """
        Constructor
        """
        super(ParameterFetcher, self).__init__()
    
    def fetch(self, processChain, parameterDict, restoreOverride = True):
        """
        Builds interface
        """
        processText = ', '.join([process.processAlias for process in processChain])
        dlgTitle = self.tr('Process parameters setter for process(es) {0}').format(processText)
        dlg = ProcessParametersDialog(None, parameterDict, title=dlgTitle, restoreOverride = restoreOverride)
        if dlg.exec_() == 0:
            return -1
        # get parameters
        params = dlg.values
        return params