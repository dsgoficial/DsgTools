# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2020-07-27
        git sha              : $Format:%H$
        copyright            : (C) 2020 by  Francisco Alves Camello Neto -
                                    Surveying Technician @ Brazilian Army
        email                : camello.francisco@eb.mil.br
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
import os, json
from os.path import expanduser

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt, QSettings
from qgis.PyQt.QtWidgets import QListWidgetItem, QMessageBox, QMenu, QApplication, QFileDialog
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'validationSetOfAttributesWidget.ui'))


class ValidationSetOfAttributesWidget(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, parent=None):
        """
        Initializates ValidationSetOfAttributesWidget
        """
        super(ValidationSetOfAttributesWidget, self).__init__(parent = parent)
        self.setupUi(self)
        # self.layerDict = layerDict
        # self.layerComboBox.addItem(self.tr('Select a layer'))
        # layerNames = list(layerDict.keys())
        # layerNames.sort()
        # self.layerComboBox.addItems(layerNames)
        # self.setComponentsEnabled(False)
        # self.validKeys = ['attributeName', 'attributeRule', 'description', 'layerName']
        # if parameterDict != {}:
        #     self.populateInterface(parameterDict)

    # def instantiateWidgetItem(self):
    #     return
