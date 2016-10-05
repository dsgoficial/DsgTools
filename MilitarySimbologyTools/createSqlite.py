# -*- coding: utf-8 -*-

# Qt imports
from PyQt4 import uic, QtGui

# lib python imports
import sqlite3, os

#DsgTools imports
from DsgTools.DbTools.SpatialiteTool.cria_spatialite_dialog import CriaSpatialiteDialog

class CreateSqlite(CriaSpatialiteDialog):
    
    def __init__(self, parent=None):
        """Constructor."""
        super(CreateSqlite, self).__init__(parent)        
        self.versionComboBox.setVisible(False)
        self.label_4.setVisible(False)
        self.start()
        self.exec_()
                         
    def start(self):
        self.nameSqlite = None
        self.pathSqlite = None
    
    def stop(self):
        del self.nameSqlite
        del self.pathSqlite
            
    def getTemplateLocation(self):
        self.nameSqlite = self.nomeLineEdit.text()
        self.stop()
        path  = os.path.join(os.path.dirname(__file__), 'templates', 'template.sqlite')        
        return path
    
    def definePastaDestino(self):
        fd = QtGui.QFileDialog()
        self.filepath = fd.getExistingDirectory()
        if self.filepath <> "":
            self.carregado = True
            self.pastaDestinoCriaSpatialiteLineEdit.setText(self.filepath)
            self.pathSqlite = self.filepath
            
        