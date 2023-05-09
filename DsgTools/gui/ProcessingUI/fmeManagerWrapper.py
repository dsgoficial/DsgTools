# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-12-13
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
from DsgTools.gui.CustomWidgets.ProcessingParameterWidgets.fmeManagerWidget import (
    FMEManagerWidget,
)
from processing.gui.wrappers import WidgetWrapper


class FMEManagerWrapper(WidgetWrapper):
    def __init__(self, *args, **kwargs):
        super(FMEManagerWrapper, self).__init__(*args, **kwargs)

    def createPanel(self):
        return FMEManagerWidget()

    def createWidget(self):
        self.panel = self.createPanel()
        self.panel.dialogType = self.dialogType
        return self.panel

    def parentLayerChanged(self, layer=None):
        pass

    def setLayer(self, layer):
        pass

    def setValue(self, value):
        pass

    def value(self):
        return self.panel.getParameters()

    def postInitialize(self, wrappers):
        pass
        # for wrapper in wrappers:
        #     if wrapper.parameterDefinition().name() == self.parameterDefinition().parentLayerParameter():
        #         pass
