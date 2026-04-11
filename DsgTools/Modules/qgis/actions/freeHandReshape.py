from qgis import gui, core
from qgis.utils import iface
from qgis.PyQt import QtCore, uic, QtWidgets, QtGui
from qgis.PyQt.QtCore import QCoreApplication


class FreeHandReshape:
    def __init__(self):
        self.baseName = "DSGTools: Free Hand Reshape"

    def execute(self):
        translatedName = QCoreApplication.translate(
            "FreeHandReshape", self.baseName
        ).lower()
        names = [self.baseName.lower(), translatedName]
        for a in gui.QgsGui.shortcutsManager().listActions():
            if not (a.text().lower() in names):
                continue
            iface.activeLayer().startEditing()
            a.trigger()
            break
