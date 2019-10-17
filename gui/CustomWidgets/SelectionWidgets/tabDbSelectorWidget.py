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
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal
from qgis.PyQt.QtWidgets import QMessageBox



FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'tabDbSelectorWidget.ui'))

class TabDbSelectorWidget(QtWidgets.QWidget, FORM_CLASS):
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
        self.setSpatiaLitePage()
        # self.setGeopackagePage()

    def setSpatiaLitePage(self):
        """
        By default, select files comes "clean", this method adapts it for SpatiaLite databases. 
        """
        self.outputDirSelector.setCaption(self.tr("Select a path to save the SpatiaLite database"))
        self.outputDirSelector.setType("dir")

    def setGeopackagePage(self):
        """
        By default, select files comes "clean", this method adapts it for Geopackage databases. 
        """
        self.outputDirSelectorGeopackage.setCaption(self.tr("Select a path to save the Geopackage database"))
        self.outputDirSelectorGeopackage.setType("dir")

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self):
        """
        Changes the database type tab and resets the previous one
        """
        self.serverWidget.clearAll()
        self.outputDirSelector.resetAll()
        # self.outputDirSelectorGeopackage.resetAll()

    def validate(self):
        """
        Validates the selector widget
        """
        if self.tabWidget.currentIndex() == 0:
            if self.serverWidget.serversCombo.currentIndex() == 0:
                QMessageBox.critical(self, self.tr('Critical!'), self.tr('Select a server!'))
                return False
            else:
                return True
        elif self.tabWidget.currentIndex() == 1:
            if self.outputDirSelector.fileNameList == []:
                QMessageBox.critical(self, self.tr('Critical!'), self.tr('Select a folder!'))
                return False
            else:
                return True
        # elif self.tabWidget.currentIndex() == 2:
        #     if self.outputDirSelectorGeopackage.fileNameList == []:
        #         QMessageBox.critical(self, self.tr('Critical!'), self.tr('Select a folder!'))
        #         return False
        #     else:
        #         return True
    
    def getFactoryCreationParam(self):
        """
        Adjusts the database selection according to the database type
        """
        if self.tabWidget.currentIndex() == 0 and self.serverWidget.serversCombo.currentIndex() > 0:
            return self.serverWidget.abstractDb 
        elif self.tabWidget.currentIndex() == 1 and self.outputDirSelector.fileNameList != []:
            return self.outputDirSelector.fileNameList[0]
        # elif self.tabWidget.currentIndex() == 2 and self.outputDirSelectorGeopackage.fileNameList != []:
        #     return self.outputDirSelectorGeopackage.fileNameList[0]
        else:
            return None
    
    def getType(self):
        """
        gets database type (QPSQL, QSQLITE, GPKG)
        """
        if self.tabWidget.currentIndex() == 0:
            return 'QPSQL'
        elif self.tabWidget.currentIndex() == 1:
            return 'QSQLITE'
        # elif self.tabWidget.currentIndex() == 2:
        #     return 'GPKG'