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
        email                : borba@dsg.eb.mil.br
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

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QMessageBox, QFileDialog, QWizard
from fileinput import filename
from DsgTools.Utils.utils import Utils

from DsgTools.DbTools.BatchDbCreator.createBatchFromCsv import CreateBatchFromCsv
from DsgTools.DbTools.BatchDbCreator.createBatchIncrementing import CreateBatchIncrementing

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'batchDbCreator.ui'))

class BatchDbCreator(QtGui.QWizard, FORM_CLASS):
    coverageChanged = pyqtSignal()
    def __init__(self, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
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