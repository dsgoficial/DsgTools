from qgis import gui
from qgis.utils import iface


class TrimExtendFeature:
    def __init__(self):
        self.names = ["mActionTrimExtendFeature"]

    def execute(self):
        for a in gui.QgsGui.shortcutsManager().listActions():
            if not (a.objectName() in self.names):
                continue
            iface.activeLayer().startEditing()
            a.trigger()
            break
