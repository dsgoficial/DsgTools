# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AboutDialog
                                 A QGIS plugin
                             -------------------
        begin                : 2014-10-16
        copyright            : (C) 2014 by Luiz Andrade
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from ui_about import Ui_AboutDialog

class AboutDialog(QDialog, Ui_AboutDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

