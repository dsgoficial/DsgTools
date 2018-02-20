# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2016-05-07
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Brazilian Army - Geographic Service Bureau
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
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt4.QtGui import QPushButton, QKeySequence, QShortcut

# QGIS imports
from qgis.core import QgsMapLayer, QgsDataSourceURI, QgsGeometry, QgsMapLayerRegistry, QgsProject, QgsLayerTreeLayer, QgsFeature, QgsMessageLog, QgsCoordinateTransform, QgsCoordinateReferenceSystem, QgsEditFormConfig, QgsVectorLayer, QgsWKBTypes
from qgis.gui import QgsMessageBar, QgisInterface
import qgis as qgis

#DsgTools imports
from DsgTools.ProductionTools.FieldToolBox.field_setup import FieldSetup
from DsgTools.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.Factories.LayerLoaderFactory.layerLoaderFactory import LayerLoaderFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'field_toolbox.ui'))

class FieldToolbox(QtGui.QDockWidget, FORM_CLASS):
    def __init__(self, iface, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface
        self.buttons = []
        self.prevLayer = None
        self.buttonName = ''
        self.category = ''
        self.widget.dbChanged.connect(self.defineFactory)
        self.releaseButtonConected = False
        self.addedFeatures = []
        self.configFromDbDict = dict()
    
    def defineFactory(self, abstractDb):
        """
        Defines the layer loader by its type
        :param abstractDb:
        :return:
        """
        self.layerLoader = LayerLoaderFactory().makeLoader(self.iface, abstractDb)
        try:
            self.populateConfigFromDb()
        except Exception as e:
            QgsMessageLog.logMessage(self.tr('Error getting stored configuration.\n')+':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
    def setEditButtonEnabled(self, enabled):
        """
        Edits the current configuration settings
        :param enabled:
        :return:
        """
        self.editCurrentConfigButton.setEnabled(enabled)
    
    @pyqtSlot(bool, name='on_setupButton_clicked')
    @pyqtSlot(bool, name='on_editCurrentConfigButton_clicked')
    def populateWindow(self):
        """
        Creates the buttons according to the field setup
        """
        if self.widget.abstractDb == None:
            QtGui.QMessageBox.critical(self, self.tr('Error!'), self.tr('First select a database!'))
            return
        if isinstance(self.sender(), QPushButton):
            sender = self.sender().text()
        else:
            sender = ''
        dlg = FieldSetup(self.widget.abstractDb)
        if sender != self.tr('Setup'):
            dlg.loadReclassificationConf(self.reclassificationDict)
        if sender != '':
            result = dlg.exec_()
        else:
            result = 1
        
        if result == 1:
            self.createButtonsOnInterface(dlg)
            self.setEditButtonEnabled(True)
            
    def createButtonsOnInterface(self, dlg):
        """
        Creates button according to what is set in the configuration
        :param dlg:
        :return:
        """
        #reclassification dictionary made from the field setup file
        self.reclassificationDict = dlg.makeReclassificationDict()
        #button size defined by the user
        self.size = dlg.slider.value()
        #check if the button must be grouped by category
        withTabs = dlg.checkBox.isChecked()
        #actual button creation step
        self.createButtons(self.reclassificationDict, withTabs)
            
    @pyqtSlot(bool, name = 'on_newFeatureRadioButton_toggled')
    def turnButtonsOn(self, enabled):
        """
        Adjusts tool behavior. The default state makes the tool work with selected features
        but the user can choose to acquire a feature in real time. When working in real time the buttons must be checkable.
        """
        if enabled:
            #connecting iface signals
            self.iface.currentLayerChanged.connect(self.acquire)
            for button in self.buttons:
                #disconnecting the clicked signal
                button.clicked.disconnect(self.reclassify)
                #changing button behavior
                button.setCheckable(True)
        else:
            #disconnecting iface signals
            self.disconnectLayerSignals()
            try:self.iface.currentLayerChanged.disconnect(self.acquire)
            except:pass
            for button in self.buttons:
                #connecting the clicked signal
                button.clicked.connect(self.reclassify)
                #changing button behavior
                button.setCheckable(False)            
        
    def createWidgetWithoutTabs(self, formLayout):
        """
        Adjusts the scroll area to receive the buttons directly (not grouped by category)
        formLayout: Layout used to receive all the buttons
        """
        w = QtGui.QWidget()
        w.setLayout(formLayout)
        self.scrollArea.setWidget(w)

    def createWidgetWithTabs(self, formLayout):
        """
        Creates a scroll area for each form layout.
        formLayout: Layout used to receive the buttons in each tab
        """
        scrollArea = QtGui.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setFrameShape(QtGui.QFrame.Shape(0))  # no frame
        w = QtGui.QWidget()
        w.setLayout(formLayout)
        scrollArea.setWidget(w)
        return scrollArea

    def on_filterLineEdit_textChanged(self, text):
        for i in self.buttons:
            if text.lower() in i.text().lower():
                i.show()
            else:
                i.hide()
    
    def createButton(self, button, propertyDict = dict()):
        """
        Creates the buttons according to the user size definition
        button: Button name
        propertyDict: optional dict parameters that may contain other properties to button, such as color, tooltip and custom category
        """

        pushButton = QtGui.QPushButton(button)
        keys = propertyDict.keys()
        styleSheet = ''
        if 'buttonColor' in keys:
            r, g, b, a = propertyDict['buttonColor'].split(',')
            styleSheet += "background-color:rgba({0},{1},{2},{3});".format(r, g, b, a)
        if 'buttonToolTip' in keys:
            pushButton.setToolTip(propertyDict['buttonToolTip'])
        if 'buttonShortcut' in keys:
            keySequence = QKeySequence(propertyDict['buttonShortcut'])
            pushButton.setText('{0} [{1}]'.format(button, keySequence.toString(format = QKeySequence.NativeText)))
            pushButton.setShortcut(keySequence)

        pushButton.clicked.connect(self.reclassify)
        pushButton.toggled.connect(self.acquire)
        if self.size == 0:
            pushButton.setMinimumSize(100, 25)
            styleSheet += 'font-size:12px;'
        elif self.size == 1:            
            pushButton.setMinimumSize(100, 40)
            styleSheet += 'font-size:20px;'
        elif self.size == 2:            
            pushButton.setMinimumSize(100, 80)
            styleSheet += 'font-size:30px;'
        pushButton.setStyleSheet(styleSheet)
        self.buttons.append(pushButton)
        return pushButton        
        
    def createButtons(self, reclassificationDict, createTabs=False):
        """
        Convenience method to create buttons
        createTabs: Indicates if the buttons must be created within tabs
        """
        self.buttons = []
        widget = self.scrollArea.takeWidget()
        if createTabs:
            self.createButtonsWithTabs(reclassificationDict)
        else:
            self.createButtonsWithoutTabs(reclassificationDict)
        self.turnButtonsOn(self.newFeatureRadioButton.isChecked())
            
    def createButtonsWithoutTabs(self, reclassificationDict):
        """
        Specific method to create buttons without tabs
        reclassificationDict: dictionary used to create the buttons
        """
        formLayout = QtGui.QFormLayout()
        self.createWidgetWithoutTabs(formLayout)
        sortedButtonNames = []
        propertyDict = dict()
        for category in reclassificationDict.keys():
            if category in ['version', 'uiParameterJsonDict']:
                continue
            for edgvClass in reclassificationDict[category].keys():
                for button in reclassificationDict[category][edgvClass].keys():
                    item = reclassificationDict[category][edgvClass][button]
                    propertyDict[button] = dict()
                    if isinstance(item, dict):
                        if 'buttonProp' in item.keys():
                            propertyDict[button] = item['buttonProp']
                    sortedButtonNames.append(button)
        sortedButtonNames.sort()
        for button in sortedButtonNames:       
            pushButton = self.createButton(button, propertyDict = propertyDict[button])
            formLayout.addRow(pushButton)

    def createButtonsWithTabs(self, reclassificationDict):
        """
        Specific method to create buttons with tabs
        reclassificationDict: dictionary used to create the buttons
        """
        gridLayout = QtGui.QGridLayout()
        tabWidget = QtGui.QTabWidget()
        tabWidget.setTabPosition(QtGui.QTabWidget.West)
        gridLayout.addWidget(tabWidget)
        self.scrollArea.setWidget(tabWidget)
        propertyDict = dict()
        for category in reclassificationDict.keys():
            if category in ['version', 'uiParameterJsonDict']:
                continue
            sortedButtonNames = []
            formLayout = QtGui.QFormLayout()
            scrollArea = self.createWidgetWithTabs(formLayout)
            tabWidget.addTab(scrollArea, category)
            for edgvClass in reclassificationDict[category].keys():
                for button in reclassificationDict[category][edgvClass].keys():
                    item = reclassificationDict[category][edgvClass][button]
                    propertyDict[button] = dict()
                    if isinstance(item, dict):
                        if 'buttonProp' in item.keys():
                            propertyDict[button] = item['buttonProp']
                    sortedButtonNames.append(button)
            sortedButtonNames.sort()
            for button in sortedButtonNames:       
                pushButton = self.createButton(button, propertyDict = propertyDict[button])
                formLayout.addRow(pushButton)
                    
    def loadLayer(self, layer):
        """
        Loads the layer used in the actual reclassification
        layer: Layer name
        """
        try:
            return self.layerLoader.load([layer], uniqueLoad=True)[layer]
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Error!'), self.tr('Could not load the selected classes!\n')+':'.join(e.args))
            
    def checkConditions(self):
        """
        Check the conditions to see if the tool can be used
        """
        if not self.widget.abstractDb:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Please, select a database.'))
            return False
        
        try:
            version = self.widget.abstractDb.getDatabaseVersion()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Problem obtaining database version! Please, check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return False

        if 'version' not in self.reclassificationDict.keys():
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('File not formated propperly.'))
            return False
            
        if self.reclassificationDict['version'] != version:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Database version does not match the field toolbox version.'))
            return False
        return True
    
    def getLayerFromButton(self, buttonText):
        """
        Gets the correct layer to be used in the tool
        """
        #edgvClass found in the dictionary (this is made using the sqlite seed)
        button = buttonText.split(' [')[0]
        (category, edgvClass) = self.findReclassificationClass(button)
        
        driverName = self.widget.abstractDb.getType()
        if driverName == "QSQLITE":
            #reclassification layer name
            reclassificationClass = '_'.join(edgvClass.split('_')[1::])
        if driverName == "QPSQL":
            #reclassification layer name
            reclassificationClass = '_'.join(edgvClass.split('.')[1::])
            
        #getting the QgsVectorLayer to perform the reclassification
        reclassificationLayer = self.loadLayer(reclassificationClass)
        
        if reclassificationLayer:
            self.iface.setActiveLayer(reclassificationLayer)
            #entering in editing mode
            if not reclassificationLayer.isEditable():
                reclassificationLayer.startEditing()
            lyrAttributes = [i.name() for i in reclassificationLayer.pendingFields()]
            for attr in self.reclassificationDict[category][edgvClass][button].keys():
                if attr == 'buttonProp':
                    continue
                candidateDict = self.reclassificationDict[category][edgvClass][button][attr]
                if isinstance(candidateDict, dict):
                    if candidateDict['isEditable'] == '0' and attr in lyrAttributes:
                        attrIdx = lyrAttributes.index(attr)
                        reclassificationLayer.setFieldEditable(attrIdx, False)

        return (reclassificationLayer, category, edgvClass)
    
    @pyqtSlot(int)
    def setAttributesFromButton(self, featureId):
        """
        Sets the attributes for the newly added feature
        featureId: added feature
        """
        layer = self.sender()
        if isinstance(layer, QgsVectorLayer):
            layer.beginEditCommand(self.tr('DsgTools reclassification'))
            self.addedFeatures.append(featureId)

    def updateAttributesAfterAdding(self):
        """
        Updates feature attributes according to the button configuration
        :return:
        """
        layer = self.sender()
        while self.addedFeatures:
            featureId = self.addedFeatures.pop()
            #begining the edit command
            # layer.beginEditCommand(self.tr("DSG Tools reclassification tool: adjusting feature's attributes"))
            #accessing added features
            editBuffer = layer.editBuffer()
            features = editBuffer.addedFeatures()
            for key in features.keys():
                #just checking the newly added feature, the other I don't care
                if key == featureId:
                    feature = features[key]
                    #setting the attributes using the reclassification dictionary
                    self.setFeatureAttributes(feature, editBuffer)
            layer.endEditCommand()

    def setFeatureAttributes(self, newFeature, editBuffer=None, oldFeat = None):
        """
        Changes attribute values according to the reclassification dict using the edit buffer
        newFeature: newly added
        editBuffer: layer edit buffer
        """
        #setting the attributes using the reclassification dictionary
        for attribute in self.reclassificationDict[self.category][self.edgvClass][self.buttonName].keys():
            if attribute == 'buttonProp':
                continue
            idx = newFeature.fieldNameIndex(attribute)
            #value to be changed
            reclass = self.reclassificationDict[self.category][self.edgvClass][self.buttonName][attribute]
            if isinstance(reclass, dict):
                value = reclass['value']
                if reclass['isIgnored'] == '1': #ignore clause
                    if oldFeat:
                        value = oldFeat[attribute]
            else:
                value = reclass
            if value == '':
                continue
            #actual attribute change
            if editBuffer:
                #this way we are working with the edit buffer
                editBuffer.changeAttributeValue(newFeature.id(), idx, value)
            else:
                #this way are working with selected features and inserting a new one in the layer
                newFeature.setAttribute(idx, value)
                
        if not editBuffer:
            # we should return when under the normal behavior
            return newFeature
        
    def disconnectLayerSignals(self):
        """
        Disconnecting the signals from the previous layer
        """
        if self.prevLayer:
            try:
                self.prevLayer.featureAdded.disconnect(self.setAttributesFromButton)
                self.prevLayer.editCommandEnded.disconnect(self.updateAttributesAfterAdding)
                self.prevLayer.editFormConfig().setSuppress(QgsEditFormConfig.SuppressOff)
            except:
                pass

    @pyqtSlot(bool)
    def acquire(self, pressed):
        """
        Performs the actual reclassification, moving the geometry to the correct layer along with the specified attributes.
        The difference here is the use of real time editing to make the reclassification
        """
        if pressed:
            if not self.checkConditions():
                return
            
            #getting the object that sent the signal
            sender = self.sender()
            
            #if the sender is the iface object, this means that the user made the click and changed the current layer
            #when this happens we should untoggle all buttons
            if isinstance(sender, QgisInterface):
                #checking if another button is checked
                for button in self.buttons:
                    button.setChecked(False)
                #return and do nothing else
                return

            #button that sent the signal
            self.buttonName = sender.text().split(' [')[0]
    
            #checking if another button is checked
            for button in self.buttons:
                if button.text().split(' [')[0] != self.buttonName and button.isChecked():
                    button.setChecked(False)
                    
            #disconnecting the previous layer
            self.disconnectLayerSignals()
    
            (reclassificationLayer, self.category, self.edgvClass) = self.getLayerFromButton(self.buttonName)

            #suppressing the form dialog
            if 'openForm' in self.reclassificationDict[self.category][self.edgvClass][self.buttonName]['buttonProp'].keys():
                reclassificationLayer.editFormConfig().setSuppress(QgsEditFormConfig.SuppressOff)
            else:
                reclassificationLayer.editFormConfig().setSuppress(QgsEditFormConfig.SuppressOn)
            #connecting addedFeature signal
            reclassificationLayer.featureAdded.connect(self.setAttributesFromButton)
            reclassificationLayer.editCommandEnded.connect(self.updateAttributesAfterAdding)
            #triggering the add feature tool
            self.iface.actionAddFeature().trigger()            
            #setting the previous layer             
            self.prevLayer = reclassificationLayer        
        else:
            #disconnecting the previous layer
            self.disconnectLayerSignals()
            
    @pyqtSlot()
    def reclassify(self):
        """
        Performs the actual reclassification, moving the geometry to the correct layer along with the specified attributes
        """
        if not self.checkConditions():
            return
        
        somethingMade = False
        reclassifiedFeatures = 0
        deleteList = []
        #button that sent the signal
        self.buttonName = self.sender().text().split(' [')[0]
        (reclassificationLayer, self.category, self.edgvClass) = self.getLayerFromButton(self.buttonName)
        geomType = reclassificationLayer.geometryType()
        hasMValues =  QgsWKBTypes.hasM(int(reclassificationLayer.wkbType()))    #generic check (not every database is implemented as ours)
        hasZValues =  QgsWKBTypes.hasZ(int(reclassificationLayer.wkbType()))    #
        isMulti = QgsWKBTypes.isMultiType(int(reclassificationLayer.wkbType())) #
        mapLayers = self.iface.mapCanvas().layers()
        #we need to get the authid that thefines the ref system of destination layer
        crsSrc = QgsCoordinateReferenceSystem(reclassificationLayer.crs().authid())
        for mapLayer in mapLayers:
            if mapLayer.type() != QgsMapLayer.VectorLayer:
                continue
            
            #iterating over selected features
            featList = []
            mapLayerCrs = mapLayer.crs()
            #creating a coordinate transformer (mapLayerCrs to crsSrc)
            coordinateTransformer = QgsCoordinateTransform(mapLayerCrs, crsSrc)
            for feature in mapLayer.selectedFeatures():
                geomList = []
                geom = feature.geometry()
                if geom.type() != geomType:
                    continue
                if 'geometry' in dir(geom):
                    if not hasMValues:
                        geom.geometry().dropMValue()
                    if not hasZValues:
                        geom.geometry().dropZValue()
                if isMulti and not geom.isMultipart():
                    geom.convertToMultiType()
                    geomList.append(geom)
                if not isMulti and geom.isMultipart():
                    #deaggregate here
                    parts = geom.asGeometryCollection()
                    for part in parts:
                        part.convertToSingleType()
                        geomList.append(part)
                else:
                    geomList.append(geom)
                for newGeom in geomList:
                    #creating a new feature according to the reclassification layer
                    newFeature = QgsFeature(reclassificationLayer.pendingFields())
                    #transforming the geometry to the correct crs
                    geom.transform(coordinateTransformer)
                    #setting the geometry
                    newFeature.setGeometry(newGeom)
                    #setting the attributes using the reclassification dictionary
                    newFeature = self.setFeatureAttributes(newFeature, oldFeat = feature)
                    #adding the newly created feature to the addition list
                    featList.append(newFeature)
                    somethingMade = True
                    deleteList.append({'originalLyr':mapLayer,'featid':feature.id()})
            #actual feature insertion
            reclassificationLayer.addFeatures(featList, False)
            reclassifiedFeatures += len(featList)
        
        for item in deleteList:
            item['originalLyr'].startEditing()
            item['originalLyr'].deleteFeature(item['featid'])
        
        if somethingMade:
            self.iface.messageBar().pushMessage(self.tr('Information!'), self.tr('{} features reclassified with success!').format(reclassifiedFeatures), level=QgsMessageBar.INFO, duration=3)

    def findReclassificationClass(self, button):
        """
        Finds the reclassification class according to the button
        button: Button clicked by the user to perform the reclassification
        """
        for category in self.reclassificationDict.keys():
            if category == 'version' or category == 'uiParameterJsonDict':
                continue
            for edgvClass in self.reclassificationDict[category].keys():
                for buttonName in self.reclassificationDict[category][edgvClass].keys():
                    if button == buttonName:
                        #returning the desired edgvClass
                        return (category, edgvClass)
        return ()
    
    def populateConfigFromDb(self):
        """
        Populates configFromDbComboBox with config from public.field_toolbox_config
        """
        driverName = self.widget.abstractDb.getType()
        self.configFromDbComboBox.clear()
        self.configFromDbComboBox.addItem(self.tr('Select Stored Config (optional)'))
        if driverName == 'QPSQL':
            self.configFromDbComboBox.setEnabled(True)
            propertyDict = self.widget.abstractDb.getPropertyDict('FieldToolBoxConfig')
            dbVersion = self.widget.abstractDb.getDatabaseVersion()
            if dbVersion in propertyDict.keys():
                self.configFromDbDict = propertyDict[dbVersion]
            nameList = self.configFromDbDict.keys()
            nameList.sort()
            for name in nameList:
                self.configFromDbComboBox.addItem(name)
        else:
            self.configFromDbComboBox.setEnabled(False)
            self.configFromDbDict = dict()
    
    @pyqtSlot(int)
    def on_configFromDbComboBox_currentIndexChanged(self, idx):
        if idx != 0 and idx != -1:
            self.reclassificationDict = self.configFromDbDict[self.configFromDbComboBox.currentText()]
            self.populateWindow()
        if idx == 0:
            self.reclassificationDict = {}
            self.createButtonsWithTabs(self.reclassificationDict)
