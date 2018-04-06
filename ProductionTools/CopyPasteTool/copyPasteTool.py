# -*- coding: utf-8 -*-
from builtins import range
from builtins import object
import os

# Qt imports
import psycopg2
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.core import QgsPoint , QgsDataSourceUri, QgsVectorLayer
from qgis.gui import QgsMessageBar, QgsMapTool
from qgis.PyQt.QtCore import QSettings, pyqtSignal, pyqtSlot, QObject, QSize
from qgis.PyQt.QtGui import QIcon, QCursor, QPixmap
from qgis.PyQt.QtWidgets import QMessageBox, QAction
from .multiLayerSelect import MultiLayerSelection
from .interface_copyPaste import CopyPaste

class CopyPasteTool(object):
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.tool1 = MultiLayerSelection(self.iface.mapCanvas(), self.iface)
        # self.iface.actionToggleEditing().triggered.connect(self.closeCursor)
        self.selectorAction = None

    def setSelectorAction(self, action):
        self.tool1.setAction(action)

    def closeCursor(self, a):
        if not a:
            self.canvas.unsetMapTool(self.tool1)
            self.canvas.unsetCursor()
            self.removeSelecoes()
                              
    def selectMulti(self):
        self.iface.mapCanvas().setMapTool(self.tool1)

    def copyPaste(self):
        if (self.iface.activeLayer()) and (len(self.iface.activeLayer().selectedFeatures()) == 1):
            layer = self.iface.activeLayer().selectedFeatures()[0]
            dialog = QtWidgets.QDialog(self.iface.mainWindow())
            self.d = CopyPaste(self.iface, layer, dialog)
            self.tool1.finished.connect(self.d.setSelectedLayers)
            self.d.show()
        else:
            self.iface.messageBar().pushMessage(u"Atenção", u"Selecione apenas uma feição",
                                                level=QgsMessageBar.INFO, duration=10)
              
    def removeSelecoes(self):
        for i in range(len(self.canvas.layers())):
            try:
                self.canvas.layers()[i].removeSelection()
            except:
                pass
        
    
       
