from qgis import gui
from qgis.utils import iface


class MoveFeature:
    def __init__(self):
        self.names = ["mActionMoveFeature"]

    def execute(self):
        for a in gui.QgsGui.shortcutsManager().listActions():
            if not (a.objectName() in self.names):
                continue
            iface.activeLayer().startEditing()
            a.trigger()
            break
