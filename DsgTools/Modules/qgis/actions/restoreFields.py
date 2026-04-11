from qgis import gui, core
from qgis.utils import iface
from qgis.PyQt import QtCore, uic, QtWidgets, QtGui
from qgis.PyQt.QtCore import QCoreApplication


class RestoreFields:
    def __init__(self):
        self.baseName = "restore layer"

    def execute(self):
        translatedName = QCoreApplication.translate(
            "RestoreFields", self.baseName
        ).lower()
        names = [self.baseName.lower(), translatedName]
        for a in gui.QgsGui.shortcutsManager().listActions():
            if not (a.text().lower() in names):
                continue
            a.trigger()
            break
