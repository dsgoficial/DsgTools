 
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

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QDialog 

import .abstractMultiDsSelectorWidget import abstractMultiDsSelectorWidget

import os

FORM_CLASS, _ = uic.load(os.path.join(os.path.dirname(__file__), 'abstractMultiDsSelectorWidget.ui'))

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
        if not self.createDbCheckBox.isChecked():
            self.edgvComboBox.hide()
        self.multiDsDict = {
            'databases' : [],
            'autoMapOption' : {
                'createDb' : self.createDbCheckBox.isChecked(),
                'outDriver' : DsgEnums.NoDriver,
                'outEdgv' : '',
                'mapType' : ''
            }
        }
        self.fillDriversVersion()
        self.fillEdgvVersion()

    def addWidgetToLayout(self, widget):
        """
        Adds a given widget to (0,0) position of this dialog's grid layout.
        :param widget: (QWidget) widget to be added to grid.
        """
        # useful for adding its own widget without much thinking...
        self.driverGridLayout.addWidget(widget, 0, 0)

    def updateEdgvOut(self, edgv=''):
        """
        Update output EDGV version with a new value.
        :param edgv: (str) new edgv version. 
        """
        self.multiDsDict['autoMapOptions']['outEdgv'] = edgv

    def updateOutDriver(self, driver):
        """
        Update output EDGV version with a new value.
        :param edgv: (str) output driver enum. 
        """
        driversDict = [
            self.tr('Select a driver...') : DsgEnums.NoDriver,
            'PostGIS' : DsgEnums.PostGIS,
            'SpatiaLite' : DsgEnums.SpatiaLite,
            'Shapefile' : DsgEnums.Shapefile,
            'Geopackage' : DsgEnums.Geopackage
        ]
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
        if isChecked:
            self.edgvComboBox.hide()
        else:
            self.edgvComboBox.show()

    @pyqtSlot(int)
    def on_driverComboBox_currentIndexChanged(self, idx):
        """
        Updates output driver info.
        :param idx: output driver combo box current index. 
        """
        currentText = self.edgvComboBox.currentText()
        self.updateOutDriver(driver=currentText)

    @pyqtSlot(int)
    def on_edgvComboBox_currentIndexChanged(self, idx):
        """
        Updates output driver info.
        :param idx: output EDGV combo box current index. 
        """
        currentText = self.edgvComboBox.currentText()
        edgv = currentText if currentText != self.tr('EDGV Version...') or self.createDbCheckBox.isChecked() else ''
        self.updateEdgvOut(edgv=edgv)

    @pyqtSlot()
    @pyqtSlot()
    @pyqtSlot()
    def radioButtonChanged(self):
        """
        Defines
        """
        pass