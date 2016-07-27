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
from qgis.core import *
from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QMessageBox

import os
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_create_inom_dialog_base.ui'))

#DsgTools imports
from DsgTools.LayerTools.map_index import UtmGrid
from DsgTools.Factories.LayerFactory.layerFactory import LayerFactory

#qgis imports
import qgis as qgis

class CreateInomDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, codeList, parent=None):
        """
        Constructor
        """
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
        self.codeList = codeList
        self.layerFactory = LayerFactory()

    @pyqtSlot()
    def on_okButton_clicked(self):
        '''
        Creates the frame and inserts it in the layer
        '''
        if not self.widget.dbLoaded:
            QMessageBox.warning(self, self.tr("Warning!"), self.tr('Please, select a database first.'))
            return

        if not self.validateMI():
            QMessageBox.warning(self, self.tr("Warning!"), self.tr('Map name index not valid!'))
            return
        frame = self.map_index.getQgsPolygonFrame(self.inomLineEdit.text())
        reprojected = self.reprojectFrame(frame)
        self.insertFrameIntoLayer(reprojected)
        self.done(1)

    def insertFrameIntoLayer(self, reprojected):
        '''
        Insert the reprojected frame in the layer
        reprojected: reprojected frame to be inserted
        '''
        self.dbVersion = self.widget.getDBVersion()
        self.qmlPath = self.widget.getQmlPath()

        layer = self.getFrameLayer(self.iface.legendInterface().layers())

        if layer == None:
            lyrName = self.widget.abstractDb.getFrameLayerName()          
            dbName = self.widget.abstractDb.getDatabaseName()
            groupList =  qgis.utils.iface.legendInterface().groups()
            edgvLayer = self.layerFactory.makeLayer(self.widget.abstractDb, self.codeList, lyrName)
            if dbName in groupList:
                layer = edgvLayer.load(self.widget.crs,groupList.index(dbName))
            else:
                self.parentTreeNode = qgis.utils.iface.legendInterface().addGroup(self.widget.abstractDb.getDatabaseName(), -1)
                layer = edgvLayer.load(self.widget.crs,self.parentTreeNode)
        
        if not layer:
            return

        layer.startEditing()
        feat = QgsFeature()
        feat.setFields(layer.dataProvider().fields())
        feat.setGeometry(reprojected)
        feat.setAttribute(2, self.inomLineEdit.text())
        feat.setAttribute(3, self.scaleCombo.currentText())
        layer.addFeatures([feat], makeSelected=True)
        layer.commitChanges()

        bbox = reprojected.boundingBox()
        for feature in layer.getFeatures():
            bbox.combineExtentWith(feature.geometry().boundingBox())

        bbox = self.iface.mapCanvas().mapSettings().layerToMapCoordinates(layer, bbox)
        self.iface.mapCanvas().setExtent(bbox)
        self.iface.mapCanvas().refresh()

    def getFrameLayer(self, ifaceLayers):
        '''
        Gets the frame layer
        '''
        for lyr in ifaceLayers:
            if 'aux_moldura_a' in lyr.name():
                dbname = self.getDBNameFromLayer(lyr)
                if dbname == self.widget.abstractDb.getDatabaseName():
                    return lyr
        return None
    
    def getDBNameFromLayer(self, lyr):
        '''
        Gets the databse name
        '''
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
        '''
        Cancels the process
        '''
        self.done(0)

    @pyqtSlot(str)
    def on_miLineEdit_textChanged(self,s):
        '''
        Slot to update the inom text using the MI text as base
        '''
        if (s!=''):
            self.inomen=self.map_index.getINomenFromMI(str(s))
            self.inomLineEdit.setText(self.inomen)

    @pyqtSlot(str)
    def on_mirLineEdit_textChanged(self,s):
        '''
        Slot to update the inom text using the MIR text as base
        '''
        if (s!=''):
            self.inomen=self.map_index.getINomenFromMIR(str(s))
            self.inomLineEdit.setText(self.inomen)

    def reprojectFrame(self, poly):
        '''
        Reprojects the frame to the layer CRS
        poly: polygon to be reprojected
        '''
        crsSrc = QgsCoordinateReferenceSystem(self.widget.crs.geographicCRSAuthId())
        coordinateTransformer = QgsCoordinateTransform(crsSrc, self.widget.crs)
        polyline = poly.asMultiPolygon()[0][0]
        newPolyline = []
        for point in polyline:
            newPolyline.append(coordinateTransformer.transform(point))
        qgsPolygon = QgsGeometry.fromMultiPolygon([[newPolyline]])
        return qgsPolygon

    def setValidCharacters(self):
        '''
        Sets the available characters used to create INOM
        '''
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
        '''
        Creates the mask used to enter the INOM (from 1:1.000.000 to 1:1.000)
        '''
        if self.scaleCombo.currentText() == '1000k':
            self.inomLineEdit.setInputMask('NN-NN')
        elif self.scaleCombo.currentText() == '500k':
            self.inomLineEdit.setInputMask('NN-NN-N')
        elif self.scaleCombo.currentText() == '250k':
            self.inomLineEdit.setInputMask('NN-NN-N-N')
        elif self.scaleCombo.currentText() == '100k':
            self.inomLineEdit.setInputMask('NN-NN-N-N-Nnn')
        elif self.scaleCombo.currentText() == '50k':
            self.inomLineEdit.setInputMask('NN-NN-N-N-Nnn-0')
        elif self.scaleCombo.currentText() == '25k':
            self.inomLineEdit.setInputMask('NN-NN-N-N-Nnn-0-NN')
        elif self.scaleCombo.currentText() == '10k':
            self.inomLineEdit.setInputMask('NN-NN-N-N-Nnn-0-NN-N')
        elif self.scaleCombo.currentText() == '5k':
            self.inomLineEdit.setInputMask('NN-NN-N-N-Nnn-0-NN-N-Nnn')
        elif self.scaleCombo.currentText() == '2k':
            self.inomLineEdit.setInputMask('NN-NN-N-N-Nnn-0-NN-N-Nnn-0')
        elif self.scaleCombo.currentText() == '1k':
            self.inomLineEdit.setInputMask('NN-NN-N-N-Nnn-0-NN-N-Nnn-0-N')

    def validateMI(self):
        '''
        Validates the MI using the available characters (method setValidCharacters)
        '''
        mi = self.inomLineEdit.text()
        split = mi.split('-')
        for i in range(len(split)):
            word = str(split[i])
            if len(word) == 0:
                return False
            if i == 0:
                if word[0] not in self.chars[0]:
                    print word
                    return False
                if word[1] not in self.chars[1]:
                    print word
                    return False
            elif i == 1:
                if word not in self.chars[2]:
                    print word
                    return False
            elif i == 2:
                if word not in self.chars[3]:
                    print word
                    return False
            elif i == 3:
                if word not in self.chars[4]:
                    print word
                    return False
            elif i == 4:
                if word not in self.chars[5]:
                    print word
                    return False
            elif i == 5:
                if word not in self.chars[6]:
                    print word
                    return False
            elif i == 6:
                if word not in self.chars[7]:
                    print word
                    return False
            elif i == 7:
                if word not in self.chars[8]:
                    print word
                    return False
            elif i == 8:
                if word not in self.chars[9]:
                    print word
                    return False
            elif i == 9:
                if word not in self.chars[10]:
                    print word
                    return False
            elif i == 10:
                if word not in self.chars[11]:
                    print word
                    return False
        return True

    def disableAll(self):
        '''
        Disables the widget items
        '''
        self.mirLineEdit.setEnabled(False)
        self.miLineEdit.setEnabled(False)
        self.inomLineEdit.setEnabled(False)

    @pyqtSlot(int)
    def on_scaleCombo_currentIndexChanged(self):
        '''
        Sets the mask according to the scale set
        '''
        self.setMask()

    @pyqtSlot(bool)
    def on_mirRadioButton_toggled(self, toggled):
        '''
        Toggles the use of MIR values
        '''
        if toggled:
            self.mirLineEdit.setEnabled(True)
        else:
            self.mirLineEdit.setEnabled(False)

    @pyqtSlot(bool)
    def on_miRadioButton_toggled(self, toggled):
        '''
        Toggles the use of MI values
        '''
        if toggled:
            self.miLineEdit.setEnabled(True)
        else:
            self.miLineEdit.setEnabled(False)

    @pyqtSlot(bool)
    def on_inomRadioButton_toggled(self, toggled):
        '''
        Toggles the use of INOM values
        '''
        if toggled:
            self.inomLineEdit.setEnabled(True)
        else:
            self.inomLineEdit.setEnabled(False)