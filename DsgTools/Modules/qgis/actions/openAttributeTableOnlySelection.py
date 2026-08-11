from qgis import gui


class OpenAttributeTableOnlySelection:
    def __init__(self):
        self.names = ["attributeTableSelectedFeatures"]

    def execute(self):
        for a in gui.QgsGui.shortcutsManager().listShortcuts():
            if not (a.objectName() in self.names):
                continue
            a.activated.emit()
            break
