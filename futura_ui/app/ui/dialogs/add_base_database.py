from PySide2 import QtWidgets
from ..ui_files import Ui_AddBaseDatabaseDialog


class BaseDatabaseDialog(Ui_AddBaseDatabaseDialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(BaseDatabaseDialog, self).__init__(parent)

        self.setupUi(self)

