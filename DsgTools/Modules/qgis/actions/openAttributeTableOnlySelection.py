from qgis import gui, core
from qgis.utils import iface
from qgis.PyQt import QtCore, uic, QtWidgets, QtGui


class OpenAttributeTableOnlySelection:
    def __init__(self):
        self.names = ["attributeTableSelectedFeatures"]

    def execute(self):
        for a in gui.QgsGui.shortcutsManager().listShortcuts():
            if not (a.objectName() in self.names):
                continue
            a.activated.emit()
            break
