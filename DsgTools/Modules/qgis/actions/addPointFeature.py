from qgis import gui, core
from qgis.utils import iface
from PyQt5 import QtCore, uic, QtWidgets, QtGui


class AddPointFeature:
    def execute(self):
        iface.activeLayer().startEditing()
        iface.actionAddFeature().trigger()
