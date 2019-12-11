from PySide2 import QtWidgets
from ..utils import load_ui_file
import os


class BaseDatabaseDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(BaseDatabaseDialog, self).__init__(parent)

        ui_path = 'add_base_database.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)
