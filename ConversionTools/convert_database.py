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
import os, ogr

# Qt imports
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtSql import QSqlDatabase, QSqlQuery

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.UserTools.create_profile import CreateProfile

import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'convert_database.ui'))

from DsgTools.UserTools.assign_profiles import AssignProfiles

class ConvertDatabase(QtGui.QDialog, FORM_CLASS):
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
        self.widget.setInitialState()
        self.widget_2.setInitialState()
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
            self.widget.tabWidget.setTabEnabled(1,True)
            self.widget.tabWidget.setTabEnabled(0,False)
            self.widget.tabWidget.setCurrentIndex(1)
            self.widget_2.tabWidget.setTabEnabled(0,True)
            self.widget_2.tabWidget.setTabEnabled(1,False)
            self.widget_2.tabWidget.setCurrentIndex(0)
            
            self.allDataRadioButton.setEnabled(False)
            self.fixDataRadioButton.setEnabled(False)        

        if conversionType == 'spatialite2postgis':
            self.widget.tabWidget.setTabEnabled(0,True)
            self.widget.tabWidget.setTabEnabled(1,False)
            self.widget.tabWidget.setCurrentIndex(0)
            self.widget_2.tabWidget.setTabEnabled(1,True)
            self.widget_2.tabWidget.setTabEnabled(0,False)
            self.widget_2.tabWidget.setCurrentIndex(1)
            
            self.allDataRadioButton.setEnabled(True)
            self.fixDataRadioButton.setEnabled(True)   
            
    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self):
        self.setConversion(self.comboBox.currentText())

    @pyqtSlot(bool)
    def on_closeButton_clicked(self):
        self.close()
    
    @pyqtSlot(bool)
    def on_convertButton_clicked(self):
        if not self.widget.db:
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Enter input database!'))
            return
        if not self.widget_2.db:
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Enter output database!'))
            return
        if self.widget.dbVersion <> self.widget_2.dbVersion:
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Version mismatch!\nConversion must be between databases with the same version!'))
            return
        self.geomClasses = self.utils.listGeomClassesWithElementsFromDatabase(self.widget.db, self.widget.isSpatialite)
        self.complexClasses = self.utils.listComplexClassesWithElementsFromDatabase(self.widget.db, self.widget.isSpatialite)
        self.makeConversion(self.comboBox.currentText(),self.complexClasses)
        self.makeConversion(self.comboBox.currentText(),self.geomClasses)
        
        QtGui.QMessageBox.warning(self, self.tr('Success!'), self.tr('Conversion complete! Ololo! Ololo! Ololo!'))



    def makeConversion(self, type, classes):
        if type == 'spatialite2postgis':
            self.convert2postgis(classes)
        if type == 'postgis2spatialite':
            self.convert2spatialite(classes)
        else:
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Conversion not defined!'))
            return
    
    def convert2spatialite(self, classes, hasFieldMapper=False):
        if not hasFieldMapper:
            fieldMap = self.buildFieldMap(self.widget.db,self.widget.dbVersion, self.widget.isSpatialite)
        conn = self.utils.makeOgrPostGISConn(self.widget.db)
        inputOgrDb = ogr.Open(conn)
        self.outputOgrDb = ogr.Open( self.widget_2.filename , update = 1)
        inputLayerList = classes
        return self.utils.translateDS(inputOgrDb, self.outputOgrDb, fieldMap, inputLayerList, self.widget.isSpatialite)
        
    
    def convert2postgis(self, classes, hasFieldMapper=False):
        return
    
    def buildFieldMap(self,db, edgvVersion, inputIsSpatialite): 
        fieldMap = self.utils.getStructureDict(db, edgvVersion, inputIsSpatialite)
        return fieldMap

    