from qgis.PyQt import QtWidgets


class InfoMessageBox:
    def __init__(self):
        super(InfoMessageBox, self).__init__()

    def show(self, parent, title, text):
        QtWidgets.QMessageBox.information(parent, title, text)
