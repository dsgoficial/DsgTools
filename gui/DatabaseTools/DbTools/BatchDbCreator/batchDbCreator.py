# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-24
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
import json

from qgis.PyQt import QtGui, uic, QtWidgets
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QMessageBox, QFileDialog, QWizard
from fileinput import filename
from DsgTools.core.Utils.utils import Utils
from DsgTools.gui.DatabaseTools.DbTools.BatchDbCreator.createBatchFromCsv import CreateBatchFromCsv
from DsgTools.gui.DatabaseTools.DbTools.BatchDbCreator.createBatchIncrementing import CreateBatchIncrementing

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'batchDbCreator.ui'))

class BatchDbCreator(QtWidgets.QWizard, FORM_CLASS):
    coverageChanged = pyqtSignal()
    def __init__(self, manager, parentButton, parentMenu, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.manager = manager
        self.parentButton = parentButton
        self.parentMenu = parentMenu
        self.parent = parent
        self.setupUi(self)
        self.sequenceDict = {'CreateBatchFromCsv':1, 'CreateBatchIncrementing':2, 'CreateBatchBasedOnList':3}
        
        self.setPage(self.sequenceDict['CreateBatchFromCsv'],CreateBatchFromCsv())
        self.setPage(self.sequenceDict['CreateBatchIncrementing'],CreateBatchIncrementing())
    
    def nextId(self):
        if self.currentId() == 0:
            if self.csvRadioButton.isChecked():
                return self.sequenceDict['CreateBatchFromCsv']
            elif self.patternRadioButton.isChecked():
                return self.sequenceDict['CreateBatchIncrementing']
            else:
                return self.currentId()
        elif self.currentId() == self.sequenceDict['CreateBatchFromCsv']:
            return -1
        elif self.currentId() == self.sequenceDict['CreateBatchIncrementing']:
            return -1
        else:
            return -1

    def initGui(self):
        """
        Instantiates user interface and prepare it to be called whenever tool button is activated. 
        """
        callback = lambda : self.manager.createDatabase(isBatchCreation=True)
        self.manager.addTool(
            text=self.tr('Create batches of PostGIS, SpatiaLite or Geopackage Databases'),
            callback=callback,
            parentMenu=self.parentMenu,
            icon='batchDatabase.png',
            parentButton=self.parentButton,
            defaultButton=False
        )

    def unload(self):
        pass