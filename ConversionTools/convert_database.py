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
        self.makeConversion(self.comboBox.currentText(),self.complexClasses,self.geomClasses)
        
        QtGui.QMessageBox.warning(self, self.tr('Success!'), self.tr('Conversion complete! Ololo! Ololo! Ololo!'))



    def makeConversion(self, type, complexClasses, geomClasses):
        if type == 'spatialite2postgis':
            self.invalidatedDataDict = self.validateSpatialite(self.widget.db,self.widget_2.db,complexClasses,geomClasses)
            self.convert2postgis(classes)
        if type == 'postgis2spatialite':
            if len(complexClasses)>0:
                self.convert2spatialite(complexClasses)
            if len(geomClasses)>0:
                self.convert2spatialite(geomClasses)
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
    
    def validateSpatialite(self, spatialiteDB, postgisDB, edgvVersion, complexClasses, geomClasses):
        invalidated = dict()
        
        domainDict = self.utils.getPostgisDomainDict(edgvVersion, postgisDB)
        notNullDict = self.utils.getPostgisNotNullDict(edgvVersion, postgisDB)
        spatialiteDbStructure = self.utils.getStructureDict(spatialiteDB, edgvVersion, True)
        aggregationColumns = self.utils.getAggregationAttributes(postgisDB,False)
        
        invalidated['notInDomain'] = dict()
        invalidated['nullAttribute'] = dict()
        invalidated['missingAggregator'] = dict()
        
        self.makeSpatialiteValidation(invalidated, spatialiteDB, postgisDB, domainDict, notNullDict, spatialiteDbStructure, aggregationColumns, complexClasses)
        self.makeSpatialiteValidation(invalidated, spatialiteDB, postgisDB, domainDict, notNullDict, spatialiteDbStructure, aggregationColumns, geomClasses)

        return invalidated
    
    def makeSpatialiteValidation(self,invalidated, spatialiteDB, postgisDB, domainDict, notNullDict, spatialiteDbStructure, aggregationColumns, classes):
        for cl in classes:
            if cl in spatialiteDbStructure.keys():
                schema = cl.split('_')[0]
                table = '_'.join(cl.split('_')[1::])
                pgClass = schema + '.' + table
                allAttrList = spatialiteDbStructure[cl].keys()
                attrList = ['OGC_FID']
                for att in allAttrList:
                    if (att in domainDict[cl].keys()) and (att not in attrList):
                        attrList.append(att)
                sql = self.widget.gen.getFeaturesWithSQL(cl,attrList) 
                query = QSqlQuery(sql, spatialiteDB)
                
                while query.next():
                    id = query.value(0)
                    for i in range(len(attrList)-1):
                        value = query.value(i+1)
                        #validates domain
                        if pgClass in domainDict.keys():
                            if (attrList[i] in domainDict[cl].keys()) and (value not in domainDict[pgClass][attrList[i]]):
                                if cl not in invalidated['notInDomain'][cl].keys():
                                    invalidated['notInDomain'][cl] = dict()
                                if id not in invalidated['notInDomain'][cl].keys():
                                    invalidated['notInDomain'][cl][id] = dict()
                                if att not in invalidated['notInDomain'][cl][id].keys():
                                    invalidated['notInDomain'][cl][id][att] = dict()
                                invalidated['notInDomain'][cl][id][att] = value
                        #validates not nulls
                        if pgClass in notNullDict.keys():
                            if attrList[i] in notNullDict[pgClass]:
                                if cl not in invalidated['nullAttribute'].keys():
                                    invalidated['nullAttribute'][cl] = dict()
                                if id not in invalidated['nullAttribute'][cl].keys():
                                    invalidated['nullAttribute'][cl][id] = dict()
                                if attrList[i] not in invalidated['nullAttribute'][cl][id].keys():
                                    invalidated['nullAttribute'][cl][id][attrList[i]] = dict()
                                invalidated['nullAttribute'][cl][id][attrList[i]] = value
                        
                        #validates aggregates
                        if attrList[i] in aggregationColumns and value <> 'NULL':
                            sql2 = self.widget_2.gen.getAggregatorFromComplexSchema(table,attrList[i])
                            query2 = QSqlQuery(sql2, postgisDB)
                            idsFound = []
                            while query2.next():
                                complexCandidate = query2.value(0)
                                sql3 = self.widget_2.gen.getAggregatorFromId(complexCandidate,attrList[i])
                                query3 = QSqlQuery(sql3, postgisDB)
                                while query3.next():
                                    fid = query3.value(0)
                                    idsFound.append(fid)
                            
                            if len(idsFound) == 0:
                                if cl not in invalidated['missingAggregator'].keys():
                                    invalidated['missingAggregator'][cl] = dict()
                                if id not in invalidated['missingAggregator'][cl].keys():
                                    invalidated['missingAggregator'][cl][id] = dict()
                                if attrList[i] not in invalidated['missingAggregator'][cl][id].keys():
                                    invalidated['missingAggregator'][cl][id][attrList[i]] = dict()
                                invalidated['missingAggregator'][cl][id][attrList[i]] = value                                
                            
        return
    
