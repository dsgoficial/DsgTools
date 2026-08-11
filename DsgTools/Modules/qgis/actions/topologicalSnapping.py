from qgis import gui


class TopologicalSnapping:
    def __init__(self):
        self.names = ["topologicaleditingaction"]

    def execute(self):
        for a in gui.QgsGui.shortcutsManager().listActions():
            if not (a.objectName().lower() in self.names):
                continue
            a.trigger()
            break
