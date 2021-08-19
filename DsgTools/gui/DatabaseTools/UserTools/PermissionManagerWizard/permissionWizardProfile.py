# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import os
import json

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtWidgets import QMessageBox, QFileDialog, QApplication
from qgis.PyQt.QtGui import QCursor
from fileinput import filename
from DsgTools.core.Utils.utils import Utils
from DsgTools.core.Factories.DbCreatorFactory.dbCreatorFactory import DbCreatorFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'permissionWizardProfile.ui'))

class PermissionWizardProfile(QtWidgets.QWizardPage, FORM_CLASS):
    def __init__(self, parent=None):
        '''Constructor.'''
        super(self.__class__, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.profileCustomSelector.setTitle(self.tr('Select profiles to be installed'))
        profiles = self.getModelProfiles()
        self.profileCustomSelector.setInitialState(profiles)
    
    def getModelProfiles(self):
        ret = []
        folder = os.path.join(os.path.dirname(__file__),'..', 'profiles')
        for root, dirs, files in os.walk(folder):
            for file in files:
                ext = file.split('.')[-1]
                if ext == 'json':
                    ret.append(file.split('.')[0])
        ret.sort()
        return ret

    def validatePage(self):
        if len(self.profileCustomSelector.toLs) == 0:
            return False
        else:
            return True
