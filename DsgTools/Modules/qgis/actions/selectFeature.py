from qgis import gui, core
from qgis.utils import iface
from PyQt5 import QtCore, uic, QtWidgets, QtGui


class SelectFeature:
    def execute(self):
        iface.actionSelectRectangle().trigger()
