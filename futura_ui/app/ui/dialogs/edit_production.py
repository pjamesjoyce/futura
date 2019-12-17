from PySide2 import QtWidgets
from ..ui_files import Ui_EditProductionDialog


class EditProductionDialog(Ui_EditProductionDialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(EditProductionDialog, self).__init__(parent)

        self.setupUi(self)
