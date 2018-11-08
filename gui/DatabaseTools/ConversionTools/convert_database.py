# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-09-14
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
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
from osgeo import ogr
#QGIS imports
from qgis.core import QgsMessageLog

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
from qgis.PyQt.QtWidgets import QApplication, QDialog
from qgis.PyQt.QtGui import QCursor

# DSGTools imports
from DsgTools.core.Utils.utils import Utils
from DsgTools.core.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.gui.DatabaseTools.UserTools.create_profile import CreateProfile

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'convert_database.ui'))

class ConvertDatabase(QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(ConvertDatabase, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.utils = Utils()
        self.geomClasses = None
        self.complexClasses = None
        self.invalidatedDataDict = dict()
        
        self.comboBox.addItem(self.tr('Select a conversion'))
        self.comboBox.addItem(self.tr('postgis2spatialite'))
        self.comboBox.addItem(self.tr('spatialite2postgis'))
        self.widget.tabWidget.setTabEnabled(0, False)
        self.widget.tabWidget.setTabEnabled(1,False)
        self.widget_2.tabWidget.setTabEnabled(0, False)
        self.widget_2.tabWidget.setTabEnabled(1,False)
        self.allDataRadioButton.setEnabled(False)
        self.fixDataRadioButton.setEnabled(False)   

    def setConversion(self,conversionType):
        """
        Sets the conversion type. It can be postgis2spatialite or spatialite2postgis
        """
        self.widget.setInitialState()
        self.widget_2.setInitialState()
        self.invalidatedDataDict = dict()
        if conversionType == 'Select a conversion':
            self.widget.tabWidget.setTabEnabled(0, False)
            self.widget.tabWidget.setTabEnabled(1,False)
            self.widget.tabWidget.setCurrentIndex(0)
            self.widget_2.tabWidget.setTabEnabled(0, False)
            self.widget_2.tabWidget.setTabEnabled(1,False)
            self.widget_2.tabWidget.setCurrentIndex(0)
            self.allDataRadioButton.setEnabled(False)
            self.fixDataRadioButton.setEnabled(False) 
                             
        if conversionType == 'postgis2spatialite':
            self.widget.tabWidget.setTabEnabled(0,True)
            self.widget.tabWidget.setTabEnabled(1,False)
            self.widget.tabWidget.setCurrentIndex(0)
            self.widget_2.tabWidget.setTabEnabled(1,True)
            self.widget_2.tabWidget.setTabEnabled(0,False)
            self.widget_2.tabWidget.setCurrentIndex(1)
            
            self.allDataRadioButton.setEnabled(False)
            self.fixDataRadioButton.setEnabled(False)        

        if conversionType == 'spatialite2postgis':
            self.widget.tabWidget.setTabEnabled(1,True)
            self.widget.tabWidget.setTabEnabled(0,False)
            self.widget.tabWidget.setCurrentIndex(1)
            self.widget_2.tabWidget.setTabEnabled(0,True)
            self.widget_2.tabWidget.setTabEnabled(1,False)
            self.widget_2.tabWidget.setCurrentIndex(0)
            
            self.allDataRadioButton.setEnabled(True)
            self.fixDataRadioButton.setEnabled(True)   
            
    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self):
        """
        Updates the conversion type when the combo box changes
        """
        self.setConversion(self.comboBox.currentText())

    @pyqtSlot(bool)
    def on_closeButton_clicked(self):
        """
        Closes dialog
        """
        self.close()
    
    @pyqtSlot(bool)
    def on_convertButton_clicked(self):
        """
        Performs the actual conversion
        """
        if not self.widget.abstractDb:
            QMessageBox.warning(self, self.tr('Error!'), self.tr('Enter input database!'))
            return
        if not self.widget_2.abstractDb:
            QMessageBox.warning(self, self.tr('Error!'), self.tr('Enter output database!'))
            return
        if self.widget.dbVersion != self.widget_2.dbVersion:
            QMessageBox.warning(self, self.tr('Error!'), self.tr('Version mismatch!\nConversion must be between databases with the same version!'))
            return
        type = ''
        if self.allDataRadioButton.isChecked():
            type = 'untouchedData'
        if self.fixDataRadioButton.isChecked():
            type = 'fixData'
        
        if not self.widget.abstractDb.slotConnected:
            self.widget.abstractDb.signals.updateLog.connect(self.logUpdated)
            self.widget.abstractDb.signals.clearLog.connect(self.logCleared)
            self.widget.abstractDb.slotConnected = True
        converted = False
        self.logCleared()
        try:
            if self.widget.crs != self.widget_2.crs:
                if QMessageBox.question(self, self.tr('Question'), self.tr('Databases CRS are different. Conversor will reproject spatial data. Do you want to proceed?'), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Ok:
                    QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                    converted = self.widget.abstractDb.convertDatabase(self.widget_2.abstractDb,type)
                    QApplication.restoreOverrideCursor()
            else:
                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                converted = self.widget.abstractDb.convertDatabase(self.widget_2.abstractDb,type)
                QApplication.restoreOverrideCursor()
        except Exception as e:
            QApplication.restoreOverrideCursor()
            converted = False
            QgsMessageLog.logMessage(':'.join(e.args), 'DSG Tools Plugin', Qgis.Critical)
        if converted:
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Conversion successfully completed!'))
        else:
            QMessageBox.warning(self, self.tr('Error!'), self.tr('Conversion not performed! Check log for details.'))
    
    @pyqtSlot(str)
    def logUpdated(self,text):
        """
        Displays the conversion log
        """
        self.logDisplay.insertPlainText(text)
        
    @pyqtSlot()
    def logCleared(self):
        """
        Clears the conversion log
        """
        self.logDisplay.clear()