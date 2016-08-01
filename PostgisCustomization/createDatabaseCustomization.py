# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-01
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba@dsg.eb.mil.br
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

from qgis.core import QgsMessageLog
from qgis.gui import QgsCollapsibleGroupBox

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtGui import QFormLayout

# DSGTools imports
from DsgTools.CustomWidgets.CustomDbManagementWidgets.newClassWidget import NewClassWidget
from DsgTools.CustomWidgets.CustomDbManagementWidgets.newAttributeWidget import NewAttributeWidget
from DsgTools.CustomWidgets.selectFileWidget import SelectFileWidget
from DsgTools.PostgisCustomization.dbCustomizer import DbCustomizer

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'createDatabaseCustomization.ui'))

class CreateDatabaseCustomization(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.connectionWidget.tabWidget.setTabEnabled(0, False)
        self.populateCustomizationCombo()
    
    def getStructDict(self):
        pass
    
    def populateCustomizationCombo(self):
        '''
        Populates the customization combo and also defines customDict.
        '''
        self.customDict = dict()
        self.customDict['attribute'] = self.tr('Attribute Customization')
        self.customDict['class'] = self.tr('Class Customization')
        self.customDict['codeName'] = self.tr('Code Name Customization')
        self.customDict['default'] = self.tr('Default Customization')
        self.customDict['domain'] = self.tr('Domain Customization')
        self.customDict['nullity'] = self.tr('Attribute Nullity Customization')
        for type in self.customDict.keys():
            self.customizationSelectionComboBox.addItem(self.customDict[type])
    
    @pyqtSlot(bool)
    def on_addAttributePushButton_clicked(self):
        self.addClassWidget()
    
    def addWidget(self, widget, title):
        layout = QtGui.QFormLayout()
        layout.addRow(widget)
        groupBox = QgsCollapsibleGroupBox(title)

        groupBox.setLayout(layout)
        self.scrollAreaLayout.addWidget(groupBox)
    
    def addClassWidget(self):
        widget = NewClassWidget()
        title = self.tr('New Custom Class')
        self.addWidget(widget, title)
        