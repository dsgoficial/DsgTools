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
import os
from string import Template

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog

# replace version from metada file
with open(os.path.join(os.path.dirname(__file__), 'ui_about.ui'), 'r') as about, \
     open(os.path.join(os.path.dirname(__file__), '..', '..', 'metadata.txt'), 'r') as meta, \
     open(os.path.join(os.path.dirname(__file__), 'ui_about_.ui'), 'w') as filledUi:
     t = Template(about.read())
     for line in meta.readlines():
         if line.strip().startswith("version="):
            version = line.split("=")[1].strip()
            break
     t = t.safe_substitute(version=version)
     filledUi.write(t)

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ui_about_.ui'))

class AboutDialog(QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """
        Constructor
        """
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)

