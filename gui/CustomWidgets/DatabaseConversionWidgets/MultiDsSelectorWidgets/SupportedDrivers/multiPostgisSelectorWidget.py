 
# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-09-26
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from .abstractMultiDsSelectorWidget import AbstractMultiDsSelectorWidget
from DsgTools.core.dsgEnums import DsgEnums
import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'multiPostgisSelectorWidget.ui'))

class MultiPostgisSelector(QWidget, FORM_CLASS):
    """
    Class designed to manipulate just the driver selection behavior.
    """
    def __init__(self, parent=None):
        """
        Class constructor.
        """
        super(MultiPostgisSelector, self).__init__(parent)
        self.setupUi(self)

class MultiPostgisSelectorWidget(AbstractMultiDsSelectorWidget):
    """
    Class designed to integrate the datasource selector widget to the abstract multi datasource selector widget.
    """
    def __init__(self, parent=None):
        super(MultiPostgisSelectorWidget, self).__init__(parent=parent)
        self.source = DsgEnums.PostGIS

    def getMultiDsWidget(self, parent=None):
        """
        parents class reimplementation to retrieve widget.
        :param parent: (QWidget) widget parent to new multi datasource widget.
        """
        return MultiPostgisSelector(parent=parent)