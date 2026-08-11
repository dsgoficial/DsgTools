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

# Qt imports

from DsgTools.gui.CustomWidgets.OrderedPropertyWidgets.orderedStructureWidget import (
    OrderedStructureWidget,
)
from DsgTools.gui.CustomWidgets.ValidationWidgets.validationProcessWidget import (
    ValidationProcessWidget,
)


class OrderedValidationProcessesWidget(OrderedStructureWidget):
    def __init__(self, parent=None):
        """
        Initializates OrderedAttributeRulesWidget
        """
        super(OrderedValidationProcessesWidget, self).__init__(parent)
        self.args = None
        self.tableWidget.setHorizontalHeaderLabels([self.tr("QGIS Processing Models")])
        self.widgetKey = "validationProcessWidgetList"
        self.parent = parent
        if self.parent:
            self.validationManager = self.parent.parent().parent().validationManager

    def instantiateWidgetItem(self):
        return ValidationProcessWidget(parent=self)
