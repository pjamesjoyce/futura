from PySide2 import QtWidgets
from ..ui_files import Ui_NewRecipeDialog


class NewRecipeDialog(Ui_NewRecipeDialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(NewRecipeDialog, self).__init__(parent)

        self.setupUi(self)


