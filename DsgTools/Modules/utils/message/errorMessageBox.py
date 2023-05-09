import os
from PyQt5 import QtWidgets, uic


class ErrorMessageBox:
    def __init__(self):
        super(ErrorMessageBox, self).__init__()

    def show(self, parent, title, text):
        QtWidgets.QMessageBox.critical(parent, title, text)
