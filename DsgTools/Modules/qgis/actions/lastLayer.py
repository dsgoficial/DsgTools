from qgis import gui, core
from qgis.utils import iface
from PyQt5 import QtCore, uic, QtWidgets, QtGui

class LastLayer:

    def __init__(self):
        self.layers = []
        self.startSignals()

    def startSignals(self):
        iface.layerTreeView().currentLayerChanged.connect(self.updateList)

    def updateList(self, vectorLayer):
        if not isinstance(vectorLayer, core.QgsVectorLayer):
            return
        if len(self.layers) == 2:
            self.layers.pop(0)
        self.layers.append(vectorLayer)

    def execute(self):
        if not( len(self.layers) > 0 ):
            return
        iface.layerTreeView().setCurrentLayer( self.layers[0] )