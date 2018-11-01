 
# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-09-26
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QDialog 

from DsgTools.core.dsgEnums import DsgEnums

import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'abstractMultiDsSelectorWidget.ui'))

class AbstractMultiDsSelectorWidget(QDialog, FORM_CLASS):
    """
    Class containing minimum structure for multiple datasource selection.
    Particularities from each driver are settled within its own class (child from this). 
    """
    def __init__(self, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) widget parent to new instance.
        """
        super(AbstractMultiDsSelectorWidget, self).__init__(parent)
        self.setupUi(self)
        self.widget = self.getMultiDsWidget()
        self.source = -1 # no source is selected
        if self.widget:
            self.addInputWidgetToLayout(widget=self.widget)
        if not self.createDbCheckBox.isChecked():
            self.edgvComboBox.hide()
            self.mQgsProjectionSelectionWidget.hide()
        self.clearMultiDsDict() # instantiate a clear multiple ds input map inclusion.
        self.fillDriversVersion(isNew=self.createDbCheckBox.isChecked())
        self.fillEdgvVersion()

    def getMultiDsWidget(self, parent=None):
        """
        Gets the multiple datasource selection widget
        :param parent: (QWidget) widget parent to new multi datasource widget.
        """
        # to be reimplemented into child class

    def clearMultiDsDict(self):
        """
        Clears multiple datasource input conversion map.
        """
        self.multiDsDict = {
            'databases' : [],
            'autoMapOptions' : {
                'createDb' : self.createDbCheckBox.isChecked(),
                'outDriver' : DsgEnums.NoDriver,
                'outEdgv' : '',
                'mapType' : ''
            }
        }

    def clearAutoMapDict(self):
        """
        Clears automatic mapping dict.
        """
        self.multiDsDict['autoMapOptions'] = {
                'createDb' : self.createDbCheckBox.isChecked(),
                'outDriver' : DsgEnums.NoDriver,
                'outEdgv' : '',
                'mapType' : ''
            }

    def resetAutoMapDict(self):
        """
        Resets automatic mapping dict to current widgets' contents.
        """
        self.on_createDbCheckBox_toggled(isChecked=self.createDbCheckBox.isChecked())
        self.on_driverComboBox_currentIndexChanged()
        self.on_edgvComboBox_currentIndexChanged()

    def addInputWidgetToLayout(self, widget):
        """
        Adds a given widget to input layout (left side of upper part).
        :param widget: (QWidget) widget to be added to grid.
        """
        # useful for adding its own widget without much thinking...
        self.inputLayout.addWidget(widget)

    def addOutputWidgetToLayout(self, widget):
        """
        Adds a given widget to output layout (right side of upper part).
        :param widget: (QWidget) widget to be added to grid.
        """
        # useful for adding its own widget without much thinking...
        self.outputLayout.addWidget(widget)

    def updateEdgvOut(self, edgv=''):
        """
        Update output EDGV version with a new value.
        :param edgv: (str) new edgv version. 
        """
        self.multiDsDict['autoMapOptions']['outEdgv'] = edgv if edgv != self.tr('EDGV Version...') else ''

    def disableAutoMap(self, status):
        """
        Set all auto map related widget enabled status.
        """
        self.createDbCheckBox.setEnabled(status)
        self.driverComboBox.setEnabled(status)
        self.edgvComboBox.setEnabled(status)
        self.mQgsProjectionSelectionWidget.setEnabled(status)
        if status:
            self.resetAutoMapDict()
        else:
            self.clearAutoMapDict()

    def updateMapType(self, mapType=''):
        """
        Update conversion mapping type with a new value. If no map is selected, all automatic 
        mapping related widgets will be disabled.
        :param mapType: (str) new mapping type. 
        """
        self.multiDsDict['autoMapOptions']['mapType'] = mapType
        self.disableAutoMap(bool(mapType))

    def updateOutDriver(self, driver):
        """
        Update output EDGV version with a new value.
        :param edgv: (str) output driver enum. 
        """
        driversDict = {
            '' : DsgEnums.NoDriver,
            self.tr('Select a driver...') : DsgEnums.NoDriver,
            'PostGIS' : DsgEnums.PostGIS,
            'SpatiaLite' : DsgEnums.SpatiaLite,
            'Shapefile' : DsgEnums.Shapefile,
            'Geopackage' : DsgEnums.Geopackage
        }
        self.multiDsDict['autoMapOptions']['outDriver'] = driversDict[driver]

    def fillEdgvVersion(self):
        """
        Fills output EDGV version combo box with all available options.
        """
        edgvs = [
            self.tr('EDGV Version...'),
            '2.1.3',
            '2.1.3 Pro',
            '3.0',
            '3.0 Pro'
        ]
        self.edgvComboBox.addItems(edgvs)

    def fillDriversVersion(self, isNew):
        """
        Fills output EDGV version combo box with all available options.
        """
        drivers = [
            self.tr('Select a driver...'),
            'PostGIS',
            'SpatiaLite',
            'Shapefile',
            'Geopackage'
        ]
        self.driverComboBox.addItems(drivers)

    @pyqtSlot(bool)
    def on_createDbCheckBox_toggled(self, isChecked):
        """
        Disables/enables EDGV version and updates dict entry. 
        """
        # update dict entry
        self.multiDsDict['autoMapOptions']['createDb'] = isChecked
        # clear output edgv version, if necessary
        edgv = self.edgvComboBox.currentText() if isChecked else ''
        self.updateEdgvOut(edgv=edgv)
        # control edgv widget enabled status
        if not isChecked:
            self.edgvComboBox.hide()
            self.mQgsProjectionSelectionWidget.hide()
        else:
            self.edgvComboBox.show()
            self.mQgsProjectionSelectionWidget.show()

    @pyqtSlot(int)
    def on_driverComboBox_currentIndexChanged(self):
        """
        Updates output driver info.
        """
        currentText = self.driverComboBox.currentText()
        self.updateOutDriver(driver=currentText)

    @pyqtSlot(int)
    def on_edgvComboBox_currentIndexChanged(self):
        """
        Updates output driver info.
        """
        currentText = self.edgvComboBox.currentText()
        edgv = currentText if currentText != self.tr('EDGV Version...') or self.createDbCheckBox.isChecked() else ''
        self.updateEdgvOut(edgv=edgv)

    @pyqtSlot(bool, name='on_noMapRadioButton_toggled')
    @pyqtSlot(bool, name='on_singleRadioButton_toggled')
    @pyqtSlot(bool, name='on_consolidateRadioButton_toggled')
    def radioButtonChanged(self):
        """
        Updates type of automatic conversion
        """
        buttonNameDict = {
            'noMapRadioButton' : '',
            'singleRadioButton' : 'single',
            'consolidateRadioButton' : 'consolidate'
        }
        buttonName = self.sender().objectName()
        self.updateMapType(mapType=buttonNameDict[buttonName])

    def validate(self):
        """
        Validates contents information.
        :return: (bool) whether contents are a valid selection.
        """
        pass

    @pyqtSlot(bool)
    def on_okPushButton_clicked(self):
        """
        Wraps GUI contents up, validates it and, if valid, pass information through to next conversion step.
        """
        self.validate()