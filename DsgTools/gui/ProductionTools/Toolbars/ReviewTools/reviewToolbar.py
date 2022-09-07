# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-08-11
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt.QtWidgets import QMessageBox, QSpinBox, QAction, QWidget
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QSettings, pyqtSignal, pyqtSlot, QObject, Qt
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.Qt import QVariant
from qgis.PyQt.Qt import QObject

from qgis.core import QgsMapLayer, Qgis, QgsVectorLayer, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsFeatureRequest, QgsWkbTypes, QgsProject
from qgis.gui import QgsMessageBar

from .review_ui import Ui_ReviewToolbar

class ReviewToolbar(QWidget, Ui_ReviewToolbar):
    idxChanged = pyqtSignal(int)
    def __init__(self, iface, parent = None):
        """
        Constructor
        """
        super(ReviewToolbar, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.splitter.hide()
        self.iface = iface
        # self.iface.currentLayerChanged.connect(self.enableScale)
        
        self.canvas = self.iface.mapCanvas()
        self.mMapLayerComboBox.layerChanged.connect(self.mFieldComboBox.setLayer)
        self.setToolTip('')
        icon_path = ':/plugins/DsgTools/icons/attributeSelector.png'
        text = self.tr('DSGTools: Mark tile as done')
        self.applyPushButtonAction = self.add_action(icon_path, text, self.applyPushButton.click, parent = self.parent)
        self.iface.registerMainWindowAction(self.applyPushButtonAction, '')
        self.mMapLayerComboBox.setAllowEmptyLayer(True)
        self.mMapLayerComboBox.setCurrentIndex(0)
    
    def add_action(self, icon_path, text, callback, parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        if parent:
            parent.addAction(action)
        return action

    def enableTool(self, enabled = True):
        allowed = False if enabled == None or not isinstance(enabled, QgsVectorLayer) else True
        toggled = self.reviewPushButton.isChecked()
        enabled = allowed and toggled
        self.applyPushButton.setEnabled(enabled)
    
    def on_preparePushButton_clicked(self):
        overviewWidget = self.getOverviewWidget()
        if overviewWidget is not None:
            overviewWidget.show()
        currentLayer = self.mMapLayerComboBox.currentLayer()
        if currentLayer is None:
            return
        currentLayerFromTreeRoot = QgsProject.instance().layerTreeRoot().findLayer( currentLayer.id() )
        currentLayerFromTreeRoot.setCustomProperty( "overview", 1 )
        fieldList = [field for field in self.mFieldComboBox.fields() if field.name() == self.mFieldComboBox.currentField()]
        if len(fieldList) == 0 or fieldList[0].type() != QVariant.Bool:
            self.iface.messageBar().pushMessage(self.tr('Warning!'), self.tr('Invalid attribute filter!'), level=Qgis.Warning, duration=2)
            return
        currentField = fieldList[0]
        self.applyStyle(currentLayer, currentField.name())
        
    
    def getOverviewWidget(self):
        itemList = [i for i in self.iface.mainWindow().children() if i.objectName() == 'Overview']
        return None if len(itemList) == 0 \
            else itemList[0]
    
    def applyStyle(self, lyr, fieldName):
        stylePath = self.createTempStyle(fieldName)
        lyr.loadNamedStyle(stylePath, True)
        lyr.triggerRepaint()
        self.deleteTempStyle(stylePath)
    
    def createTempStyle(self, fieldName):
        currentPath = os.path.dirname(os.path.abspath(__file__))
        templatePath = os.path.join(currentPath, 'grid_style.qml')
        tempOutputPath = os.path.join(currentPath, 'grid_style_temp.qml')
        with open(templatePath) as f:
            templateFile = f.read()
        templateFile = templateFile.replace('attr="visited"', f'attr="{fieldName}"')
        with open(tempOutputPath, 'w') as f:
            f.write(templateFile)
        return tempOutputPath
    
    def deleteTempStyle(self, tempStylePath):
        os.remove(tempStylePath)
        
    @pyqtSlot(bool, name = 'on_reviewPushButton_toggled')
    def toggleBar(self, toggled=None):
        """
        Shows/Hides the tool bar
        """
        if toggled is None:
            toggled = self.reviewPushButton.isChecked()
        if toggled:
            self.splitter.show()
            self.enableTool(self.mMapLayerComboBox.currentLayer())
            self.setToolTip(self.tr('Select a vector layer to enable tool'))
        else:
            self.splitter.hide()   
            self.enableTool(False)
            self.setToolTip('')

    def unload(self):
        self.iface.unregisterMainWindowAction(self.applyPushButtonAction)      
