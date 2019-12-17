from PySide2 import QtWidgets
from ..ui_files import Ui_EcoinventDialog


class EcoinventLoginDialog(Ui_EcoinventDialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(EcoinventLoginDialog, self).__init__(parent)

        self.setupUi(self)
