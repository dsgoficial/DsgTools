# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-02-19
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from collections import OrderedDict
# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from PyQt4.QtGui import QTableWidgetItem

from DsgTools.CustomWidgets.BasicInterfaceWidgets.orderedStructureWidget import OrderedStructureWidget
from DsgTools.CustomWidgets.ValidationWidgets.validationProcessWidget import ValidationProcessWidget

class OrderedValidationProcessesWidget(OrderedStructureWidget):

    def __init__(self, parent=None):
        """
        Initializates OrderedAttributeRulesWidget
        """
        super(OrderedValidationProcessesWidget, self).__init__(parent)
        self.args = None
        self.tableWidget.setHorizontalHeaderLabels([self.tr('Validation Processes')])
        self.widgetKey = 'validationProcessWidgetList'
    
    def instantiateWidgetItem(self):
        return ValidationProcessWidget(None)
    

