# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-19
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
from processing.gui.wrappers import WidgetWrapper
from DsgTools.gui.CustomWidgets.OrderedPropertyWidgets.orderedRecursiveSnapWidget import OrderedRecursiveSnapWidget

class SnapHierarchyWrapper(WidgetWrapper):
    def __init__(self, *args, **kwargs):
        super(SnapHierarchyWrapper, self).__init__(*args, **kwargs)
    
    def createPanel(self):
        return OrderedRecursiveSnapWidget()
    
    def createWidget(self):
        self.panel = self.createPanel()
        self.panel.dialogType = self.dialogType
        if self.dialogType == DIALOG_MODELER:
            #TODO
            return self.panel
        else:
            return self.panel
    
    def parentLayerChanged(self, layer=None):
        pass
    
    def setLayer(self, layer):
        pass
    
    def setValue(self, value):
        pass
    
    def value(self):
        pass