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
        converted = False
        converted = self.makeConversion(self.comboBox.currentText(),self.complexClasses,self.geomClasses)
        if converted:
            QtGui.QMessageBox.warning(self, self.tr('Success!'), self.tr('Conversion complete! Ololo! Ololo! Ololo!'))
        else:
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Conversion not performed! Check log for details.'))

    def makeConversion(self, type, complexClassesDict, geomClassesDict):
        self.logDisplay.clear()
        self.logDisplay.insertPlainText(self.tr('Conversion type: '+type+'\n'))
        self.logDisplay.insertPlainText(self.tr('Input database: ')+self.widget.db.databaseName()+'\n')
        self.logDisplay.insertPlainText(self.tr('Output database: ')+self.widget_2.db.databaseName()+'\n')
        self.logDisplay.insertPlainText(self.tr('\n---------------- Complex Classes With Elements Read Summary ------------------------\n'))
        self.logDisplay.insertPlainText(self.tr('Class -> Elements\n'))
        complexClasses = complexClassesDict.keys()
        geomClasses = geomClassesDict.keys()
        complexClasses.sort()
        geomClasses.sort()
        for i in complexClasses:
            self.logDisplay.insertPlainText(i+self.tr('->')+str(complexClassesDict[i])+'\n')
        self.logDisplay.insertPlainText(self.tr('\n---------------- Geometric Classes With Elements Read Summary ------------------------\n'))
        self.logDisplay.insertPlainText(self.tr('Class -> Elements\n'))
        for i in geomClasses:
            self.logDisplay.insertPlainText(i+self.tr('->')+str(geomClassesDict[i])+'\n')        

        if type == 'spatialite2postgis':
            self.invalidatedDataDict = self.validateSpatialite(self.widget.db,self.widget_2.db,self.widget_2.dbVersion,complexClasses,geomClasses)
            converted = False
            allClasses = []
            for i in complexClasses:
                allClasses.append(i)
            for i in geomClasses:
                allClasses.append(i)
            hasErrors = self.buildInvalidatedLog(allClasses, self.invalidatedDataDict)
            if self.fixDataRadioButton.isChecked():
                if len(complexClasses) > 0:
                    converted = self.convert2postgis(complexClasses, self.invalidatedDataDict)
                if len(geomClasses) > 0:
                    converted = False
                    converted = self.convert2postgis(geomClasses, self.invalidatedDataDict)
            else:
                if not hasErrors:
                    if len(complexClasses) > 0:
                        converted = self.convert2postgis(complexClasses, self.invalidatedDataDict)
                    if len(geomClasses) > 0:
                        converted = False
                        converted = self.convert2postgis(geomClasses, self.invalidatedDataDict)                    
        if type == 'postgis2spatialite':
            converted = False
    
            if len(complexClasses) > 0:
                converted = self.convert2spatialite(complexClasses)
            if len(geomClasses) > 0:
                converted = False
                converted = self.convert2spatialite(geomClasses)
            return converted
        else:
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Conversion not defined!'))
            return False
    
    def convert2spatialite(self, classes, hasFieldMapper=False):
        if not hasFieldMapper:
            fieldMap = self.buildFieldMap(self.widget.db, self.widget.dbVersion, self.widget.isSpatialite)
        conn = self.utils.makeOgrPostGISConn(self.widget.db)
        inputOgrDb = ogr.Open(conn)
        self.outputOgrDb = ogr.Open( self.widget_2.filename , update = 1)
        inputLayerList = classes
        return self.utils.translateDS(inputOgrDb, self.outputOgrDb, fieldMap, inputLayerList, self.widget.isSpatialite)
    
    def convert2postgis(self, classes, invalidatedDataDict, hasFieldMapper=False):
        if not hasFieldMapper:
            fieldMap = self.buildFieldMap(self.widget.db, self.widget.dbVersion, self.widget.isSpatialite)
        inputOgrDb = ogr.Open(self.widget.filename)
        conn = self.utils.makeOgrPostGISConn(self.widget_2.db)        
        self.outputOgrDb = ogr.Open(conn)
        inputLayerList = classes
        return self.utils.translateDS(inputOgrDb, self.outputOgrDb, fieldMap, inputLayerList, self.widget.isSpatialite,invalidatedDataDict)
    
    def buildInvalidatedLog(self,classes,invalidatedDataDict):
        hasErrors = False
        for key in invalidatedDataDict.keys():
            if len(invalidatedDataDict[key].keys()) > 0:
                hasErrors = True
        if hasErrors:
            self.logDisplay.insertPlainText(self.tr('\n-------Validation Problems Summary-----------\n'))
            for key in invalidatedDataDict.keys():
                if key == 'nullComplexPk' and len(invalidatedDataDict[key].keys())>0:
                    self.logDisplay.insertPlainText(self.tr('\nComplex Features with null primary keys:\n'))
                    for cl in invalidatedDataDict[key].keys():
                        self.logDisplay.insertPlainText(self.tr('Class: ')+cl+self.tr(' number of features: ')+str(invalidatedDataDict[key][cl])+'\n')

                if key == 'notInDomain' and len(invalidatedDataDict[key].keys())>0:
                    self.logDisplay.insertPlainText(self.tr('\nFeatures with attributes not in domain:\n'))
                    for cl in invalidatedDataDict[key].keys():
                        self.logDisplay.insertPlainText(self.tr('Class: ')+cl+'\n')
                        for id in invalidatedDataDict[key][cl].keys():
                            attrCommaList = '(id,'+','.join(invalidatedDataDict[key][cl][id].keys())+') = '
                            at = invalidatedDataDict[key][cl][id].keys()
                            valueList = '('+str(id)
                            for i in range(len(at)):
                                valueList += ','+str(invalidatedDataDict[key][cl][id][at[i]])
                            valueList += ')\n'
                        
                            self.logDisplay.insertPlainText(attrCommaList+valueList)

                if key == 'nullAttribute' and len(invalidatedDataDict[key].keys())>0:
                    self.logDisplay.insertPlainText(self.tr('\nFeatures with null attributes in a not null field:\n'))
                    for cl in invalidatedDataDict[key].keys():
                        self.logDisplay.insertPlainText(self.tr('Class: ')+cl+'\n')
                        for id in invalidatedDataDict[key][cl].keys():
                            for attr in invalidatedDataDict[key][cl][id].keys():
                                self.logDisplay.insertPlainText(self.tr('id: ')+str(id)+self.tr(' Attribute: ')+attr+self.tr(' Value: ')+str(invalidatedDataDict[key][cl][id][attr])+'\n')

                if key == 'missingAggregator' and len(invalidatedDataDict[key].keys())>0:
                    self.logDisplay.insertPlainText(self.tr('\nFeatures with null aggregator missing:\n'))
                    for cl in invalidatedDataDict[key].keys():
                        self.logDisplay.insertPlainText(self.tr('Class: ')+cl+'\n')
                        for id in invalidatedDataDict[key][cl].keys():
                            for attr in invalidatedDataDict[key][cl][id].keys():
                                self.logDisplay.insertPlainText(self.tr('id: ')+str(id)+self.tr(' Attribute: ')+attr+self.tr(' Value: ')+str(invalidatedDataDict[key][cl][id][attr])+'\n')
        return hasErrors
    
    def buildFieldMap(self,db, edgvVersion, inputIsSpatialite): 
        fieldMap = self.utils.getStructureDict(db, edgvVersion, inputIsSpatialite)
        return fieldMap
    
    def validateSpatialite(self, spatialiteDB, postgisDB, edgvVersion, complexClasses, geomClasses):
        invalidated = dict()
        
        domainDict = self.utils.getPostgisDomainDict(edgvVersion, postgisDB)
        notNullDict = self.utils.getPostgisNotNullDict(edgvVersion, postgisDB)
        spatialiteDbStructure = self.utils.getStructureDict(spatialiteDB, edgvVersion, True)
        aggregationColumns = self.utils.getAggregationAttributes(postgisDB,False)
        
        invalidated['nullComplexPk'] = dict() #only complexes are checked, because geom classes won't have its ids converted
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
                if schema == 'complexos':
                    attrList = ['id']
                else:
                    attrList = ['OGC_FID']
                for att in allAttrList:
                    if pgClass in domainDict.keys():
                        if (att in domainDict[pgClass].keys()) and (att not in attrList):
                            attrList.append(att)
                sql = self.widget.gen.getFeaturesWithSQL(cl,attrList) 
                query = QSqlQuery(sql, spatialiteDB)
                
                while query.next():
                    id = query.value(0)
                    #validates complex pk
                    if cl not in invalidated['nullComplexPk'].keys():
                        invalidated['nullComplexPk'][cl]=0
                    invalidated['nullComplexPk'][cl]+=1
                    
                    for i in range(len(attrList)):
                        value = query.value(i)
                        #validates domain
                        if pgClass in domainDict.keys():
                            if (attrList[i] in domainDict[pgClass].keys()) and (value not in domainDict[pgClass][attrList[i]]):
                                if cl not in invalidated['notInDomain'].keys():
                                    invalidated['notInDomain'][cl] = dict()
                                if id not in invalidated['notInDomain'][cl].keys():
                                    invalidated['notInDomain'][cl][id] = dict()
                                if att not in invalidated['notInDomain'][cl][id].keys():
                                    invalidated['notInDomain'][cl][id][attrList[i]] = dict()
                                invalidated['notInDomain'][cl][id][attrList[i]] = value
                        #validates not nulls
                        if pgClass in notNullDict.keys():
                            if attrList[i] in notNullDict[pgClass] and value == 'NULL':
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
    