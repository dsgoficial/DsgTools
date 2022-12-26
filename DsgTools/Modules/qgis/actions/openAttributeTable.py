from qgis import gui, core
from qgis.utils import iface
from PyQt5 import QtCore, uic, QtWidgets, QtGui


class OpenAttributeTable:
    def execute(self):
        iface.actionOpenTable().trigger()
