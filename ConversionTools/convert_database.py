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
        self.classWithElements = self.utils.listClassesWithElementsFromDatabase(self.widget.db, self.widget.isSpatialite)
        converted = False
        converted = self.makeConversion(self.comboBox.currentText(),self.classWithElements)
        if converted:
            QtGui.QMessageBox.warning(self, self.tr('Success!'), self.tr('Conversion complete! Ololo! Ololo! Ololo!'))
        else:
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Conversion not performed! Check log for details.'))

    def makeConversion(self, type, classesDict):
        self.logDisplay.clear()
        self.logDisplay.insertPlainText(self.tr('Conversion type: '+type+'\n'))
        self.logDisplay.insertPlainText(self.tr('\nInput database: ')+self.widget.db.databaseName()+'\n')
        self.logDisplay.insertPlainText(self.tr('\nOutput database: ')+self.widget_2.db.databaseName()+'\n')
        self.logDisplay.insertPlainText('\n'+'{:-^60}'.format(self.tr('Read Summary')))
        self.logDisplay.insertPlainText('\n\n'+'{:<50}'.format(self.tr('Class'))+self.tr('Elements\n\n'))
        classes = classesDict.keys()
        classes.sort()
        clStr = ''
        for i in classes:
            self.logDisplay.insertPlainText('{:<50}'.format(i)+str(classesDict[i])+'\n')

        if type == 'spatialite2postgis':
            self.invalidatedDataDict = self.validateSpatialite(self.widget.db,self.widget_2.db,self.widget_2.dbVersion,classes)
            converted = False
            hasErrors = self.buildInvalidatedLog(classes, self.invalidatedDataDict)
            if self.fixDataRadioButton.isChecked():
                if len(classes) > 0:
                    converted = self.convert2postgis(classes, self.invalidatedDataDict)
            else:
                if not hasErrors:
                    if len(classes) > 0:
                        converted = self.convert2postgis(classes, self.invalidatedDataDict)
            
            return converted
               
        if type == 'postgis2spatialite':
            converted = False
            if len(classes) > 0:
                converted = self.convert2spatialite(classes)

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
            self.logDisplay.insertPlainText('\n'+'{:-^60}'.format(self.tr('Validation Problems Summary')))
            for key in invalidatedDataDict.keys():
                
                if key == 'nullLine' and len(invalidatedDataDict[key].keys())>0:
                    self.logDisplay.insertPlainText(self.tr('\n\nClasses with null lines:\n'))
                    self.logDisplay.insertPlainText('\n\n'+'{:<50}'.format(self.tr('Class'))+self.tr('Elements\n\n'))
                    for cl in invalidatedDataDict[key].keys():
                        self.logDisplay.insertPlainText('{:<50}'.format(cl)+str(invalidatedDataDict[key][cl])+'\n')

                if key == 'nullPk' and len(invalidatedDataDict[key].keys())>0:
                    self.logDisplay.insertPlainText(self.tr('\n\nClasses with null primary keys:\n'))
                    self.logDisplay.insertPlainText('\n\n'+'{:<50}'.format(self.tr('Class'))+self.tr('Elements\n\n'))
                    for cl in invalidatedDataDict[key].keys():
                        self.logDisplay.insertPlainText('{:<50}'.format(cl)+str(invalidatedDataDict[key][cl])+'\n')

                if key == 'notInDomain' and len(invalidatedDataDict[key].keys())>0:
                    self.logDisplay.insertPlainText(self.tr('\n\nFeatures with attributes not in domain:\n\n'))
                    for cl in invalidatedDataDict[key].keys():
                        self.logDisplay.insertPlainText(self.tr('\nClass: ')+cl+'\n')
                        for id in invalidatedDataDict[key][cl].keys():
                            attrCommaList = '(id,'+','.join(invalidatedDataDict[key][cl][id].keys())+') = '
                            at = invalidatedDataDict[key][cl][id].keys()
                            valueList = '('+str(id)
                            for i in range(len(at)):
                                valueList += ','+str(invalidatedDataDict[key][cl][id][at[i]])
                            valueList += ')\n'
                        
                            self.logDisplay.insertPlainText(attrCommaList+valueList)

                if key == 'nullAttribute' and len(invalidatedDataDict[key].keys())>0:
                    self.logDisplay.insertPlainText(self.tr('\n\nFeatures with null attributes in a not null field:\n\n'))
                    for cl in invalidatedDataDict[key].keys():
                        self.logDisplay.insertPlainText(self.tr('Class: ')+cl+'\n')
                        for id in invalidatedDataDict[key][cl].keys():
                            attrCommaList = '(id,'+','.join(invalidatedDataDict[key][cl][id].keys())+') = '
                            valueList = '('+str(id)
                            for attr in invalidatedDataDict[key][cl][id].keys():
                                valueList += ','+str(invalidatedDataDict[key][cl][id][attr])
                            valueList += ')\n'
                            
                            self.logDisplay.insertPlainText(attrCommaList+valueList)
        return hasErrors
    
    def buildFieldMap(self,db, edgvVersion, inputIsSpatialite): 
        fieldMap = self.utils.getStructureDict(db, edgvVersion, inputIsSpatialite)
        return fieldMap
    
    def validateSpatialite(self, spatialiteDB, postgisDB, edgvVersion, classes):
        invalidated = dict()
        
        domainDict = self.utils.getPostgisDomainDict(edgvVersion, postgisDB)
        notNullDict = self.utils.getPostgisNotNullDict(edgvVersion, postgisDB)
        spatialiteDbStructure = self.utils.getStructureDict(spatialiteDB, edgvVersion, True)
        aggregationColumns = self.utils.getAggregationAttributes(postgisDB,False)
 
        invalidated['nullLine'] = dict()       
        invalidated['nullPk'] = dict()
        invalidated['notInDomain'] = dict()
        invalidated['nullAttribute'] = dict()
   
        self.makeSpatialiteValidation(invalidated, spatialiteDB, postgisDB, domainDict, notNullDict, spatialiteDbStructure, aggregationColumns, classes)

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
                    if att not in attrList:
                        attrList.append(att)
                sql = self.widget.gen.getFeaturesWithSQL(cl,attrList) 
                query = QSqlQuery(sql, spatialiteDB)
                
                while query.next():
                    id = query.value(0)
                    #detects null lines
                    for i in range(len(attrList)):
                        nullLine = True
                        value = query.value(i)
                        if value <> None:
                            nullLine = False
                            break
                    if nullLine:
                        if cl not in invalidated['nullLine'].keys():
                            invalidated['nullLine'][cl]=0
                        invalidated['nullLine'][cl]+=1
                    
                    #validates pks
                    if id == None and (not nullLine):
                        if cl not in invalidated['nullPk'].keys():
                            invalidated['nullPk'][cl]=0
                        invalidated['nullPk'][cl]+=1
                    
                    for i in range(len(attrList)):
                        value = query.value(i)
                        #validates domain
                        if pgClass in domainDict.keys():    
                            if attrList[i] in domainDict[pgClass].keys():
                                if value not in domainDict[pgClass][attrList[i]] and (not nullLine):
                                    if cl not in invalidated['notInDomain'].keys():
                                        invalidated['notInDomain'][cl] = dict()
                                    if id not in invalidated['notInDomain'][cl].keys():
                                        invalidated['notInDomain'][cl][id] = dict()
                                    if att not in invalidated['notInDomain'][cl][id].keys():
                                        invalidated['notInDomain'][cl][id][attrList[i]] = dict()
                                    invalidated['notInDomain'][cl][id][attrList[i]] = value
                        #validates not nulls
                        if pgClass in notNullDict.keys():
                            if pgClass in domainDict.keys():
                                if attrList[i] in notNullDict[pgClass] and attrList[i] not in domainDict[pgClass].keys():
                                    if (value == None) and (not nullLine) and (attrList[i] not in domainDict[pgClass].keys()):
                                        if cl not in invalidated['nullAttribute'].keys():
                                            invalidated['nullAttribute'][cl] = dict()
                                        if id not in invalidated['nullAttribute'][cl].keys():
                                            invalidated['nullAttribute'][cl][id] = dict()
                                        if attrList[i] not in invalidated['nullAttribute'][cl][id].keys():
                                            invalidated['nullAttribute'][cl][id][attrList[i]] = dict()
                                        invalidated['nullAttribute'][cl][id][attrList[i]] = value                                    
                            else:
                                if attrList[i] in notNullDict[pgClass]:
                                    if (value == None) and (not nullLine) and (attrList[i] not in domainDict[pgClass].keys()):
                                        if cl not in invalidated['nullAttribute'].keys():
                                            invalidated['nullAttribute'][cl] = dict()
                                        if id not in invalidated['nullAttribute'][cl].keys():
                                            invalidated['nullAttribute'][cl][id] = dict()
                                        if attrList[i] not in invalidated['nullAttribute'][cl][id].keys():
                                            invalidated['nullAttribute'][cl][id][attrList[i]] = dict()
                                        invalidated['nullAttribute'][cl][id][attrList[i]] = value 
                                
        return
    