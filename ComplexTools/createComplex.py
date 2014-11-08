# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from PyQt4.QtXml import *

from ui_createComplex import Ui_Dialog

class CreateComplexDialog(QDialog, Ui_Dialog):
    def __init__(self, iface):
        """Constructor.
        """
        QDialog.__init__( self )
        self.setupUi( self )
        
        self.iface = iface
        
        self.populateSelectedFeaturesWidget()
        
    def populateSelectedFeaturesWidget(self):
        self.layers = self.iface.mapCanvas().layers()
        for layer in self.layers:
            selectedFeatures = layer.selectedFeatures()
            if len(selectedFeatures) == 0:
                continue
            item = QTreeWidgetItem(self.selectedFeaturesTreeWidget)
            item.setText(0,layer.name())
            for feature in selectedFeatures:
                featureItem = QTreeWidgetItem(item)
                featureItem.setText(0,str(feature.id()))
