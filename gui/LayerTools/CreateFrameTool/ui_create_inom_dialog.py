# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools

                             -------------------
        begin                : 2014-09-19
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Felipe Ferrari
        email                : ferrari@dsg.eb.mil.br
         mod history          : 2014-12-17 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
         mod history          : 2014-03-31 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from __future__ import print_function
from builtins import str
from builtins import range
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform
from qgis.PyQt import QtWidgets, QtCore, uic
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import pyqtSlot

import os
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_create_inom_dialog_base.ui'))

#DsgTools imports
from DsgTools.LayerTools.CreateFrameTool.map_index import UtmGrid
from DsgTools.core.Factories.LayerLoaderFactory.layerLoaderFactory import LayerLoaderFactory

#qgis imports
import qgis as qgis

class CreateInomDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(CreateInomDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface
        self.map_index = UtmGrid()
        self.disableAll()
        self.setValidCharacters()
        self.setMask()

    @pyqtSlot()
    def on_okButton_clicked(self):
        """
        Creates the actual frame.
        """
        if not self.widget.dbLoaded:
            QMessageBox.warning(self, self.tr("Warning!"), self.tr('Please, select a database first.'))
            return

        if not self.validateMI():
            QMessageBox.warning(self, self.tr("Warning!"), self.tr('Map name index not valid!'))
            return
        layer = self.loadFrameLayer()
        inom = self.inomLineEdit.text()
        scale = self.scaleCombo.currentText()
        try:
            frame = self.widget.abstractDb.createFrame('inom', scale, inom)
        except Exception as e:
            QMessageBox.warning(self, self.tr("Critical!"), ':'.join(e.args))
            return
        reprojected = self.reprojectFrame(frame)
        self.zoomToLayer(layer, reprojected)
        self.done(1)
    
    def zoomToLayer(self, layer, frame):
        """
        Zooms in to the updated frame layer.
        """
        bbox = frame.boundingBox()
        for feature in layer.getFeatures():
            bbox.combineExtentWith(feature.geometry().boundingBox())

        bbox = self.iface.mapCanvas().mapSettings().layerToMapCoordinates(layer, bbox)
        self.iface.mapCanvas().setExtent(bbox)
        self.iface.mapCanvas().refresh()
    
    def loadFrameLayer(self):
        """
        Loads the frame layer case it is not loaded yet.
        """
        loader = LayerLoaderFactory().makeLoader(self.iface,self.widget.abstractDb)
        if loader.provider == 'postgres':
            layerMeta = {'cat': 'aux', 'geom': 'geom', 'geomType':'MULTIPOLYGON', 'lyrName': 'moldura_a', 'tableName':'aux_moldura_a', 'tableSchema':'public', 'tableType': 'BASE TABLE'}
        elif loader.provider == 'spatialite':
            layerMeta = {'cat': 'aux', 'geom': 'GEOMETRY', 'geomType':'MULTIPOLYGON', 'lyrName': 'moldura_a', 'tableName':'aux_moldura_a', 'tableSchema':'public', 'tableType': 'BASE TABLE'}
        else:
            layerMeta = None
        layerDict = loader.load([layerMeta], uniqueLoad = True)
        if layerMeta['lyrName'] in list(layerDict.keys()):
            layer = layerDict[layerMeta['lyrName']]
        else:
            layer = None
        return layer

    def getFrameLayer(self,ifaceLayers):
        """
        Gets the frame layer according to the database.
        """
        for lyr in ifaceLayers:
            if 'moldura_a' in lyr.name():
                dbname = self.getDBNameFromLayer(lyr)
                if dbname == self.widget.abstractDb.getDatabaseName():
                    return lyr
        return None
    
    def getDBNameFromLayer(self, lyr):
        """
        Gets the database name according to the database.
        """
        dbname = None
        splitUri = lyr.dataProvider().dataSourceUri().split(' ')
        if len(splitUri) > 0:
            dbsplit = splitUri[0].split('=')
            if len(dbsplit) > 1 and dbsplit[0] == 'dbname':
                dbnameInString = dbsplit[1]
                dbnameSplit = dbnameInString.split('\'')
                if len(dbnameSplit) > 1:
                    dbname = dbnameSplit[1]
        return dbname

    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        Closes the dialog returning 0.
        """
        self.done(0)
    
    @pyqtSlot(str)
    def on_inomLineEdit_textEdited(self,s):
        """
        Method to automatically update MI based on the INOM.
        It also changes all characters to upper case
        """
        if (s!=''):
            s = s.upper()
            self.inomLineEdit.setText(s)
            mi = self.map_index.getMIfromInom(str(s))
            self.miLineEdit.setText(mi)

    @pyqtSlot(str)
    def on_miLineEdit_textEdited(self,s):
        """
        Method to automatically update INOM based on the MI.
        It also changes all characters to upper case
        """
        if (s!=''):
            s = s.upper()
            self.miLineEdit.setText(s)
            self.inomen=self.map_index.getINomenFromMI(str(s))
            self.inomLineEdit.setText(self.inomen)

    @pyqtSlot(str)
    def on_mirLineEdit_textEdited(self,s):
        """
        Method to automatically update INOM based on the MIR.
        It also changes all characters to upper case
        """
        if (s!=''):
            s = s.upper()
            self.mirLineEdit.setText(s)
            self.inomen=self.map_index.getINomenFromMIR(str(s))
            self.inomLineEdit.setText(self.inomen)

    def reprojectFrame(self, poly):
        """
        Reprojects the frame to the correspondent CRS (geographic CRS to the actual CRS).
        """
        crsSrc = QgsCoordinateReferenceSystem(self.widget.crs.geographicCRSAuthId())
        coordinateTransformer = QgsCoordinateTransform(crsSrc, self.widget.crs)
        polyline = poly.asMultiPolygon()[0][0]
        newPolyline = []
        for point in polyline:
            newPolyline.append(coordinateTransformer.transform(point))
        qgsPolygon = QgsGeometry.fromMultiPolygon([[newPolyline]])
        return qgsPolygon

    def setValidCharacters(self):
        """
        Method to define the valid characters
        """
        self.chars = []

        chars = 'NS'
        self.chars.append(chars)
        chars = 'ABCDEFGHIJKLMNOPQRSTUVZ'
        self.chars.append(chars)
        chars = ['01','02','03','04','05','06','07','08','09','10',
                   '11','12','13','14','15','16','17','18','19','20',
                   '21','22','23','24','25','26','27','28','29','30',
                   '31','32','33','34','35','36','37','38','39','40',
                   '41','42','43','44','45','46','47','48','49','50',
                   '51','52','53','54','55','56','57','58','59','60']
        self.chars.append(chars)
        chars = 'VXYZ'
        self.chars.append(chars)
        chars = 'ABCD'
        self.chars.append(chars)
        chars = ['I','II','III','IV','V','VI']
        self.chars.append(chars)
        chars = '1234'
        self.chars.append(chars)
        chars = ['NO','NE','SO','SE']
        self.chars.append(chars)
        chars = 'ABCDEF'
        self.chars.append(chars)
        chars = ['I','II','III','IV']
        self.chars.append(chars)
        chars = '123456'
        self.chars.append(chars)
        chars = 'ABCD'
        self.chars.append(chars)

    def setMask(self):
        """
        REGEx closely related to the valid chars method 'setValidCharacters'
        """
        if self.scaleCombo.currentText() == '1000k':
            regex = QtCore.QRegExp('[NSns]{1}[A-Za-z]{1}\-[0-9]{1,2}')
            validator = QtGui.QRegExpValidator(regex, self.inomLineEdit)
            self.inomLineEdit.setValidator(validator)
        elif self.scaleCombo.currentText() == '500k':
            regex = QtCore.QRegExp('[NSns]{1}[A-Za-z]{1}\-[0-9]{1,2}\-[V-Zv-z]{1}')
            validator = QtGui.QRegExpValidator(regex, self.inomLineEdit)
            self.inomLineEdit.setValidator(validator)
        elif self.scaleCombo.currentText() == '250k':
            regex = QtCore.QRegExp('[NSns]{1}[A-Za-z]{1}\-[0-9]{1,2}\-[V-Zv-z]{1}\-[A-Da-d]{1}')
            validator = QtGui.QRegExpValidator(regex, self.inomLineEdit)
            self.inomLineEdit.setValidator(validator)
        elif self.scaleCombo.currentText() == '100k':
            regex = QtCore.QRegExp('[NSns]{1}[A-Za-z]{1}\-[0-9]{1,2}\-[V-Zv-z]{1}\-[A-Da-d]{1}\-[IViv]{1,3}')
            validator = QtGui.QRegExpValidator(regex, self.inomLineEdit)
            self.inomLineEdit.setValidator(validator)
        elif self.scaleCombo.currentText() == '50k':
            self.inomLineEdit.setInputMask('NN-NN-N-N-Nnn-0')
            regex = QtCore.QRegExp('[NSns]{1}[A-Za-z]{1}\-[0-9]{1,2}\-[V-Zv-z]{1}\-[A-Da-d]{1}\-[IViv]{1,3}\-[1-4]{1}')
            validator = QtGui.QRegExpValidator(regex, self.inomLineEdit)
            self.inomLineEdit.setValidator(validator)
        elif self.scaleCombo.currentText() == '25k':
            regex = QtCore.QRegExp('[NSns]{1}[A-Za-z]{1}\-[0-9]{1,2}\-[V-Zv-z]{1}\-[A-Da-d]{1}\-[IViv]{1,3}\-[1-4]{1}\-[NSns]{1}[OEoe]{1}')
            validator = QtGui.QRegExpValidator(regex, self.inomLineEdit)
            self.inomLineEdit.setValidator(validator)
        elif self.scaleCombo.currentText() == '10k':
            regex = QtCore.QRegExp('[NSns]{1}[A-Za-z]{1}\-[0-9]{1,2}\-[V-Zv-z]{1}\-[A-Da-d]{1}\-[IViv]{1,3}\-[1-4]{1}\-[NSns]{1}[OEoe]{1}\-[A-Fa-f]{1}')
            validator = QtGui.QRegExpValidator(regex, self.inomLineEdit)
            self.inomLineEdit.setValidator(validator)
        elif self.scaleCombo.currentText() == '5k':
            regex = QtCore.QRegExp('[NSns]{1}[A-Za-z]{1}\-[0-9]{1,2}\-[V-Zv-z]{1}\-[A-Da-d]{1}\-[IViv]{1,3}\-[1-4]{1}\-[NSns]{1}[OEoe]{1}\-[A-Fa-f]{1}\-[IViv]{1,3}')
            validator = QtGui.QRegExpValidator(regex, self.inomLineEdit)
            self.inomLineEdit.setValidator(validator)
        elif self.scaleCombo.currentText() == '2k':
            regex = QtCore.QRegExp('[NSns]{1}[A-Za-z]{1}\-[0-9]{1,2}\-[V-Zv-z]{1}\-[A-Da-d]{1}\-[IViv]{1,3}\-[1-4]{1}\-[NSns]{1}[OEoe]{1}\-[A-Fa-f]{1}\-[IViv]{1,3}\-[1-6]{1}')
            validator = QtGui.QRegExpValidator(regex, self.inomLineEdit)
            self.inomLineEdit.setValidator(validator)
        elif self.scaleCombo.currentText() == '1k':
            regex = QtCore.QRegExp('[NSns]{1}[A-Za-z]{1}\-[0-9]{1,2}\-[V-Zv-z]{1}\-[A-Da-d]{1}\-[IViv]{1,3}\-[1-4]{1}\-[NSns]{1}[OEoe]{1}\-[A-Fa-f]{1}\-[IViv]{1,3}\-[1-6]{1}\-[A-Da-d]{1}')
            validator = QtGui.QRegExpValidator(regex, self.inomLineEdit)
            self.inomLineEdit.setValidator(validator)

    def validateMI(self):
        """
        Method to validate INOM based on the valid characters.
        """
        mi = self.inomLineEdit.text()
        split = mi.split('-')
        for i in range(len(split)):
            word = str(split[i])
            if len(word) == 0:
                return False
            if i == 0:
                if word[0] not in self.chars[0]:
                    # fix_print_with_import
                    print(word)
                    return False
                if word[1] not in self.chars[1]:
                    # fix_print_with_import
                    print(word)
                    return False
            elif i == 1:
                if word not in self.chars[2]:
                    # fix_print_with_import
                    print(word)
                    return False
            elif i == 2:
                if word not in self.chars[3]:
                    # fix_print_with_import
                    print(word)
                    return False
            elif i == 3:
                if word not in self.chars[4]:
                    # fix_print_with_import
                    print(word)
                    return False
            elif i == 4:
                if word not in self.chars[5]:
                    # fix_print_with_import
                    print(word)
                    return False
            elif i == 5:
                if word not in self.chars[6]:
                    # fix_print_with_import
                    print(word)
                    return False
            elif i == 6:
                if word not in self.chars[7]:
                    # fix_print_with_import
                    print(word)
                    return False
            elif i == 7:
                if word not in self.chars[8]:
                    # fix_print_with_import
                    print(word)
                    return False
            elif i == 8:
                if word not in self.chars[9]:
                    # fix_print_with_import
                    print(word)
                    return False
            elif i == 9:
                if word not in self.chars[10]:
                    # fix_print_with_import
                    print(word)
                    return False
            elif i == 10:
                if word not in self.chars[11]:
                    # fix_print_with_import
                    print(word)
                    return False
        return True

    def disableAll(self):
        """
        Disables all line edits.
        """
        self.mirLineEdit.setEnabled(False)
        self.miLineEdit.setEnabled(False)
        self.inomLineEdit.setEnabled(False)

    @pyqtSlot(int)
    def on_scaleCombo_currentIndexChanged(self):
        """
        Adjusts the mask according to the scale.
        """
        self.setMask()
        if self.scaleCombo.currentText() == '1000k':
            self.miRadioButton.setEnabled(False)
            self.miLineEdit.setEnabled(False)
            self.mirRadioButton.setEnabled(True)
            self.mirLineEdit.setEnabled(True)
        else:
            self.miRadioButton.setEnabled(True)
            self.miLineEdit.setEnabled(True)
            self.mirRadioButton.setEnabled(False)
            self.mirLineEdit.setEnabled(False)

    @pyqtSlot(bool)
    def on_mirRadioButton_toggled(self, toggled):
        """
        Toggles the correct line edit (MIR or MI)
        """
        if toggled:
            self.mirLineEdit.setEnabled(True)
        else:
            self.mirLineEdit.setEnabled(False)

    @pyqtSlot(bool)
    def on_miRadioButton_toggled(self, toggled):
        """
        Toggles the correct line edit (MIR or MI)
        """
        if toggled:
            self.miLineEdit.setEnabled(True)
        else:
            self.miLineEdit.setEnabled(False)

    @pyqtSlot(bool)
    def on_inomRadioButton_toggled(self, toggled):
        """
        Toggles the INOM line edit
        """
        if toggled:
            self.inomLineEdit.setEnabled(True)
        else:
            self.inomLineEdit.setEnabled(False)