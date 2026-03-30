from qgis import gui, core
from qgis.utils import iface
from qgis.PyQt import QtCore, uic, QtWidgets, QtGui


class AddPointFeature:
    def execute(self):
        iface.activeLayer().startEditing()
        iface.actionAddFeature().trigger()
