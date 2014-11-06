# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CriaMolduraDialog
                                 A QGIS plugin
Create chart's boundary polygon according to Brazilian systematic mapping system.
                             -------------------
        begin                : 2014-06-17
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from PyQt4 import QtGui, uic, QtCore

# FORM_CLASS, _ = uic.loadUiType(os.path.join(
#     os.path.dirname(__file__), 'carrega_categoria_dialog_base.ui'))
import cria_moldura_dialog_base
import sqlite3, os
from pyspatialite import dbapi2 as sqlite
from PyQt4.QtCore import QFileInfo,QSettings
from qgis.core import QgsCoordinateReferenceSystem,QgsDataSourceURI,QgsVectorLayer,QgsMapLayerRegistry
from qgis.gui import QgsGenericProjectionSelector,QgsMessageBar
import qgis as qgis
from PyQt4 import QtGui
import sys

# class CarregaCategoriaDialog(QtGui.QDialog, FORM_CLASS):
class CriaMolduraDialog(QtGui.QDialog, cria_moldura_dialog_base.Ui_CriaMoldura):
    def __init__(self, parent=None):
        """Constructor."""
#         super(QtGui.QDialog).__init__(parent)

        super(CriaMolduraDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
#         self.connect(self.pushButtonBuscarArquivo, QtCore.SIGNAL("clicked()"), self.carregaSpatialite)
        self.filename = ""
        self.carregado = False
        self.coordSysDefinido = False
        self.epsg = 0
        self.srs = ''

        self.setupUi(self)

        self.seedFile = os.path.dirname(__file__)+'/spatialite_articulacao/articulacao.sqlite'
        self.seedFile.replace('\\','/')
        tables = ['','f_1_milhao','f500k','f250k','f100k','f50k','f25k']
        self.scales = ['','1:1.000.000','1:500.000','1:250.000','1:100.000','1:50.000','1:25.000']

        self.escalas = dict(zip(self.scales,tables))
        self.atr_MI = ['','','','mi','mi','mi','mi_1']
        self.MI = []
        self.INOM = []
        self.escala_selecionada = ''

        self.bar = QgsMessageBar()
        self.setLayout(QtGui.QGridLayout(self))
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(1)
        self.bar.setSizePolicy(sizePolicy)
        self.layout().addWidget(self.bar, 0,0,1,1)

        self.group = QtGui.QButtonGroup()
        self.group.addButton(self.radioButtonMI)
        self.group.addButton(self.radioButtonINOM)
        self.group.setExclusive(True)

        self.radioButtonMI.setEnabled(False)
        self.radioButtonINOM.setEnabled(False)

        self.populaEscalas()



        QtCore.QObject.connect(self.pushButtonBuscarArquivoCriaMoldura, QtCore.SIGNAL(("clicked()")), self.carregaSpatialite)
        QtCore.QObject.connect(self.arquivoCriaMolduraLineEdit, QtCore.SIGNAL(("textChanged(QString)")), self.updateBDField)
        QtCore.QObject.connect(self.comboBoxEscala, QtCore.SIGNAL(("currentIndexChanged(int)")), self.popula)
        QtCore.QObject.connect(self.comboBoxMI, QtCore.SIGNAL(("currentIndexChanged(int)")), self.setaMI)
        QtCore.QObject.connect(self.comboBoxINOM, QtCore.SIGNAL(("currentIndexChanged(int)")), self.setaINOM)
        QtCore.QObject.connect(self.pushButtonCancelarCriaMoldura, QtCore.SIGNAL(("clicked()")), self.cancela)
        QtCore.QObject.connect(self.radioButtonINOM, QtCore.SIGNAL(("clicked()")), self.radioINOM)
        QtCore.QObject.connect(self.radioButtonMI, QtCore.SIGNAL(("clicked()")), self.radioMI)

        QtCore.QObject.connect(self.pushButtonOkCriaMoldura, QtCore.SIGNAL(("clicked()")), self.okselecionadoCriaMoldura)
#
    def setaMI(self):
        self.MI = self.comboBoxMI.currentText()

    def setaINOM(self):
        self.INOM = self.comboBoxINOM.currentText()

    def populaEscalas(self):
        self.comboBoxEscala.addItems(self.scales)

    def popula(self):
        self.limpa()
        index = self.comboBoxEscala.currentIndex()
        if index == 1 or index == 2:  #1kk -> n�o tem MI

            self.radioButtonINOM.setChecked(True)
            list = self.descobreListaMolduras(self.seedFile,self.escalas[self.scales[index]],'inom')
            list.insert(0,'')
            self.comboBoxINOM.setEnabled(True)

            self.comboBoxINOM.addItems(list)

        elif index == 3 or index == 4 or index == 5:
            self.comboBoxMI.setEnabled(True)
            self.comboBoxINOM.setEnabled(False)
            self.radioButtonMI.setChecked(True)

            self.radioButtonINOM.setEnabled(True)
            self.radioButtonMI.setEnabled(True)


            list_inom = self.descobreListaMolduras(self.seedFile,self.escalas[self.scales[index]],'inom')
            list_inom.sort()
            list_inom.insert(0,'')
            list_mi = self.descobreListaMolduras(self.seedFile,self.escalas[self.scales[index]],'mi')
            list_mi.sort()
            list_mi.insert(0,'')


            self.comboBoxINOM.addItems(list_inom)
            self.comboBoxMI.addItems(list_mi)

        elif index == 6:
            self.radioButtonMI.setEnabled(True)
            self.radioButtonINOM.setEnabled(True)
            self.radioButtonMI.setChecked(True)
            self.radioButtonINOM.setChecked(False)
            self.comboBoxMI.setEnabled(True)
            self.comboBoxINOM.setEnabled(False)

            list_inom = self.descobreListaMolduras(self.seedFile,self.escalas[self.scales[index]],'inom')
            list_inom.sort()
            list_inom.insert(0,'')
            list_mi = self.descobreListaMolduras(self.seedFile,self.escalas[self.scales[index]],'mi_1')
            list_mi.sort()
            list_mi.insert(0,'')




            self.comboBoxINOM.addItems(list_inom)
            self.comboBoxMI.addItems(list_mi)

        else:
#             self.limpa()

            self.comboBoxINOM.setEnabled(False)

            self.comboBoxMI.setEnabled(False)

    def radioINOM(self):

        if self.radioButtonINOM.isChecked() == True:
            self.comboBoxINOM.setEnabled(True)
            self.comboBoxMI.setEnabled(False)

    def radioMI(self):
        if self.radioButtonMI.isChecked() == True:
            self.comboBoxMI.setEnabled(True)
            self.comboBoxINOM.setEnabled(False)

    def descobreListaMolduras(self,db_articulacao,nome_tabela_escala,atributo):

        con_articulacao = sqlite.connect(db_articulacao)
        cursor_articulacao = con_articulacao.cursor()

        #procura o mi na articulacao
        cursor_articulacao.execute("SELECT "+atributo+" from "+nome_tabela_escala)
        lista = []
        iterator = cursor_articulacao.fetchall()
        for i in iterator:
            lista.append(i[0])
        return lista

    def limpa(self):
        self.comboBoxMI.clear()
        self.comboBoxINOM.clear()

        self.radioButtonMI.setEnabled(False)
        self.radioButtonINOM.setEnabled(False)




    def carregaMoldura(self,db_articulacao,db_destino,srid,nome_tabela_escala,atributo,valor_atributo):
        coordSys = QgsCoordinateReferenceSystem(srid,QgsCoordinateReferenceSystem.EpsgCrsId)
        nomeCoordSys = coordSys.description()

        con_articulacao = sqlite.connect(db_articulacao)
        con_destino = sqlite.connect(db_destino)

        cursor_articulacao = con_articulacao.cursor()
        cursor_destino = con_destino.cursor()

        #procura o mi na articulacao
        cursor_articulacao.execute("SELECT astext(geometry) from \'"+nome_tabela_escala+"\' where "+atributo+"=\'"+valor_atributo+"\'")

        mold_text = cursor_articulacao.fetchall()[0][0]

        if len(nomeCoordSys.split('/'))>1:
            print nomeCoordSys.split('/')[0][0:-1]
            if nomeCoordSys.split('/')[0][0:-1] == 'WGS 84':

                cursor_articulacao.execute("SELECT astext(Transform(geomfromtext(?,?),?))",(mold_text,4326,srid))
                mold_text = cursor_articulacao.fetchall()[0][0]
                con_articulacao.close()


                print mold_text
                print srid
                cursor_destino.execute("INSERT INTO aux_moldura_a(GEOMETRY) VALUES (geomfromtext(?,?))",(mold_text,srid))


                con_destino.commit()
                con_destino.close()

            if nomeCoordSys.split('/')[0][0:-1] == 'SIRGAS':

                cursor_articulacao.execute("SELECT astext(Transform(geomfromtext(?,?),?))",(mold_text,4170,srid))
                mold_text = cursor_articulacao.fetchall()[0][0]
                con_articulacao.close()


                print mold_text
                print srid
                cursor_destino.execute("INSERT INTO aux_moldura_a(GEOMETRY) VALUES (geomfromtext(?,?))",(mold_text,srid))


                con_destino.commit()
                con_destino.close()

            if nomeCoordSys.split('/')[0][0:-1] == 'SIRGAS 2000':

                cursor_articulacao.execute("SELECT astext(Transform(geomfromtext(?,?),?))",(mold_text,4674,srid))
                mold_text = cursor_articulacao.fetchall()[0][0]
                con_articulacao.close()


                print mold_text
                print srid
                cursor_destino.execute("INSERT INTO aux_moldura_a(GEOMETRY) VALUES (geomfromtext(?,?))",(mold_text,srid))


                con_destino.commit()
                con_destino.close()



            if nomeCoordSys.split('/')[0][0:-1] == 'SAD69':
                print ''
                cursor_articulacao.execute("SELECT astext(Transform(geomfromtext(?,?),?))",(mold_text,4618,srid))
                mold_text = cursor_articulacao.fetchall()[0][0]
                con_articulacao.close()


                print mold_text
                print srid
                cursor_destino.execute("INSERT INTO aux_moldura_a(GEOMETRY) VALUES (geomfromtext(?,?))",(mold_text,srid))


                con_destino.commit()
                con_destino.close()
            if nomeCoordSys.split('/')[0][0:-1] == 'Corrego Alegre':
                print ''
                cursor_articulacao.execute("SELECT astext(Transform(geomfromtext(?,?),?))",(mold_text,4225,srid))
                mold_text = cursor_articulacao.fetchall()[0][0]
                con_articulacao.close()


                print mold_text
                print srid
                cursor_destino.execute("INSERT INTO aux_moldura_a(GEOMETRY) VALUES (geomfromtext(?,?))",(mold_text,srid))


                con_destino.commit()
                con_destino.close()
            else:
                con_articulacao.close()
                self.bar.pushMessage("Erro!", "O datum deve ser WGS84 ou SAD69 ou Corrego Alegre!", level=QgsMessageBar.CRITICAL)
                return


        else:

            con_articulacao.close()


            print mold_text
            print srid
            cursor_destino.execute("INSERT INTO aux_moldura_a(GEOMETRY) VALUES (geomfromtext(?,?))",(mold_text,srid))


            con_destino.commit()
            con_destino.close()



    def restauraInicio(self):
        self.filename = ""
        self.carregado = False
        self.coordSysDefinido = False
        self.epsg = 0
        self.srs = ''
        self.MI = []
        self.INOM = []

        self.arquivoCriaMolduraLineEdit.setReadOnly(False)
        self.coordSysCriaMolduraLineEdit.setText("")
        self.arquivoCriaMolduraLineEdit.setText("")
        self.radioButtonMI.setEnabled(False)
        self.radioButtonINOM.setEnabled(False)
        self.comboBoxMI.clear()
        self.comboBoxINOM.clear()
        self.comboBoxEscala.clear()
        self.populaEscalas()

    def carregaSpatialite(self):
        fd = QtGui.QFileDialog()
        self.filename = fd.getOpenFileName(filter='*.sqlite')
        if self.filename <> "":
            self.carregado = True
            self.arquivoCriaMolduraLineEdit.setText(self.filename)



    def updateBDField(self):
        if self.carregado == True:
            self.arquivoCriaMolduraLineEdit.setText(self.filename)
            self.arquivoCriaMolduraLineEdit.setReadOnly(True)
            if self.coordSysDefinido == False:
                self.updateSistCoordField()    #problema aqui

        else:
            self.filename = ""
            self.arquivoCriaMolduraLineEdit.setText(self.filename)
            self.srs = ""
            self.arquivoCriaMolduraLineEdit.setText(self.srs)

    def descobreEPSG(self):
        con = sqlite3.connect(self.filename)
        cursor = con.cursor()
        cursor.execute("SELECT srid from geometry_columns;")
        lista = cursor.fetchall()
        return lista[0][0]

    def updateSistCoordField(self):
#         if self.bdCarregado == True:
        try:

            epsg = self.descobreEPSG()

            if epsg == -1:
                self.bar.pushMessage("", "Sistema de coordenadas n�o definido.", level=QgsMessageBar.WARNING)
                self.coordSysCriaMolduraLineEdit.setReadOnly(False)

            else:

                self.epsg = epsg
                self.srs = QgsCoordinateReferenceSystem(self.epsg, QgsCoordinateReferenceSystem.EpsgCrsId)
                if self.srs <> "":
                    self.coordSysDefinido = True
                    self.coordSysCriaMolduraLineEdit.setText(self.srs.description())
                    self.coordSysCriaMolduraLineEdit.setReadOnly(True)
        except:
            pass




    def okselecionadoCriaMoldura(self):

#
        if self.carregado and self.coordSysDefinido:

#             try:
# #                 destino = self.sqliteFileName
            if self.radioButtonMI.isChecked():

                try:
                    index = self.comboBoxMI.currentIndex()
                    self.escala_selecionada = self.scales[self.comboBoxEscala.currentIndex()]

                    nome_tabela_escala = self.escalas[self.escala_selecionada]

                    if nome_tabela_escala == '':
                        self.bar.pushMessage("Erro!", "Selecione a escala!", level=QgsMessageBar.CRITICAL)
                    else:

                        self.carregaMoldura(self.seedFile,self.filename,int(self.epsg),nome_tabela_escala,self.atr_MI[self.comboBoxEscala.currentIndex()],self.MI)
                        self.close()
                        self.restauraInicio()
                except:

                    if self.comboBoxMI.currentText() == '' and self.radioButtonMI.isChecked():
                        self.bar.pushMessage("Erro!", "Selecione o MI!", level=QgsMessageBar.CRITICAL)
                    if self.comboBoxINOM.currentText() == '' and self.radioButtonINOM.isChecked():
                        self.bar.pushMessage("Erro!", "Selecione o INOM!", level=QgsMessageBar.CRITICAL)
                    if self.epsg == -1:
                        self.bar.pushMessage("Erro!", "Sistema de coordenadas n�o definido!", level=QgsMessageBar.CRITICAL)
                    if self.filename == '':
                        self.bar.pushMessage("Erro!", "Selecione o arquivo!", level=QgsMessageBar.CRITICAL)
                    pass

            if self.radioButtonINOM.isChecked():
                try:
                    index = self.comboBoxINOM.currentIndex()
                    self.escala_selecionada = self.scales[self.comboBoxEscala.currentIndex()]

                    nome_tabela_escala = self.escalas[self.escala_selecionada]

                    if nome_tabela_escala == '':
                        self.bar.pushMessage("Erro!", "Selecione a escala!", level=QgsMessageBar.CRITICAL)
                    else:

                        self.carregaMoldura(self.seedFile,self.filename,int(self.epsg),nome_tabela_escala,'inom',self.INOM)
                        self.close()
                        self.restauraInicio()
                except:

                    if self.comboBoxMI.currentText() == '' and self.radioButtonMI.isChecked():
                        self.bar.pushMessage("Erro!", "Selecione o MI!", level=QgsMessageBar.CRITICAL)
                    if self.comboBoxINOM.currentText() == '' and self.radioButtonINOM.isChecked():
                        self.bar.pushMessage("Erro!", "Selecione o INOM!", level=QgsMessageBar.CRITICAL)
                    if self.epsg == -1:
                        self.bar.pushMessage("Erro!", "Sistema de coordenadas n�o definido!", level=QgsMessageBar.CRITICAL)
                    if self.filename == '':
                        self.bar.pushMessage("Erro!", "Selecione o arquivo!", level=QgsMessageBar.CRITICAL)
                    pass



#             except:
#                 qgis.utils.iface.messageBar().pushMessage("Erro!", "Entre com os par�metros corretamente!", level=QgsMessageBar.CRITICAL)
#                 self.restauraInicio()
#                 pass

        else:
#             qgis.utils.iface.messageBar().pushMessage("Erro!", "Selecione o sistema de coordenadas e o banco de dados corretamente!", level=QgsMessageBar.CRITICAL)
            if self.coordSysDefinido == False:
                self.bar.pushMessage("Erro!", "Selecione o sistema de coordenadas n�o definido!", level=QgsMessageBar.CRITICAL)
            if self.carregado == False:
                self.bar.pushMessage("Erro!", "Selecione o arquivo!", level=QgsMessageBar.CRITICAL)



#             self.pushMessage("Erro!", "Selecione o sistema de coordenadas e o banco de dados corretamente!", level=QgsMessageBar.WARNING)


    def cancela(self):
        self.restauraInicio()


