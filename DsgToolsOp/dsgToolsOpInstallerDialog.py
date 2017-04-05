# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-30
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
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal



FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'dsgToolsOpInstallerDialog.ui'))

class DsgToolsOpInstallerDialog(QtGui.QDialog, FORM_CLASS):
    selectionChanged = pyqtSignal(list,str)

    def __init__(self, dsgToolsInstaller, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.dsgToolsInstaller = dsgToolsInstaller
        self.fileSelector.setType('single')
        self.fileSelector.setTitle(self.tr('Select zip installer'))
        self.fileSelector.setFilter('DsgTools installer (*.zip)')
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        pass