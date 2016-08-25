# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
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
from PyQt4.QtCore import *
from PyQt4.QtGui import QMessageBox, QFileDialog
from fileinput import filename
from DsgTools.Utils.utils import Utils

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'createBatchIncrementingSpatialite.ui'))

class CreateBatchIncrementingSpatialite(QtGui.QWizardPage, FORM_CLASS):
    coverageChanged = pyqtSignal()
    def __init__(self, parent=None):
        '''Constructor.'''
        super(self.__class__, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.outputDirSelector.setCaption(self.tr('Select the output dir'))
        self.outputDirSelector.setFilter(self.tr('Comma Separated Values File (*.csv)'))
        self.outputDirSelector.setType('dir')
        self.outputDirSelector.setTitle(self.tr('Output Directory'))
    
    def getParameters(self):
        #Get outputDir, outputDbNameList, refSys
        pass
    
    def getOutputDbNameList(self):
        prefix = None
        sufix = None
        dbBaseName = self.dbNameLineEdit.text()
        outputDbNameList = []
        if self.prefixLineEdit.text() <> '':
            prefix = self.prefixLineEdit.text()
        if self.sufixLineEdit.text() <> '':
            sufix = self.prefixLineEdit.text()
        for i in range(self.spinBox.value()):
            attrNameList = []
            if prefix:
                attrNameList.append(prefix)
            attrNameList.append(dbBaseName+str(i+1))
            if sufix:
                attrNameList.append(sufix)
            dbName = '_'.join(attrNameList)
            outputDbNameList.append(dbName)
        return outputDbNameList

    def validatePage(self):
        if self.dbNameLineEdit.text() == '':
            return False
        if self.outputDirSelector.fileNameList == []:
            return False
        return True