# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-05
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

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import pyqtSlot, pyqtSignal

# QGIS imports
from qgis.gui import QgsMessageBar
import qgis as qgis

#DsgTools imports
from militarySimbology import MilitarySymbology
from createSqlite import CreateSqlite

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'militarySimbologyDock.ui'))

class MilitarySimbologyDock(QtGui.QDockWidget, MilitarySymbology, FORM_CLASS):
    
    def __init__(self, iface, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.iface = iface
        self.sqlitePath = False
        self.setupUi(self)
        self.widget.lineEdit.textChanged.connect(self.setCurrentSqlite)            
    
    def setCurrentSqlite(self, pathSqliteDB):
        """
        defino o Sqlite em Uso
        """
        self.sqlitePath =  pathSqliteDB
      
    @pyqtSlot(bool)
    def on_createSqliteButton_clicked(self):
        """
        Chamo a classe para Criar o Sqlite
        """
        CreateSqlite()
    
    @pyqtSlot(bool)
    def on_loadAlliedButton_clicked(self):
        """Chamo a classe para carregar a feições passando a path do estilo, a path do Sqlite e o tipo da feição
        """
        if self.sqlitePath:
            stylePath = os.path.join(os.path.dirname(__file__), 'templates', 'templateStyleAllied.qml')
            MilitarySymbology(self.iface, self.sqlitePath, stylePath, 'Aliado')
        else:
            self.message()
       
    @pyqtSlot(bool)
    def on_loadEnemyButton_clicked(self):
        """
        Chamo a classe para carregar a feições passando a path do estilo, a path do Sqlite e o tipo da feição
        """
        if self.sqlitePath:
            stylePath = os.path.join(os.path.dirname(__file__), 'templates', 'templateStyleEnemy.qml')
            MilitarySymbology(self.iface, self.sqlitePath, stylePath, 'Inimigo')
        else:
            self.message()
     
    def message(self):
        """messagem para avisar o usuário caso tente carregar uma feição sem ter definido o Banco Sqlite
        """
        self.iface.messageBar().pushMessage(self.tr('warning'), self.tr('Select a SQLite database'),
                                            level=QgsMessageBar.INFO, duration=3)