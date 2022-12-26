from qgis import gui, core
from qgis.utils import iface
from PyQt5 import QtCore, uic, QtWidgets, QtGui


class RightDegreeAngleDigitizing:
    def __init__(self):
        self.names = [
            "dsgtools: right degree angle digitizing",
            "dsgtools: ferramenta de aquisição com ângulos retos",
        ]

    def execute(self):
        for a in gui.QgsGui.shortcutsManager().listActions():
            if not (a.text().lower() in self.names):
                continue
            iface.activeLayer().startEditing()
            a.trigger()
            break
