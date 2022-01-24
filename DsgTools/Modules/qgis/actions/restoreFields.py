from qgis import gui, core
from qgis.utils import iface
from PyQt5 import QtCore, uic, QtWidgets, QtGui

class RestoreFields:

    def __init__(self):
        self.names = [ 'restaurar camada' ]
        
    def execute(self):
        for a in gui.QgsGui.shortcutsManager().listActions():
            if not( a.text().lower() in self.names ):
                continue
            a.trigger()
            break