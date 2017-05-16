# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-26
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

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtGui import QFileDialog, QMessageBox


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'databaseParameterWidget.ui'))

class DatabaseParameterWidget(QtGui.QWidget, FORM_CLASS):
    filesSelected = pyqtSignal()
    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setInitialState()
    
    def setInitialState(self):
        """
        Sets the initial state
        """
        self.prefixVisible = True
        self.sufixVisible = True
        self.dbNameVisible = True
    
    def setPrefixVisible(self, visible):
        """
        Sets if the database prefix should be visible
        """
        if isinstance(visible,bool):
            self.prefixLineEdit.setVisible(visible)
            self.prefixLabel.setVisible(visible)
            self.prefixVisible = visible
    
    def setSufixVisible(self, visible):
        """
        Sets if the database sufix should be visible
        """
        if isinstance(visible,bool):
            self.sufixLineEdit.setVisible(visible)
            self.sufixLabel.setVisible(visible)
            self.sufixVisible = visible
    
    def setDbNameVisible(self, visible):
        """
        Sets if the database name should be visible
        """
        if isinstance(visible,bool):
            self.dbNameLineEdit.setVisible(visible)
            self.dbNameLabel.setVisible(visible)
            self.dbNameVisible = visible
    
    def getVersion(self):
        """
        Get the database version
        """
        return self.versionComboBox.currentText()
    
    def validate(self):
        """
        Validate database name
        """
        errorMsg = ''
        if self.dbNameVisible:
            if self.dbNameLineEdit.text() == '':
                errorMsg += self.tr('Enter a database name!\n')
        if self.mQgsProjectionSelectionWidget.crs().authid() == '':        
            errorMsg += self.tr('Select a coordinate reference system!\n')
        if not self.edgvTemplateRadioButton.isChecked() and not self.comboBoxPostgis.currentDb():
            errorMsg += self.tr('Select a template database!\n')
        
        if errorMsg != '':
            QMessageBox.critical(self, self.tr('Critical!'), errorMsg)
            return False
        else:
            return True
    
    @pyqtSlot(bool, name = 'on_edgvTemplateRadioButton_toggled')
    def changeInterfaceState(self, edgvTemplateToggled, hideInterface = True):
        if edgvTemplateToggled:
            self.comboBoxPostgis.setEnabled(False)
            self.selectFrameCheckBox.setEnabled(False)
            self.frameComboBox.setEnabled(False)
            self.versionComboBox.setEnabled(True)
        else:
            self.comboBoxPostgis.setEnabled(True)
            self.selectFrameCheckBox.setEnabled(True)
            self.frameComboBox.setEnabled(self.selectFrameCheckBox.isChecked())
            self.versionComboBox.setEnabled(False)
        if hideInterface:
            self.comboBoxPostgis.hide()
            self.dbTemplateRadioButton.hide()
            self.selectFrameCheckBox.hide()
            self.frameComboBox.hide()
        else:
            self.comboBoxPostgis.show()
            self.dbTemplateRadioButton.show()
            self.selectFrameCheckBox.show()
            self.frameComboBox.show()
    
    def getTemplateName(self):
        if self.edgvTemplateRadioButton.isChecked():
            return None
        else:
            return self.comboBoxPostgis.currentDb()
