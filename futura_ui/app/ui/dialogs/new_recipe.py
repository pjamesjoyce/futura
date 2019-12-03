from PySide2 import QtWidgets
from ..utils import load_ui_file
import os


class NewRecipeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(NewRecipeDialog, self).__init__(parent)

        ui_path = 'new_recipe.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)


