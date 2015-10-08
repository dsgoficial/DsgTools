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
        if conversionType == 'postgis2spatialite':
            self.widget.tabWidget.setTabEnabled(1,True)
            self.widget.tabWidget.setTabEnabled(0,False)
            self.widget.tabWidget.setCurrentIndex(1)
            self.widget_2.tabWidget.setTabEnabled(0,True)
            self.widget_2.tabWidget.setTabEnabled(1,False)
            self.widget_2.tabWidget.setCurrentIndex(0)
        if conversionType == 'spatialite2postgis':
            self.widget.tabWidget.setTabEnabled(0,True)
            self.widget.tabWidget.setTabEnabled(1,False)
            self.widget.tabWidget.setCurrentIndex(0)
            self.widget_2.tabWidget.setTabEnabled(1,True)
            self.widget_2.tabWidget.setTabEnabled(0,False)
            self.widget_2.tabWidget.setCurrentIndex(1)
            
    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self):
        self.setConversion(self.comboBox.currentText())

    @pyqtSlot(bool)
    def on_cancelButton_clicked(self):
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
        print self.utils.makeOgrPostGISConn(self.widget_2.db)
#         print self.getPostgisDomainDict('2.1.3', self.widget_2.db)

    def getPostgisNotNullDict(self,edgvVersion,db):
        if edgvVersion == '2.1.3':
            schemaList = ['cb','complexos']
        else:
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Conversion not defined for this database version!'))
            return
        sql = self.widget_2.gen.getNotNullFields(schemaList)
        query = QSqlQuery(sql, db)
        notNullDict = dict()
        while query.next():
            className = query(0)
            attName = query(1)
            if className not in notNullDict.keys():
                notNullDict[className]=[]
            notNullDict[className].append(attName)
        return notNullDict
    
    def getPostgisDomainDict(self,edgvVersion,db):
        if edgvVersion == '2.1.3':
            schemaList = ['cb','complexos','dominios']
        else:
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Conversion not defined for this database version!'))
            return
        sql = self.widget_2.gen.validateWithDomain(schemaList)

        query = QSqlQuery(sql, db)
        classDict = dict()
        domainDict = dict()
        
        while query.next():

            className = query.value(0)
            attName = query.value(1)
            domainName = query.value(2)
            domainTable = query.value(3)
            domainQuery = query.value(4)

            if className not in classDict.keys():
                classDict[className]=dict()
            if attName not in classDict[className].keys():
                classDict[className][attName]=[]
                query2 = QSqlQuery(domainQuery,db)
                while query2.next():
                    value = query2.value(0)
                    classDict[className][attName].append(value)

        return classDict