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
        email                : borba@dsg.eb.mil.br
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

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QTreeWidgetItem

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'validation_config.ui'))

from DsgTools.ValidationTools.setupEarthCoverage import SetupEarthCoverage
from qgis.core import QgsMessageLog

class ValidationConfig(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        '''Constructor.'''
        super(ValidationConfig, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.widget.tabWidget.setTabEnabled(1,True)
        self.widget.tabWidget.setTabEnabled(0,False)
        self.widget.tabWidget.setCurrentIndex(1)
        self.widget.connectionChanged.connect(self.loadEarthCoverage)

    @pyqtSlot(bool)
    def on_closePushButton_clicked(self):
        self.hide()

    @pyqtSlot(bool)
    def on_defineEarthCoverageButton_clicked(self):
        if not self.widget.abstractDb:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Select a database to manage earth coverage'))
            return
        try:
            classList = self.widget.abstractDb.getOrphanGeomTables()
            areas = []
            lines = []
            for cl in classList:
                if cl[-1] == 'a':
                    areas.append(cl)
                if cl[-1] == 'l':
                    lines.append(cl)
            lines.append('public.aux_linhas_l')
            
            dlg = SetupEarthCoverage(areas,lines)
            dlg.coverageChanged.connect(self.loadEarthCoverage)
            dlg.exec_()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        
        pass
    
    def loadEarthCoverage(self,version=None):
        try:
            fileName = os.path.join(os.path.dirname(__file__), 'ValidationConfig', 'earthCoverage.cfg')
            file = open(fileName, 'r')
            data = file.read()
            earthCoverageDict = json.loads(data)
            rootItem = self.earthCoverageTreeWidget.invisibleRootItem()
            #database item
            for key in earthCoverageDict.keys():
                item = QTreeWidgetItem(rootItem)
                item.setText(0,key)
                item.setExpanded(True)
                for cl in earthCoverageDict[key]:
                    covItem = QTreeWidgetItem(item)
                    covItem.setText(1,cl)
                    covItem.setExpanded(True)
        except Exception as e:
            QgsMessageLog.logMessage(self.tr('Earth Coverage not loaded! Check log for details.')+str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        
