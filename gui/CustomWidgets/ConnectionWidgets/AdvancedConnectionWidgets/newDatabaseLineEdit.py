# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-10-09
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

from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt import uic

import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'newDatabaseLineEdit.ui'))

class NewDatabaseLineEdit(QWidget, FORM_CLASS):
    """
    Class designed to control generic behaviors of a widget able to
    retrieve parameters for a PostGIS database creation.
    """
    def __init__(self, parent=None):
        """
        Class contructor.
        """
        super(NewDatabaseLineEdit, self).__init__()
        self.setupUi(self)
        self.reset()

    def fillEdgvVersions(self):
        """
        Populates EDGV combo box with available versions. 
        """
        versions = [
            self.tr("EDGV Version..."),
            "EDGV 2.1.3",
            "EDGV 2.1.3 Pro",
            "EDGV 3.0",
            "EDGV 3.0 Pro"
        ]

    def reset(self):
        """
        Clears all GUI selections. 
        """
        self.dsLineEdit.setText(self.tr("Insert New Database Name"))
        self.edgvComboBox.setCurrentIndex(0)
        # self.mQgsProjectionSelectionWidget.setCrs(0)

    def validate(self):
        """
        Validates current widget. To be validated, it is necessary:
        - a valid NEW datasource name;
        - a valid server selection;
        - a valid EDGV version selection; and
        - a valid projection selection. 
        """
        # check a valid server name
        # check if datasource is a valid name and if it already exists into selected server
        if self.dsLineEdit.text() in ['', self.tr("Insert New Database Name")]:
            return False
        else:
            # check if it exists
            pass
        # check if a valid EDGV version was selected
        if self.edgvComboBox.currentText() in ['', self.tr("EDGV Version...")]:
            return False
        else:
            # check if it exists
            pass
        # check if a valid projection was selected
        # if all tests were positive, widget has a valid selection
        return True
