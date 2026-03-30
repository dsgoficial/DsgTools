from qgis import gui, core
from qgis.utils import iface
from qgis.PyQt import QtCore, uic, QtWidgets, QtGui


class SelectFeature:
    def execute(self):
        iface.actionSelectRectangle().trigger()
