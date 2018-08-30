# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CriaSpatialiteDialog
                                 A QGIS plugin
Create spatialite database built according to Brazilian's EDGV
                             -------------------
        begin                : 2014-06-17
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from qgis.PyQt import QtCore, QtWidgets
from qgis.core import QgsCoordinateReferenceSystem, Qgis
from qgis.gui import QgsProjectionSelectionTreeWidget, QgsMessageBar
from qgis.PyQt import uic, QtWidgets

import sqlite3, os
import qgis as qgis

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'cria_spatialite_dialog_base.ui'))

class CriaSpatialiteDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, manager, parentButton=None, parent=None, parentMenu=None):
        """Constructor."""
        super(CriaSpatialiteDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.parentMenu = parentMenu
        self.manager = manager
        self.parentButton = parentButton
        self.filepath = ""
        self.carregado = False
        self.coordSysDefinido = False
        self.epsgCriaSpatialite = 0
        self.srsCriaSpatialite = ''
        self.sqliteFileName = ''
        self.action = None

        self.bar = QgsMessageBar()
        self.setLayout(QtWidgets.QGridLayout(self))
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.bar.setSizePolicy(sizePolicy)
        self.layout().addWidget(self.bar, 0,0,1,1)

        self.pushButtonBuscarPastaDestinoCriaSpatialite.clicked.connect(self.definePastaDestino)
        self.pushButtonBuscarSistCoordCriaSpatialite.clicked.connect(self.setaSistCoordCriaSpatialite)
        self.pushButtonOkCriaSpatialite.clicked.connect(self.okselecionadoCriaSpatialite)

    def getTemplateLocation(self):
        """
        gets the template location
        """
        currentPath = os.path.dirname(__file__)
        if self.versionComboBox.currentText() == '2.1.3':
            edgvPath = os.path.join(currentPath, 'template', '213', 'seed_edgv213.sqlite')
        elif self.versionComboBox.currentText() == 'FTer_2a_Ed':
            edgvPath = os.path.join(currentPath, 'template', 'FTer_2a_Ed', 'seed_edgvfter_2a_ed.sqlite')
        elif self.versionComboBox.currentText() == '3.0':
            edgvPath = os.path.join(currentPath, 'template', '3', 'seed_edgv3.sqlite')
        return edgvPath

    def restauraInicio(self):
        """
        Sets the initial state
        """
        self.filepath = ""
        self.carregado = False
        self.coordSysDefinido = False
        self.epsgCriaSpatialite = 0
        self.srsCriaSpatialite = ''
        self.sqliteFileName = ''
        self.pastaDestinoCriaSpatialiteLineEdit.setText("")
        self.coordSysCriaSpatialiteLineEdit.setText("")
        self.nomeLineEdit.setText("")
        self.action = None

    def definePastaDestino(self):
        """
        Defines destination folder
        """
        fd = QtWidgets.QFileDialog()
        self.filepath = fd.getExistingDirectory()
        if self.filepath != "":
            self.carregado = True
            self.pastaDestinoCriaSpatialiteLineEdit.setText(self.filepath)

    def setAction(self, action):
        """
        Sets a action to tool button.
        :param action: (QAction) action to be set to tool button.
        """
        self.action = action

    def setaSistCoordCriaSpatialite(self):
        """
        Opens the CRS selector
        """
        projSelector = QgsProjectionSelectionTreeWidget(self)
        self.addWidget(projSelector)
        # projSelector.setMessage(theMessage=self.tr('Please, select the coordinate system'))
        projSelector.show()
        try:
            self.epsgCriaSpatialite = int(projSelector.selectedAuthId().split(':')[-1])
            self.srsCriaSpatialite = QgsCoordinateReferenceSystem(self.epsgCriaSpatialite, QgsCoordinateReferenceSystem.EpsgCrsId)
            if self.srsCriaSpatialite != "":
                self.coordSysDefinido = True
                self.coordSysCriaSpatialiteLineEdit.setText(self.srsCriaSpatialite.description())
        except:
            self.bar.pushMessage("", self.tr('Please, select the coordinate system'), level=Qgis.Warning)
            pass

    def copiaSemente(self, destino, srid):
        """
        Copies the spatialite seed template
        """
        f = open(self.getTemplateLocation(),'rb')
        g = open(destino,'wb')
        x = f.readline()
        while x:
            g.write(x)
            x = f.readline()

        g.close()

        con = sqlite3.connect(destino)
        cursor = con.cursor()
        srid_sql = (srid,)
        cursor.execute("UPDATE geometry_columns SET srid=?",srid_sql)
        con.commit()
        con.close()

    def okselecionadoCriaSpatialite(self):
        """
        Performs the database creation
        """
        if self.carregado and self.coordSysDefinido and len(self.nomeLineEdit.text()) > 0:
            try:
                self.sqliteFileName = self.filepath+'/'+self.nomeLineEdit.text()+'.sqlite'
                destino = self.sqliteFileName
                self.copiaSemente(destino,self.epsgCriaSpatialite)
                self.close()
                self.restauraInicio()
                QMessageBox.information(self, self.tr('Information'), self.tr('Spatialite created successfully!'))
            except:
                qgis.utils.iface.messageBar().pushMessage(self.tr("Error!"), self.tr("Problem creating the database!"), level=Qgis.Critical)
                self.restauraInicio()
                pass
        else:
            if self.coordSysDefinido == False:
                self.bar.pushMessage(self.tr("Warning!"), self.tr('Please, select the coordinate system'), level=Qgis.Warning)
            if self.carregado == False:
                self.bar.pushMessage(self.tr("Warning!"), self.tr('Please, select a folder to save the database'), level=Qgis.Critical)
            if len(self.nomeLineEdit.text()) == 0:
                self.bar.pushMessage(self.tr("Warning!"), self.tr('Please, fill the file name.'), level=Qgis.Critical)

    # def addAction(self):
    #     """
    #     Adds the action to button on QGIS GUI and adds it to DSGTools menu.
    #     """
    #     icon_path = ':/plugins/DsgTools/icons/spatialite.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Create Spatialite'),
    #         callback=self.createSpatialiteDatabase,
    #         parent=self.parentMenu,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     database.addAction(action)
    #     self.setAction(action)
    #     self.manager.addTool(

            
    #     )
    #     self.databaseButton.addAction(action) 

    def initGui(self):
        """
        Instantiates user interface and prepare it to be called whenever tool button is activated. 
        """
        callback = lambda : self.manager.createDatabase(isSpatialite=True)
        self.manager.addTool(
            text=self.tr('Create a Spatialite Database'),
            callback=callback,
            parentMenu=self.parentMenu,
            icon='spatialite.png',
            parentButton=self.parentButton,
            defaultButton=True
        )

    def unload(self):
        pass
