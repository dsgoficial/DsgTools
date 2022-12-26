# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-04-25
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from qgis.PyQt.QtWidgets import QFontComboBox
from processing.gui.wrappers import WidgetWrapper
from qgis.PyQt.QtGui import QFont


class FontWidgetWrapper(WidgetWrapper):
    def __init__(self, *args, **kwargs):
        super(FontWidgetWrapper, self).__init__(*args, **kwargs)

    def createPanel(self):
        return QFontComboBox()

    def createWidget(self):
        self.panel = self.createPanel()
        self.panel.dialogType = self.dialogType
        return self.panel

    def parentLayerChanged(self, layer=None):
        pass

    def setLayer(self, layer):
        pass

    def setValue(self, value):
        self.panel.setCurrentFont(value)

    def value(self):
        return self.panel.currentFont()

    def postInitialize(self, wrappers):
        pass
