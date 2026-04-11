from qgis import gui, core
from qgis.utils import iface
from qgis.PyQt import QtCore, uic, QtWidgets, QtGui
from qgis.PyQt.QtCore import QCoreApplication


class SetFeatureInspector:
    def __init__(self):
        self.baseName = "DSGTools: Set Active Layer on Feature Inspector"

    def execute(self):
        translatedName = QCoreApplication.translate(
            "InspectFeatures", self.baseName
        ).lower()
        names = [self.baseName.lower(), translatedName]
        for a in gui.QgsGui.shortcutsManager().listActions():
            if not (a.text().lower() in names):
                continue
            a.trigger()
            break
