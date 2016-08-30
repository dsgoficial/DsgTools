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
    os.path.dirname(__file__), 'tabDbSelectorWidget.ui'))

class TabDbSelectorWidget(QtGui.QWidget, FORM_CLASS):
    selectionChanged = pyqtSignal(list,str)

    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.serverWidget.populateServersCombo()
        self.outputDirSelector.setType('dir')
    
    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self):
        self.serverWidget.clearAll()
        self.outputDirSelector.resetAll()

    def validate(self):
        if not self.getFactoryCreationParam():
            return False
        if self.tabWidget.currentIndex() == 0:
            if self.serverWidget.currentIndex() == 0:
                return False
            else:
                return True
        elif self.tabWidget.currentIndex() == 1:
            if self.outputDirSelector.fileNameList == []:
                return False
            else:
                return True
    
    def getFactoryCreationParam(self):
        if self.tabWidget.currentIndex() == 0 and self.serverWidget.currentIndex() > 0:
            return self.serverWidget.abstractDb 
        elif self.tabWidget.currentIndex() == 1 and self.outputDirSelector.fileNameList <> []:
            return self.outputDirSelector.fileNameList[0]
        else:
            return None
    
    def getType(self):
        if self.tabWidget.currentIndex() == 0:
            return 'QPSQL'
        elif self.tabWidget.currentIndex() == 1:
            return 'QSQLITE'