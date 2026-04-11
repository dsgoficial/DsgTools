from qgis import gui, core
from qgis.utils import iface
from qgis.PyQt import QtCore, uic, QtWidgets, QtGui
from qgis.PyQt.QtCore import QCoreApplication


class SetDefaultFields:
    def __init__(self):
        self.baseName = "create more like this"

    def execute(self):
        translatedName = QCoreApplication.translate(
            "SetDefaultFields", self.baseName
        ).lower()
        names = [self.baseName.lower(), translatedName]
        for a in gui.QgsGui.shortcutsManager().listActions():
            if not (a.text().lower() in names):
                continue
            a.trigger()
            break
