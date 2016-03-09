# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-09-10
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot

# DSGTools imports

import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'rules_editor.ui'))

class RulesEditor(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(RulesEditor, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.tableWidget.setColumnCount(4)
        
        self.rulesFile = os.path.join(os.path.dirname(__file__), 'ValidationRules', 'rules.json')
        
    def on_insertRuleButton_clicked(self):
        layer1Item = QTableWidgetItem(self.layer1Combo.currentText())
        layer2Item = QTableWidgetItem(self.layer2Combo.currentText())
        necessityItem = QTableWidgetItem(self.necessityCombo.currentText())
        predicateItem = QTableWidgetItem(self.predicateCombo.currentText())

        self.tableWidget.setItem(self.tableWidget.rowCount(), 0, layer1Item)
        self.tableWidget.setItem(self.tableWidget.rowCount(), 1, necessityItem)        
        self.tableWidget.setItem(self.tableWidget.rowCount(), 2, predicateItem)
        self.tableWidget.setItem(self.tableWidget.rowCount(), 3, layer2Item)        
        
    def on_removeRuleButton_clicked(self):
        selectedItems = self.tableWidget.selectedItems()
        row = self.tableWidget.row(selectedItems[0])
        self.tablwWidget.removeRow(row)
    
    def makeRulesDict(self):
        pass
        
    def writeJsonFile(self):
        try:
            with open(self.rulesFile, 'w') as outfile:
                json.dump(self.makeRulesDict(), outfile, sort_keys=True, indent=4)
        except:
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Problem saving file!'))
            
        QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Profile saved successfully!'))
