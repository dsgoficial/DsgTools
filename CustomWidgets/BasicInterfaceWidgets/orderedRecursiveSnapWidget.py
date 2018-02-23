# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-02-22
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
from DsgTools.CustomWidgets.BasicInterfaceWidgets.snapChooserWidget import SnapChooserWidget

class OrderedRecursiveSnapWidget(OrderedStructureWidget):

    def __init__(self, parent=None):
        """
        Initializates OrderedRecursiveSnapWidget
        """
        super(OrderedRecursiveSnapWidget, self).__init__(parent)
        self.args = None
        self.tableWidget.setHorizontalHeaderLabels([self.tr('Snap Order')])
        self.widgetKey = 'snapChooserWidgetList'
    
    def instantiateWidgetItem(self):
        return SnapChooserWidget(*self.args)
    
    def setInitialState(self):
        pass
    
    def getHierarchicalSnapDict(self):
        snapList = self.getParameterDict()[self.widgetKey]
        snapDictList = []
        for i in range(len(snapList)-1):
            snapItemDict = dict()
            snapItemDict['referenceLayer'] = snapList[i]['layerName']
            snapItemDict['snap'] = snapList[i]['snap']
            snapItemDict['snapLayerList'] = [i['layerName'] for i in snapList[(i+1)::]]
            snapDictList.append(snapItemDict)
        return snapDictList
    

