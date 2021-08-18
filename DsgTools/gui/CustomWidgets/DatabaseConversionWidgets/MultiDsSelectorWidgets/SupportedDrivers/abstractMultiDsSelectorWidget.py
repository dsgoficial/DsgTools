 
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

from qgis.PyQt.QtCore import QObject

class AbstractMultiDsSelectorWidget(QObject):
    """
    Class containing minimum structure for multiple datasource selection.
    Particularities from each driver are settled within its own class (child from this). 
    """
    def __init__(self, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) widget parent to new instance of datasource representative widget.
        """
        super(AbstractMultiDsSelectorWidget, self).__init__()
        self.selector = self.getWidget(parent=parent)
        self.datasources = {}
        self.source = -1

    def getWidget(self, parent=None):
        """
        Retrieves current datasource selector dialog.
        """
        # to be reimplemented in each class
        pass

    def validate(self):
        """
        Validates contents information.
        :return: (bool) whether contents are a valid selection.
        """
        pass
