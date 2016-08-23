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
from PyQt4.QtCore import pyqtSlot, Qt
from PyQt4.QtCore import pyqtSlot, pyqtSignal

# QGIS imports
from qgis.core import QgsMapLayer, QgsDataSourceURI, QgsGeometry, QgsMapLayerRegistry, QgsProject, QgsLayerTreeLayer, QgsFeature, QgsMessageLog, QgsCoordinateTransform, QgsCoordinateReferenceSystem, QgsEditFormConfig
from qgis.gui import QgsMessageBar, QgisInterface
import qgis as qgis

#DsgTools imports
from DsgTools.ProductionTools.FieldToolBox.field_setup import FieldSetup
from DsgTools.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.Factories.LayerFactory.layerFactory import LayerFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'field_toolbox.ui'))

class FieldToolbox(QtGui.QDockWidget, FORM_CLASS):
    def __init__(self, iface, codeList, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface
        self.codeList = codeList
        self.buttons = []
        self.prevLayer = None
        self.buttonName = ''
        self.category = ''
        self.layerFactory = LayerFactory()        
        
    @pyqtSlot(bool)
    def on_setupButton_clicked(self):
        '''
        Creates the buttons according to the field setup
        '''
        dlg = FieldSetup()
        result = dlg.exec_()
        
        if result == 1:
            #reclassification dictionary made from the field setup file
            self.reclassificationDict = dlg.makeReclassificationDict()
            #button size defined by the user
            self.size = dlg.slider.value()
            #check if the button must be grouped by category
            withTabs = dlg.checkBox.isChecked()
            #actual button creation step
            self.createButtons(self.reclassificationDict, withTabs)
            
    @pyqtSlot(int)
    def on_checkBox_stateChanged(self, state):
        '''
        Adjusts tool behavior. The default state makes the tool work with selected features
        but the user can choose to acquire a feature in real time. When working in real time the buttons must be checkable.
        '''
        if self.checkBox.checkState() == Qt.Checked:
            #connecting iface signals
            self.iface.currentLayerChanged.connect(self.acquire)
            for button in self.buttons:
                #disconnecting the clicked signal
                button.clicked.disconnect(self.reclassify)
                #changing button behavior
                button.setCheckable(True)
        else:
            #disconnecting iface signals
            try:self.iface.currentLayerChanged.disconnect(self.acquire)
            except:pass
            for button in self.buttons:
                #connecting the clicked signal
                button.clicked.connect(self.reclassify)
                #changing button behavior
                button.setCheckable(False)            
        
    def createWidgetWithoutTabs(self, formLayout):
        '''
        Adjusts the scroll area to receive the buttons directly (not grouped by category)
        formLayout: Layout used to receive all the buttons
        '''
        w = QtGui.QWidget()
        w.setLayout(formLayout)
        self.scrollArea.setWidget(w)

    def createWidgetWithTabs(self, formLayout):
        '''
        Creates a scroll area for each form layout.
        formLayout: Layout used to receive the buttons in each tab
        '''
        scrollArea = QtGui.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setFrameShape(QtGui.QFrame.Shape(0))  # no frame
        w = QtGui.QWidget()
        w.setLayout(formLayout)
        scrollArea.setWidget(w)
        return scrollArea
    
    def createButton(self, button):
        '''
        Creates the buttons according to the user size definition
        button: Button name
        '''
        pushButton = QtGui.QPushButton(button)
        pushButton.clicked.connect(self.reclassify)
        pushButton.toggled.connect(self.acquire)
        if self.size == 0:
            pushButton.setMinimumSize(100, 25)
            pushButton.setStyleSheet('font-size:12px')
        elif self.size == 1:            
            pushButton.setMinimumSize(100, 40)
            pushButton.setStyleSheet('font-size:20px')
        elif self.size == 2:            
            pushButton.setMinimumSize(100, 80)
            pushButton.setStyleSheet('font-size:30px')
        self.buttons.append(pushButton)
        return pushButton        
        
    def createButtons(self, reclassificationDict, createTabs = False):
        '''
        Convenience method to create buttons
        createTabs: Indicates if the buttons must be created within tabs
        '''
        self.buttons = []
        widget = self.scrollArea.takeWidget()
        if createTabs:
            self.createButtonsWithTabs(reclassificationDict)
        else:
            self.createButtonsWithoutTabs(reclassificationDict)
            
        self.on_checkBox_stateChanged(0)
            
    def createButtonsWithoutTabs(self, reclassificationDict):
        '''
        Specific method to create buttons without tabs
        reclassificationDict: dictionary used to create the buttons
        '''
        formLayout = QtGui.QFormLayout()
        self.createWidgetWithoutTabs(formLayout)
        sortedButtonNames = []
        for category in reclassificationDict.keys():
            if category == 'version':
                continue
            for edgvClass in reclassificationDict[category].keys():
                for button in reclassificationDict[category][edgvClass].keys():
                    sortedButtonNames.append(button)
        sortedButtonNames.sort()
        for button in sortedButtonNames:       
            pushButton = self.createButton(button)
            formLayout.addRow(pushButton)

    def createButtonsWithTabs(self, reclassificationDict):
        '''
        Specific method to create buttons with tabs
        reclassificationDict: dictionary used to create the buttons
        '''
        gridLayout = QtGui.QGridLayout()
        tabWidget = QtGui.QTabWidget()
        tabWidget.setTabPosition(QtGui.QTabWidget.West)
        gridLayout.addWidget(tabWidget)
        self.scrollArea.setWidget(tabWidget)
        
        for category in reclassificationDict.keys():
            if category == 'version':
                continue
            sortedButtonNames = []
            formLayout = QtGui.QFormLayout()
            scrollArea = self.createWidgetWithTabs(formLayout)
            tabWidget.addTab(scrollArea, category)
            for edgvClass in reclassificationDict[category].keys():
                for button in reclassificationDict[category][edgvClass].keys():
                    sortedButtonNames.append(button)
            sortedButtonNames.sort()
            for button in sortedButtonNames:       
                pushButton = self.createButton(button)
                formLayout.addRow(pushButton)
                    
    def loadLayer(self, layer):
        '''
        Loads the layer used in the actual reclassification
        layer: Layer name
        '''
        try:
            dbName = self.widget.abstractDb.getDatabaseName()
            groupList =  qgis.utils.iface.legendInterface().groups()
            edgvLayer = self.layerFactory.makeLayer(self.widget.abstractDb, self.codeList, layer)
            if dbName in groupList:
                return edgvLayer.load(self.widget.crs, groupList.index(dbName))
            else:
                parentTreeNode = qgis.utils.iface.legendInterface().addGroup(dbName, -1)
                return edgvLayer.load(self.widget.crs, parentTreeNode)
        except:
            QtGui.QMessageBox.critical(self, self.tr('Error!'), self.tr('Could not load the selected classes!'))
            
    def checkConditions(self):
        '''
        Check the conditions to see if the tool can be used
        '''
        if not self.widget.abstractDb:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Please, select a database.'))
            return False
        
        try:
            version = self.widget.abstractDb.getDatabaseVersion()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Problem obtaining database version! Please, check log for details.'))
            QgsMessageLog.logMessage(e.args[0], "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return False
            
        if self.reclassificationDict['version'] != version:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Database version does not match the field toolbox version.'))
            return False
        return True
    
    def getLayerFromButton(self, button):
        '''
        Gets the correct layer to be used in the tool
        '''
        #edgvClass found in the dictionary (this is made using the sqlite seed)
        (category, edgvClass) = self.findReclassificationClass(button)
        #reclassification layer name
        reclassificationClass = '_'.join(edgvClass.split('_')[1::])
        
        driverName = self.widget.abstractDb.getType()
        if driverName == "QSQLITE":
            dsgClass = edgvClass # do not change the class name, already is in schema_table form
        if driverName == "QPSQL":
            dsgClass = edgvClass.split('_')[0] +'.'+ '_'.join(edgvClass.split('_')[1::]) # change the class name, must be in schema.table form
            
        #searching the QgsVectorLayer to perform the reclassification
        root = QgsProject.instance().layerTreeRoot()
        reclassificationLayer = self.searchLayer(root, reclassificationClass)
        if not reclassificationLayer:
            reclassificationLayer = self.loadLayer(dsgClass)
             
        self.iface.setActiveLayer(reclassificationLayer)
            
        #entering in editing mode
        reclassificationLayer.startEditing()

        return (reclassificationLayer, category, edgvClass)
    
    @pyqtSlot(int)
    def setAttributesFromButton(self, featureId):
        '''
        Sets the attributes for the newly added feature
        featureId: added feature
        '''
        #layer that sent the signal
        layer = self.sender()
        #accessing added features
        editBuffer = layer.editBuffer()
        features = editBuffer.addedFeatures()
        for key in features.keys():
            #just checking the newly added feature, the other I don't care
            if key == featureId:
                feature = features[key]
                #setting the attributes using the reclassification dictionary
                self.setFeatureAttributes(feature, editBuffer)
                
    def setFeatureAttributes(self, newFeature, editBuffer = None):
        '''
        Changes attribute values according to the reclassification dict using the edit buffer
        newFeature: newly added
        editBuffer: layer edit buffer
        '''
        #setting the attributes using the reclassification dictionary
        for attribute in self.reclassificationDict[self.category][self.edgvClass][self.buttonName].keys():
            idx = newFeature.fieldNameIndex(attribute)
            #value to be changed
            value = self.reclassificationDict[self.category][self.edgvClass][self.buttonName][attribute]
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
        '''
        Disconnecting the signals from the previous layer
        '''
        if self.prevLayer:
            try:
                self.prevLayer.featureAdded.disconnect(self.setAttributesFromButton)
            except:
                pass
            self.prevLayer.editFormConfig().setSuppress(QgsEditFormConfig.SuppressOff)
            
    @pyqtSlot(bool)
    def acquire(self, pressed):
        '''
        Performs the actual reclassification, moving the geometry to the correct layer along with the specified attributes.
        The difference here is the use of real time editing to make the reclassification
        '''
        if pressed:
            if not self.checkConditions():
                return
            
            #getting the object that sent the signal
            sender = self.sender()
            
            #if the sender is out iface object, this means that the user made the click and changed the current layer
            #when this happens we should untoggle all buttons
            if isinstance(sender, QgisInterface):
                #checking if another button is checked
                for button in self.buttons:
                    button.setChecked(False)
                #return and do nothing else
                return

            #button that sent the signal
            self.buttonName = sender.text()
    
            #checking if another button is checked
            for button in self.buttons:
                if button.text() != self.buttonName and button.isChecked():
                    button.setChecked(False)
                    
            #disconnecting the previous layer
            self.disconnectLayerSignals()
    
            (reclassificationLayer, self.category, self.edgvClass) = self.getLayerFromButton(self.buttonName)
            #suppressing the form dialog
            reclassificationLayer.editFormConfig().setSuppress(QgsEditFormConfig.SuppressOn)
            #connecting addedFeature signal
            reclassificationLayer.featureAdded.connect(self.setAttributesFromButton)
            #triggering the add feature tool
            self.iface.actionAddFeature().trigger()            

            #setting the previous layer             
            self.prevLayer = reclassificationLayer                
        else:
            #disconnecting the previous layer
            self.disconnectLayerSignals()
            
    @pyqtSlot()
    def reclassify(self):
        '''
        Performs the actual reclassification, moving the geometry to the correct layer along with the specified attributes
        '''
        if not self.checkConditions():
            return
        
        somethingMade = False
        
        #button that sent the signal
        self.buttonName = self.sender().text()
        (reclassificationLayer, self.category, self.edgvClass) = self.getLayerFromButton(self.buttonName)

        mapLayers = self.iface.mapCanvas().layers()
        crsSrc = QgsCoordinateReferenceSystem(self.widget.crs.authid())
        for mapLayer in mapLayers:
            if mapLayer.type() != QgsMapLayer.VectorLayer:
                continue
            
            #iterating over selected features
            featList = []
            mapLayerCrs = mapLayer.crs()
            #creating a coordinate transformer (mapLayerCrs to crsSrc)
            coordinateTransformer = QgsCoordinateTransform(mapLayerCrs, crsSrc)
            for feature in mapLayer.selectedFeatures():
                geom = feature.geometry()
                geom.convertToMultiType()
                if 'geometry' in dir(geom):
                    if 'Multi' not in geom.geometry().geometryType():
                        geom.geometry().dropMValue()
                        geom.geometry().dropZValue()
                #creating a new feature according to the reclassification layer
                newFeature = QgsFeature(reclassificationLayer.pendingFields())
                #transforming the geometry to the correct crs
                geom.transform(coordinateTransformer)
                #setting the geometry
                newFeature.setGeometry(geom)
                #setting the attributes using the reclassification dictionary
                newFeature = self.setFeatureAttributes(newFeature)
                #adding the newly created feature to the addition list
                featList.append(newFeature)
                somethingMade = True
            #actual feature insertion
            reclassificationLayer.addFeatures(featList, False)
        
            if len(mapLayer.selectedFeatures()) > 0:
                mapLayer.startEditing()
                mapLayer.deleteSelectedFeatures()
        
        if somethingMade:
            self.iface.messageBar().pushMessage(self.tr('Information!'), self.tr('Features reclassified with success!'), level=QgsMessageBar.INFO, duration=3)
    
    def findReclassificationClass(self, button):
        '''
        Finds the reclassification class according to the button
        button: Button clicked by the user to perform the reclassification
        '''
        for category in self.reclassificationDict.keys():
            if category == 'version':
                continue
            for edgvClass in self.reclassificationDict[category].keys():
                for buttonName in self.reclassificationDict[category][edgvClass].keys():
                    if button == buttonName:
                        #returning the desired edgvClass
                        return (category, edgvClass)
        return ()
                    
    def searchLayer(self, group, name):
        '''
        Checks if a layer is already loaded in TOC. Case positive return it, case negative return None
        group: Group name
        name: Layer name
        '''
        layerNodes = group.findLayers()
        for node in layerNodes:
            if node.layerName() == name:
                return node.layer()
        return None